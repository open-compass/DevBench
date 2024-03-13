from subeval import *
from subeval.subjective.util import calc_win_rate, find_inconsistent, length_statistics_inferin
import re
import os

FAIL_MSG = 'Failed to obtain answer via API.'
FONT_FILE = os.environ.get('FONT_FILE', None)

# Function to extract the chosen answer from a string using regular expressions.
def match_answer(s):
    if result := re.findall('(?:选择：|Choice: )([ABCD])', s): 
        return result[0]
    else:
        return None

# Function to process and categorize tasks from the dataset.
def proc_task(tasks):
    task_lists = [task_str.split(', ') for task_str in tasks]
    task_all = []
    for lst in task_lists:
        task_all.extend(lst)
    task_set = set(task_all)
    task_set = list(task_set)
    return task_set, [', '.join(lst) for lst in task_lists]

def preprocess(data_file, col_name, failure_cnt, fout):
    '''
    Purpose:
        1. Calculate and log length statistics
        2. Check and log the number of failures
        3. Filter out exact match answers
        4. Extract answers from data and check for successful extraction
        5. Find and log inconsistencies
    Params:
        col_name: judge name in the data_file
        failure_cnt: maximum time for failures; otherwise exit
        fout: file output path
    '''
    data_root = osp.dirname(data_file)  # Gets the directory of the data file.
    data = load(data_file)  # Loads the data from the file.

    # Logs and calculates the statistics related to the length of answers.
    double_log('Reponse length', fout)
    stats = length_statistics_inferin(data)
    double_log(tabulate(stats, headers='keys', tablefmt='pretty'), fout)
    dump(stats, f'{data_root}/length_stats.csv')

    # Checks for and logs the number of failures based on a specific message.
    failed = [FAIL_MSG in x for x in data[col_name]]
    double_log(f'Total comparisons: {len(data)}. Failed to response: {sum(failed)}', fout)
    if sum(failed) >= failure_cnt:
        double_log(f'Failed more than {failure_cnt} times. The analysis process exits.')
        exit(-1)  # Exits if failures exceed a threshold.

    # Filters out data where the answers are an exact match ('EM').
    nonem = [x != 'EM' for x in data[col_name]]
    double_log(f'Total comparisons: {len(data)}. Non exact matches:  {sum(nonem)}', fout)
    data = data[nonem]

    # Extracts answers from the data and checks for successful extraction.
    data['extracted'] = [match_answer(ans) for ans in data[col_name]]
    succeed = [not pd.isna(x) for x in data['extracted']]
    succeed_rate = np.mean(succeed)
    double_log(f'Extracted {sum(succeed)} answers from the responses (extraction success rate {succeed_rate * 100:.2f}%)', fout)
    data = data[succeed]


    # data.colums now should becomes ['cmp_index', 'question', 'answer1', 'answer2', 'A', 'B', 'reference_answer', 'evaluating_guidance', 'task', 'gpt-3.5-turbo-1106', 'extracted']

    # Finds and logs inconsistencies in the data.
    cons, incons = find_inconsistent(data, 'ABCD')
    if len(cons) != len(data):
        double_log(f'{len(cons)} out of {len(data)} answers are consistent. (A vs. B <-> B vs. A) The consistent rate is {len(cons) / len(data) * 100:.2f}%', fout)
        dump(cons, f'{data_root}/consistent_cmp.tsv', quoting=csv.QUOTE_ALL)
        dump(incons, f'{data_root}/inconsistent_cmp.tsv', quoting=csv.QUOTE_ALL)
    return cons, incons


# Function to conduct statistical analysis
def analyze(data, refm, langs, tasks, fout, data_root):
    # Collects all unique models from columns 'A' and 'B' in the data.
    models = set(list(data['A']) + list(data['B']))
    models = list(models)
    assert refm in models  # Ensures the reference model is in the list of models.

    # Initializes tables for different statistics.
    wr_table = defaultdict(list)  # Win rate table.
    wd2_table = defaultdict(list) # Win + Draw/2 rate table.
    wb_table = defaultdict(list)  # Win + Both good rate table.

    # Iterates through each model, excluding the reference model.
    for m in models:
        if m == refm:
            continue
        for t in [wr_table, wd2_table, wb_table]:
            t['model'].append(m)
        # Calculates and logs statistics for each language.
        for lang in langs:
            wr, wff, lff = calc_win_rate(data, models, lang=lang)
            dr = wff + lff  # Draw rate.

            lang_name = lang.upper() if lang is not None else 'Overall-lang'
            # Appends calculated rates to the tables.

            wr_table[lang_name].append(wr.at[m, refm])
            wd2_table[lang_name].append(wr.at[m, refm] + dr.at[m, refm] / 2.)
            wb_table[lang_name].append(wr.at[m, refm] + wff.at[m, refm])
        
        # Does the same calculation for taskbilities.
        for task in tasks:
            wr, wff, lff = calc_win_rate(data, models, task=task)
            dr = wff + lff
            wr_table[task].append(wr.at[m, refm])
            wd2_table[task].append(wr.at[m, refm] + dr.at[m, refm] / 2.)
            wb_table[task].append(wr.at[m, refm] + wff.at[m, refm])

    # Converts tables to DataFrames, sorts, and logs them.
    wd2_table = pd.DataFrame(wd2_table)
    wd2_table = wd2_table.sort_values('Overall-lang').iloc[::-1].round(4)
    double_log(f'(Win + Draw / 2) w. {refm}: ', fout)
    double_log(tabulate(wd2_table, headers='keys', tablefmt='pretty'), fout)
    dump(wd2_table, f'{data_root}/win+halfdraw.xlsx')

    wb_table = pd.DataFrame(wb_table)
    wb_table = wb_table.sort_values('Overall-lang').iloc[::-1].round(4)
    double_log(f'(Win + Both Good) w. {refm}: ', fout)
    double_log(tabulate(wb_table, headers='keys', tablefmt='pretty'), fout)
    dump(wb_table, f'{data_root}/win+bothgood.xlsx')

# Main statistical analysis logic
def analyze_pipe(data_file, refm=None, col_name='gpt-4-1106-preview', failure_cnt=5):
    # Opens a log file for writing.
    log_file = osp.join(osp.dirname(data_file), 'log.txt')
    fout = open(log_file, 'w')
    # Preprocesses the data.
    data, _ = preprocess(data_file, col_name, failure_cnt, fout)
    data_root = osp.dirname(data_file)  # Gets the root directory of the data file.

    # Processes tasks and sorts them.
    tasks, task_list = proc_task(data['task'])
    data['task'] = task_list
    tasks.sort()
    suptasks = list(set([x.split('-')[0] for x in tasks]))
    suptasks.sort()

    # Extracts and sorts languages.
    data['lang'] = 'en'
    langs = [None, 'en']

    # Calls the analyze function with the prepared data.
    analyze(data, refm, langs, suptasks + tasks, fout, data_root)
    fout.close()  # Closes the log file.
