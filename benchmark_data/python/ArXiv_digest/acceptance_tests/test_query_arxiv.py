import pandas as pd
import os
import re
import unittest
import shutil

class TestQueryArxiv(unittest.TestCase):

    # Test cases
    def test_acceptance_category_search(self):

        os.makedirs("output_temp", exist_ok=True)

        # Standard Code for reference
        os.system('python query_arxiv.py --category cs.CL --max_results=10 --recent_days 5 --to_file output_temp/reference_output.csv --verbose >> output_temp/reference_output.txt')
        
        # test script
        os.system('python query_arxiv.py --category cs.CL --max_results=10 --recent_days 5 --to_file output_temp/test_output.csv --verbose >> output_temp/test_output.txt')

        # Compare terminal output with reference
        with open("output_temp/reference_output.txt", "r") as ref_file, open(f"output_temp/reference_output.txt", "r") as test_file:
            reference_output = ref_file.read()
            test_output = test_file.read()
            # Regular expression to get the first line of each param of reference_output
            titles = re.findall(r"Title:\s*(.*?)\n", reference_output)
            authors = re.findall(r"Authors:\s*(.*?)\n", reference_output)
            abstracts = re.findall(r"Abstract:\s*(.*?)\n", reference_output)
            published_dates = re.findall(r"Published Date:\s*(.*?)\n", reference_output)
            links = re.findall(r"Link:\s*(.*?)\n?", reference_output)

            # Comparison
            for title in titles:
                assert title in test_output, f"Title '{title}' not found in terminal output."
            for author in authors:
                assert author in test_output, f"Author '{author}' not found in terminal output."
            for abstract in abstracts:
                assert abstract in test_output, f"Abstract '{abstract}' not found in terminal output."
            for date in published_dates:
                assert date in test_output, f"Published date '{date}' not found in terminal output."
            for link in links:
                assert link in test_output, f"Link '{link}' not found in terminal output."
        
        # Compare the CSV file output with reference CSV using Pandas
        df_reference = pd.read_csv("output_temp/reference_output.csv")
        df_test = pd.read_csv("output_temp/test_output.csv")
        pd.testing.assert_frame_equal(df_reference, df_test)

        # Cleanup
        shutil.rmtree("output_temp")

    def test_acceptance_title_search(self):
        
        os.makedirs("output_temp", exist_ok=True)

        # Standard Code for reference
        os.system('python query_arxiv.py --title LLM --max_results=10 --recent_days 5 --to_file output_temp/reference_output.csv --verbose >> output_temp/reference_output.txt')
        
        # test script
        os.system('python query_arxiv.py --title LLM --max_results=10 --recent_days 5 --to_file output_temp/test_output.csv --verbose >> output_temp/test_output.txt')

        # Compare terminal output with reference
        with open("output_temp/reference_output.txt", "r") as ref_file, open(f"output_temp/reference_output.txt", "r") as test_file:
            reference_output = ref_file.read()
            test_output = test_file.read()
            # Regular expression to get the first line of each param of reference_output
            titles = re.findall(r"Title:\s*(.*?)\n", reference_output)
            authors = re.findall(r"Authors:\s*(.*?)\n", reference_output)
            abstracts = re.findall(r"Abstract:\s*(.*?)\n", reference_output)
            published_dates = re.findall(r"Published Date:\s*(.*?)\n", reference_output)
            links = re.findall(r"Link:\s*(.*?)\n?", reference_output)

            # Comparison
            for title in titles:
                assert title in test_output, f"Title '{title}' not found in terminal output."
            for author in authors:
                assert author in test_output, f"Author '{author}' not found in terminal output."
            for abstract in abstracts:
                assert abstract in test_output, f"Abstract '{abstract}' not found in terminal output."
            for date in published_dates:
                assert date in test_output, f"Published date '{date}' not found in terminal output."
            for link in links:
                assert link in test_output, f"Link '{link}' not found in terminal output."
        
        # Compare the CSV file output with reference CSV using Pandas
        df_reference = pd.read_csv("output_temp/reference_output.csv")
        df_test = pd.read_csv("output_temp/test_output.csv")
        pd.testing.assert_frame_equal(df_reference, df_test)

        # Cleanup
        shutil.rmtree("output_temp")

    def test_acceptance_author_search(self):

        os.makedirs("output_temp", exist_ok=True)

        # Standard Code for reference
        os.system('python query_arxiv.py --author Smith --max_results=10 --recent_days 20 --to_file output_temp/reference_output.csv --verbose >> output_temp/reference_output.txt')
        
        # test script
        os.system('python query_arxiv.py --author Smith --max_results=10 --recent_days 20 --to_file output_temp/test_output.csv --verbose >> output_temp/test_output.txt')

        # Compare terminal output with reference
        with open("output_temp/reference_output.txt", "r") as ref_file, open(f"output_temp/reference_output.txt", "r") as test_file:
            reference_output = ref_file.read()
            test_output = test_file.read()
            # Regular expression to get the first line of each param of reference_output
            titles = re.findall(r"Title:\s*(.*?)\n", reference_output)
            authors = re.findall(r"Authors:\s*(.*?)\n", reference_output)
            abstracts = re.findall(r"Abstract:\s*(.*?)\n", reference_output)
            published_dates = re.findall(r"Published Date:\s*(.*?)\n", reference_output)
            links = re.findall(r"Link:\s*(.*?)\n?", reference_output)

            # Comparison
            for title in titles:
                assert title in test_output, f"Title '{title}' not found in terminal output."
            for author in authors:
                assert author in test_output, f"Author '{author}' not found in terminal output."
            for abstract in abstracts:
                assert abstract in test_output, f"Abstract '{abstract}' not found in terminal output."
            for date in published_dates:
                assert date in test_output, f"Published date '{date}' not found in terminal output."
            for link in links:
                assert link in test_output, f"Link '{link}' not found in terminal output."
        
        # Compare the CSV file output with reference CSV using Pandas
        df_reference = pd.read_csv("output_temp/reference_output.csv")
        df_test = pd.read_csv("output_temp/test_output.csv")
        pd.testing.assert_frame_equal(df_reference, df_test)

        # Cleanup
        shutil.rmtree("output_temp")

    def test_acceptance_abstract_search(self):

        os.makedirs("output_temp", exist_ok=True)

        # Standard Code for reference
        os.system('python query_arxiv.py --abstract Deep+Learning --max_results=10 --recent_days 5 --to_file output_temp/reference_output.csv --verbose >> output_temp/reference_output.txt')
        
        # test script
        os.system('python query_arxiv.py --abstract Deep+Learning --max_results=10 --recent_days 5 --to_file output_temp/test_output.csv --verbose >> output_temp/test_output.txt')

        # Compare terminal output with reference
        with open("output_temp/reference_output.txt", "r") as ref_file, open(f"output_temp/reference_output.txt", "r") as test_file:
            reference_output = ref_file.read()
            test_output = test_file.read()
            # Regular expression to get the first line of each param of reference_output
            titles = re.findall(r"Title:\s*(.*?)\n", reference_output)
            authors = re.findall(r"Authors:\s*(.*?)\n", reference_output)
            abstracts = re.findall(r"Abstract:\s*(.*?)\n", reference_output)
            published_dates = re.findall(r"Published Date:\s*(.*?)\n", reference_output)
            links = re.findall(r"Link:\s*(.*?)\n?", reference_output)

            # Comparison
            for title in titles:
                assert title in test_output, f"Title '{title}' not found in terminal output."
            for author in authors:
                assert author in test_output, f"Author '{author}' not found in terminal output."
            for abstract in abstracts:
                assert abstract in test_output, f"Abstract '{abstract}' not found in terminal output."
            for date in published_dates:
                assert date in test_output, f"Published date '{date}' not found in terminal output."
            for link in links:
                assert link in test_output, f"Link '{link}' not found in terminal output."
        
        # Compare the CSV file output with reference CSV using Pandas
        df_reference = pd.read_csv("output_temp/reference_output.csv")
        df_test = pd.read_csv("output_temp/test_output.csv")
        pd.testing.assert_frame_equal(df_reference, df_test)

        # Cleanup
        shutil.rmtree("output_temp")