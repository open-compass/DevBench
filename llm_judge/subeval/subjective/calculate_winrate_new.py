from subeval import *
from subeval.subjective.analyze_util import proc_task, match_answer
from subeval.subjective.util import find_inconsistent

### Analyze ###
'''
Main analyze function to seperate consistent and inconsistent data
and then analyze seperately.

Note: the count-win-rate functions here are NOT the win-rate calculation functions.
The actual new-version win-rate calculation is done after aggregation (See below after aggregate_data).
'''
def analyze(data_file, refm, judge):
    # Preprocesses the data (seperate consistent and inconsistent data).
    cons_data, incons_data = seperate_inconsistent(data_file,judge)

    # Initialize dictionaries for consistent, tie, and total counts
    cnt = defaultdict(lambda: 0)    # win
    tie = defaultdict(lambda: 0)    # tie
    tot = defaultdict(lambda: 0)    # total

    # Process consistent data
    # Processes tasks and sorts them.
    cons_tasks, cons_task_list = proc_task(cons_data['task'])
    cons_data['task'] = cons_task_list
    cons_tasks.sort()
    cons_suptasks = list(set([x.split('-')[0] for x in cons_tasks]))
    cons_suptasks.sort()


    # Calls the analyze function with the prepared data.
    cons_cnt, cons_tie, cons_tot = analyze_cons(cons_data, refm, cons_tasks)
    cnt.update(cons_cnt)
    tie.update(cons_tie)
    tot.update(cons_tot)
    
    
    # Process inconsistent data
    # Processes tasks and sorts them.
    incons_tasks, incons_task_list = proc_task(incons_data['task'])
    incons_data['task'] = incons_task_list
    incons_tasks.sort()
    incons_suptasks = list(set([x.split('-')[0] for x in incons_tasks]))
    incons_suptasks.sort()
    

    # Calls the analyze function with the prepared data.
    incons_cnt, incons_tie, incons_tot = analyze_incons(incons_data, refm, incons_tasks)
    cnt = add_dict(cnt, incons_cnt)
    tie = add_dict(tie, incons_tie)
    tot = add_dict(tot, incons_tot)
    
    return cnt, tie, tot


def add_dict(a, b):
    return {key: a.get(key, 0) + b.get(key, 0) for key in set(a) | set(b)}


# Inspired by preprocess from analyze_util.py to fit new needs.
def seperate_inconsistent(data_file, judge):
    data = load(data_file)
    
    # Filters out data where the answers are an exact match ('EM').
    nonem = [x != 'EM' for x in data[judge]]
    data = data[nonem]
    
    # Extracts answers from the data and checks for successful extraction.
    data['extracted'] = [match_answer(ans) for ans in data[judge]]
    succeed = [not pd.isna(x) for x in data['extracted']]
    data = data[succeed]
    
    cons_data, incons_data = find_inconsistent(data, 'ABCD')
    return cons_data, incons_data


def analyze_cons(data, refm, tasks):
    # Collects all unique models from columns 'A' and 'B' in the data.
    models = set(list(data['A']) + list(data['B']))
    models = list(models)
    assert refm in models  # Ensures the reference model is in the list of models.

    # Initializes tables for different statistics.
    cnt = defaultdict(lambda: 0)    # win
    tie = defaultdict(lambda: 0)    # tie
    tot = defaultdict(lambda: 0)    # total

    for task in tasks:
        sub_cnt, sub_tie, sub_tot = count_win_rate_cons(data, task=task)
        cnt.update(sub_cnt)
        tie.update(sub_tie)
        tot.update(sub_tot)
    
    return cnt, tie, tot

def analyze_incons(data, refm, tasks):
    # Collects all unique models from columns 'A' and 'B' in the data.
    models = set(list(data['A']) + list(data['B']))
    models = list(models)
    assert refm in models  # Ensures the reference model is in the list of models.

    # Initializes tables for different statistics.
    cnt = defaultdict(lambda: 0)    # win
    tie = defaultdict(lambda: 0)    # tie
    tot = defaultdict(lambda: 0)    # total

    for task in tasks:
        sub_cnt, sub_tie, sub_tot = count_win_rate_incons(data, task=task)
        cnt.update(sub_cnt)
        tie.update(sub_tie)
        tot.update(sub_tot)
    
    return cnt, tie, tot

def count_win_rate_cons(data_copy, lang=None, task=None):
    # Optional fields: 'task'
    # Mandatory fields:  'A', 'B', 'extracted'
    # Choices of extracted: A, B, C, D
    data = cp.deepcopy(data_copy)
    if task is not None and 'task' in data:
        flag = [(task in x) for x in data['task']]
        data = data[flag]
    
    cnt = defaultdict(lambda: 0)    # win
    tie = defaultdict(lambda: 0)    # tie
    tot = defaultdict(lambda: 0)    # total
    
    for i in range(len(data)):
        v = data.iloc[i]
        o = v['extracted']
        m1, m2 = v['A'], v['B']
        cmp_idx = v['cmp_index']
        repo_prefix = cmp_idx.split(';')[0]
        
        if o == 'A':
            cnt[f"{repo_prefix};{m1};{m2}"] += 1
        if o == 'B':
            cnt[f"{repo_prefix};{m2};{m1}"] += 1
        if o == 'C':
            tie[f"{repo_prefix};{m1};{m2}"] += 1
            tie[f"{repo_prefix};{m2};{m1}"] += 1

        tot[f"{repo_prefix};{m1};{m2}"] += 1
        tot[f"{repo_prefix};{m2};{m1}"] += 1

    return cnt, tie, tot    # win, tie, total 

