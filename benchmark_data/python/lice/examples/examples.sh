#!/bin/bash

cd "$(dirname "$0")/.."
# Generate a BSD3 license using default options
python lice/core.py bsd3

# Generate an MIT license using default options
python lice/core.py mit

# Generate a GPL3 license for the year 2021 and organization 'ExampleOrg'
python lice/core.py gpl3 --year 2021 --org 'ExampleOrg'

# Generate a BSD2 license and save it to a file named 'LICENSE'
python lice/core.py bsd2 --file LICENSE
