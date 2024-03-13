"""
Simple methods for processing JSON files
"""

import os
import json
from sys import stdout

'''
Write given JSON to given file, or standard output if filepath is "-".
'''

def output_json(json_struct, json_filepath):
    if json_filepath and json_filepath == "-":
        stdout.write(str(json_struct))
    else:
        with open(json_filepath, 'w') as f:
            json.dump(json_struct, f, indent=2, sort_keys=True)
