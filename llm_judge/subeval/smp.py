# flake8: noqa: F401, F403
import abc
import argparse
import collections
import csv
import json
import multiprocessing as mp
import numpy as np
import os, sys, time, base64, io
import os.path as osp
import copy as cp
import pickle
import random as rd
import requests
import shutil
import string
import subprocess
import warnings
import pandas as pd
from collections import OrderedDict, defaultdict
from multiprocessing import Pool, current_process
from tqdm import tqdm
from PIL import Image
import uuid
from uuid import uuid4
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

# Function to split a string by a separator and return the number of parts
def splitlen(s, sep='/'):
    return len(s.split(sep))

# Function to check if a string contains Chinese characters
def cn_string(s):
    import re
    if re.search(u'[\u4e00-\u9fff]', s):
        return True
    return False

# Global variable for output file
fout = None
# Function to print a message and optionally write it to a file
def double_log(msg, fout=None):
    print(msg)
    if fout is not None:
        fout.write(str(msg) + '\n')
        fout.flush()

# Function to generate a timestamp string
def timestr(second=False, minute=False):
    s = datetime.now().strftime('%Y%m%d_%H%M%S')[2:]
    if second:
        return s
    elif minute:
        return s[:-2]
    else:
        return s[:-4]

# Function to run a command in the shell and return its output
def run_command(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()
    return subprocess.check_output(cmd)

# Function to dump data to a file in various formats
def dump(data, f, **kwargs):
    def dump_pkl(data, pth, **kwargs):
        pickle.dump(data, open(pth, 'wb'))

    def dump_json(data, pth, **kwargs):
        json.dump(data, open(pth, 'w'), indent=4, ensure_ascii=False)

    def dump_jsonl(data, f, **kwargs):
        lines = [json.dumps(x, ensure_ascii=False) for x in data]
        with open(f, 'w', encoding='utf8') as fout:
            fout.write('\n'.join(lines))

    def dump_xlsx(data, f, **kwargs):
        data.to_excel(f, index=False)

    def dump_csv(data, f, quoting=csv.QUOTE_MINIMAL):
        data.to_csv(f, index=False, encoding='utf-8', quoting=quoting)

    def dump_tsv(data, f, quoting=csv.QUOTE_MINIMAL):
        data.to_csv(f, sep='\t', index=False, encoding='utf-8', quoting=quoting)

    handlers = dict(pkl=dump_pkl, json=dump_json, jsonl=dump_jsonl, xlsx=dump_xlsx, csv=dump_csv, tsv=dump_tsv)
    suffix = f.split('.')[-1]
    return handlers[suffix](data, f, **kwargs)

# Function to load data from a file in various formats
def load(f):
    # load data file
    def load_pkl(pth):
        return pickle.load(open(pth, 'rb'))

    def load_json(pth):
        return json.load(open(pth, 'r', encoding='utf-8'))

    def load_jsonl(f):
        lines = open(f, encoding='utf-8').readlines()
        lines = [x.strip() for x in lines]
        if lines[-1] == '':
            lines = lines[:-1]
        data = [json.loads(x) for x in lines]
        return data

    def load_xlsx(f):
        return pd.read_excel(f)

    def load_csv(f):
        return pd.read_csv(f)

    def load_tsv(f):
        return pd.read_csv(f, sep='\t')

    handlers = dict(pkl=load_pkl, json=load_json, jsonl=load_jsonl, xlsx=load_xlsx, csv=load_csv, tsv=load_tsv)
    suffix = f.split('.')[-1]
    return handlers[suffix](f) 


def load_file_content(df, col):
    """
    This function reads a dataframe and substitutes the paths in df[col] with the contents of the file at the path.
    If df[col] contains multiple paths (like in the 'question' column), it replaces each path with its content.
    For other columns, it simply replaces a single path with the file content.
    """
    for index, row in df.iterrows():
        data = row[col]

        # Check if the data contains multiple paths (specifically for the 'question' column)
        if ';' in data and col == 'question':
            # Split the string into separate paths
            parts = data.split(';')
            contents = []

            for part in parts:
                # Extract the path
                label, path = part.split(': ')
                content = load_content_from_path(path)
                # Combine label with loaded content
                contents.append(f"{label}: {content}")

            # Join the contents back into a single string
            df.at[index, col] = ';'.join(contents)
        else:
            # For other columns, or if there's only a single path
            content = load_content_from_path(data)
            if content:
                df.at[index, col] = content

def load_content_from_path(path):
    """
    Helper function to load content from a given file path.
    Returns the content if the file exists, otherwise returns None.
    """
    try:
        with open(path, 'r') as file:
            return file.read()
    except (FileNotFoundError, OSError):
        # If the path is not valid or reading the file fails, return None
        return None