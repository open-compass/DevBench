#! /bin/bash
# Run logistics

mkdir "./outputs"

INPUT_FILE_PATH="./inputs/test001"
OUTPUT_FILE_PATH="./outputs/test001"

./logistics < ${INPUT_FILE_PATH} > ${OUTPUT_FILE_PATH}