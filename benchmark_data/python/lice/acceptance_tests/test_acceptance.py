import subprocess
import os
import sys
import tempfile
import re

def run_lice(arguments):
    """
    Helper function to run the lice command with the provided arguments.
    """
    cmd = [sys.executable, 'lice/core.py'] + arguments
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def assert_in_license(content, expected_string):
    """
    Asserts that the expected string is in the license content, ignoring
    leading/trailing whitespace and line endings.
    """
    content = content.strip().replace('\r\n', '\n')
    assert expected_string in content

def test_default_license_generation():
    """
    Test if the default license (BSD3) is generated when no license is specified.
    """
    stdout, stderr, returncode = run_lice([])
    assert_in_license(stdout, "All rights reserved.")
    assert returncode == 0

def test_specified_license_generation():
    """
    Test if a specified license (MIT) is generated correctly.
    """
    stdout, stderr, returncode = run_lice(['mit'])
    assert_in_license(stdout, "Permission is hereby granted")
    assert returncode == 0

def test_license_with_organization():
    """
    Test if the organization name is replaced correctly.
    """
    organization = "TestOrg"
    stdout, stderr, returncode = run_lice(['-o', organization])
    assert_in_license(stdout, organization)
    assert returncode == 0

def test_license_with_year():
    """
    Test if the year is replaced correctly.
    """
    year = "2023"
    stdout, stderr, returncode = run_lice(['-y', year])
    assert_in_license(stdout, year)
    assert returncode == 0

def test_license_with_project():
    """
    Test if the project name is replaced correctly.
    """
    project = "TestProject"
    stdout, stderr, returncode = run_lice(['-p', project])
    assert_in_license(stdout, project)
    assert returncode == 0

def test_license_with_output_file():
    """
    Test if the license is written to a file.
    """
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        run_lice(['-f', tmp_file.name])
        tmp_file.seek(0)
        content = tmp_file.read().decode('utf-8')
        assert_in_license(content, "All rights reserved.")

def run_tests():
    """
    Run all the acceptance tests.
    """
    test_default_license_generation()
    test_specified_license_generation()
    test_license_with_organization()
    test_license_with_year()
    test_license_with_project()
    test_license_with_output_file()
    print("All acceptance tests passed!")

if __name__ == "__main__":
    run_tests()
