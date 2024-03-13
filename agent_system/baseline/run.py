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
import argparse
import logging
import os
import sys

from camel.typing import ModelType

root = os.path.dirname(__file__)
sys.path.append(root)

from devagent.chat_chain import DevAgentChain
from test import Test
import subprocess
import signal

class TimeoutError(Exception):
    pass

def handler(signum, frame):
    raise TimeoutError("Timeout")
# 设置超时时间为5秒
timeout_seconds = 3600

# 注册信号处理器
signal.signal(signal.SIGALRM, handler)
signal.alarm(timeout_seconds)

def get_config(company, review=True):
    """
    return configuration json files for ChatChain
    user can customize only parts of configuration json files, other files will be left for default
    Args:
        company: customized configuration name under CompanyConfig/

    Returns:
        path to three configuration jsons: [config_path, config_phase_path, config_role_path]
    """
    if review:
        config_dir = os.path.join(root, "CompanyConfig", company)
    else:
        config_dir = os.path.join(root, "CompanyConfigNoReview", company)
    default_config_dir = os.path.join(root, "CompanyConfig", "Implementation")

    config_files = [
        "ChatChainConfig.json",
        "PhaseConfig.json",
        "RoleConfig.json"
    ]

    config_paths = []

    for config_file in config_files:
        company_config_path = os.path.join(config_dir, config_file)
        default_config_path = os.path.join(default_config_dir, config_file)

        if os.path.exists(company_config_path):
            config_paths.append(company_config_path)
        else:
            config_paths.append(default_config_path)

    return tuple(config_paths)


parser = argparse.ArgumentParser(description='argparse')
parser.add_argument('--config', type=str, default="Implementation",
                    help="Name of config, which is used to load configuration under CompanyConfig/ or CompanyConfigNoReview/, [SoftwareDesign, EnvironmentSetup, Implementation, AcceptanceTesting, UnitTesting]")
parser.add_argument('--project_name', type=str, default="",
                    help="Name of project")
parser.add_argument('--model', type=str, default="gpt-4-32k", # gpt-4-turbo-new
                    help="Model, choose from [gpt-3.5-turbo, gpt-4, gpt-4-32k, gpt-4-turbo, gpt-4-turbo-new, claude-3, claude-2.1, codellama-7b, codellama-13b, codellama-34b, deepseek-coder-1.3b, deepseek-coder-6.7b, deepseek-coder-33b, customized_model]")
parser.add_argument('--customized_model_name', type=str, default="default", 
                    help="If the value of the 'model' parameter is 'customized-model', then you need to specify the custom model name.")                   
parser.add_argument('--model_source', type=str, default="openai",
                    help="choose from [server, pjlab, open_source, openai]")
parser.add_argument('--input_path', type=str, default="third_party/DevBench/proj_data/bowen/graph-cpp",
                    help="input path")
parser.add_argument('--read_src_code', action='store_true',
                    help="Whether to use source codes during the AcceptanceTesting and UnitTesting.")
parser.add_argument('--evaluate', action='store_true',
                    help="Whether to evaluate after forward pass")      
parser.add_argument('--review', type=str, default="normal",
                    help="choose from [none, normal, execution], none: single forward pass, normal: default review, execution: review with exection feedback")
parser.add_argument('--temperature', type=float, default=0, help="temperature")
parser.add_argument('--top_p', type=float, default=1.0, help="top_p")             
args = parser.parse_args()

# Start ChatDev

# ----------------------------------------
#          Init ChatChain
# ----------------------------------------
config_path, config_phase_path, config_role_path = get_config(args.config, args.review != "none")
args2type = {
    'gpt-3.5-turbo': ModelType.GPT_3_5_TURBO, 
    'gpt-4': ModelType.GPT_4, 
    'gpt-4-32k': ModelType.GPT_4_32K, 
    'gpt-4-turbo': ModelType.GPT_4_TURBO,
    'gpt-4-turbo-new': ModelType.GPT_4_TURBO_NEW,
    'claude-2': ModelType.CLAUDE_2, 
    'claude-2.1': ModelType.CLAUDE_2_1, 
    'codellama-7b': ModelType.CODELLAMA_7B,
    'codellama-13b': ModelType.CODELLAMA_13B,
    'codellama-34b': ModelType.CODELLAMA_34B,
    'deepseek-coder-1.3b': ModelType.DEEPSEEK_CODER_1_3B,
    'deepseek-coder-6.7b': ModelType.DEEPSEEK_CODER_6_7B,
    'deepseek-coder-33b': ModelType.DEEPSEEK_CODER_33B,
    'customized-model': ModelType.CUSTOMIZED_MODEL
    }

chat_chain = DevAgentChain(input_path=args.input_path,
                       review = args.review,
                       warehouse_path="WareHouse_results/{}{}/{}/{}".format(args.config, "_code" if args.read_src_code else "", args.model if args.model != "customized-model" else args.customized_model_name, args.review),
                       model_source=args.model_source,
                       read_src_code=args.read_src_code,
                       temperature=args.temperature,
                       top_p=args.top_p,
                       config_path=config_path,
                       config_phase_path=config_phase_path,
                       config_role_path=config_role_path,
                       project_name=args.project_name,
                       model_type=args2type[args.model],
                       config_name=args.config
                    )

# ----------------------------------------
#          Init Log
# ----------------------------------------
logging.basicConfig(filename=chat_chain.log_filepath, level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")

# ----------------------------------------
#          Pre Processing
# ----------------------------------------

chat_chain.pre_processing()

# ----------------------------------------
#          Personnel Recruitment
# ----------------------------------------

chat_chain.make_recruitment()

# ----------------------------------------
#          Chat Chain
# ----------------------------------------
try:
    chat_chain.execute_chain()
    signal.alarm(0)  # 清除信号
except TimeoutError:
    print("Timeout occurred")

chat_chain.execute_chain()

# ----------------------------------------
#          Post Processing
# ----------------------------------------

chat_chain.post_processing()

if args.evaluate:
    src_path = args.input_path
    tgt_path = ".".join(chat_chain.log_filepath.split('.')[:-1])
    t = Test(src_path, tgt_path)
    check_output = t.test(args.config, tgt_path, chat_chain.chat_env.env_dict["language"])
