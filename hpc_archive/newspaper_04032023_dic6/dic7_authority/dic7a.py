# purpose: apply dictionary-based word-counting method on the entire corpus.
# note: we've previously separated the cleaned corpus into 12 chunks,
# each containing 20 million documents

import pandas as pd
from collections import Counter
from datetime import datetime
from gc import collect
from os import walk
import json


i = '7a'


def log(msg):
    print(f'{datetime.now()}; {msg}')


def word_count(text, dic=None):
    dic = dic.copy()
    words = text.split()

    for word in words:
        if word in dic:
            dic[word] += 1

    return dic


if __name__ == '__main__':
    # load config.json
    with open('config.json') as f:
        config = json.load(f)

    # file structure: ocri_j.csv, ...
    # ocr partition i has ~20 million documents
    # each of the ~20 chunks of partition i has 1 million documents
    # we further reduce each chunk to 500,000 documents, this will be j, the sub-chunk index

    all_files = next(walk('/n/henrich_lab/Lab/ocr/'), (None, None, []))[2]  # [] if no file
    curr_partition_files = list(filter(lambda f: f.startswith(f'ocr{i}_'), all_files))

    j = 0

    for f in curr_partition_files:

        try:

            with pd.read_csv(f'/n/henrich_lab/Lab/ocr/{f}', dtype=str, chunksize=500000, on_bad_lines='skip', encoding_errors='ignore', engine='python') as reader:
                for df in reader:
                    try:
                        print('===== a chunk =====')
                        print(f'chunk {j}')
                        # do it by chunk to save memory

                        df.dropna(subset=['text'], inplace=True)
                        df.reset_index(inplace=True, drop=True)  # essential!!!
                        print(f'# documents: {df.shape[0]}')

                        # standard NLP preprocessing (bag-of-words transformation)
                        log('preprocessing starts')
                        t1 = datetime.now()

                        # to lower
                        df['text'] = df['text'].str.lower()
                        # remove punctuation
                        df['text'] = df['text'].str.replace(r'([^\w\s]|_)+', '', regex=True)
                        # tokenization
                        df['text'] = df['text'].str.split()
                        log('tokenization done')
                        # define vocabulary
                        vocab = pd.read_csv(config['dictionary'])['word'].to_list()
                        # filter out words not in dictionary
                        df['text'] = df['text'].apply(lambda x: [w for w in x if w in vocab])
                        log('filter done')
                        # each Counter containing word counts for each row in the DataFrame
                        counts = df['text'].apply(Counter).to_list()
                        log('counter done')
                        # create bag-of-words df from list of dictionaries
                        bow_df = pd.DataFrame(counts).fillna(0).astype(int)

                        # concat from original
                        res_curr_chunk = pd.concat([df[['path_id']], bow_df], axis=1)
                        # res = pd.concat([res, res_curr_chunk], axis=0)
                        res_curr_chunk.to_csv(f'/n/henrich_lab/Lab/{config["name"]}/dic{config["index"]}-{i}-{j}.csv')
                        del res_curr_chunk

                        t2 = datetime.now()
                        log('preprocessing ends')
                        print(f'\ttime elapsed: {t2 - t1}')
                        print('==========')

                        collect()
                        j += 1
                    except Exception as e:
                        print(f'===== exception at sub chunk {j} =====')
                        print(e)
                        print('==========')
                        j += 1

        except Exception as e:
            print(f'?????????? cannot even read chunk {f} ??????????')
            print(e)
            print('????????????????????')
            j += 2
