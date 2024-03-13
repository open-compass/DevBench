import xml.etree.ElementTree as ET
from datetime import datetime
from query_arxiv import process_entries

def test_process_entries_one_author():
    # Sample XML entry
    xml_sample = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Understanding Natural Language Processing</title>
    <published>2023-10-15T00:00:00Z</published>
    <author><name>John Doe</name></author>
    <summary>Summary of the paper</summary>
    <id>link of the paper</id>
  </entry>
</feed>"""
    root = ET.fromstring(xml_sample)
    entries = root.findall('default:entry', {'default': 'http://www.w3.org/2005/Atom'})
    
    papers = process_entries(entries, {'default': 'http://www.w3.org/2005/Atom'}, datetime(2023, 10, 16), 1)

    assert papers[0]['title'] == "Understanding Natural Language Processing"
    assert papers[0]['authors'] == "John Doe"
    assert papers[0]['abstract'] == "Summary of the paper"
    assert papers[0]['published'] == "2023-10-15T00:00:00Z"
    assert papers[0]['link'] == "link of the paper"

def test_process_entries_multiple_authors():
    # Sample XML entry
    xml_sample = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Understanding Natural Language Processing</title>
    <published>2023-10-15T00:00:00Z</published>
    <author>
      <name>First Author</name>
    </author>
    <author>
      <name>Second Author</name>
    </author>
    <author>
      <name>Third Author</name>
    </author>
    <summary>Summary of the paper</summary>
    <id>link of the paper</id>
  </entry>
</feed>"""
    root = ET.fromstring(xml_sample)
    entries = root.findall('default:entry', {'default': 'http://www.w3.org/2005/Atom'})
    
    papers = process_entries(entries, {'default': 'http://www.w3.org/2005/Atom'}, datetime(2023, 10, 16), 2)

    assert papers[0]['title'] == "Understanding Natural Language Processing"
    assert papers[0]['authors'] == "First Author, Second Author, Third Author"
    assert papers[0]['abstract'] == "Summary of the paper"
    assert papers[0]['published'] == "2023-10-15T00:00:00Z"
    assert papers[0]['link'] == "link of the paper"

def test_process_entries_out_of_date():
    # Sample XML entry
    xml_sample = """<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Understanding Natural Language Processing</title>
    <published>2023-10-15T00:00:00Z</published>
    <author>
      <name>First Author</name>
    </author>
    <author>
      <name>Second Author</name>
    </author>
    <author>
      <name>Third Author</name>
    </author>
    <summary>Summary of the paper</summary>
    <id>link of the paper</id>
  </entry>
</feed>"""
    root = ET.fromstring(xml_sample)
    entries = root.findall('default:entry', {'default': 'http://www.w3.org/2005/Atom'})
    
    papers = process_entries(entries, {'default': 'http://www.w3.org/2005/Atom'}, datetime(2023, 11, 11), 2)

    assert papers == []