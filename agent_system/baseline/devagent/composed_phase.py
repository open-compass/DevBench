import os
import re
import shutil
import importlib
from abc import ABC, abstractmethod
from collections import defaultdict

from camel.typing import ModelType
from devagent.chat_env import DevAgentEnv
from devagent.utils import log_and_print_online, prepare_required_files, src2tgt
from test import Test


def check_bool(s):
    return s.lower() == "true"


class ComposedPhase(ABC):
    def __init__(self,
                 phase_name: str = None,
                 cycle_num: int = None,
                 composition: list = None,
                 config_phase: dict = None,
                 config_role: dict = None,
                 model_type: ModelType = ModelType.GPT_3_5_TURBO,
                 log_filepath: str = ""
                 ):
        """

        Args:
            phase_name: name of this phase
            cycle_num: loop times of this phase
            composition: list of SimplePhases in this ComposePhase
            config_phase: configuration of all SimplePhases
            config_role: configuration of all Roles
        """

        self.phase_name = phase_name
        self.cycle_num = cycle_num
        self.composition = composition
        self.model_type = model_type
        self.log_filepath = log_filepath

        self.config_phase = config_phase
        self.config_role = config_role

        self.phase_env = dict()
        self.phase_env["cycle_num"] = cycle_num

        # init chat turn
        self.chat_turn_limit_default = 10

        # init role
        self.role_prompts = dict()
        for role in self.config_role:
            self.role_prompts[role] = "\n".join(self.config_role[role])

        # init all SimplePhases instances in this ComposedPhase
        self.phases = dict()
        for phase in self.config_phase:
            assistant_role_name = self.config_phase[phase]['assistant_role_name']
            user_role_name = self.config_phase[phase]['user_role_name']
            phase_prompt = "\n".join(self.config_phase[phase]['phase_prompt'])
            phase_module = importlib.import_module("devagent.phase")
            phase_class = getattr(phase_module, phase)
            phase_instance = phase_class(assistant_role_name=assistant_role_name,
                                         user_role_name=user_role_name,
                                         phase_prompt=phase_prompt,
                                         role_prompts=self.role_prompts,
                                         phase_name=phase,
                                         model_type=self.model_type,
                                         log_filepath=self.log_filepath)
            self.phases[phase] = phase_instance

    @abstractmethod
    def update_phase_env(self, chat_env):
        """
        update self.phase_env (if needed) using chat_env, then the chatting will use self.phase_env to follow the context and fill placeholders in phase prompt
        must be implemented in customized phase
        the usual format is just like:
        ```
            self.phase_env.update({key:chat_env[key]})
        ```
        Args:
            chat_env: global chat chain environment

        Returns: None

        """
        pass

    @abstractmethod
    def update_chat_env(self, chat_env) -> DevAgentEnv:
        """
        update chan_env based on the results of self.execute, which is self.seminar_conclusion
        must be implemented in customized phase
        the usual format is just like:
        ```
            chat_env.xxx = some_func_for_postprocess(self.seminar_conclusion)
        ```
        Args:
            chat_env:global chat chain environment

        Returns:
            chat_env: updated global chat chain environment

        """
        pass

    @abstractmethod
    def break_cycle(self, phase_env) -> bool:
        """
        special conditions for early break the loop in ComposedPhase
        Args:
            phase_env: phase environment

        Returns: None

        """
        pass

    def execute(self, chat_env) -> DevAgentEnv:
        """
        similar to Phase.execute, but add control for breaking the loop
        1. receive information from environment(ComposedPhase): update the phase environment from global environment
        2. for each SimplePhase in ComposedPhase
            a) receive information from environment(SimplePhase)
            b) check loop break
            c) execute the chatting
            d) change the environment(SimplePhase)
            e) check loop break
        3. change the environment(ComposedPhase): update the global environment using the conclusion

        Args:
            chat_env: global chat chain environment

        Returns:

        """
        self.update_phase_env(chat_env)
        for cycle_index in range(1, self.cycle_num + 1):
            for phase_item in self.composition:
                assert phase_item["phaseType"] == "SimplePhase"  # right now we do not support nested composition
                phase = phase_item['phase']
                max_turn_step = phase_item['max_turn_step']
                need_reflect = check_bool(phase_item['need_reflect'])
                self.phase_env["cycle_index"] = cycle_index
                log_and_print_online(
                    f"**[Execute Detail]**\n\nexecute SimplePhase:[{phase}] in ComposedPhase:[{self.phase_name}], cycle {cycle_index}")
                if phase in self.phases:
                    self.phases[phase].phase_env = self.phase_env
                    self.phases[phase].update_phase_env(chat_env)
                    if self.break_cycle(self.phases[phase].phase_env):
                        return chat_env
                    chat_env = self.phases[phase].execute(chat_env,
                                                          self.chat_turn_limit_default if max_turn_step <= 0 else max_turn_step,
                                                          need_reflect)
                    if self.break_cycle(self.phases[phase].phase_env):
                        return chat_env
                else:
                    print(f"Phase '{phase}' is not yet implemented. \
                            Please write its config in phaseConfig.json \
                            and implement it in chatdev.phase")
        chat_env = self.update_chat_env(chat_env)
        return chat_env


