import os
import re
import shutil

from abc import ABC, abstractmethod
from camel.agents import RolePlaying
from camel.messages import ChatMessage
from camel.typing import TaskType, ModelType
from devagent.utils import log_and_print_online, log_arguments
from devagent.statistics import get_info
from devagent.chat_env import DevAgentEnv

class Phase(ABC):

    def __init__(self,
                 assistant_role_name,
                 user_role_name,
                 phase_prompt,
                 role_prompts,
                 phase_name,
                 model_type,
                 log_filepath):
        """

        Args:
            assistant_role_name: who receives chat in a phase
            user_role_name: who starts the chat in a phase
            phase_prompt: prompt of this phase
            role_prompts: prompts of all roles
            phase_name: name of this phase
        """
        self.seminar_conclusion = None
        self.assistant_role_name = assistant_role_name
        self.user_role_name = user_role_name
        self.phase_prompt = phase_prompt
        self.phase_env = dict()
        self.phase_name = phase_name
        self.assistant_role_prompt = role_prompts[assistant_role_name]
        self.user_role_prompt = role_prompts[user_role_name]
        # self.ceo_prompt = role_prompts["Chief Executive Officer"]
        # self.counselor_prompt = role_prompts["Counselor"]
        self.max_retries = 3
        self.reflection_prompt = """Here is a conversation between two roles: {conversations} {question}"""
        self.model_type = model_type
        self.log_filepath = log_filepath

    @log_arguments
    def chatting(
            self,
            chat_env,
            task_prompt: str,
            assistant_role_name: str,
            user_role_name: str,
            phase_prompt: str,
            phase_name: str,
            assistant_role_prompt: str,
            user_role_prompt: str,
            task_type=TaskType.CHATDEV,
            need_reflect=False,
            with_task_specify=False,
            model_type=ModelType.GPT_3_5_TURBO,
            placeholders=None,
            chat_turn_limit=10
    ) -> str:
        """

        Args:
            chat_env: global chatchain environment TODO: only for employee detection, can be deleted
            task_prompt: user query prompt for building the software
            assistant_role_name: who receives the chat
            user_role_name: who starts the chat
            phase_prompt: prompt of the phase
            phase_name: name of the phase
            assistant_role_prompt: prompt of assistant role
            user_role_prompt: prompt of user role
            task_type: task type
            need_reflect: flag for checking reflection
            with_task_specify: with task specify
            model_type: model type
            placeholders: placeholders for phase environment to generate phase prompt
            chat_turn_limit: turn limits in each chat

        Returns:

        """

        if placeholders is None:
            placeholders = {}
        assert 1 <= chat_turn_limit <= 100

        if not chat_env.exist_employee(assistant_role_name):
            raise ValueError(f"{assistant_role_name} not recruited in ChatEnv.")
        if not chat_env.exist_employee(user_role_name):
            raise ValueError(f"{user_role_name} not recruited in ChatEnv.")

        # init role play
        role_play_session = RolePlaying(
            assistant_role_name=assistant_role_name,
            user_role_name=user_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_prompt=user_role_prompt,
            task_prompt=task_prompt,
            task_type=task_type,
            with_task_specify=with_task_specify,
            model_type=model_type,
        )

        # log_and_print_online("System", role_play_session.assistant_sys_msg)
        # log_and_print_online("System", role_play_session.user_sys_msg)

        # start the chat
        _, input_user_msg = role_play_session.init_chat(None, placeholders, phase_prompt)
        seminar_conclusion = None

        # handle chats
        # the purpose of the chatting in one phase is to get a seminar conclusion
        # there are two types of conclusion
        # 1. with "<INFO>" mark
        # 1.1 get seminar conclusion flag (ChatAgent.info) from assistant or user role, which means there exist special "<INFO>" mark in the conversation
        # 1.2 add "<INFO>" to the reflected content of the chat (which may be terminated chat without "<INFO>" mark)
        # 2. without "<INFO>" mark, which means the chat is terminated or normally ended without generating a marked conclusion, and there is no need to reflect
        for i in range(chat_turn_limit):
            # start the chat, we represent the user and send msg to assistant
            # 1. so the input_user_msg should be assistant_role_prompt + phase_prompt
            # 2. then input_user_msg send to LLM and get assistant_response
            # 3. now we represent the assistant and send msg to user, so the input_assistant_msg is user_role_prompt + assistant_response
            # 4. then input_assistant_msg send to LLM and get user_response
            # all above are done in role_play_session.step, which contains two interactions with LLM
            # the first interaction is logged in role_play_session.init_chat
            assistant_response, user_response = role_play_session.step(input_user_msg, chat_turn_limit == 1, chat_env.env_dict["model_source"], chat_env.env_dict["temperature"], chat_env.env_dict["top_p"])

            conversation_meta = "**" + assistant_role_name + "<->" + user_role_name + " on : " + str(
                phase_name) + ", turn " + str(i) + "**\n\n"

            # TODO: max_tokens_exceeded errors here
            if isinstance(assistant_response.msg, ChatMessage):
                # we log the second interaction here
                log_and_print_online(role_play_session.assistant_agent.role_name,
                                     conversation_meta + "[" + role_play_session.user_agent.system_message.content + "]\n\n" + assistant_response.msg.content)
                if role_play_session.assistant_agent.info:
                    seminar_conclusion = assistant_response.msg.content
                    break
                if assistant_response.terminated:
                    break

            if isinstance(user_response.msg, ChatMessage):
                # here is the result of the second interaction, which may be used to start the next chat turn
                log_and_print_online(role_play_session.user_agent.role_name,
                                     conversation_meta + "[" + role_play_session.assistant_agent.system_message.content + "]\n\n" + user_response.msg.content)
                if role_play_session.user_agent.info:
                    seminar_conclusion = user_response.msg.content
                    break
                if user_response.terminated:
                    break

            # continue the chat
            if chat_turn_limit > 1 and isinstance(user_response.msg, ChatMessage):
                input_user_msg = user_response.msg
            else:
                break

        # conduct self reflection
        if need_reflect:
            if seminar_conclusion in [None, ""]:
                seminar_conclusion = "<INFO> " + self.self_reflection(task_prompt, role_play_session, phase_name,
                                                                      chat_env)
            if "recruiting" in phase_name:
                if "Yes".lower() not in seminar_conclusion.lower() and "No".lower() not in seminar_conclusion.lower():
                    seminar_conclusion = "<INFO> " + self.self_reflection(task_prompt, role_play_session,
                                                                          phase_name,
                                                                          chat_env)
            elif seminar_conclusion in [None, ""]:
                seminar_conclusion = "<INFO> " + self.self_reflection(task_prompt, role_play_session, phase_name,
                                                                      chat_env)
        else:
            seminar_conclusion = assistant_response.msg.content

        log_and_print_online("**[Seminar Conclusion]**:\n\n {}".format(seminar_conclusion))
        seminar_conclusion = seminar_conclusion.split("<INFO>")[-1]
        return seminar_conclusion

    def self_reflection(self,
                        task_prompt: str,
                        role_play_session: RolePlaying,
                        phase_name: str,
                        chat_env: DevAgentEnv) -> str:
        """

        Args:
            task_prompt: user query prompt for building the software
            role_play_session: role play session from the chat phase which needs reflection
            phase_name: name of the chat phase which needs reflection
            chat_env: global chatchain environment

        Returns:
            reflected_content: str, reflected results

        """
        messages = role_play_session.assistant_agent.stored_messages if len(
            role_play_session.assistant_agent.stored_messages) >= len(
            role_play_session.user_agent.stored_messages) else role_play_session.user_agent.stored_messages
        messages = ["{}: {}".format(message.role_name, message.content.replace("\n\n", "\n")) for message in messages]
        messages = "\n\n".join(messages)

        if "recruiting" in phase_name:
            question = """Answer their final discussed conclusion (Yes or No) in the discussion without any other words, e.g., "Yes" """
        elif phase_name == "DemandAnalysis":
            question = """Answer their final product modality in the discussion without any other words, e.g., "PowerPoint" """
        elif phase_name == "LanguageChoose":
            question = """Conclude the programming language being discussed for software development, in the format: "*" where '*' represents a programming language." """
        elif phase_name == "EnvironmentDoc":
            question = """According to the codes and file format listed above, write a requirements.txt file to specify the dependencies or packages required for the project to run properly." """
        else:
            raise ValueError(f"Reflection of phase {phase_name}: Not Assigned.")

        # Reflections actually is a special phase between CEO and counselor
        # They read the whole chatting history of this phase and give refined conclusion of this phase
        reflected_content = \
            self.chatting(chat_env=chat_env,
                          task_prompt=task_prompt,
                          assistant_role_name="Chief Executive Officer",
                          user_role_name="Counselor",
                          phase_prompt=self.reflection_prompt,
                          phase_name="Reflection",
                          assistant_role_prompt=self.ceo_prompt,
                          user_role_prompt=self.counselor_prompt,
                          placeholders={"conversations": messages, "question": question},
                          need_reflect=False,
                          chat_turn_limit=1,
                          model_type=self.model_type)

        if "recruiting" in phase_name:
            if "Yes".lower() in reflected_content.lower():
                return "Yes"
            return "No"
        else:
            return reflected_content

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

    def execute(self, chat_env, chat_turn_limit, need_reflect) -> DevAgentEnv:
        """
        execute the chatting in this phase
        1. receive information from environment: update the phase environment from global environment
        2. execute the chatting
        3. change the environment: update the global environment using the conclusion
        Args:
            chat_env: global chat chain environment
            chat_turn_limit: turn limit in each chat
            need_reflect: flag for reflection

        Returns:
            chat_env: updated global chat chain environment using the conclusion from this phase execution

        """
        self.update_phase_env(chat_env)
        self.seminar_conclusion = \
            self.chatting(chat_env=chat_env,
                          task_prompt=chat_env.env_dict['task_prompt'],
                          need_reflect=need_reflect,
                          assistant_role_name=self.assistant_role_name,
                          user_role_name=self.user_role_name,
                          phase_prompt=self.phase_prompt,
                          phase_name=self.phase_name,
                          assistant_role_prompt=self.assistant_role_prompt,
                          user_role_prompt=self.user_role_prompt,
                          chat_turn_limit=chat_turn_limit,
                          placeholders=self.phase_env,
                          model_type=self.model_type)
        chat_env = self.update_chat_env(chat_env)
        return chat_env

