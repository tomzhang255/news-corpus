import pandas as pd
from sentence_transformers import SentenceTransformer, util
from datetime import datetime


def log(msg):
    print(f'{datetime.now()}; {msg}')


def encode_column(model, filename, col_name):
    df = pd.read_csv(filename)
    df["embedding"] = list(model.encode(df[col_name]))
    return df


def item_level_ccr(data_encoded_df, questionnaire_encoded_df):
    q_embeddings = questionnaire_encoded_df.embedding
    d_embeddings = data_encoded_df.embedding
    similarities = util.pytorch_cos_sim(d_embeddings, q_embeddings)
    for i in range(1, len(questionnaire_encoded_df)+1):
        data_encoded_df["sim_item_{}".format(i)] = similarities[:, i-1]
    return data_encoded_df


def ccr_wrapper(data_file, data_col, q_file, q_col):

    model = SentenceTransformer('all-MiniLM-L6-v2')
    questionnaire_filename = q_file
    data_filename = data_file
    print(data_filename)

    q_encoded_df = encode_column(model, questionnaire_filename, q_col)
    data_encoded_df = encode_column(model, data_filename, data_col)

    ccr_df = item_level_ccr(data_encoded_df, q_encoded_df)
    ccr_df = ccr_df.drop(columns=["embedding"])

    return ccr_df


if __name__ == '__main__':
    log('wrapper start')
    t1 = datetime.now()

    res = ccr_wrapper('data/test3.csv', 'd', 'data/test.csv', 'q')

    t2 = datetime.now()
    log('wrapper end')
    print(f'\ttime elapsed: {t2 - t1}')


    log('saving to csv...')
    t1 = datetime.now()

    res.to_csv('ccr_results.csv', index=False)

    t2 = datetime.now()
    log('saved to csv')
    print(f'\ttime elapsed: {t2 - t1}')


    log('saving to parquet...')
    t1 = datetime.now()

    res.to_parquet('ccr_results.parquet.gzip', compression='gzip', index=False)

    t2 = datetime.now()
    log('saved to parquet')
    print(f'\ttime elapsed: {t2 - t1}')
