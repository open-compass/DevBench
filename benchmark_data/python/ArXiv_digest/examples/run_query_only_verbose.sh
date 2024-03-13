#! /bin/bash
# Query with all parameters given
# Results only print to console

python query_arxiv.py \
--category cs.CL \
--title LLM \
--author Smith \
--abstract Deep+Learning \
--recent_days 10 \
--verbose \
>> output/query_only_verbose_results.txt