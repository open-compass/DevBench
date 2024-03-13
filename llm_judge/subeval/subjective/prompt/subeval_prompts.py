import pandas as pd


en_prefix = """
Please evaluate the two responses (Response 1, Response 2) based on the provided scoring criteria.

Scoring criteria:
<Evaluating Guidance> \n
- If the response is incomplete or misses any required key component, regard it as a bad one.
- If the response is verbose and/or repetitive, consider it negatively based on the extent.
- If the response is well-formatted and clearly-structured, give it extra credit.

**Important**: 
You should act as an IMPARTIAL judge and be as OBJECTIVE as possible. 
AVOID ANY POSITION BIASES and ensure that the ORDER in which the responses were presented DOES NOT influence your decision. 
"""

en_suffix = """
Please provide detailed reasons for your choice.
Also, you should pay adequate and same attention to both responses.
Your output should be in the following format:
Choice: A
Reason: 
1. xxxxxx
2. xxxxxx
......\n
"""

en_4opt = """
Please choose from the following 4 options based on the scoring criteria:
A. Response 1 is good; Response 2 is not good.
B. Response 2 is good; Response 1 is not good.
C. Both Response 1 and Response 2 are good.
D. Neither Response 1 nor Response 2 is good.

NOTE: If you think both reponses are good, but one is better than the other, choose C instead of A or B, but you should explain who is better in the reason part.
Only choose A or B if one of the response is not good.
"""

en_3opt = """
Please choose from the following 3 options based on the scoring criteria:
A. Response 1 is better.
B. Response 2 is better.
C. Tie.
"""

en_2opt = """
Please choose from the following 2 options based on the scoring criteria:
A. Response 1 is better than Response 2.
B. Response 2 is better than Response 1.
"""

prompt_map = dict(
    en4=en_prefix+en_4opt+en_suffix, 
    en3=en_prefix+en_3opt+en_suffix,
    en2=en_prefix+en_2opt+en_suffix
)


def build_prompt_en(item, prompt):
    # If evaluting guidance is provided, then replace <Evaluating Guidance> with the actual content in prefix
    if 'evaluating_guidance' in item and not pd.isna(item['evaluating_guidance']):
        prompt = prompt.replace("<Evaluating Guidance>", item['evaluating_guidance'])

    # Input question and answers    
    prompt += f"Question: \n\n<Question Start>\n\n {item['question']} \n\n<Question End>\n\n"
    prompt += f"Response 1: \n\n<Response 1 Start>\n\n {item['answer1']} \n\n<Response 1 End>\n\n"
    prompt += f"Response 2: \n\n<Response 2 Start>\n\n {item['answer2']} \n\n<Response 2 End>\n\n"
    if 'reference_answer' in item and not pd.isna(item['reference_answer']):
        prompt += f"Reference Answer: \n\n<Reference Answer Start>\n\n {item['reference_answer']} \n\n<Reference Answer End>\n\n"

    return prompt

def build_prompt(item, nopt=4):
    prompt = prompt_map[f'en{nopt}']
    return build_prompt_en(item, prompt)
