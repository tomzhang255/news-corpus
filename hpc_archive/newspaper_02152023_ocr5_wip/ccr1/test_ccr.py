# purpose:          test CCR on a stratified sample;
# implementation:   takes about 2 seconds to apply CCR to one document;
#                   median number of chars for a document is about 7000;
#                   median word count for any document is about 3000;
#                   max word count supported on input text for most models is 512;
#                   we're splitting each piece of input text into 6 chunks;
# transformer used: multi-qa-MiniLM-L6-cos-v1;
#                   it's the fastest for sentence embeddings
#                   and supports a max sequence length of 512 (words)
# info on models:   https://www.sbert.net/docs/pretrained_models.html#sentence-embedding-models/

import pandas as pd
from datetime import datetime
t1 = datetime.now()
from sentence_transformers import SentenceTransformer, util
t2 = datetime.now()
print('====================')
print(f'Took {(t2 - t1).total_seconds()} seconds to load sentence_transformers')
import warnings
warnings.filterwarnings("ignore")


def log(msg):
    print(f'{datetime.now()}; {msg}')


def encode_column(model, df, col_name):
    df["embedding"] = list(model.encode(df[col_name]))
    return df


def item_level_ccr(data_encoded_df, questionnaire_encoded_df):
    q_embeddings = questionnaire_encoded_df.embedding
    d_embeddings = data_encoded_df.embedding
    similarities = util.pytorch_cos_sim(d_embeddings, q_embeddings)
    for i in range(1, len(questionnaire_encoded_df)+1):
        data_encoded_df["sim_item_{}".format(i)] = similarities[:, i-1]
    return data_encoded_df


def ccr_wrapper(data_df, data_col, q_df, q_col):
    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

    q_encoded_df = encode_column(model, q_df, q_col)
    data_encoded_df = encode_column(model, data_df, data_col)

    ccr_df = item_level_ccr(data_encoded_df, q_encoded_df)
    ccr_df = ccr_df.drop(columns=["embedding"])

    return ccr_df


if __name__ == '__main__':
    # median word count for any document is about 3000
    # max word count supported on input text for most models is about 500
    # so we need to split each input text into 6 chunks
    # this chunk size preserves most of the information
    # any chunk with > 500 words will be truncated, which is a reasonable tradeoff for speed
    df = pd.read_csv('/n/henrich_lab/Lab/clean/stat4.csv')
    print(f'Median # words for a document: {df.word_counts.median()}')

    # median number of chars for a document is about 7000
    # that's about 1200 chars per chunk if using 6 chunks per document
    df = pd.read_csv('/n/henrich_lab/Lab/clean/strat_sample_200.csv')

    # original stratified sample is with replacement - drop duplicates first, then take smaller sample
    df.drop_duplicates(subset=['path_id'], inplace=True)
    df = df.sample(n=1000, random_state=42).copy()

    # some stat
    df['nchar'] = df.text.str.len()
    print(f'Median # chars for a document: {df.nchar.median()}')
    print(f'# documents: {df.shape[0]}')

    # process input text column - split into 6 separate columns (chunks)
    # the first 5 chunks all have 1200 chars, the rest go into the last chunk
    df['chunk1'] = df['text'].str.slice(0, 1200)
    df['chunk2'] = df['text'].str.slice(1200, 2400)
    df['chunk3'] = df['text'].str.slice(2400, 3600)
    df['chunk4'] = df['text'].str.slice(3600, 4800)
    df['chunk5'] = df['text'].str.slice(4800, 6000)
    df['chunk6'] = df['text'].str.slice(start=6000)  # note: if text is not long enough then it's ''

    # pivot longer
    df_d = pd.melt(df, id_vars=['path_id', 'year'],
        value_vars=['chunk1', 'chunk2', 'chunk3', 'chunk4', 'chunk5', 'chunk6'],
        var_name='chunk', value_name='chunked_text')

    # load questionnaire df
    df_q = pd.read_csv('data/q6.csv')

    # now we can simply apply the ccr wrapper function to chunked_text column and q column
    log('wrapper starts')
    t1 = datetime.now()

    res = ccr_wrapper(df_d, 'chunked_text', df_q, 'q')

    t2 = datetime.now()
    log('wrapper ends')
    print(f'\ttime elapsed: {t2 - t1}')

    # save result
    log('saving to csv...')
    t1 = datetime.now()

    res.to_csv('/n/henrich_lab/Lab/clean/ccr1.csv', index=False)

    t2 = datetime.now()
    log('saved to csv')
    print(f'\ttime elapsed: {t2 - t1}')