class UMLClass(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"prd": chat_env.env_dict['prd']})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_uml_classes(self.seminar_conclusion)
        chat_env.rewrite_uml_classes()
        chat_env.env_dict["uml_class"] = self.seminar_conclusion
        return chat_env


class UMLSequenceFlow(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"prd": chat_env.env_dict['prd']})
        self.phase_env.update({'uml_class':chat_env.env_dict['uml_class']})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_uml_sequences(self.seminar_conclusion)
        chat_env.rewrite_uml_sequences()
        chat_env.env_dict["uml_sequence"] = self.seminar_conclusion
        return chat_env


class ArchitectureDesign(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"prd": chat_env.env_dict['prd']})
        self.phase_env.update({'uml_class':chat_env.env_dict['uml_class']})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_architecture_designs(self.seminar_conclusion)
        chat_env.rewrite_architecture_designs()
        chat_env.env_dict["architecture_design"] = self.seminar_conclusion
        return chat_env


class EnvironmentDoc(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "uml_class": chat_env.env_dict['uml_class'],
                               "uml_sequence": chat_env.env_dict['uml_sequence'],
                               "architecture_design": chat_env.env_dict["architecture_design"],
                               "language": chat_env.env_dict["language"],
                               "filename": "requirements.txt" if chat_env.env_dict["language"] == "python" else "package.json",
                               "command_rc": chat_env.env_dict["command_rc"] if "command_rc" in chat_env.env_dict.keys() else -1,
                               "command_modification": chat_env.env_dict["command_modification"] if "command_modification" in chat_env.env_dict.keys() else "",
                               "command_output": chat_env.env_dict["command_output"] if "command_output" in chat_env.env_dict.keys() else "",
                               "usage_rcs": chat_env.env_dict["usage_rcs"] if "usage_rcs" in chat_env.env_dict.keys() else True,
                               "usage_outputs": chat_env.env_dict["usage_outputs"] if "usage_outputs" in chat_env.env_dict.keys() else ""})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_requirements(self.seminar_conclusion, predifined_filename=self.phase_env["filename"])
        chat_env.rewrite_requirements()
        if chat_env.env_dict["language"] == "python":
            chat_env.check_commands("conda remove --name myenv --all -y".split(' '), chat_env.requirements.directory)
            chat_env.check_commands("conda create --name myenv python=3.10 -y".split(' '), chat_env.requirements.directory)
            (command_output, command_rc) = chat_env.check_commands("conda run -n myenv pip install -r requirements.txt".split(' '), chat_env.requirements.directory)
        else:
            command_output = str()
            command_rc = 0
        usage_outputs = []
        usage_rcs = False
        if chat_env.env_dict["review"] == "execution":
            for example in chat_env.env_dict['usage_examples']:
                if example.endswith(".sh"):
                    (usage_output, usage_rc) = chat_env.check_commands(["conda", "run", "-n", "myenv", "sh", example], chat_env.requirements.directory)
                    if usage_rc != 0:
                        usage_outputs.append(usage_output)
                        usage_rcs = True
            chat_env.env_dict.update({
                    "command_output": command_output if command_rc != 0  else "",
                    "dependencies": chat_env.get_requirements(),
                    "command_rc": command_rc,
                    "usage_outputs": '\n'.join(usage_outputs),
                    "usage_rcs": usage_rcs
                })
                                    
                # chat_env.env_dict["command_rc"] = command_rc
                # chat_env.env_dict["usage_rc"] = usage_rc
                # chat_env.env_dict["command_output"] = command_output
            if command_rc != 0:
                log_and_print_online("**[Command Errors]**:\n\n{}".format(command_output))
        elif chat_env.env_dict["review"] == "normal":
            chat_env.env_dict.update({
                    "command_output": "",
                    "dependencies": chat_env.get_requirements(),
                    "command_rc": command_rc,
                    "usage_outputs": "",
                    "usage_rcs": usage_rcs
                })
        return chat_env


