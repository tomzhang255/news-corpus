import pandas as pd
from editdistance import eval as distance
from datetime import datetime
from multiprocessing import Pool
from gc import collect  # garbage collector


def not_in_set(word):
    return word not in coha_set


def correct(nonword_error):
    """
    A helper function at the correction step for one single non-word error.
    """
    # calculate Damerau-Levenshtein (DL) distance between non-word error and each coha word
    df_coha['dist_with_curr_error'] = df_coha['word'].apply(lambda w: distance(nonword_error, w))

    # set distance thresold
    err_len = len(nonword_error)
    if err_len >= 3 and err_len <= 5:
        thresold = 1
    elif err_len >= 6 and err_len <= 9:
        thresold = 2
    else:
        thresold = 3

    # get correction candidates
    df_coha['is_candidate'] = df_coha['dist_with_curr_error'] <= thresold

    if df_coha['is_candidate'].sum() == 0:
        # uncorrectable, not processed to a correction, return original error word
        return nonword_error

    df_candidates = df_coha.loc[df_coha.is_candidate].reset_index(
        drop=True).copy()

    # correction step - find best candidate based on distance, then frequency
    for dist in range(1, thresold + 1):
        sub = df_candidates.loc[df_candidates['dist_with_curr_error'] == dist]
        if sub.shape[0] > 0:
            best = sub.nlargest(1, 'freq')
            best_correction = best.iloc[0, 0]
            return best_correction


def post_ocr_processing(ocr_text):
    """
    Processes one single piece of OCR text.
    ---
    ocr_text: string
    """

    df_ocr_text = pd.DataFrame(ocr_text.split(), columns=['word'])

    # detect non-word errors in OCR text:
    # any word in the OCR text of length 3 or higher that cannot be found in the
    # reference dictionary of real words is flagged as a non-word error.
    df_ocr_text['nchar'] = df_ocr_text['word'].str.len()
    df_ocr_text['at_least_3'] = df_ocr_text['nchar'] >= 3

    # df_ocr_text['not_in_set'] = df_ocr_text['word'].apply(lambda word: word not in coha_set)

    pool = Pool(None)  # None <- os.cpu_count() <- use all
    res = pool.map(not_in_set, df_ocr_text['word'])
    df_ocr_text['not_in_set'] = pd.Series(res)

    df_ocr_text['nonword_error'] = df_ocr_text['at_least_3'] & df_ocr_text['not_in_set']
    df_ocr_text.drop(['nchar', 'at_least_3', 'not_in_set'], axis=1, inplace=True)

    # apply correct() to the words that are nonword_errors
    df_ocr_text['corrected'] = df_ocr_text['word']

    # df_ocr_text.loc[df_ocr_text['nonword_error'], 'corrected'] = df_ocr_text.loc[df_ocr_text['nonword_error'], 'word'].apply(correct)

    pool = Pool(None)  # None <- os.cpu_count() <- use all
    error_series = df_ocr_text.loc[df_ocr_text['nonword_error'], 'word']
    res = pool.map(correct, error_series)
    df_ocr_text.loc[df_ocr_text['nonword_error'], 'corrected'] = pd.Series(res, index=error_series.index)
    pool.close()
    pool.join()
    collect()

    # return df_ocr_text
    return ' '.join(df_ocr_text['corrected'])


if __name__ == '__main__':
    # OCR text
    df_all_ocr = pd.read_csv('data/res0_5k.csv')

    # COHA reference dictionary
    df_coha = pd.read_csv('data/coha_dict.csv')
    df_coha['word'] = df_coha['word'].astype('string')
    df_coha.dropna(inplace=True)

    coha_list = df_coha['word'].to_list()
    coha_set = set(coha_list)

    # process a subset
    t1 = datetime.now()
    sub = df_all_ocr
    print(sub.shape[0])
    sub['text'] = sub['text'].apply(post_ocr_processing)
    sub.to_csv('test.csv', index=False)
    t2 = datetime.now()
    print(f'Time elapsed: {t2 - t1}')
