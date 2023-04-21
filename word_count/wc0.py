# a simple word count script for result csv files
# saves as new csv with original text column dropped


import pandas as pd
from datetime import datetime

t1 = datetime.now()

i = 0
BASE = '/n/henrich_lab/Lab/clean/'
print('wc{}'.format(i))

wc_list = None
id_list = None

with pd.read_csv('{}res{}.csv'.format(BASE, i), dtype=str, chunksize=1000000, lineterminator='\n') as reader:
    for chunk in reader:
        wc_curr_chunk = chunk['text'].str.split().str.len()
        wc_list = pd.concat([wc_list, wc_curr_chunk])
        id_curr_chunk = chunk['path_id']
        id_list = pd.concat([id_list, id_curr_chunk])

res = pd.DataFrame({'path_id': id_list, 'word_count': wc_list})

print('saving csv now...')
res.to_csv('{}wc{}.csv'.format(BASE, i), index=False)
print('{} (to_csv done)'.format(datetime.now()))

t2 = datetime.now()
print('Time elapsed: {}'.format(t2 - t1))
