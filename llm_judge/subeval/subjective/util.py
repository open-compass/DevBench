import math
from collections import defaultdict
from tqdm import tqdm 
import random as rd
import numpy as np
import multiprocessing as mp
import pandas as pd
import copy as cp
from subeval.smp import load, dump

# ALL FUNCTIONS IN THIS FILE TAKE ENTRY-LEVEL RESULT DICT AS INPUTS !!!

### Calculate the win rate between models based on the result df ###
def calc_win_rate(data_copy, models, lang=None, task=None):
    # Optional fields: 'lang', 'task'
    # Mandatory fields:  'A', 'B', 'extracted'
    # Choices of extracted: A, B, C, D
    data = cp.deepcopy(data_copy)
    if lang is not None and 'lang' in data:
        data = data[data['lang'] == lang]
    if task is not None and 'task' in data:
        flag = [(task in x) for x in data['task']]
        data = data[flag]
    
    win = defaultdict(lambda: 0)
    both = defaultdict(lambda: 0)
    neither = defaultdict(lambda: 0)
    lose = defaultdict(lambda: 0)
    
    for i in range(len(data)):
        v = data.iloc[i]
        o = v['extracted']
        key = v['A'] + ';' + v['B']
        
        if o == 'A':
            win[key] += 1
        if o == 'B':
            lose[key] += 1
        if o == 'C':
            both[key] += 1
        if o == 'D':
            neither[key] += 1
            
    nmodel = len(models)
    cnt = pd.DataFrame({k: [0] * nmodel for k in models}, index=models, dtype=np.float32)
    wff = pd.DataFrame({k: [0] * nmodel for k in models}, index=models, dtype=np.float32)
    lff = pd.DataFrame({k: [0] * nmodel for k in models}, index=models, dtype=np.float32)
    tot = pd.DataFrame({k: [0] * nmodel for k in models}, index=models, dtype=np.float32)

    all_keys = list(win) + list(both) + list(neither) + list(lose)   
    all_keys = list(set(all_keys))
    
    for k in all_keys:
        m1, m2 = k.split(';')
        # Win count
        cnt.at[m1, m2] += win[k]
        cnt.at[m2, m1] += lose[k]
        # Both good count
        wff.at[m1, m2] += both[k]
        wff.at[m2, m1] += both[k]
        # Neither good count
        lff.at[m1, m2] += neither[k]
        lff.at[m2, m1] += neither[k]
        # Total count
        tot.at[m1, m2] += both[k] + neither[k] + win[k] + lose[k]
        tot.at[m2, m1] += both[k] + neither[k] + win[k] + lose[k]

    for m1 in models:
        for m2 in models:
            if tot.at[m1, m2]:
                cnt.at[m1, m2] /= tot.at[m1, m2]
                wff.at[m1, m2] /= tot.at[m1, m2]
                lff.at[m1, m2] /= tot.at[m1, m2]
    return cnt, wff, lff

### Split the DataFrame `data` into consistent and inconsistent parts ###
def find_inconsistent(data, vals=['A', 'B', 'C', 'D']):
    # Checks for mandatory fields and sets up a prediction map.
    assert 'extracted' in data
    cons, incons = [], []
    pred_map = {x: y for x, y in zip(data['cmp_index'], data['extracted'])}

    # Loops through the data to find inconsistencies.
    for k in data['cmp_index']:
        parts = k.split(';')
        kct = ';'.join([parts[0], parts[2], parts[1]])  # Reverses the order for comparison (swap answer 1 and answer 2).
        if kct not in pred_map:
            cons.append(k)
            continue
        cons_tups = [(vals[0], vals[1]), (vals[1], vals[0]), (vals[2], vals[2]), (vals[3], vals[3])]
        flag = True
        for tup in cons_tups:
            if pred_map[k] == tup[0] and pred_map[kct] == tup[1]:
                flag = False
                cons.append(k)
                break
        if flag:
            incons.append(k)
    cons, incons = data[data['cmp_index'].isin(cons)], data[data['cmp_index'].isin(incons)]
    return cons, incons


### extract qualitative examples for a specific pair of models ### 
def extract_vispair(data, vals='ABCD', vispair=None):
    # Mandatory fields: 'A', 'B', 'extracted'
    # Choices of extracted: 4 items in vals
    assert vispair is not None
    ma, mb = vispair
    indices_map = defaultdict(list)
    lt = len(data)
    for i in range(lt):
        item = data.iloc[i]

        if item['A'] == ma and item['B'] == mb and item['extracted'] == vals[0]:
            indices_map[f'{ma}_win_{mb}'].append(i)

        if item['A'] == mb and item['B'] == ma and item['extracted'] == vals[1]:
            indices_map[f'{ma}_win_{mb}'].append(i)

        if item['A'] == ma and item['B'] == mb and item['extracted'] == vals[1]:
            indices_map[f'{ma}_lose_{mb}'].append(i)

        if item['A'] == mb and item['B'] == ma and item['extracted'] == vals[0]:
            indices_map[f'{ma}_lose_{mb}'].append(i)

        if set([item['A'], item['B']]) == set([ma, mb]) and item['extracted'] == vals[2]:
            indices_map[f'{ma}_both_{mb}'].append(i)

        if set([item['A'], item['B']]) == set([ma, mb]) and item['extracted'] == vals[3]:
            indices_map[f'{ma}_neither_{mb}'].append(i)
    
    for k in indices_map:
        data_sub = data.iloc[indices_map[k]]
        dump(data_sub, f'{k}.xlsx')

### obtain answer length statistics ###
def length_statistics(data):
    keys = data.keys()
    keys = [k for k in keys if k.startswith('ans-' )]
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')
    length_map = defaultdict(list)
    for k in keys:
        model = k[4:]
        answers = data[k]
        for ans in answers:
            length_map[model].append(len(enc.encode(str(ans))))
    res = defaultdict(list)
    for k in length_map:
        res['model'].append(k)
        res['mean'].append(np.mean(length_map[k]))
        res['std'].append(np.std(length_map[k]))
    return pd.DataFrame(res)

def length_statistics_inferin(data):
    lt = len(data)
    length_map = defaultdict(list)
    import tiktoken
    enc = tiktoken.get_encoding('cl100k_base')
    for i in range(lt):
        item = data.iloc[i]
        length_map[item['A']].append(len(enc.encode(str(item['answer1']))))
        length_map[item['B']].append(len(enc.encode(str(item['answer2']))))
    res = defaultdict(list)
    for k in length_map:
        res['model'].append(k)
        res['mean'].append(np.mean(length_map[k]))
        res['std'].append(np.std(length_map[k]))
    return pd.DataFrame(res)

### Get the shape (h, w) of a concatenated figure of lt sub-figures ###
def get_shape(lt):
    h = int(math.sqrt(lt))
    w = lt // h
    if h * w < lt:
        w += 1
    return h, w