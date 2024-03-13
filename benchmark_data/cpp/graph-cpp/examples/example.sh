#!/bin/bash

inputFile="./inputs/sample_input.txt"  
outputFile="./test_outputs/sample_output.txt" 

cd "$(dirname "$0")/.."

make

./graph file "$inputFile" "$outputFile"