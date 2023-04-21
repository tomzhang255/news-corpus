# summarize dic2.csv
# want columns: page id, # hits on page, # words on page

import pandas as pd
from gc import collect  # garbage collector
from datetime import datetime


if __name__ == '__main__':
    id_list = None
    year_list = None
    hits_list = None
    words_list = None

    with pd.read_csv('/n/henrich_lab/Lab/clean/dic2.csv', chunksize=100000) as reader:
        for chunk in reader:
            id_curr_chunk = chunk['path_id']
            id_list = pd.concat([id_list, id_curr_chunk])
            year_curr_chunk = chunk['year']
            year_list = pd.concat([year_list, year_curr_chunk])

            hits_curr_chunk = chunk.iloc[:, 3:].sum(axis=1)  # sum of dictionary word occurrences
            hits_list = pd.concat([hits_list, hits_curr_chunk])
            words_curr_chunk = chunk['text'].str.split().str.len()  # number of words in raw text
            words_list = pd.concat([words_list, words_curr_chunk])

            print(f'{datetime.now()}; curr chunk done')

    df = pd.DataFrame({'path_id': id_list, 'year': year_list,
                        'num_hits': hits_list, 'num_words': words_list})

    df.to_csv('/n/henrich_lab/Lab/clean/dic2_sum.csv', index=False)
    print(df.head())
    print(df.tail())

    """
    df = pd.read_csv('/n/henrich_lab/Lab/clean/dic2.csv')
    print(f'dic2.csv shape: {df.shape}; #na: {df.isna().sum()}')

    # calc
    df['num_hits'] = df.iloc[:, 3:].sum(axis=1)  # sum of dictionary word occurrences
    df['num_words'] = df['text'].str.split().str.len()  # number of words in raw text

    df.drop(df.columns[2:156], axis=1, inplace=True)  # drop text + dictionary word columns
    collect()

    df.to_csv('/n/henrich_lab/Lab/clean/dic2_sum.csv', index=False)
    print(df.head())
    print(df.tail())
    """
