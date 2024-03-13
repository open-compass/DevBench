#! /bin/bash

mkdir -p outputs

make clean
make
./area_calculation inputs/1.txt outputs/1.txt
