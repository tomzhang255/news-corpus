# concatenates all word count csv files together


import pandas as pd
from datetime import datetime


t1 = datetime.now()
BASE = '/n/henrich_lab/Lab/ocr/'
num_list = ['0', '1', '2', '3', '4', '5', '6a', '6b', '7a', '7b', '8', '9', '10', '11']

df = pd.DataFrame(columns=['path_id', 'word_count'])
for i in num_list:
    curr = pd.read_csv('{}wc_ocr_{}.csv'.format(BASE, i))
    df = pd.concat([df, curr], ignore_index=True)

print('{}. Done, {} rows in total. Saving...'.format(datetime.now(), df.shape[0]))

df.to_csv('{}wc_all.csv'.format(BASE), index=False)

t2 = datetime.now()
print('{}. Finished. Time elapsed: {}'.format(t2, t2 - t1))
