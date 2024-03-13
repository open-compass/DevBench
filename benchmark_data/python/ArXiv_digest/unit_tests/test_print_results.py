from query_arxiv import print_results

def test_print_with_multiple_papers(capfd):
    papers = [
        {
            "title": "Paper 1",
            "authors": "Author 1",
            "abstract": "Abstract 1 " * 50,  # repeating to ensure it's long enough
            "published": "Date 1",
            "link": "Link 1"
        },
        {
            "title": "Paper 2",
            "authors": "Author 2",
            "abstract": "Abstract 2 " * 50,
            "published": "Date 2",
            "link": "Link 2"
        }
    ]
    print_results(papers)
    captured = capfd.readouterr()  # Capture the print output
    
    assert "Paper 1" in captured.out and "Paper 2" in captured.out
    assert "Author 1" in captured.out and "Author 2" in captured.out
    assert "Abstract 1" in captured.out and "Abstract 2" in captured.out
    assert "Date 1" in captured.out and "Date 2" in captured.out
    assert "Link 1" in captured.out and "Link 2" in captured.out

def test_abstract_truncation(capfd):
    paper = {
        "title": "Test Paper",
        "authors": "Test Author",
        "abstract": "Word1 " * 298 + "Word2 "*3,  # 301 words
        "published": "Test Date",
        "link": "Test Link"
    }
    
    print_results([paper])
    captured = capfd.readouterr()
    
    assert "Word1" in captured.out and "Word2" in captured.out
