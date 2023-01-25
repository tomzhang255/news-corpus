# for each year, sample about 200 documents, and create a data with the # of non-word errors.
# stratified sampling with replacement because some years have < 200 documents

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
from gc import collect  # garbage collector


t1 = datetime.now()
print(t1)

# read meta
meta = pd.read_csv('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt',
                    sep='|', encoding_errors='ignore',
                    usecols=['Publication_Date', 'File_Path'],
                    dtype={'Publication_Date': str, 'File_Path': str})
print(f'{datetime.now()} (meta loaded)')
meta['Year'] = meta['Publication_Date'].str.slice(0, 4)
meta.drop('Publication_Date', axis=1, inplace=True)

# keep year and index only
meta1 = meta[['Year']].reset_index()

# take stratified sample based on year (sample 200 documents for each year)
np.random.seed(42)
stratified_sample = meta1.groupby('Year').apply(lambda x: x.sample(n=200, replace=True))
print(f'{datetime.now()} (got stratified sample)')

# get original rows based on sample indices
sub = meta.loc[stratified_sample['index']]
sub.reset_index(drop=True, inplace=True)

# clean up file path from subsetted meta data
sub['File_Path1'] = sub['File_Path'].str.slice(11).str.replace('\\', '/', regex=False)

# for each corpus html file relevant to subsetted meta data
paths = sub['File_Path']
paths1 = sub['File_Path1']
years = sub['Year']

base_og = '/n/henrich_lab/Lab/newspaperarchive_corpus/'
base_clean = '/n/henrich_lab/Lab/clean/'

# an iteration in the for-loop
def process(i):
    path = paths[i]
    path1 = paths1[i]
    year = years[i]

    path_read = base_og + path1

    with open(path_read, 'rb') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        obj = soup.body

        if obj is None:
            obj = soup
        
        txt = obj.get_text()

    return path, year, txt

# run for-loop but parallelized
pool = Pool(None)
res = pool.map(process, range(len(paths)))  # None <- os.cpu_count() <- use all
pool.close()
pool.join()
collect()

# save csv
print(f'{datetime.now()} (saving strat sample with original text)')
res = pd.DataFrame(res, columns=['path_id', 'year', 'text'])
collect()
res.to_csv('' + 'strat_sample_200.csv', index=False)

# done
t2 = datetime.now()
print(f'{t2} (done)')
print(f'Time elapsed: {t2 - t1}')