class EnvironmentReview(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "uml_class": chat_env.env_dict['uml_class'],
                               "uml_sequence": chat_env.env_dict['uml_sequence'],
                               "architecture_design": chat_env.env_dict["architecture_design"],
                               "command_rc": chat_env.env_dict["command_rc"] if "command_rc" in chat_env.env_dict.keys() else -1,
                               "dependencies": chat_env.env_dict["dependencies"],
                               "command_output": chat_env.env_dict["command_output"] if "command_output" in chat_env.env_dict.keys() else "",
                               "usage_rcs": chat_env.env_dict["usage_rcs"] if "usage_rcs" in chat_env.env_dict.keys() else True,
                               "usage_outputs": chat_env.env_dict["usage_outputs"] if "usage_outputs" in chat_env.env_dict.keys() else ""})


    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.env_dict["command_modification"] = self.seminar_conclusion
        return chat_env


class Coding(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "uml_class": chat_env.env_dict['uml_class'],
                               "uml_sequence": chat_env.env_dict['uml_sequence'],
                               "golden_plan": chat_env.env_dict["golden_plan"],
                               "next_plan_id": chat_env.env_dict["next_plan_id"],
                               "next_code_filename": chat_env.env_dict["next_code_filename"],
                               "architecture_design": chat_env.env_dict["architecture_design"],
                               "previous_code": chat_env.get_codes(),
                               "current_code": chat_env.get_codefiles([chat_env.env_dict["next_code_filename"]]),
                               "current_coding_turn": chat_env.env_dict["current_coding_turn"],
                               "execution_feedback": chat_env.env_dict["execution_feedback"],
                               "code_modification": chat_env.env_dict["code_modification"]})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_codes(self.seminar_conclusion, chat_env.env_dict["next_code_filename"])
        chat_env.rewrite_codes()
        filename = chat_env.env_dict["next_code_filename"]
        chat_env.env_dict["codes"] = chat_env.get_codefiles([filename])
        chat_env.env_dict["next_plan_id"] += 1
        if chat_env.env_dict["next_plan_id"] < len(chat_env.env_dict["golden_plan"]):
            chat_env.env_dict["next_code_filename"] = chat_env.env_dict["golden_plan"][chat_env.env_dict["next_plan_id"]]
        return chat_env


