import os
import time
import shutil
from devagent.roster import Roster
from devagent.codes import Codes
from devagent.documents import Documents
import subprocess


class ChatEnvConfig:
    def __init__(self, clear_structure,
                 gui_design,
                 git_management,
                 incremental_develop):
        self.clear_structure = clear_structure
        self.gui_design = gui_design
        self.git_management = git_management
        self.incremental_develop = incremental_develop

    def __str__(self):
        string = ""
        string += "ChatEnvConfig.clear_structure: {}\n".format(self.clear_structure)
        string += "ChatEnvConfig.git_management: {}\n".format(self.git_management)
        string += "ChatEnvConfig.gui_design: {}\n".format(self.gui_design)
        string += "ChatEnvConfig.incremental_develop: {}\n".format(self.incremental_develop)
        return string


class DevAgentEnv:
    def __init__(self, chat_env_config: ChatEnvConfig):
        self.config = chat_env_config
        self.roster: Roster = Roster()
        self.uml_class = Documents()
        self.uml_sequence = Documents()
        self.requirements = Documents()
        self.architecture_design = Documents()
        self.codes = Codes()
        self.acceptance_test_codes = Codes()
        self.unit_test_codes = Codes()
        self.env_dict = {
            "directory": "",
            "task_prompt": "",
            "prd": "",
            "uml_class": "",
            "uml_sequence": "",
            "architecture_design": "",
            "golden_plan": "",
            "next_plan_id": 0,
            "current_coding_turn": 0,
            "codes": "",
            "previous_code": "",
            "next_code_filename": "",
            "language": "",
            "execution_feedback": "",
            "code_modification": ""
        }

    def recruit(self, agent_name: str):
        self.roster._recruit(agent_name)

    def exist_employee(self, agent_name: str) -> bool:
        return self.roster._exist_employee(agent_name)

    def print_employees(self):
        self.roster._print_employees()

    def init_env_dict(self):
        self.env_dict["next_plan_id"] = 0
        self.env_dict["next_code_filename"] = self.env_dict["golden_plan"][self.env_dict["next_plan_id"]]
        self.code_modification = ""
    
    def get_feedback(self):
        return self.env_dict["execution_feedback"]

    def set_directory(self, directory):
        assert len(self.env_dict['directory']) == 0
        self.env_dict['directory'] = directory
        self.uml_class.directory = directory
        self.uml_sequence.directory = directory
        self.architecture_design.directory = directory
        self.requirements.directory = directory
        self.codes.directory = directory
        self.acceptance_test_codes.directory = directory
        self.unit_test_codes.directory = directory

        if os.path.exists(self.env_dict['directory']) and len(os.listdir(directory)) > 0:
            new_directory = "{}.{}".format(directory, time.strftime("%Y%m%d%H%M%S", time.localtime()))
            shutil.copytree(directory, new_directory)
            print("{} Copied to {}".format(directory, new_directory))
        if self.config.clear_structure:
            if os.path.exists(self.env_dict['directory']):
                shutil.rmtree(self.env_dict['directory'])
                os.mkdir(self.env_dict['directory'])
                print("{} Created".format(directory))
            else:
                os.mkdir(self.env_dict['directory'])

    def update_uml_classes(self, generated_content):
        self.uml_class._update_docs(generated_content, parse=False, predifined_filename="uml_class.md")

    def rewrite_uml_classes(self):
        self.uml_class._rewrite_docs()

    def update_uml_sequences(self, generated_content):
        self.uml_sequence._update_docs(generated_content, parse=False, predifined_filename="UML_sequence.md")

    def rewrite_uml_sequences(self):
        self.uml_sequence._rewrite_docs()

    def update_architecture_designs(self, generated_content):
        self.architecture_design._update_docs(generated_content, parse=False, predifined_filename="architecture_design.md")

    def rewrite_architecture_designs(self):
        self.architecture_design._rewrite_docs()

    def update_requirements(self, generated_content, predifined_filename):
        self.requirements._update_docs(generated_content, parse=True, predifined_filename=predifined_filename)

    def rewrite_requirements(self):
        self.requirements._rewrite_docs()

    def get_requirements(self) -> str:
        return self.requirements._get_docs()

    def update_codes(self, generated_content, filename=None):
        self.codes._update_codes(generated_content, filename)

    def rewrite_codes(self) -> None:
        self.codes._rewrite_codes()

    def get_codes(self) -> str:
        return self.codes._get_codes()

    def get_codefiles(self, target_filenames) -> str:
        return self.codes._get_codefiles(target_filenames)

    def load_from_hardware_files(self, directory, filenames) -> None:
        self.codes._load_from_hardware_files(directory, filenames)

    def update_acceptance_test_codes(self, generated_content, filename=None):
        self.acceptance_test_codes._update_codes(generated_content, filename)

    def rewrite_acceptance_test_codes(self) -> None:
        self.acceptance_test_codes._rewrite_codes()

    def update_unit_test_codes(self, generated_content, filename=None):
        self.unit_test_codes._update_codes(generated_content, filename)

    def rewrite_unit_test_codes(self) -> None:
        self.unit_test_codes._rewrite_codes()

    def check_commands(self, shell_script, cwd):
        process = subprocess.Popen(shell_script, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        outputs = []
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
                outputs.append(output.strip().decode())

        process.wait()
        rc = process.returncode
        return "\n".join(outputs), rc



