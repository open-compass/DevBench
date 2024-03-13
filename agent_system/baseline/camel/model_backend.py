# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict

import openai
import tiktoken
import requests
import copy

from camel.typing import ModelType
from devagent.statistics import prompt_cost
from devagent.utils import log_and_print_online


class ModelBackend(ABC):
    r"""Base class for different model backends.
    May be OpenAI API, a local LLM, a stub for unit tests, etc."""

    @abstractmethod
    def run(self, model_source, *args, **kwargs) -> Dict[str, Any]:
        r"""Runs the query to the backend model.

        Raises:
            RuntimeError: if the return value from OpenAI API
            is not a dict that is expected.

        Returns:
            Dict[str, Any]: All backends must return a dict in OpenAI format.
        """
        pass


class OpenAIModel(ModelBackend):
    r"""OpenAI API in a unified ModelBackend interface."""

    def __init__(self, model_type, model_config_dict) -> None:
        super().__init__()
        self.model_type = model_type
        self.model_config_dict = model_config_dict
        with open("open_source_config.json", "r") as f:
            self.url_open_source = json.load(f)
        if self.model_type.value == "customized-model":
            self.model_type_value = list(self.url_open_source["customized-model"].keys())[0]
            self.url_open_source = self.url_open_source["customized-model"]
        else:
            self.model_type_value = self.model_type.value


    def run(self, model_source, temperature, top_p, *args, **kwargs) -> Dict[str, Any]:
        string = "\n".join([message["content"] for message in kwargs["messages"]])
        # encoding = tiktoken.encoding_for_model(self.model_type)
        # num_prompt_tokens = len(encoding.encode(string))
        # gap_between_send_receive = 15 * len(kwargs["messages"])
        # num_prompt_tokens += gap_between_send_receive
        # num_max_token_map = {
        #     "gpt-3.5-turbo": 4096,
        #     "gpt-3.5-turbo-1106": 8192,
        #     "gpt-3.5-turbo-0613": 4096,
        #     "gpt-3.5-turbo-16k-0613": 16384,
        #     "gpt-4": 8192,
        #     "gpt-4-0613": 8192,
        #     "gpt-4-32k": 8192,
        #     "gpt-4-1106-preview": 8192,
        #     "claude-2": 8192,
        #     "claude-2.1": 8192,
        #     "codellama-7b-instruct": 8192,
        #     "codellama-13b-instruct": 8192,
        #     "codellama-34b-instruct": 8192,
        #     "deepseek-coder-1.3b-instruct": 8192,
        #     "deepseek-coder-6.7b-instruct": 8192,
        #     "deepseek-coder-33b-instruct": 8192,
        # }
        # num_max_token = num_max_token_map[new_model_type]
        # num_max_completion_tokens = num_max_token - num_prompt_tokens
        self.model_config_dict['max_tokens'] = 4096
        data = copy.deepcopy(self.model_config_dict)
        data.update(kwargs)
        data.update({
            "model": self.model_type_value,
            "request_timeout": 200,
            "temperature": temperature,
            "top_p": top_p})
        if model_source == "open_source":
            from lmdeploy.serve.openai.api_client import APIClient
            url = self.url_open_source[self.model_type_value]
            api_client = APIClient(url)
            model_name = api_client.available_models[0]
            if "deepseek" in self.model_type_value:
                response = list(api_client.chat_completions_v1(model=model_name, messages=kwargs["messages"], temperature=temperature, top_p=top_p, max_tokens=4096, stop="<|EOT|>"))[0]
            else:
                response = list(api_client.chat_completions_v1(model=model_name, messages=kwargs["messages"], temperature=temperature, top_p=top_p, max_tokens=4096))[0]
        elif model_source == "openai":
            try:
                response = openai.ChatCompletion.create(*args, **kwargs, model=self.model_type_value, **self.model_config_dict)
            except AttributeError:
                response = openai.chat.completions.create(*args, **kwargs, model=self.model_type_value, **self.model_config_dict)
        else:
            raise NotImplementedError("No model source")
            

        if "usage" in response:
            cost = prompt_cost(
                self.model_type_value,
                num_prompt_tokens=response["usage"]["prompt_tokens"],
                num_completion_tokens=response["usage"]["completion_tokens"]
            )

            log_and_print_online(
                "**[OpenAI_Usage_Info Receive]**\nprompt_tokens: {}\ncompletion_tokens: {}\ntotal_tokens: {}\ncost: ${:.6f}\n".format(
                    response["usage"]["prompt_tokens"], response["usage"]["completion_tokens"],
                    response["usage"]["total_tokens"], cost))
        if not isinstance(response, Dict):
            raise RuntimeError("Unexpected return from OpenAI API")
        return response


class StubModel(ModelBackend):
    r"""A dummy model used for unit tests."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

    def run(self, model_source, *args, **kwargs) -> Dict[str, Any]:
        ARBITRARY_STRING = "Lorem Ipsum"

        return dict(
            id="stub_model_id",
            usage=dict(),
            choices=[
                dict(finish_reason="stop",
                     message=dict(content=ARBITRARY_STRING, role="assistant"))
            ],
        )


class ModelFactory:
    r"""Factory of backend models.

    Raises:
        ValueError: in case the provided model type is unknown.
    """

    @staticmethod
    def create(model_type: ModelType, model_config_dict: Dict) -> ModelBackend:
        default_model_type = ModelType.GPT_3_5_TURBO

        if model_type in {
            ModelType.GPT_3_5_TURBO, ModelType.GPT_4, ModelType.GPT_4_32K, ModelType.GPT_4_TURBO, ModelType.GPT_4_TURBO_NEW, \
            ModelType.CLAUDE_2, ModelType.CLAUDE_2_1, \
            ModelType.CODELLAMA_7B, ModelType.CODELLAMA_13B, ModelType.CODELLAMA_34B, \
            ModelType.DEEPSEEK_CODER_1_3B, ModelType.DEEPSEEK_CODER_6_7B, ModelType.DEEPSEEK_CODER_33B, \
            ModelType.CUSTOMIZED_MODEL, \
            None
        }:
            model_class = OpenAIModel
        elif model_type == ModelType.STUB:
            model_class = StubModel
        else:
            raise ValueError("Unknown model")

        if model_type is None:
            model_type = default_model_type

        inst = model_class(model_type, model_config_dict)
        return inst
