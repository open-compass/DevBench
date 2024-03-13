All parameters script (both save to csv and print to console):
```python
python query_arxiv.py --category cs.CL --title LLM --author Smith --abstract Deep+Learning --recent_days 10 --to_file output/result.csv --verbose >> output/result.txt
```

All parameters script (only save to csv):
```python
python query_arxiv.py --category cs.CL --title LLM --author Smith --abstract Deep+Learning --recent_days 10 --to_file output/result.csv
```

All parameters script (only print to console):
```python
python query_arxiv.py --category cs.CL --title LLM --author Smith --abstract Deep+Learning --recent_days 10 --verbose
```

Only given category script (both save to csv and print to console):
```python
python query_arxiv.py --category cs.CL --recent_days 10 --to_file output/result.csv --verbose >> output/result.txt
```

Only given title script (both save to csv and print to console):
```python
python query_arxiv.py --title LLM --recent_days 10 --to_file output/result.csv --verbose >> output/result.txt
```

Only given author script (both save to csv and print to console):
```python
python query_arxiv.py --author Smith --recent_days 10 --to_file output/result.csv --verbose >> output/result.txt
```

Only given abstract script (both save to csv and print to console):
```python
python query_arxiv.py --abstract Deep+Learning --recent_days 10 --to_file output/result.csv --verbose >> output/result.txt
```

Run acceptance tests
```
export PYTHONPATH="/cpfs01/shared/public/libowen/Projects/DevBench/proj_data/lin:$PYTHONPATH"
pytest acceptance_tests/test.py
```