#! /bin/bash
# Query with all parameters given
# Results only save to csv

python query_arxiv.py \
--category cs.CL \
--title LLM \
--author Smith \
--abstract Deep+Learning \
--recent_days 10 \
--to_file output/query_only_csv_results.csv