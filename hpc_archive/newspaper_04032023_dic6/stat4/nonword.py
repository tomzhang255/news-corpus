# counts number of non-word errors from the stratified sample

import pandas as pd
import numpy as np
from datetime import datetime


def log(msg):
    print(f'{datetime.now()}; {msg}')


def count_nonword_error(ocr_text, df_coha=None, coha_set=None):
    """
    Processes one single piece of OCR text.
    ---
    ocr_text: string
    df_coha: specific format
    coha_set: specific format
    ---
    returns: all word count, non-word error count
    """
    if len(ocr_text) == 0:
        return 0, 0

    df_ocr_text = pd.DataFrame(ocr_text.split(), columns=['word'])

    # detect non-word errors in OCR text:
    # any word in the OCR text of length 3 or higher that cannot be found in the
    # reference dictionary of real words is flagged as a non-word error.
    df_ocr_text['nchar'] = df_ocr_text['word'].str.len()
    df_ocr_text['at_least_3'] = df_ocr_text['nchar'] >= 3
    df_ocr_text['not_in_set'] = df_ocr_text['word'].apply(
        lambda word: word not in coha_set)
    df_ocr_text['nonword_error'] = df_ocr_text['at_least_3'] & df_ocr_text['not_in_set']
    df_ocr_text.drop(
        ['nchar', 'at_least_3', 'not_in_set'], axis=1, inplace=True)

    return df_ocr_text.shape[0], df_ocr_text['nonword_error'].sum()


if __name__ == '__main__':
    # read
    log('start')
    df = pd.read_csv('/n/henrich_lab/Lab/clean/strat_sample_200.csv')
    log('loaded sample')

    # sampled with replacement - check year distribution
    df.drop_duplicates(subset=['path_id'], inplace=True)
    df['text'].fillna('', inplace=True)
    # freq = df['year'].value_counts()
    # freq.to_csv('bootstrap_freq.csv', index=True)

    # COHA reference dictionary
    df_coha = pd.read_csv('coha_dict.csv')
    df_coha['word'] = df_coha['word'].astype('string')
    df_coha.dropna(inplace=True)

    coha_list = df_coha['word'].to_list()
    coha_set = set(coha_list)

    # for each row, count non-word errors
    log('counting non-word errors')
    tmp = df['text'].apply(count_nonword_error, df_coha=df_coha, coha_set=coha_set)
    word_counts, error_counts = zip(*tmp)
    df['word_counts'] = word_counts
    df['error_counts'] = error_counts

    # save result
    log('saving result')
    df.drop('text', axis=1, inplace=True)
    df.to_csv('/n/henrich_lab/Lab/clean/stat4.csv', index=False)
    log('done')
