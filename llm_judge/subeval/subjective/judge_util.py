from subeval.smp import *
from subeval.subjective.prompt.subeval_prompts import build_prompt
from functools import partial
from subeval.utils.mp_util import track_progress_rich
from subeval.chat_api import OpenAIWrapper

# Function to get a unique record index for file naming
def get_record_index(data_base, tgt_name, judge, nopt):
    i = 0
    def valid(i):
        return not osp.exists(f'{data_base}_record{i}_{judge}_{nopt}/{tgt_name}')
    while not valid(i):
        i += 1
    return i

# Function to separate data into two groups based on whether answers match exactly (em-exact match)
def filter_em(data):
    lt = len(data)
    em_inds = []
    nonem_inds = []
    for i in range(lt):
        item = data.iloc[i]
        if item['answer1'].strip() == item['answer2'].strip():
            em_inds.append(i)
        else:
            nonem_inds.append(i)
    em = data.iloc[em_inds]
    nonem = data.iloc[nonem_inds]
    return em, nonem


# Function to make evaluationsusing the given judge
def judge_infer(data, judge='gpt-4-1106-preview', nopt=2, nproc=1, failure_cnt=5):
    # Assigns the filename of the data to a variable and model judge
    data_name = data
    model = partial(OpenAIWrapper, judge, retry=16, timeout=150, verbose=True)()
        

    # Extracts the base name of the data file for later use in naming output directories and files.
    data_base = data_name.split('/')[-1].split('.')[0]
    # Loads the data from the file.
    data = load(data_name)
    
    # Ensures that all mandatory columns are present in the data.
    manda_cols = ['question', 'answer1', 'answer2', 'A', 'B', 'cmp_index']
    for name in manda_cols:
        assert name in data

    # Converts the answers in the data to strings.
    data['answer1'] = [str(x) for x in data['answer1']]
    data['answer2'] = [str(x) for x in data['answer2']]


    # Prepares the target file name for storing the results.
    tgt_name = f'record_{judge}_{nopt}.tsv'
    # Gets a unique index for file naming to avoid overwriting.
    idx = get_record_index(data_base, tgt_name, judge, nopt)
    # Creates the directory for storing results.
    root = f'output/{data_base}_record{idx}_{judge}_{nopt}'
    os.makedirs(root, exist_ok=True)

    # Sets up a temporary file for intermediate results.
    tmp_file = osp.join(root, 'tmp.pkl')

    # Filters the data into exact matches and non-exact matches.
    data_em, data_nonem = filter_em(data)

    # Prints the count of exact matches, which will be skipped in the evaluation.
    print(f'Among {len(data)} comparisons, {len(data_em)} cases are exact match and will be skipped. ')
    # Creates prompts for the GPT model for each non-exact match.
    prompts = [build_prompt(data_nonem.iloc[i], nopt=nopt) for i in range(len(data_nonem))]

    # Maps comparison indices to their respective prompts.
    prompts_map = {x: p for x, p in zip(data_nonem['cmp_index'], prompts)}

    # Initializes a dictionary to store answers.
    ans = {}

    # Support resuming
    # Checks if a temporary file exists with some results and loads them.
    if osp.exists(tmp_file):
        ans = load(tmp_file)
        # Filters out any failed results.
        ans_ok = {x: y for x, y in ans.items() if 'Failed' not in y}

        # Removes failed results from the total count and updates the answers dictionary.
        if len(ans) != len(ans_ok):
            print(f'{len(ans) - len(ans_ok)} results removed during prefetching. ')
            ans = ans_ok

        # Updates the prompts map to exclude any prompts that already have answers.
        prompts_map = {x: y for x, y in prompts_map.items() if x not in ans}

    # If multiple processes are specified, the processing is done in parallel.
    if nproc > 1:
        # Prepares tuples of comparison indices and prompts.
        tups = list(zip(data_nonem['cmp_index'], prompts))
        tups = [x for x in tups if x[0] not in ans]
        keys = [x[0] for x in tups]
        prompts = [x[1] for x in tups]
        # If there are prompts to process, it processes them in parallel.
        if len(prompts):
            results = track_progress_rich(
                model.generate, 
                prompts, 
                keys=keys, 
                save=tmp_file,
                nproc=nproc,
                chunksize=nproc,
                description=f'Processing {data_name} with {judge}...'
            )
            # Stores the results in the answers dictionary.
            for t, r in zip(tups, results):
                ans[t[0]] = r
        # Saves the results to the temporary file.
        dump(ans, tmp_file)
    else:
        # If only one process is specified, it processes the prompts sequentially.
        for cmp_idx, prompt in tqdm(list(zip(data_nonem['cmp_index'], prompts))):
            if cmp_idx in ans:
                continue
            ans[cmp_idx] = model.generate(prompt)
            dump(ans, tmp_file)
        
    # Filters out any failed results after processing.
    ans_ok = {x: y for x, y in ans.items() if model.fail_msg not in y}
    if len(ans) != len(ans_ok):
        print(f'{len(ans) - len(ans_ok)} results failed. Rerun the command if you think that is too much. ')

    # Checks if the number of failed results is acceptable.
    if len(ans) - len(ans_ok) >= failure_cnt:
        print(f'{len(ans) - len(ans_ok)} results failed, which is more than {failure_cnt} records. Will not generate the inference result tsv. ')
        exit(-1)

    # Merges the results back into the data frames for both exact matches and non-exact matches.
    data_nonem[judge] = [ans[cmp_idx] for cmp_idx in data_nonem['cmp_index']]
    data_em[judge] = ['EM'] * len(data_em)
    data_all = pd.concat([data_nonem, data_em])

    # Saves the combined data to a file.
    dump(data_all, f'{root}/{tgt_name}', quoting=csv.QUOTE_ALL)
    return f'{root}/{tgt_name}'

