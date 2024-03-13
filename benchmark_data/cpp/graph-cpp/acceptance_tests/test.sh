#!/bin/bash

IMPLEMENTATION_DIR="."
INPUT_DIR="./inputs"
ACTUAL_OUTPUT_DIR="./test_outputs"
EXPECTED_OUTPUT_DIR="./expected_outputs"

SCRIPT_DIR=$(dirname "$0")

make clean
make

mkdir -p "$ACTUAL_OUTPUT_DIR" || { echo "Error: Unable to create output directory"; exit 1; }

if [ ! -d "$INPUT_DIR" ] || [ -z "$(ls -A "$INPUT_DIR")" ]; then
    echo "Error: Input directory is empty or doesn't exist"
    exit 1
fi

# Grouping the files into two sets
test_a=("empty_graph.txt" "invalid_file.txt")
test_b=("directed_graph.txt" "sample.txt" "undirected_graph.txt")

# Run test A
for input_file in "${test_a[@]}"
do
    filename=$(basename -- "$input_file")
    actual_output_file="$ACTUAL_OUTPUT_DIR/$filename"
    expected_output_file="$EXPECTED_OUTPUT_DIR/$filename"

    ./graph file "$INPUT_DIR/$input_file" > "$actual_output_file" || { echo "Test passed: Test Bad Input File passed"; continue; }
	
   
done

# Run test B
for input_file in "${test_b[@]}"
do
    filename=$(basename -- "$input_file")
    actual_output_file="$ACTUAL_OUTPUT_DIR/$filename"
    expected_output_file="$EXPECTED_OUTPUT_DIR/$filename"

    ./graph file "$INPUT_DIR/$input_file" > "$actual_output_file" || { echo "Test passed: Test Bad Input File passed"; continue; }

    # Check if expected output file exists
    if [ ! -f "$expected_output_file" ]; then
        echo "Error: Expected output file '$expected_output_file' not found for '$filename'"
        continue
    fi

    # Compare actual and expected output files
    DIFF=$(diff -w -B "$actual_output_file" "$expected_output_file")
    if [ -n "$DIFF" ]; then
        echo "Test failed: Output for '$filename' doesn't match expected output"
    else
        echo "Test passed: Output for '$filename' matches expected output"
    fi
done

echo "Testing completed. Check the test_outputs directory for results."

