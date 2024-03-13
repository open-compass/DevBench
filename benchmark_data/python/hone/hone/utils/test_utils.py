"""
Simple methods used for tests
"""

import os
import json
import csv

'''
Open and parse a given JSON file.
'''

def parse_json_file(json_filepath):
    with open(json_filepath, 'r') as f:
        return json.load(f)

'''
Open and parse a given CSV file.
'''

def parse_csv_file(csv_filepath):
    with open(csv_filepath, newline='') as f:
        csvreader = csv.reader(f)
        return list(csvreader)
