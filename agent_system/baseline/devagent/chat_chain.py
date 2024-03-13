from datetime import datetime
import importlib
import logging
import os
import shutil
import time
import json
from camel.agents import RolePlaying
from camel.configs import ChatGPTConfig
from camel.typing import TaskType, ModelType
from devagent.chat_env import DevAgentEnv, ChatEnvConfig
from devagent.statistics import get_info
from devagent.utils import log_and_print_online, get_coding_plan, now

def check_bool(s):
    return s.lower() == "true"

class DevAgentChain:
    def __init__(self, 
                 input_path, 
                 model_source, 
                 review,
                 warehouse_path,
                 read_src_code=False, 
                 temperature=0.2,
                 top_p=1.0,
                 config_path: str = None,
                 config_phase_path: str = None,
                 config_role_path: str = None,
                 project_name: str = None,
                 config_name: str = None,
                 model_type: ModelType = ModelType.GPT_3_5_TURBO,
                ):
        """

        Args:
            config_path: path to the ChatChainConfig.json
            config_phase_path: path to the PhaseConfig.json
            config_role_path: path to the RoleConfig.json
            project_name: the user input name for software
        """

        # load config file
        self.config_path = config_path
        self.config_phase_path = config_phase_path
        self.config_role_path = config_role_path
        self.input_path = input_path[:-1] if input_path[-1] == '/' else input_path
        self.project_name = project_name if project_name != "" else self.input_path.split('/')[-1]
        self.config_name = config_name
        self.model_type = model_type
        self.warehouse_path = warehouse_path

        with open(self.config_path, 'r', encoding="utf8") as file:
            self.config = json.load(file)
        with open(self.config_phase_path, 'r', encoding="utf8") as file:
            self.config_phase = json.load(file)
        with open(self.config_role_path, 'r', encoding="utf8") as file:
            self.config_role = json.load(file)

        # init chatchain config and recruitments
        self.chain = self.config["chain"]
        self.recruitments = self.config["recruitments"]

        # init default max chat turn
        self.chat_turn_limit_default = 10

        # init ChatEnv
        self.chat_env_config = ChatEnvConfig(clear_structure=check_bool(self.config["clear_structure"]),
                                             gui_design=check_bool(self.config["gui_design"]),
                                             git_management=check_bool(self.config["git_management"]),
                                             incremental_develop=check_bool(self.config["incremental_develop"]))
        self.chat_env = DevAgentEnv(self.chat_env_config)

        # init role prompts
        self.role_prompts = dict()
        for role in self.config_role:
            self.role_prompts[role] = "\n".join(self.config_role[role])

        # init log
        self.start_time, self.log_filepath = self.get_logfilepath()

        # init SimplePhase instances
        # import all used phases in PhaseConfig.json from chatdev.phase
        # note that in PhaseConfig.json there only exist SimplePhases
        # ComposedPhases are defined in ChatChainConfig.json and will be imported in self.execute_step
        self.compose_phase_module = importlib.import_module("devagent.composed_phase")
        self.phase_module = importlib.import_module("devagent.phase")
        self.phases = dict()
        for phase in self.config_phase:
            assistant_role_name = self.config_phase[phase]['assistant_role_name']
            user_role_name = self.config_phase[phase]['user_role_name']
            phase_prompt = "\n\n".join(self.config_phase[phase]['phase_prompt'])
            phase_class = getattr(self.phase_module, phase)
            phase_instance = phase_class(assistant_role_name=assistant_role_name,
                                         user_role_name=user_role_name,
                                         phase_prompt=phase_prompt,
                                         role_prompts=self.role_prompts,
                                         phase_name=phase,
                                         model_type=self.model_type,
                                         log_filepath=self.log_filepath)
            self.phases[phase] = phase_instance

        with open(os.path.join(self.input_path, "repo_config.json"), "r") as f:
            self.inputs = json.load(f)
        
        self.chat_env.env_dict["root_path"] = input_path
        self.chat_env.env_dict["model_source"] = model_source
        self.chat_env.env_dict["temperature"] = temperature
        self.chat_env.env_dict["top_p"] = top_p
        self.chat_env.env_dict["review"] = review
        self.chat_env.env_dict["prd"] = open(os.path.join(self.input_path, self.inputs["PRD"])).read()

        if self.config_name == "EnvironmentSetup":
            self.es_required = True
        else:
            self.es_required = False

        if self.config_name == "Implementation":
            self.impl_required = True
        else:
            self.impl_required = False

        if self.config_name == "AcceptanceTesting":
            self.at_required = True
        else:
            self.at_required = False

        if self.config_name == "UnitTesting":
            self.ut_required = True
        else:
            self.ut_required = False

        if self.es_required or self.impl_required or self.at_required or self.ut_required:
            self.chat_env.env_dict["UML_class"] = open(os.path.join(self.input_path, self.inputs["UML_class"])).read()
            self.chat_env.env_dict["uml_sequence"] = open(os.path.join(self.input_path, self.inputs["UML_sequence"])).read()
            self.chat_env.env_dict["architecture_design"] = open(os.path.join(self.input_path, self.inputs["architecture_design"])).read()
            self.chat_env.env_dict["language"] = self.inputs["language"]
  
        if self.es_required:
            if os.path.isdir(os.path.join(self.input_path, self.inputs["usage_examples"])):
                self.chat_env.env_dict["usage_examples"] = []
                for root, _, files in os.walk(os.path.join(self.input_path, self.inputs["usage_examples"])):
                    for file in files:
                        self.chat_env.env_dict["usage_examples"].append(os.path.join(self.inputs["usage_examples"], file))
            else:
                self.chat_env.env_dict["usage_examples"] = [os.path.join(self.input_path, self.inputs["usage_examples"])]
        
        if self.impl_required or self.at_required or self.ut_required:
            self.chat_env.env_dict["golden_plan"] = get_coding_plan(self.inputs["code_file_DAG"])
            self.chat_env.env_dict["src_files"] = self.chat_env.env_dict["golden_plan"] if read_src_code else []
            self.chat_env.load_from_hardware_files(self.input_path, self.chat_env.env_dict["src_files"])
            self.chat_env.env_dict["codes"] = self.chat_env.get_codes()
            self.chat_env.env_dict["required_files"] = self.inputs["required_files"]

        if self.impl_required or self.at_required:
            self.chat_env.env_dict["acceptance_tests_path"] = self.inputs["acceptance_tests"]
        
        if self.impl_required or self.ut_required:
            self.chat_env.env_dict["unit_tests_path"] = self.inputs["unit_tests"]

        if self.impl_required:
            self.chat_env.env_dict["next_plan_id"] = 0
            self.chat_env.env_dict["next_code_filename"] = self.chat_env.env_dict["golden_plan"][self.chat_env.env_dict["next_plan_id"]]

        if self.at_required:
            self.chat_env.env_dict["fine_acceptance_test_prompt"] = self.inputs["fine_acceptance_test_prompt"]
            self.chat_env.env_dict["coarse_acceptance_test_prompt"] = self.inputs["coarse_acceptance_test_prompt"]

        if self.ut_required:
            self.chat_env.env_dict["fine_unit_test_prompt"] = self.inputs["fine_unit_test_prompt"]
            self.chat_env.env_dict["coarse_unit_test_prompt"] = self.inputs["coarse_unit_test_prompt"]
            self.chat_env.env_dict["unit_test_linking"] = self.inputs["unit_test_linking"]

    def make_recruitment(self):
        """
        recruit all employees
        Returns: None

        """
        for employee in self.recruitments:
            self.chat_env.recruit(agent_name=employee)

    def execute_step(self, phase_item: dict):
        """
        execute single phase in the chain
        Args:
            phase_item: single phase configuration in the ChatChainConfig.json

        Returns:

        """

        phase = phase_item['phase']
        phase_type = phase_item['phaseType']
        # For SimplePhase, just look it up from self.phases and conduct the "Phase.execute" method
        if phase_type == "SimplePhase":
            max_turn_step = phase_item['max_turn_step']
            need_reflect = check_bool(phase_item['need_reflect'])
            if phase in self.phases:
                self.chat_env = self.phases[phase].execute(self.chat_env,
                                                           self.chat_turn_limit_default if max_turn_step <= 0 else max_turn_step,
                                                           need_reflect)
            else:
                raise RuntimeError(f"Phase '{phase}' is not yet implemented in chatdev.phase")
        # For ComposedPhase, we create instance here then conduct the "ComposedPhase.execute" method
        elif phase_type == "ComposedPhase":
            cycle_num = phase_item['cycleNum']
            composition = phase_item['Composition']
            compose_phase_class = getattr(self.compose_phase_module, phase)
            if not compose_phase_class:
                raise RuntimeError(f"Phase '{phase}' is not yet implemented in chatdev.compose_phase")
            compose_phase_instance = compose_phase_class(phase_name=phase,
                                                         cycle_num=cycle_num,
                                                         composition=composition,
                                                         config_phase=self.config_phase,
                                                         config_role=self.config_role,
                                                         model_type=self.model_type,
                                                         log_filepath=self.log_filepath)
            self.chat_env = compose_phase_instance.execute(self.chat_env)
        else:
            raise RuntimeError(f"PhaseType '{phase_type}' is not yet implemented.")

    def get_logfilepath(self):
        """
        get the log path (under the software path)
        Returns:
            start_time: time for starting making the software
            log_filepath: path to the log

        """
        start_time = now()
        filepath = os.path.dirname(__file__)
        root = os.path.dirname(filepath)
        directory = os.path.join(root, self.warehouse_path)
        os.makedirs(directory, exist_ok=True)
        log_filepath = os.path.join(directory,
                                    "{}.log".format("_".join([self.model_type.value, self.project_name, self.config_name, start_time])))
        return start_time, log_filepath

    def execute_chain(self):
        """
        execute the whole chain based on ChatChainConfig.json
        Returns: None

        """
        for phase_item in self.chain:
            self.execute_step(phase_item)

    def pre_processing(self):
        """
        remove useless files and log some global config settings
        Returns: None

        """
        if self.chat_env.config.clear_structure:
            filepath = os.path.dirname(__file__)
            root = os.path.dirname(filepath)
            directory = os.path.join(root, self.warehouse_path)
            os.makedirs(directory, exist_ok=True)
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                # logs with error trials are left in WareHouse/
                if os.path.isfile(file_path) and not filename.endswith(".py") and not filename.endswith(".log"):
                    os.remove(file_path)
                    print("{} Removed.".format(file_path))

        software_path = os.path.join(directory, "_".join([self.model_type.value, self.project_name, self.config_name, self.start_time]))
        self.chat_env.set_directory(software_path)

        # copy config files to software path
        shutil.copy(self.config_path, software_path)
        shutil.copy(self.config_phase_path, software_path)
        shutil.copy(self.config_role_path, software_path)

        preprocess_msg = "**[Preprocessing]**\n\n"
        chat_gpt_config = ChatGPTConfig()

        preprocess_msg += "**ChatDev Starts** ({})\n\n".format(self.start_time)
        preprocess_msg += "**Timestamp**: {}\n\n".format(self.start_time)
        preprocess_msg += "**config_path**: {}\n\n".format(self.config_path)
        preprocess_msg += "**config_phase_path**: {}\n\n".format(self.config_phase_path)
        preprocess_msg += "**config_role_path**: {}\n\n".format(self.config_role_path)
        preprocess_msg += "**project_name**: {}\n\n".format(self.project_name)
        preprocess_msg += "**Log File**: {}\n\n".format(self.log_filepath)
        preprocess_msg += "**ChatDevConfig**:\n{}\n\n".format(self.chat_env.config.__str__())
        preprocess_msg += "**ChatGPTConfig**:\n{}\n\n".format(chat_gpt_config)
        log_and_print_online(preprocess_msg)

    def post_processing(self):
        """
        summarize the production and move log files to the software directory
        Returns: None

        """
        
        filepath = os.path.dirname(__file__)
        root = os.path.dirname(filepath)

        if self.chat_env_config.git_management:
            git_online_log = "**[Git Information]**\n\n"

            self.chat_env.codes.version += 1
            os.system("cd {}; git add .".format(self.chat_env.env_dict["directory"]))
            git_online_log += "cd {}; git add .\n".format(self.chat_env.env_dict["directory"])
            os.system("cd {}; git commit -m \"v{} Final Version\"".format(self.chat_env.env_dict["directory"], self.chat_env.codes.version))
            git_online_log += "cd {}; git commit -m \"v{} Final Version\"\n".format(self.chat_env.env_dict["directory"], self.chat_env.codes.version)
            log_and_print_online(git_online_log)

            git_info = "**[Git Log]**\n\n"
            import subprocess

            # execute git log
            command = "cd {}; git log".format(self.chat_env.env_dict["directory"])
            completed_process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE)

            if completed_process.returncode == 0:
                log_output = completed_process.stdout
            else:
                log_output = "Error when executing " + command

            git_info += log_output
            log_and_print_online(git_info)

        post_info = "**[Post Info]**\n\n"
        now_time = now()
        time_format = "%Y%m%d%H%M%S"
        datetime1 = datetime.strptime(self.start_time, time_format)
        datetime2 = datetime.strptime(now_time, time_format)
        duration = (datetime2 - datetime1).total_seconds()

        # post_info += "Software Info: {}".format(
        #     get_info(self.chat_env.env_dict['directory'], self.log_filepath) + "\n\n🕑**duration**={:.2f}s\n\n".format(
        #         duration))

        post_info += "ChatDev Starts ({})".format(self.start_time) + "\n\n"
        post_info += "ChatDev Ends ({})".format(now_time) + "\n\n"

        if self.chat_env.config.clear_structure:
            directory = self.chat_env.env_dict['directory']
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isdir(file_path) and file_path.endswith("__pycache__"):
                    shutil.rmtree(file_path, ignore_errors=True)
                    post_info += "{} Removed.".format(file_path) + "\n\n"

        log_and_print_online(post_info)

        logging.shutdown()
        time.sleep(1)

        # shutil.move(self.log_filepath,
        #             os.path.join(root + "/WareHouse", "_".join([self.project_name, self.config_name, self.start_time]),
        #                          os.path.basename(self.log_filepath)))