def count_win_rate_incons(data_copy, lang=None, task=None):
    # Optional fields: 'task'
    # Mandatory fields:  'A', 'B', 'extracted'
    # Choices of extracted: A, B, C, D
    data = cp.deepcopy(data_copy)
    if task is not None and 'task' in data:
        flag = [(task in x) for x in data['task']]
        data = data[flag]
    
    cnt = defaultdict(lambda: 0)    # win
    tie = defaultdict(lambda: 0)    # tie
    tot = defaultdict(lambda: 0)    # total
    
    for i in range(len(data)):
        v = data.iloc[i]
        m1, m2 = v['A'], v['B']
        cmp_idx = v['cmp_index']
        repo_prefix = cmp_idx.split(';')[0]
        tie[f"{repo_prefix};{m1};{m2}"] += 1   # inconsistent -> tie
        tie[f"{repo_prefix};{m2};{m1}"] += 1   # inconsistent -> tie
    
    tot = cp.deepcopy(tie)
    
    return cnt, tie, tot    # win, tie, total 



### Aggregate and compute win rate ###
'''
Analyze acts as a preprocessing of the data for new version of win rate computation.
The new version win-rate (inconsistent as tie) is calculated as below
'''
def aggregate_data(original_dict):
    aggregated_dict = {}
    for key, value in original_dict.items():
        prefix, model_part = key.split(';', 1)
        *repo_and_design_parts, metric = prefix.rsplit('-', 1) # Split at the last hyphen to get the metric

        # Create a new key for the aggregated dictionary
        new_key = f"{metric};{model_part}"

        # Sum the values for the new key
        if new_key in aggregated_dict:
            aggregated_dict[new_key] += value
        else:
            aggregated_dict[new_key] = value

    return aggregated_dict

def compute_win_rate(merged_cnt, merged_tie, merged_tot, refm):
    # win rate = (cnt + tie / 2) / (tot)
    win_rates = {}
    for key in merged_tot.keys():
        if refm in key:  # Only calculate for the reference model
            cnt = merged_cnt.get(key, 0)
            tie = merged_tie.get(key, 0)
            tot = merged_tot[key]
            win_rates[key] = ((cnt + 0.5 * tie) / tot) if tot > 0 else 0
    return win_rates
    
def compute_win_rate_wo_tie(merged_cnt, merged_tie, merged_tot, refm):
    # win rate = cnt / (tot - tie)
    win_rates = {}
    for key in merged_tot.keys():
        if refm in key:  # Only calculate for the reference model
            cnt = merged_cnt.get(key, 0)
            tie = merged_tie.get(key, 0)
            tot = merged_tot[key]
            win_rates[key] = (cnt / (tot - tie)) if (tot - tie) > 0 else 0
    return win_rates



### Only need to call this to calculate the new-version win-rate ###
def calculate_winrate_new_call(infer_result_file, refm, judge, save_to_directory=None):
    '''
    Purpose:
        1. calculate the new-version win-rate of an SubEval experiment (inconsistent as tie)
        2. Optionally save the results to a directory
    Params:
        1. infer_result_file: The result tsv file path obtained by running SubEval
        2. refm: reference model (need to ensure it corresponds to the infer_result_file)
        3. judge: judge model (need to ensure it corresponds to the infer_result_file)
        4. save_to_directory: If need to save to the winrate csv, specifiy the directory
    '''
    
    # Construct data for win rate calculation
    cnt, tie, tot = analyze(infer_result_file, refm, judge)

    merged_cnt = aggregate_data(cnt)
    merged_tie = aggregate_data(tie)
    merged_tot = aggregate_data(tot)

    # Calculate win rate
    win_rate_with_tie = compute_win_rate(merged_cnt, merged_tie, merged_tot, refm)
    win_rate_wo_tie = compute_win_rate_wo_tie(merged_cnt, merged_tie, merged_tot, refm)

    if save_to_directory:
        # Convert dictionaries to pandas data frames
        df_with_tie = pd.DataFrame(list(win_rate_with_tie.items()), columns=['Metric;Model', 'WinRateWithTie'])
        df_wo_tie = pd.DataFrame(list(win_rate_wo_tie.items()), columns=['Metric;Model', 'WinRateWithoutTie'])
        
        # Construct the CSV file paths
        with_tie_file_path = os.path.join(save_to_directory, f'win_rate_with_tie.csv')
        wo_tie_file_path = os.path.join(save_to_directory, f'win_rate_without_tie.csv')

        # Save the data frames to CSV
        df_with_tie.to_csv(with_tie_file_path, index=False)
        df_wo_tie.to_csv(wo_tie_file_path, index=False)

        print(f"Win rate with tie saved to {with_tie_file_path}")
        print(f"Win rate without tie saved to {wo_tie_file_path}")
    
    return win_rate_with_tie, win_rate_wo_tie

if __name__=="__main__":
    # Parameters: Adjust to your desiried ones
    refm = "gpt-3.5-turbo-1106"
    judge = "gpt-3.5-turbo-1106"
    infer_result_file = "output/DevBench_projects_example_infer_input_2680_record0_gpt-3.5-turbo-1106_2/record_gpt-3.5-turbo-1106_2.tsv"
    save_to_directory = "output/DevBench_projects_example_infer_input_2680_record0_gpt-3.5-turbo-1106_2"
    
    calculate_winrate_new_call(infer_result_file, refm, judge, save_to_directory)


