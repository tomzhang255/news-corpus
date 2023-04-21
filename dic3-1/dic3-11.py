# a script that reads in a subset of corpus html files, cleans them (extracts text)
# then applies dictionary word counting
# note: we actually need to break the result csv file into several pieces to not exceed memory
# this script only deals with part of the corpus; there will be 12 result csv files eventually


import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
from collections import Counter
from gc import collect  # garbage collector


def log(msg):
    print(f'{datetime.now()}; {msg}')


def word_count(text, dic=None):
    dic = dic.copy()
    words = text.split()

    for word in words:
        if word in dic:
            dic[word] += 1

    return dic


# read in a subset of meta data
# note: the entire meta data file alone is 30.5 GB (~230 million rows)
t11 = datetime.now()
print('{} (reading meta data, all rows)'.format(t11))
meta = pd.read_table('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt', sep='|', encoding_errors='ignore')
print('{} (done reading meta data, {} rows)'.format(datetime.now(), meta.shape[0]))

# clean up file path from meta data
meta['File_Path1'] = meta['File_Path'].str.slice(11).str.replace('\\', '/', regex=False)

# for each corpus html file
paths = meta['File_Path']
paths1 = meta['File_Path1']

base_og = '/n/henrich_lab/Lab/newspaperarchive_corpus/'
base_clean = '/n/henrich_lab/Lab/clean/'

# an iteration in the for-loop
def process(i):
    path = paths[i]
    path1 = paths1[i]

    path_read = base_og + path1

    try:
        with open(path_read, 'rb') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'lxml')
            obj = soup.body

            if obj is None:
                obj = soup
            
            txt = obj.get_text()
    except FileNotFoundError:
        return path, ''

    return path, txt

# need to break result into several pieces as to not exceed memory
# note: only dealing with one chunk in this script
i = 11
start = 220000000
end = 238803125

# run for-loop but parallelized
print('{}, on {} - {}'.format(datetime.now(), start, end))
# pool = Pool(None)
# clean = pool.map(process, range(start, end))  # None <- os.cpu_count() <- use all
clean = pd.Series(range(start, end)).apply(process).to_list()
# pool.close()
# pool.join()
collect()

# the final cleaned csv
print('{} (saving csv {}: {} - {})'.format(datetime.now(), i, start, end))
clean = pd.DataFrame(clean, columns=['path_id', 'text'])
collect()

# ========== the actual word counting part ==========
# same procedure as the scripts in dic3/

res = None

chunksize = 200000
j = 0
while j < clean.shape[0]:
    try:
        # do it by chunk to save memory
        df = clean.iloc[j : min(j + chunksize, end), :]

        print(f'===== a chunk ({j}) =====')
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
    except Exception as e:
        print(f'===== exception at chunk {j} =====')
        print(e)
        print('==========')

    # increment chunk start
    j += chunksize

res.fillna(0, inplace=True)

# save result
log('saving to csv...')
t1 = datetime.now()

# res.to_csv(f'/n/henrich_lab/Lab/dic/dic3-{i}.csv', index=False)

t2 = datetime.now()
log('saved to csv')
print(f'\ttime elapsed: {t2 - t1}')

# done
t22 = datetime.now()
print('{} (script finished)'.format(t22))
print('Total time elapsed: {}'.format(t22 - t11))
