import os
import csv
from query_arxiv import save_to_csv 

def test_no_papers_to_save(capfd):
    save_to_csv([], 'some_path/some_file.csv')
    captured = capfd.readouterr()  # Capture the print statement
    assert captured.out == "No papers to save.\n"

def test_directory_created(tmpdir):
    file_name = f"{tmpdir}/some_directory/some_file.csv"
    save_to_csv([{'id': "1", 'name': 'Test Paper'}], file_name)
    assert os.path.isdir(f"{tmpdir}/some_directory")  # Check if directory was created

def test_file_written(tmpdir):
    file_name = f"{tmpdir}/some_file.csv"
    papers = [{'id': "1", 'name': 'Test Paper'}, {'id': "2", 'name': 'Another Test Paper'}]
    save_to_csv(papers, file_name)
    
    # Check if file was written
    assert os.path.isfile(file_name)

    # Check the content of the file
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        assert [row for row in reader] == papers

def test_no_directory():
    file_name = "some_file.csv"
    paper = [{'id': "1", 'name': 'Test Paper'}]
    save_to_csv(paper, file_name)

    # Check if file was written
    assert os.path.isfile(file_name)

    # Check the content of the file
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        assert [row for row in reader] == paper
