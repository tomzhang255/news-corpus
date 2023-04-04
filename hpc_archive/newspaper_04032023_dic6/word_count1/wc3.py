# a simple word count script for result csv files
# saves as new csv with original text column dropped


import pandas as pd
from datetime import datetime

t1 = datetime.now()

i = 3
BASE = '/n/henrich_lab/Lab/clean/'

res = pd.read_csv('{}res{}.csv'.format(BASE, i), lineterminator='\n')
print('{} (read_csv done)'.format(datetime.now()))
res['word_count'] = res['text'].str.split().str.len()
print('{} (word count done)'.format(datetime.now()))
res.drop('text', axis=1, inplace=True)
print('{} (drop col done)'.format(datetime.now()))
print('saving csv now...')
res.to_csv('{}wc{}.csv'.format(BASE, i), index=False)
print('{} (to_csv done)'.format(datetime.now()))

t2 = datetime.now()
print('Time elapsed: {}'.format(t2 - t1))
