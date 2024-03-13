import argparse
import os
from io import StringIO
import unittest
from unittest.mock import patch,mock_open
import sys

from lice import core
from lice.core import (
    LICENSES, clean_path, extract_vars, generate_license,
    format_license,get_suffix,load_file_template, 
    load_template,valid_year)



def test_paths():
    """
        Test the functionality of the `clean_path` function from the `lice.core` module.

        This function asserts that the `clean_path` function correctly transforms relative paths
        to their absolute path equivalents, and expands user and environment variables to their
        respective values.

        Args:
            None

        Returns:
            None: The function does not return a value but asserts that path transformations are correct.
    """
    assert clean_path(".") == os.getcwd()
    # On Windows, 'HOME' may not be set, so 'USERPROFILE' should be used.
    home_env_var = 'USERPROFILE' if os.name == 'nt' else 'HOME'
    expected_home_path = os.environ[home_env_var]
    assert clean_path(f"${home_env_var}") == expected_home_path
    assert clean_path("~") == expected_home_path


def test_file_template():
    """
        Test the ability to load license templates from file system paths.

        This function iterates over all licenses, constructs the path to the corresponding template
        file, and asserts that the content read from the file matches the content retrieved by the
        `load_file_template` function.

        Args:
            None

        Returns:
            None: The function does not return a value but asserts that the file templates are loaded correctly.
    """
    for license in LICENSES:
        path = f"templates/template-{license}.txt"
        with open(path, 'r', newline='') as infile:
            content = infile.read().strip()  # Strips newline characters
            file_template_content = load_file_template(path).getvalue().strip()
            assert content == file_template_content

def test_package_template():
    """
        Test the loading of license templates included in the package.

        For each license in the LICENSES list, this function asserts that the content returned by the
        `load_template` function matches the content of the corresponding template file within
        the package.

        Args:
            None

        Returns:
            None: The function does not return a value but asserts that the package templates are loaded correctly.
    """
    for license in LICENSES:
        path = f"templates/template-{license}.txt"
        with open(path, 'r', newline='') as infile:
            content = infile.read().strip()  # Strips newline characters
            package_template_content = load_template(license).getvalue().strip()
            assert content == package_template_content

def test_extract_vars():
    """
        Test the variable extraction from templates using the `extract_vars` function.

        Writes a test string into a StringIO object, then uses `extract_vars` to extract the template
        variables and asserts that the extracted variable list is correct.

        Args:
            None

        Returns:
            None: The function does not return a value but asserts that the template variables are extracted correctly.
    """
    template = StringIO()
    for license in LICENSES:
        template.write(u'Oh hey, {{ this }} is a {{ template }} test.')
        var_list = extract_vars(template)
        assert var_list == ["template", "this"]

def test_license():
    """
        Test the license content generation for all available licenses.

        Constructs a context dictionary with year, project, and organization, then for each license
        in LICENSES list, it loads the template, replaces the placeholders with the context, and asserts
        that the generated content matches the expected outcome.

        Args:
            None

        Returns:
            None: The function does not return a value but asserts that licenses are generated correctly.
    """
    context = {
        "year": u'1981',
        "project": u'lice',
        "organization": u'Awesome Co.'
    }

    for license in LICENSES:

        template = load_template(license)
        content = template.getvalue()

        content = content.replace(u'{{ year }}', context["year"])
        content = content.replace(u'{{ project }}', context["project"])
        content = content.replace(u'{{ organization }}',
                                    context["organization"])

        assert content == generate_license(template, context).getvalue()
        template.close()  # discard memory

def test_license_header():
    """
        Test the header generation for license files.

        Similar to `test_license`, but also attempts to load header templates for each license and
        asserts the generated content with headers matches the expected outcome. It passes silently
        if a header template is not found.

        Args:
            None

        Returns:
            None: The function does not return a value but asserts that license headers are generated correctly or skips if not applicable.
    """
    context = {
        "year": u'1981',
        "project": u'lice',
        "organization": u'Awesome Co.'
    }

    for license in LICENSES:

        try:

            template = load_template(license, header=True)
            content = template.getvalue()

            content = content.replace(u'{{ year }}', context["year"])
            content = content.replace(u'{{ project }}', context["project"])
            content = content.replace(u'{{ organization }}',
                                        context["organization"])

            assert content == generate_license(template, context).getvalue()
            template.close()  # discard memory

        except IOError:
            pass  # it's okay to not find templates


