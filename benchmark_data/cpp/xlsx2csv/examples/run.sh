#! /bin/bash
# Run xlsx2csv

mkdir "./outputs"
mkdir "./outputs/test001"

INPUT_FILE_PATH="./inputs/test001.xlsx"
OUTPUT_FILE_PATH="./outputs/test001/"

./xlsx2csv ${INPUT_FILE_PATH} ${OUTPUT_FILE_PATH}