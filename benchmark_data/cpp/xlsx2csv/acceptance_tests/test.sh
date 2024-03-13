#!/bin/bash

# Path to the executable
IMPLEMENTATION_DIR="."
EXECUTABLE="../xlsx2csv"
mkdir "./outputs"
mkdir "./outputs/test001"
mkdir "./outputs/test002"
mkdir "./outputs/test003"

# Base paths
INPUT_BASE="../inputs"
OUTPUT_BASE="../outputs"
EXPECTED_BASE="../expected_outputs"

# Build the program using Makefile
cd "${IMPLEMENTATION_DIR}"
make clean
make
BUILD_STATUS=$?
cd "./acceptance_tests"

if [[ "${BUILD_STATUS}" -ne 0 ]]; then
    echo "Build failed"
    exit 1
fi

# Run the bad usage
OUTPUT=$(${EXECUTABLE})

if [[ "${OUTPUT}" == "Error: Please check the usage: ./xlsx2csv [xlsx filename] [output file path]" ]]; then
    echo "Test 0: [PASSED]. Details: Test Bad Usage passed"
else
    echo "Test 0: [FAILED]. Details: Test Bad Usage failed"
fi

# Run the bad input file
OUTPUT=$(${EXECUTABLE} ${INPUT_BASE}/test000.xlsx ${OUTPUT_BASE} 2>&1)

if [[ "${OUTPUT}" == "Error: Input File error." ]]; then
    echo "Test 1: [PASSED]. Details: Test Bad Input File passed"
else
    echo "Test 1: [FAILED]. Details: Test Bad Input File failed"
fi

CNT=1

# Iterate over the test files
for i in 001 002 003; do

    CNT=$((CNT+1))

    INPUT_FILE="${INPUT_BASE}/test${i}.xlsx"
    OUTPUT_DIR="${OUTPUT_BASE}/test${i}"
    EXPECTED_DIR="${EXPECTED_BASE}/test${i}"

    # Create the output directory if it doesn't exist
    mkdir -p "${OUTPUT_DIR}"

    # Run the executable
    OUTPUT=$(${EXECUTABLE} "${INPUT_FILE}" "${OUTPUT_DIR}" 2>&1)

    # Check for program usage message
    if [[ "${OUTPUT}" == "Error: Please check the usage: ./xlsx2csv [xlsx filename] [output file path]" ]]; then
        echo "Test ${CNT}: [FAILED]. Details: Wrong usage message."
        continue
    elif [[ "${OUTPUT}" == "Error: Input File error." ]]; then
        echo "Test ${CNT}: [FAILED]. Details: Wrong input file error message."
        continue
    elif [[ "${OUTPUT}" != "Conversion successful. CSV files generated." ]]; then
        echo "Test ${CNT}: [FAILED]. Details: Error message: ${OUTPUT}"
        continue
    fi

    DIFF=$(diff -r "${OUTPUT_DIR}" "${EXPECTED_DIR}")

    if [[ -z "${DIFF}" ]]; then
        echo "Test ${CNT}: [PASSED]."
    else
        echo "Test ${CNT}: [FAILED]."
    fi
done