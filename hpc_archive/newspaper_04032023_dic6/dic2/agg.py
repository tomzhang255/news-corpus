# summarize dic2.csv
# want 2 columns: average percentage of raw text words that are dictionary words, aggregated by year

import pandas as pd
import numpy as np
from gc import collect  # garbage collector


if __name__ == '__main__':
    df = pd.read_csv('/n/henrich_lab/Lab/clean/dic2.csv')

    """
    This is what it looks like right now, want to basically shift everything up, so there's no NA
        a    b    c
    0  1.0  NaN  NaN
    1  2.0  NaN  NaN
    2  NaN  3.0  5.0
    3  NaN  4.0  6.0
    """
    # fix NA
    print(f'dic2.csv shape: {df.shape}; #na: {df.isna().sum()}')

    problem_row_indices = df.loc[df['encourage'].isna()].index
    fill_content = df.loc[df['path_id'].isna()].drop(['path_id', 'year', 'text'], axis=1)
    fill_content.index = problem_row_indices
    df.dropna(subset=['path_id'], inplace=True)
    df.fillna(fill_content, inplace=True)
    df.to_csv('/n/henrich_lab/Lab/clean/dic2_fixed.csv', index=False)

    print(f'fixed dic2.csv shape: {df.shape}; #na: {df.isna().sum()}')

    # calc
    df['occurrence_sum'] = df.iloc[:, 3:].sum(axis=1)  # sum of dictionary word occurrences
    df['num_words'] = df['text'].str.split().str.len()  # number of words in raw text

    df.drop(df.columns[2:156], axis=1, inplace=True)  # drop dictionary word columns
    df.drop('path_id', axis=1, inplace=True)
    collect()

    df['percent_dic_occurrence'] = df['occurrence_sum'].div(df['num_words'])
    df.replace([np.inf, -np.inf], 0, inplace=True)  # zero divide by zero results in inf

    df.drop(['occurrence_sum', 'num_words'], axis=1, inplace=True)
    collect()

    res = df.groupby('year')[['percent_dic_occurrence']].mean()
    res.reset_index(inplace=True)
    
    res.to_csv('/n/henrich_lab/Lab/clean/dic2_agg.csv', index=False)
    print(res.head())
    print(res.tail())
