import pytest
from query_arxiv import construct_query_url

def test_query_url_header():
    query_url = construct_query_url(category='cs.CL', title=None, author=None, abstract=None)
    assert query_url.startswith('http://export.arxiv.org/api/query?')
    
def test_query_url_sort_by_submitted_date_descending():
    query_url = construct_query_url(category='cs.CL', title=None, author=None, abstract=None)
    assert 'sortBy=submittedDate' in query_url
    assert 'sortOrder=descending' in query_url

# Test Cases with one arg
def test_query_url_with_only_category():
    query_url = construct_query_url(category='cs.CL')
    assert 'cat:cs.CL' in query_url

def test_query_url_with_only_title():
    query_url = construct_query_url(title='Natural+Language+Processing')
    assert 'ti:Natural+Language+Processing' in query_url

def test_query_url_with_only_author():
    query_url = construct_query_url(author='John+Doe')
    assert 'au:John+Doe' in query_url

def test_query_url_with_only_abstract():
    query_url = construct_query_url(abstract='Machine+Learning+in+NLP')
    assert 'abs:Machine+Learning+in+NLP' in query_url

# Test Cases with two args
def test_query_url_with_category_and_title():
    query_url = construct_query_url(category='cs.CL', title='AI+Research')
    assert 'cat:cs.CL' in query_url
    assert 'ti:AI+Research' in query_url

def test_query_url_with_category_and_author():
    query_url = construct_query_url(category='cs.CL', author='Jane+Doe')
    assert 'cat:cs.CL' in query_url
    assert 'au:Jane+Doe' in query_url

def test_query_url_with_category_and_abstract():
    query_url = construct_query_url(category='cs.CL', abstract='Deep+Learning+Applications')
    assert 'cat:cs.CL' in query_url
    assert 'abs:Deep+Learning+Applications' in query_url

def test_query_url_with_title_and_author():
    query_url = construct_query_url(title='AI+Advances', author='John+Doe')
    assert 'ti:AI+Advances' in query_url
    assert 'au:John+Doe' in query_url

def test_query_url_with_title_and_abstract():
    query_url = construct_query_url(title='AI+Advances', abstract='Deep+Learning')
    assert 'ti:AI+Advances' in query_url
    assert 'abs:Deep+Learning' in query_url

def test_query_url_with_author_and_abstract():
    query_url = construct_query_url(author='Jane+Doe', abstract='Deep+Learning')
    assert 'au:Jane+Doe' in query_url
    assert 'abs:Deep+Learning' in query_url

# Test Cases with three args
def test_query_url_with_category_title_author():
    query_url = construct_query_url(category='cs.CL', title='AI+Advances', author='John+Doe')
    assert 'cat:cs.CL' in query_url
    assert 'ti:AI+Advances' in query_url
    assert 'au:John+Doe' in query_url

def test_query_url_with_category_title_abstract():
    query_url = construct_query_url(category='cs.CL', title='AI+Advances', abstract='Machine+Learning')
    assert 'cat:cs.CL' in query_url
    assert 'ti:AI+Advances' in query_url
    assert 'abs:Machine+Learning' in query_url

def test_query_url_with_category_author_abstract():
    query_url = construct_query_url(category='cs.CL', author='John+Doe', abstract='Machine+Learning')
    assert 'cat:cs.CL' in query_url
    assert 'au:John+Doe' in query_url
    assert 'abs:Machine+Learning' in query_url

def test_query_url_with_title_author_abstract():
    query_url = construct_query_url(title='Deep+Learning', author='Jane+Doe', abstract='NLP+Applications')
    assert 'ti:Deep+Learning' in query_url
    assert 'au:Jane+Doe' in query_url
    assert 'abs:NLP+Applications' in query_url

# Test Cases Four (All) arguments
def test_construct_query_all_arguments():
    query_url = construct_query_url(category='cs.CL', title='language', author='Smith', abstract='translation')
    assert all(param in query_url for param in ['cat:cs.CL', 'ti:language', 'au:Smith', 'abs:translation'])

# Test Cases for ValueError
def test_construct_query_special_characters_in_title():
    with pytest.raises(ValueError):
        construct_query_url(title='deep+learning+in*neural%networks', category=None, author=None, abstract=None)

def test_construct_query_non_ascii_characters_in_title():
    with pytest.raises(ValueError):
        construct_query_url(title='深度学习', category=None, author=None, abstract=None)

def test_construct_query_empty_query():
    with pytest.raises(ValueError):
        construct_query_url()

# Test Cases for assigning max_results
def test_construct_query_default_max_results():
    query_url = construct_query_url(category='cs.CL', title='language', author='Smith', abstract='translation')
    assert "max_results=100" in query_url

def test_construct_query_max_results():
    query_url = construct_query_url(category='cs.CL', max_results=500, title='language', author='Smith', abstract='translation')
    assert "max_results=500" in query_url

