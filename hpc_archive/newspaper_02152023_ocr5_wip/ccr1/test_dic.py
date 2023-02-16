# purpose: test dictionary-based word-counting method on a stratified sample;

import pandas as pd
from collections import Counter
from datetime import datetime


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
    df = pd.read_csv('/n/henrich_lab/Lab/clean/strat_sample_200.csv')

    # original stratified sample is with replacement - drop duplicates first
    df.drop_duplicates(subset=['path_id'], inplace=True)
    # df = df.sample(n=1000, random_state=42).copy()
    df.dropna(subset=['text'], inplace=True)
    print(f'# documents: {df.shape[0]}')

    df_original = df.copy()

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
    vocab = pd.read_csv('data/dic.csv')['word'].to_list()
    # filter out words not in dictionary
    df['text'] = df['text'].apply(lambda x: [w for w in x if w in vocab])
    log('filter done')
    # each Counter containing word counts for each row in the DataFrame
    counts = df['text'].apply(Counter).to_list()
    log('counter done')
    # create bag-of-words df from list of dictionaries
    bow_df = pd.DataFrame(counts).fillna(0).astype(int)

    # concat from original
    res = pd.concat([df_original, bow_df], axis=1)

    t2 = datetime.now()
    log('preprocessing ends')
    print(f'\ttime elapsed: {t2 - t1}')

    # save result
    log('saving to csv...')
    t1 = datetime.now()

    res.to_csv('/n/henrich_lab/Lab/clean/dic1.csv', index=False)

    t2 = datetime.now()
    log('saved to csv')
    print(f'\ttime elapsed: {t2 - t1}')
