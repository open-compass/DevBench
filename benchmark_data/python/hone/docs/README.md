# hone
[![PyPI version](https://badge.fury.io/py/hone.svg)](https://badge.fury.io/py/hone)
[![PyPI license](https://img.shields.io/pypi/l/hone.svg)](https://pypi.python.org/pypi/hone/)

Convert CSV to automatically nested JSON.

## Table of Contents
<!--ts-->
   + [Getting Started](#getting-started)
      + [Installation](#installation)
      + [Usage: Command Line](#usage-command-line)
      + [Usage: Python Module](#usage-python-module)
   + [Examples](#examples)
   + [Development](#development)
      + [Running tests](#running-tests)
   + [License](#license)
<!--te-->

## Getting Started
Available as both a [Python module](#usage-python-module) and a [command line tool](#usage-command-line).

### Installation
```
pip install hone
```

### Usage: Command Line
```shell
$ hone --help
usage: hone [-h] [-d [DELIMITERS]] [-s [SCHEMA]] csv_filepath json_filepath

positional arguments:
  csv_filepath          Specify the filepath for the file to read CSV data
                        from. To read from standard input, use a dash ("-") as
                        the value
  json_filepath         Specify the filepath for the file to output JSON data
                        to. To write to standard output, use a dash ("-") as
                        the value.

optional arguments:
  -h, --help            show this help message and exit
  -d [DELIMITERS], --delimiters [DELIMITERS]
                        Override the default delimiters for generating a
                        nested structure from column names. [DELIMITERS] must
                        be a Python-compatible list of strings. The default
                        value is [',', '_', ' '].
  -s [SCHEMA], --schema [SCHEMA]
                        Manually specify the schema that defines the structure
                        of the generated JSON, instead of having it
                        automatically generated. [SCHEMA] must be a valid JSON
                        object encoded as a string.
```

### Usage: Python Module
```python
import hone

optional_arguments = {
  "delimiters": [" ", "_", ","]
}
Hone = hone.Hone(**optional_arguments)
schema = Hone.get_schema('path/to/input.csv')  # nested JSON schema for input.csv
result = Hone.convert('path/to/input.csv', schema=schema)  # final structure, nested according to schema
```

## Examples

You can view all examples of conversions in the [examples](/examples) directory.
### CSV
| name  | birth day | birth month | birth year | reference | reference name | 
|-------|-----------|-------------|------------|-----------|----------------| 
| Bob   | 7         | May         | 1985       | TRUE      | Smith          | 
| Julia | 21        | January     | 1997       | FALSE     | N/A            | 
| Rick  | 12        | June        | 1996       | TRUE      | Clara          | 
### Generated JSON
```
[
  {
    "birth": {
      "day": "7",
      "month": "May",
      "year": "1985"
    },
    "name": "Bob",
    "reference": "TRUE",
    "reference name": "Smith"
  },
  {
    "birth": {
      "day": "21",
      "month": "January",
      "year": "1997"
    },
    "name": "Julia",
    "reference": "FALSE",
    "reference name": "N/A"
  },
  {
    "birth": {
      "day": "12",
      "month": "June",
      "year": "1996"
    },
    "name": "Rick",
    "reference": "TRUE",
    "reference name": "Clara"
  }
]
```

## Development
### Running tests
From the root directory of this repository, run `python3 -m unittest` to execute the entire test suite.

# License
Hone is licensed under the [MIT license](LICENSE).
