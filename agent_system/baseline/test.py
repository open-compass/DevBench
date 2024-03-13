import subprocess
import os
import json
import shutil
from devagent.utils import log_and_print_online
def output_process(process):
    outputs = list()
    while True:
        output = process.stdout.readline()
        if not output and process.poll() is not None:
            break
        if output:
            print(output.strip().decode())
            outputs.append(output.strip().decode())
    return outputs

class Test:
    def __init__(self, src_path, tgt_path):
        self.src_path = src_path
        self.tgt_path = tgt_path
        with open(os.path.join(self.src_path, "repo_config.json"), "r") as f:
            self.config = json.load(f)
        self.usage_examples = self.config["usage_examples"]
        self.required_files = self.config["required_files"]
        self.unit_tests_path = self.config["unit_tests"]
        self.acceptance_tests_path = self.config["acceptance_tests"]
        self.unit_tests_command = self.config["unit_test_script"]
        self.acceptance_tests_command = self.config["acceptance_test_script"]
        self.dependencies = self.config["dependencies"]
    
    def copy_files(self, file_path):
        os.makedirs(os.path.dirname(os.path.join(self.tgt_path, file_path)), exist_ok=True)
        process = subprocess.Popen(["cp", "-r", os.path.join(self.src_path, file_path), os.path.join(self.tgt_path, file_path)], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    def setup_implementation(self):
        if "setup_shell_script" in self.config.keys() and self.config["setup_shell_script"] != "":
            process = subprocess.Popen(["sh", self.config["setup_shell_script"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.tgt_path)
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())
    
    def setup_tests(self, path, language):
        if language == "python":
            process = subprocess.Popen(["pip", "install", "-r", self.dependencies], cwd=path, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT)
            output_process(process)
        
    def check_commands(self, filename, cwd):
        process = subprocess.Popen(["conda", "run", "-n", "myenv", "sh", filename], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        outputs = list()
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
                outputs.append(output.strip().decode())

        # exit code
        rc = process.poll()
        return "\n".join(outputs), rc

    def check_tests(self, path, language, test_mode):
        if language == "python":
            process = subprocess.Popen(["pytest", "--cov=.", test_mode], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            if test_mode == "unit_tests":
                process = subprocess.Popen(self.unit_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                process = subprocess.Popen(self.acceptance_tests_command, shell=True, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        try:
            outputs = list()
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())
                    outputs.append(output.strip().decode())
            check_output = '\n'.join(outputs)
        except subprocess.TimeoutExpired:
            check_output = "check_tests function has timed out."
        return check_output

    def test(self, phase, path, language):
        if phase == "EnvironmentSetup":
            test_output = "Build Success."
            for filename in os.listdir(os.path.join(path, self.usage_examples)):
                if filename.endswith(".sh"):
                    print(filename)
                    _, test_rc = self.check_commands(os.path.join(self.usage_examples, filename), path)
                    if test_rc != 0:
                        test_output = "Build Failed."
        elif phase == "AcceptanceTesting":
            self.setup_tests(path, language)
            test_output = self.check_tests(path, language, "acceptance_tests")
        elif phase == "UnitTesting":
            self.setup_tests(path, language)
            test_output = self.check_tests(path, language, "unit_tests")
        elif phase == "Implementation":
            self.setup_implementation()
            unit_test_output = self.check_tests(path, language, "unit_tests")
            acceptance_test_output = self.check_tests(path, language, "acceptance_tests")
            test_output = "[unit test]\n" + unit_test_output + "\n[acceptance test]\n" + acceptance_test_output
        else:
            raise RuntimeError("No phase")
        test_msg = "**[Evaluation results]**\n\n"
        test_msg += test_output
        log_and_print_online(test_msg)
        return test_output


if __name__ == '__main__':
    src_path = "/DevBench/proj_data/yuxuan/TextCNN"
    tgt_path = "/DevAgents/WareHouse/TextCNN_UnitTesting_20240104070921"
    t = Test("/DevAgents/TextCNN", "/DevAgents/TextCNN")
    check_output = t.test("EnvironmentSetup", tgt_path, "python")
    print(check_output)