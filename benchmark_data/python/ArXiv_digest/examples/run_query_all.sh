#! /bin/bash
# Query with all parameters given
# Results both print to console and stored as csv

python query_arxiv.py \
--category cs.CL \
--title LLM \
--author Smith \
--abstract Deep+Learning \
--recent_days 10 \
--to_file output/query_all_results.csv \
--verbose \
>> output/query_all_results.txt