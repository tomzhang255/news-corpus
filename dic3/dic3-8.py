# purpose: apply dictionary-based word-counting method on the entire corpus.
# note: we've previously separated the cleaned corpus into 12 chunks,
# each containing 20 million documents

import pandas as pd
from collections import Counter
from datetime import datetime
from gc import collect


i = 8


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
    # res = None

    j = 0
    with pd.read_csv(f'/n/henrich_lab/Lab/clean/res{i}.csv', dtype=str, chunksize=500000, encoding_errors='ignore', lineterminator='\n') as reader:
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
                vocab = pd.read_csv('data/norm_tightness.csv')['word'].to_list()
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
                res_curr_chunk.to_csv(f'/n/henrich_lab/Lab/dic/dic3-{i}-{j}.csv')
                del res_curr_chunk

                t2 = datetime.now()
                log('preprocessing ends')
                print(f'\ttime elapsed: {t2 - t1}')
                print('==========')

                collect()
                j += 1
            except Exception as e:
                print(f'===== exception at chunk {j} =====')
                print(e)
                print('==========')
                j += 1

    # res.fillna(0, inplace=True)

    # save result
    log('saving to csv...')
    t1 = datetime.now()

    # res.to_csv(f'/n/henrich_lab/Lab/dic/dic3-{i}.csv', index=False)

    t2 = datetime.now()
    log('saved to csv')
    print(f'\ttime elapsed: {t2 - t1}')
