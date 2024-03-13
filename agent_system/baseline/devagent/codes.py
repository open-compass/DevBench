import difflib
import os
import re
import subprocess

from devagent.utils import log_and_print_online

class Codes:
    def __init__(self, generated_content="", file_name=None):
        self.directory: str = None
        self.version: float = 0.0
        self.generated_content: str = generated_content
        self.codebooks = {}
        self.new_codebooks = {}

        def extract_filename_from_line(lines):
            file_name = ""
            for candidate in re.finditer(r"(\w+\.\w+)", lines, re.DOTALL):
                file_name = candidate.group()
            return file_name
        
        if generated_content != "":
            regex = r"(.+?)\n```.*?\n(.*?)```"
            matches = re.finditer(regex, self.generated_content, re.DOTALL)
            for match in matches:
                code = match.group(2)
                group1 = match.group(1)
                if file_name is not None:
                    filename = file_name
                else:
                    filename = extract_filename_from_line(group1)
                if filename == "":
                    continue
                if filename is not None and code is not None and len(filename) > 0 and len(code) > 0:
                    self.codebooks[filename] = self._format_code(code)
                    return
            # Implementation content
            regex = r"```.*?\n(.*?)```"
            matches = re.finditer(regex, self.generated_content, re.DOTALL)
            for match in matches:
                code = match.group(1)
                filename = file_name
                if filename is not None and code is not None and len(filename) > 0 and len(code) > 0:
                    self.codebooks[filename] = self._format_code(code)
            
    def _format_code(self, code):
        code = "\n".join([line for line in code.split("\n") if len(line.strip()) > 0])
        return code
    
    def _update_codes(self, generated_content, file_name=None):
        new_codes = Codes(generated_content, file_name)
        self.new_codebooks = new_codes.codebooks
        differ = difflib.Differ()
        for key in new_codes.codebooks.keys():
            if key not in self.codebooks.keys() or self.codebooks[key] != new_codes.codebooks[key]:
                update_codes_content = "**[Update Codes]**\n\n"
                update_codes_content += "{} updated.\n".format(key)
                old_codes_content = self.codebooks[key] if key in self.codebooks.keys() else "# None"
                new_codes_content = new_codes.codebooks[key]

                lines_old = old_codes_content.splitlines()
                lines_new = new_codes_content.splitlines()

                unified_diff = difflib.unified_diff(lines_old, lines_new, lineterm='', fromfile='Old', tofile='New')
                unified_diff = '\n'.join(unified_diff)
                update_codes_content = update_codes_content + "\n\n" + """```
'''

'''\n""" + unified_diff + "\n```"

                log_and_print_online(update_codes_content)
                self.codebooks[key] = new_codes.codebooks[key]

    def _rewrite_codes(self) -> None:
        directory = self.directory
        rewrite_codes_content = "**[Rewrite Codes]**\n\n"
        if os.path.exists(directory) and len(os.listdir(directory)) > 0:
            self.version += 1.0
        if not os.path.exists(directory):
            os.mkdir(self.directory)
            rewrite_codes_content += "{} Created\n".format(directory)

        for filename in self.codebooks.keys():
            filepath = os.path.join(directory, filename)
            with open(filepath, "w", encoding="utf-8") as writer:
                writer.write(self.codebooks[filename])
                rewrite_codes_content += os.path.join(directory, filename) + " Wrote\n"

    def _get_codes(self) -> str:
        content = ""
        for filename in self.codebooks.keys():
            content += "The content of file {} is:\n```{}\n{}\n```\n\n".format(filename,
                                                       "python" if filename.endswith(".py") else filename.split(".")[
                                                           -1], self.codebooks[filename])
        return content
    
    def _get_codefiles(self, target_filenames):
        content = ""
        for filename in target_filenames:
            if filename in self.codebooks.keys():
                content += "{}\n```{}\n{}\n```\n\n".format(filename,
                                                       "python" if filename.endswith(".py") else filename.split(".")[
                                                           -1], self.codebooks[filename])
        return content

    def _load_from_hardware_files(self, directory, filenames) -> None:
        for filename in filenames:
            code = open(os.path.join(directory, filename), "r", encoding="utf-8").read()
            self.codebooks[filename] = self._format_code(code)

