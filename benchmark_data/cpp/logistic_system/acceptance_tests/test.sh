#!/bin/bash

# Path to the executable
IMPLEMENTATION_DIR="."
EXECUTABLE="./logistics"
mkdir "./data"
mkdir "./outputs"
cp "acceptance_tests/account_init.txt" "./data/account.txt"
cp "acceptance_tests/expressage_init.txt" "./data/expressage.txt"

# Base paths
INPUT_BASE="./inputs"
OUTPUT_BASE="./outputs"
EXPECTED_BASE="./expected_outputs"

# Build the program using Makefile
cd "${IMPLEMENTATION_DIR}"
make clean
make
BUILD_STATUS=$?

if [[ "${BUILD_STATUS}" -ne 0 ]]; then
    echo "Build failed"
    exit 1
fi

CNT=0

# Iterate over the test files
for i in 000 001 002 003 004 005 006; do

    INPUT_FILE="${INPUT_BASE}/test${i}"
    OUTPUT_FILE="${OUTPUT_BASE}/test${i}"
    EXPECTED_FILE="${EXPECTED_BASE}/test${i}"

    # Run the executable
    "${EXECUTABLE}" < "${INPUT_FILE}" > "${OUTPUT_FILE}"

    # Compare the output with the expected output
    DIFF=$(diff "${OUTPUT_FILE}" "${EXPECTED_FILE}")

    if [[ -z "${DIFF}" ]]; then
        echo "Test ${CNT}: [PASSED]."
    else
        echo "Test ${CNT}: [FAILED]."
    fi
    
    CNT=$((CNT+1))

done