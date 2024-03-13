#!/bin/bash

# Compile main.cpp
make

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# Create outputs directory if it doesn't exist
mkdir -p outputs

# Run the program with each input file and store the results in the corresponding output file
for i in 1 2 3; do
    if [ -f "inputs/$i.txt" ]; then
        ./area_calculation "inputs/$i.txt" "outputs/$i.txt"
        echo "Processed input/$i.txt and saved the output to outputs/$i.txt"
    else
        echo "inputs/$i.txt not found."
    fi
done

# Function to compare two floating point numbers with precision
compare_numbers() {
    awk -v num1="$1" -v num2="$2" 'BEGIN { 
        if (sprintf("%.3f", num1) == sprintf("%.3f", num2))
            exit 0
        else
            exit 1
    }'
}

# Compare output files with expected output files
for i in 1 2 3; do
    if [ -f "outputs/$i.txt" ] && [ -f "expected_outputs/$i.txt" ]; then
        while IFS= read -r lineA && IFS= read -r lineB <&3; do
            compare_numbers "$lineA" "$lineB"
            if [ $? -ne 0 ]; then
                echo "Mismatch found in file $i.txt"
                exit 1
            fi
        done <"outputs/$i.txt" 3<"expected_outputs/$i.txt"
        echo "File $i.txt matches"
    else
        echo "File $i.txt in outputs or expected_outputs not found."
    fi
done

# echo "All files match!"