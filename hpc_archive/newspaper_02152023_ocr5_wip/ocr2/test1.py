import pandas as pd
from editdistance import eval as distance
from datetime import datetime
from multiprocessing import Pool
from gc import collect  # garbage collector


def not_in_set(word):
    return word not in coha_set


def get_dist(word):
    return distance(nonword_error, word)


def correct(nonword_error):
    """
    A helper function at the correction step for one single non-word error.
    """
    # calculate Damerau-Levenshtein (DL) distance between non-word error and each coha word
    pool = Pool(None)
    # res = pool.map(get_dist, df_coha['word'])
    args = [(nonword_error, w) for w in df_coha['word']]
    res = pool.starmap(distance, args)
    df_coha['dist_with_curr_error'] = pd.Series(res, index=df_coha.index)
    # df_coha['dist_with_curr_error'] = df_coha['word'].apply(lambda w: distance(nonword_error, w))

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

    df_candidates = df_coha.loc[df_coha.is_candidate].reset_index(drop=True).copy()

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
    df_coha: specific format
    coha_set: specific format
    """
    df_ocr_text = pd.DataFrame(ocr_text.split(), columns=['word'])

    # detect non-word errors in OCR text:
    # any word in the OCR text of length 3 or higher that cannot be found in the
    # reference dictionary of real words is flagged as a non-word error.
    df_ocr_text['nchar'] = df_ocr_text['word'].str.len()
    df_ocr_text['at_least_3'] = df_ocr_text['nchar'] >= 3
    df_ocr_text['not_in_set'] = df_ocr_text['word'].apply(lambda word: word not in coha_set)
    df_ocr_text['nonword_error'] = df_ocr_text['at_least_3'] & df_ocr_text['not_in_set']
    df_ocr_text.drop(
        ['nchar', 'at_least_3', 'not_in_set'], axis=1, inplace=True)

    # apply correct() to the words that are nonword_errors
    df_ocr_text['corrected'] = df_ocr_text['word']
    df_ocr_text.loc[df_ocr_text['nonword_error'], 'corrected'] = df_ocr_text.loc[df_ocr_text['nonword_error'], 'word'].apply(correct)

    return ' '.join(df_ocr_text['corrected'])


if __name__ == '__main__':
    # COHA reference dictionary
    df_coha = pd.read_csv('data/coha_dict.csv')
    df_coha['word'] = df_coha['word'].astype('string')
    df_coha.dropna(inplace=True)

    coha_list = df_coha['word'].to_list()
    coha_set = set(coha_list)

    # OCR text
    OCR_FILE_PATH = 'data/res0_5k.csv'
    df_all_ocr = pd.read_csv(OCR_FILE_PATH, nrows=100)
    print(f'{datetime.now()} Data read: {OCR_FILE_PATH}')
    print(f'{df_all_ocr.shape[0]} rows')

    # process all
    t1 = datetime.now()

    df_all_ocr['text'] = df_all_ocr['text'].apply(post_ocr_processing)
    df_all_ocr.to_csv('test1.csv', index=False)

    t2 = datetime.now()
    print(f'Time elapsed: {t2 - t1}')