class SoftwareDesign(ComposedPhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        pass

    def update_chat_env(self, chat_env):
        return chat_env

    def break_cycle(self, phase_env) -> bool:
        return False


class EnvironmentSetup(ComposedPhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        shutil.copytree(os.path.join(os.getcwd(), chat_env.env_dict["root_path"]), chat_env.env_dict["directory"], dirs_exist_ok=True)
        doc_path = os.path.join(chat_env.env_dict["directory"], "requirements.txt") if chat_env.env_dict["language"] == "python" else os.path.join(chat_env.env_dict["directory"], "package.json")
        if os.path.exists(doc_path):  
            os.remove(doc_path)  

    def update_chat_env(self, chat_env):
        return chat_env

    def break_cycle(self, phase_env) -> bool:
        if phase_env["usage_rcs"] == False and phase_env["command_rc"] == 0:
            return True
        else:
            return False


class Implementation(ComposedPhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_structure(self, file_tree, directory):
        lines = file_tree.strip().split('\n')
        current_path = []

        for line in lines:
            indent_level = line.count('│')
            name = line.strip('├── │').strip().strip('└──').strip()
            # update current path
            current_path[indent_level:] = [name]

            if '.' in name or "makefile" in name or "Makefile" in name:  # file
                file_path = os.path.join(directory, '/'.join(current_path))
                if not os.path.exists(file_path):
                    open(file_path, 'a').close()  # make empty file
            else:  # dir
                dir_path = os.path.join(directory, '/'.join(current_path))
                os.makedirs(dir_path, exist_ok=True)

    def parse_architecture_design(self, chat_env):
        content = chat_env.env_dict["architecture_design"]
        regex = r"(.+?)\n```.*?\n(.*?)```"
        matches = re.finditer(regex, content, re.DOTALL)
        for match in matches:
            notes = match.group(1)
            content = match.group(2)
            if "file tree" in notes:
                self.create_structure(content, chat_env.env_dict["directory"])

    def update_phase_env(self, chat_env):
        prepare_required_files(chat_env.env_dict["root_path"], chat_env.env_dict["directory"])
        self.test = Test(chat_env.env_dict["root_path"], chat_env.env_dict["directory"])
        self.test.setup_implementation()
        self.parse_architecture_design(chat_env)

    def update_chat_env(self, chat_env):
        if chat_env.env_dict["next_plan_id"] == len(chat_env.env_dict["golden_plan"]):
            if chat_env.env_dict["review"] == "execution":
                chat_env.env_dict["execution_feedback"] = self.test.test("Implementation", chat_env.env_dict["directory"], chat_env.env_dict["language"])
            else:
                chat_env.env_dict["execution_feedback"] = str()
            chat_env.env_dict["current_coding_turn"] += 1
            chat_env.init_env_dict()
        return chat_env

    def break_cycle(self, phase_env) -> bool:
        return False
    
    def execute(self, chat_env) -> DevAgentEnv:
        self.update_phase_env(chat_env)
        for cycle_index in range(1, self.cycle_num + 1):
            for filename in chat_env.env_dict["golden_plan"]:
                for phase_item in self.composition:
                    assert phase_item["phaseType"] == "SimplePhase"
                    phase = phase_item['phase']
                    max_turn_step = phase_item['max_turn_step']
                    need_reflect = check_bool(phase_item['need_reflect'])
                    self.phase_env["cycle_index"] = cycle_index
                    log_and_print_online(
                        f"**[Execute Detail]**\n\nexecute SimplePhase:[{phase}] in ComposedPhase:[{self.phase_name}], cycle {cycle_index}")
                    if phase in self.phases:
                        if chat_env.env_dict["current_coding_turn"] != 0 or phase != "CodeReview":
                            self.phases[phase].phase_env = self.phase_env
                            self.phases[phase].update_phase_env(chat_env)
                            if self.break_cycle(self.phases[phase].phase_env):
                                return chat_env
                            chat_env = self.phases[phase].execute(chat_env,
                                                                self.chat_turn_limit_default if max_turn_step <= 0 else max_turn_step,
                                                                need_reflect)
                            if self.break_cycle(self.phases[phase].phase_env):
                                return chat_env
                    else:
                        print(f"Phase '{phase}' is not yet implemented. \
                                Please write its config in phaseConfig.json \
                                and implement it in chatdev.phase")
                chat_env = self.update_chat_env(chat_env)
        return chat_env


class AcceptanceTesting(ComposedPhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def update_phase_env(self, chat_env):
        self.test = Test(chat_env.env_dict["root_path"], chat_env.env_dict["directory"])
    
    def execute(self, chat_env) -> DevAgentEnv:
        self.update_phase_env(chat_env)
        src2tgt(chat_env.env_dict["root_path"], chat_env.env_dict["directory"], chat_env.env_dict["fine_acceptance_test_prompt"])
        items = chat_env.env_dict["fine_acceptance_test_prompt"].items()
        chat_env.env_dict["acceptance_test_codes"] = {}
        chat_env.env_dict["code_modification"] = {}
        for cycle_index in range(1, self.cycle_num + 1):
            for phase_item in self.composition:
                for filename, prompt in items:
                    file_path = os.path.join(chat_env.env_dict["directory"], filename)
                    self.phase_env.update({"acceptance_test_prompt": prompt,
                                        "filename": filename})
                    assert phase_item["phaseType"] == "SimplePhase"  # right now we do not support nested composition
                    phase = phase_item['phase']
                    max_turn_step = phase_item['max_turn_step']
                    need_reflect = check_bool(phase_item['need_reflect'])
                    self.phase_env["cycle_index"] = cycle_index
                    log_and_print_online(
                        f"**[Execute Detail]**\n\nexecute SimplePhase:[{phase}] in ComposedPhase:[{self.phase_name}], cycle {cycle_index}")
                    if phase in self.phases:
                        self.phases[phase].phase_env = self.phase_env
                        self.phases[phase].update_phase_env(chat_env)
                        if self.break_cycle(self.phases[phase].phase_env):
                            return chat_env
                        chat_env = self.phases[phase].execute(chat_env,
                                                            self.chat_turn_limit_default if max_turn_step <= 0 else max_turn_step,
                                                            need_reflect)
                        if self.break_cycle(self.phases[phase].phase_env):
                            return chat_env
                    else:
                        print(f"Phase '{phase}' is not yet implemented. \
                                Please write its config in phaseConfig.json \
                                and implement it in chatdev.phase")
                if "Review" not in phase_item['phase'] and cycle_index != self.cycle_num:
                    chat_env = self.update_chat_env(chat_env)
        return chat_env

    def update_chat_env(self, chat_env):
        chat_env.env_dict["execution_feedback"] = str()
        return chat_env

    def break_cycle(self, phase_env) -> bool:
        return False


class UnitTesting(ComposedPhase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def update_phase_env(self, chat_env):
        self.test = Test(chat_env.env_dict["root_path"], chat_env.env_dict["directory"])
    
    def execute(self, chat_env) -> DevAgentEnv:
        self.update_phase_env(chat_env)
        src2tgt(chat_env.env_dict["root_path"], chat_env.env_dict["directory"], chat_env.env_dict["fine_unit_test_prompt"])
        items = chat_env.env_dict["fine_unit_test_prompt"].items()
        chat_env.env_dict["unit_test_codes"] = dict()
        chat_env.env_dict["code_modification"] = dict()
        for cycle_index in range(1, self.cycle_num + 1):
            for phase_item in self.composition:
                for filename, prompt in items:
                    file_path = os.path.join(chat_env.env_dict["directory"], filename)
                    self.phase_env.update({"unit_test_prompt": prompt,
                                        "codes": chat_env.get_codefiles(chat_env.env_dict["unit_test_linking"][filename]),
                                        "filename": filename})
                    assert phase_item["phaseType"] == "SimplePhase"  # right now we do not support nested composition
                    phase = phase_item['phase']
                    max_turn_step = phase_item['max_turn_step']
                    need_reflect = check_bool(phase_item['need_reflect'])
                    self.phase_env["cycle_index"] = cycle_index
                    log_and_print_online(
                        f"**[Execute Detail]**\n\nexecute SimplePhase:[{phase}] in ComposedPhase:[{self.phase_name}], cycle {cycle_index}")
                    if phase in self.phases:
                        self.phases[phase].phase_env = self.phase_env
                        self.phases[phase].update_phase_env(chat_env)
                        if self.break_cycle(self.phases[phase].phase_env):
                            return chat_env
                        chat_env = self.phases[phase].execute(chat_env,
                                                            self.chat_turn_limit_default if max_turn_step <= 0 else max_turn_step,
                                                            need_reflect)
                        if self.break_cycle(self.phases[phase].phase_env):
                            return chat_env
                    else:
                        print(f"Phase '{phase}' is not yet implemented. \
                                Please write its config in phaseConfig.json \
                                and implement it in chatdev.phase")
                if "Review" not in phase_item['phase'] and cycle_index != self.cycle_num:
                    chat_env = self.update_chat_env(chat_env)
        return chat_env

    def update_chat_env(self, chat_env):
        chat_env.env_dict["execution_feedback"] = str()
        return chat_env

    def break_cycle(self, phase_env) -> bool:
        return False