class CodeReview(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        execution_feedback = chat_env.get_feedback()
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                            "uml_class": chat_env.env_dict['uml_class'],
                            "uml_sequence": chat_env.env_dict['uml_sequence'],
                            "golden_plan": chat_env.env_dict["golden_plan"],
                            "next_plan_id": chat_env.env_dict["next_plan_id"],
                            "next_code_filename": chat_env.env_dict["next_code_filename"],
                            "architecture_design": chat_env.env_dict["architecture_design"],
                            "previous_code": chat_env.get_codes(),
                            "current_code": chat_env.get_codefiles([chat_env.env_dict["next_code_filename"]]),
                            "current_coding_turn": chat_env.env_dict["current_coding_turn"],
                            "execution_feedback": execution_feedback})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        execution_feedback = chat_env.get_feedback()
        if execution_feedback != "":
            chat_env.env_dict["code_modification"] = self.seminar_conclusion
        else:
            chat_env.env_dict["code_modification"] = str()
        return chat_env


class AcceptanceTestCoding(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        execution_feedback = chat_env.get_feedback() if chat_env.env_dict["review"] == "execution" else str()
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "uml_class": chat_env.env_dict['uml_class'],
                               "uml_sequence": chat_env.env_dict['uml_sequence'],
                               "architecture_design": chat_env.env_dict["architecture_design"],
                               "codes": chat_env.get_codes(),
                               "acceptance_test_codes": "" if self.phase_env["filename"] not in chat_env.env_dict["acceptance_test_codes"] else chat_env.env_dict["acceptance_test_codes"][self.phase_env["filename"]],
                               "code_modification": "" if self.phase_env["filename"] not in chat_env.env_dict["code_modification"] else chat_env.env_dict["code_modification"][self.phase_env["filename"]],
                               "filename": self.phase_env["filename"],
                               "coding_prompt": "you should write an acceptance test code" if self.phase_env["filename"] not in chat_env.env_dict["acceptance_test_codes"] else "you should update the acceptance test code based on the code modification.",
                               "execution_feedback": execution_feedback
                               })

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_acceptance_test_codes(self.seminar_conclusion, self.phase_env["filename"])
        chat_env.rewrite_acceptance_test_codes()
        chat_env.env_dict["acceptance_test_codes"][self.phase_env["filename"]] = self.seminar_conclusion
        return chat_env


