from subeval.smp import *
import os
from .base import BaseAPI
from openai import OpenAI
from collections import defaultdict

def GPT_context_window(model):
    length_map = {
        'gpt-4-0125-preview': 128000,
        'gpt-4-1106-preview': 128000, 
        'gpt-4-vision-preview': 128000, 
        'gpt-4': 8192,
        'gpt-4-32k': 32768,
        'gpt-4-0613': 8192, 
        'gpt-4-32k-0613': 32768,
        'gpt-3.5-turbo-1106': 16385, 
        'gpt-3.5-turbo': 4096, 
        'gpt-3.5-turbo-16k': 16385, 
        'gpt-3.5-turbo-instruct': 4096, 
        'gpt-3.5-turbo-0613': 4096, 
        'gpt-3.5-turbo-16k-0613': 16385, 
    }
    if model in length_map:
        return length_map[model]
    else:
        return 4096

class OpenAIWrapper(BaseAPI):

    is_api: bool = True

    def __init__(self, 
                 model: str = 'gpt-3.5-turbo-0613', 
                 retry: int = 5,
                 wait: int=5, 
                 verbose: bool = True, 
                 system_prompt: str = None,
                 temperature: float = 0,
                 max_tokens: int = 1024,
                 **kwargs):

        self.model = model
        self.cur_idx = 0
        self.fail_cnt = defaultdict(lambda: 0)
        self.fail_msg = 'Failed to obtain answer via API. '
        self.max_tokens = max_tokens
        self.temperature = temperature

        openai_keys = []
        if 'KEYS' in os.environ and osp.exists(os.environ['KEYS']):
            keys = load(os.environ['KEYS'])
            openai_keys = keys.get('openai-keys', [])

        self.keys = openai_keys
        self.num_keys = len(self.keys)
        
        super().__init__(
            wait=wait, retry=retry, system_prompt=system_prompt, verbose=verbose, **kwargs)

    def generate_inner(self, inputs, **kwargs) -> str:
        input_msgs = []
        if self.system_prompt is not None:
            input_msgs.append(dict(role='system', content=self.system_prompt))

        if isinstance(inputs, str):
            input_msgs.append(dict(role='user', content=inputs))
        elif isinstance(inputs[0], str):
            roles = ['user', 'assistant'] if len(inputs) % 2 == 1 else ['assistant', 'user']
            roles = roles * len(inputs)
            for role, msg in zip(roles, inputs):
                input_msgs.append(dict(role=role, content=msg))
        elif isinstance(inputs[0], dict):
            input_msgs.extend(inputs)
        else:
            raise NotImplementedError
        
        temperature = kwargs.pop('temperature', self.temperature)
        max_tokens = kwargs.pop('max_tokens', self.max_tokens)

        context_window = GPT_context_window(self.model)
        max_tokens = min(max_tokens, context_window - self.get_token_len(inputs))
        if 0 < max_tokens <= 100:
            warnings.warn('Less than 100 tokens left, may exceed the context window with some additional meta symbols. ')
        if max_tokens <= 0:
            return 0, self.fail_msg + 'Input string longer than context window. ', 'Length Exceeded. '

        for i in range(self.num_keys):
            idx = (self.cur_idx + i) % self.num_keys
            if self.fail_cnt[idx] >= min(self.fail_cnt.values()) + 20:
                continue
            try:
                client = OpenAI(api_key=self.keys[idx])
                response = client.chat.completions.create(
                    model=self.model,
                    messages=input_msgs,
                    max_tokens=max_tokens,
                    n=1,
                    stop=None,
                    temperature=temperature,
                    **kwargs)
                
                result = response.choices[0].message.content.strip()
                self.cur_idx = idx
                return 0, result, 'API Call Succeed'
            except:
                self.fail_cnt[idx] += 1
                if self.verbose:
                    warnings.warn(f'OPENAI KEY {self.keys[idx]} FAILED !!!')
                    try:
                        warnings.warn(response)
                    except:
                        pass
        # x = 1 / 0

    def get_token_len(self, prompt: str) -> int:
        import tiktoken
        enc = tiktoken.encoding_for_model(self.model)
        return len(enc.encode(prompt))