class TestFormatLicense(unittest.TestCase):
    def test_format_license_c_language(self):
        license_text = StringIO("Example License Text")
        formatted_text = format_license(license_text, "c").getvalue()
        expected_output = "/*\n * Example License Text */\n"
        self.assertEqual(formatted_text, expected_output)

    def test_format_license_python_language(self):
        license_text = StringIO("Example License Text")
        formatted_text = format_license(license_text, "py").getvalue()
        expected_output = "\n# Example License Text\n"
        self.assertEqual(formatted_text, expected_output)


class TestGetSuffix(unittest.TestCase):
    def test_valid_suffix(self):
        filename = "example.py"
        self.assertEqual(get_suffix(filename), "py")

    def test_no_suffix(self):
        filename = "example"
        self.assertFalse(get_suffix(filename))

    def test_unrecognized_suffix(self):
        filename = "example.xyz"
        self.assertFalse(get_suffix(filename))

class TestValidYear(unittest.TestCase):

    def test_valid_year(self):
        self.assertEqual(valid_year("2024"), "2024")

    def test_invalid_year_non_numeric(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_year("abc")

    def test_invalid_year_not_four_digits(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_year("202")

    def test_invalid_year_extra_characters(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            valid_year("2024abc")

class TestMainFunction(unittest.TestCase):

    def test_help_message(self):
        test_args = ["program", "-h"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                core.main()
            self.assertEqual(cm.exception.code, 0)

    def test_invalid_license(self):
        test_args = ["program", "invalid_license"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                core.main()
            self.assertNotEqual(cm.exception.code, 0)

    def test_valid_license(self):
        test_args = ["program", "bsd3"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO):
                core.main()

    def test_list_languages_option(self):
        test_args = ["program", "--languages"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.assertRaises(SystemExit) as cm:
                    core.main()
                self.assertEqual(cm.exception.code, 0)
                output = mock_stdout.getvalue()
                self.assertIn("cpp", output)

    def test_template_path_not_exist(self):
        test_args = ["program", "-t", "nonexistent_path"]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(ValueError) as cm:
                core.main()
            self.assertEqual(str(cm.exception), "path does not exist: nonexistent_path")

    def test_output_to_file(self):
        test_args = ["program", "bsd3", "-f", "output.txt"]
        with patch.object(sys, 'argv', test_args):
            with patch("builtins.open", new_callable=mock_open()) as mock_file:
                core.main()
                mock_file.assert_called_with("output.txt", "w")

    def test_list_template_vars(self):
            test_args = ["program", "--vars"]
            expected_output = "The bsd3 license template contains the following variables"

            with patch.object(sys, 'argv', test_args):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    with self.assertRaises(SystemExit):
                        core.main()
                    output = mock_stdout.getvalue()
                    self.assertIn(expected_output, output)

    def test_list_template_vars_with_custom_template(self):
        test_args = ["program", "--vars", "-t", "custom_template_path"]
        mock_template_content = "{{ variable1 }}\n{{ variable2 }}"

        with patch.object(sys, 'argv', test_args):
            with patch('lice.core.load_file_template', return_value=StringIO(mock_template_content)):
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    with self.assertRaises(SystemExit):
                        core.main()
                    output = mock_stdout.getvalue()
                    self.assertIn("variable1", output)
                    self.assertIn("variable2", output)

    def test_custom_organization(self):
        test_args = ["program", "-o", "CustomOrg"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                core.main()
                self.assertIn("CustomOrg", mock_stdout.getvalue())


    def test_custom_project(self):
        test_args = ["program", "-p", "CustomProject"]
        with patch.object(sys, 'argv', test_args):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                core.main()
                self.assertIn("CustomProject", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