class AcceptanceTestCodeReview(Phase):
    def update_phase_env(self, chat_env):
        execution_feedback = chat_env.get_feedback() if chat_env.env_dict["review"] == "execution" else str()
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "acceptance_test_codes": chat_env.env_dict["acceptance_test_codes"][self.phase_env["filename"]],
                               "execution_feedback": execution_feedback})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.env_dict["code_modification"][self.phase_env["filename"]] = self.seminar_conclusion
        return chat_env


class UnitTestCoding(Phase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_phase_env(self, chat_env):
        execution_feedback = chat_env.get_feedback() if chat_env.env_dict["review"] == "execution" else str()
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "uml_class": chat_env.env_dict['uml_class'],
                               "uml_sequence": chat_env.env_dict['uml_sequence'],
                               "architecture_design": chat_env.env_dict["architecture_design"],
                               "code_modification": "" if self.phase_env["filename"] not in chat_env.env_dict["code_modification"] else chat_env.env_dict["code_modification"][self.phase_env["filename"]],
                               "unit_test_codes": "" if self.phase_env["filename"] not in chat_env.env_dict["unit_test_codes"] else chat_env.env_dict["unit_test_codes"][self.phase_env["filename"]],
                               "filename": self.phase_env["filename"],
                               "coding_prompt": "you should write a unit test code" if self.phase_env["filename"] not in chat_env.env_dict["unit_test_codes"] else "you should update the unit test code based on the code modification.",
                               "execution_feedback": execution_feedback
                               })

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.update_unit_test_codes(self.seminar_conclusion, self.phase_env["filename"])
        chat_env.rewrite_unit_test_codes()
        chat_env.env_dict["unit_test_codes"][self.phase_env["filename"]] = self.seminar_conclusion
        return chat_env


class UnitTestCodeReview(Phase):
    def update_phase_env(self, chat_env):
        execution_feedback = chat_env.get_feedback() if chat_env.env_dict["review"] == "execution" else str()
        self.phase_env.update({"prd": chat_env.env_dict['prd'],
                               "unit_test_codes": chat_env.env_dict["unit_test_codes"][self.phase_env["filename"]],
                               "execution_feedback": execution_feedback})

    def update_chat_env(self, chat_env) -> DevAgentEnv:
        chat_env.env_dict["code_modification"][self.phase_env["filename"]] = self.seminar_conclusion
        return chat_env
