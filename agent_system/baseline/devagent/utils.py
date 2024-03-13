from typing import Any, Dict, List, Optional, Tuple
import html
import logging
import re
import time
import markdown
import inspect
from camel.messages.system_messages import SystemMessage
from online_log.app import send_msg

import subprocess
import os
import json
import shutil


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def log_and_print_online(role, content=None):
    if not content:
        logging.info(role + "\n")
        send_msg("System", role)
        print(role + "\n")
    else:
        print(str(role) + ": " + str(content) + "\n")
        logging.info(str(role) + ": " + str(content) + "\n")
        if isinstance(content, SystemMessage):
            records_kv = []
            content.meta_dict["content"] = content.content
            for key in content.meta_dict:
                value = content.meta_dict[key]
                value = str(value)
                value = html.unescape(value)
                value = markdown.markdown(value)
                value = re.sub(r'<[^>]*>', '', value)
                value = value.replace("\n", " ")
                records_kv.append([key, value])
            content = "**[SystemMessage**]\n\n" + convert_to_markdown_table(records_kv)
        else:
            role = str(role)
            content = str(content)
        send_msg(role, content)


def convert_to_markdown_table(records_kv):
    # Create the Markdown table header
    header = "| Parameter | Value |\n| --- | --- |"

    # Create the Markdown table rows
    rows = [f"| **{key}** | {value} |" for (key, value) in records_kv]

    # Combine the header and rows to form the final Markdown table
    markdown_table = header + "\n" + '\n'.join(rows)

    return markdown_table


def log_arguments(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        params = sig.parameters

        all_args = {}
        all_args.update({name: value for name, value in zip(params.keys(), args)})
        all_args.update(kwargs)

        records_kv = []
        for name, value in all_args.items():
            if name in ["self", "chat_env", "task_type"]:
                continue
            value = str(value)
            value = html.unescape(value)
            value = markdown.markdown(value)
            value = re.sub(r'<[^>]*>', '', value)
            value = value.replace("\n", " ")
            records_kv.append([name, value])
        records = f"**[{func.__name__}]**\n\n" + convert_to_markdown_table(records_kv)
        log_and_print_online("System", records)

        return func(*args, **kwargs)

    return wrapper

def get_coding_plan(code_file_DAG: Dict) -> List:
    """
    get coding plan from code_file_DAG
    Args:
        code_file_DAG: code_file_DAG from repo_config.json
    """

    def dfs(node):
        if node in gold_plan:
            return
        if node not in code_file_DAG or len(code_file_DAG[node]) == 0:
            gold_plan.append(node)
        else:
            for child in code_file_DAG[node]:
                dfs(child)
            if node not in gold_plan:
                gold_plan.append(node)

    gold_plan = []
    
    for k,v in code_file_DAG.items():
        if k in gold_plan:
            continue
        dfs(k)
    
    return gold_plan

def copy_file(file_path, src_path, tgt_path):
    os.makedirs(os.path.dirname(os.path.join(tgt_path, file_path)), exist_ok=True)
    process = subprocess.Popen(["cp", "-r", os.path.join(src_path, file_path), os.path.join(tgt_path, file_path)], stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

def prepare_required_files(src_path: str, tgt_path: str):
    with open(os.path.join(src_path, "repo_config.json"), "r") as f:
        config = json.load(f)
    required_files = config["required_files"]
    unit_tests = config["unit_tests"]
    acceptance_tests = config["acceptance_tests"]
    dependencies = config["dependencies"]
    setup_shell_script = config["setup_shell_script"] if "setup_shell_script" in config.keys() else ""

    if unit_tests in os.listdir(tgt_path):
        return
    if dependencies != "":
        copy_file(dependencies, src_path, tgt_path)
    if setup_shell_script != "":
        copy_file(setup_shell_script, src_path, tgt_path)
    copy_file(unit_tests, src_path, tgt_path)
    copy_file(acceptance_tests, src_path, tgt_path)

    for required_file in required_files:
        if '*' in required_file:
            copy_file(required_file.split('/*')[0], src_path, tgt_path)
        else:
            copy_file(required_file, src_path, tgt_path)

def src2tgt(root_path, directory, test_paths):
    shutil.copytree(os.path.join(os.getcwd(), root_path), directory, dirs_exist_ok=True)
    for filename in test_paths:
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
