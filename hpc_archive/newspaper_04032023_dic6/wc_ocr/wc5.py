# a simple word count script for particion 0 (out of 12) of OCR-processed files
# saves as new csv with original text column dropped


import pandas as pd
from datetime import datetime
from os import walk


t1 = datetime.now()

i = 5
BASE = '/n/henrich_lab/Lab/ocr/'
print(f'wc{i}')

wc_list = None
id_list = None

all_files = next(walk(f'{BASE}'), (None, None, []))[2]  # [] if no file
curr_partition_files = list(filter(lambda f: f.startswith(f'ocr{i}'), all_files))

for f in curr_partition_files:
    chunk = pd.read_csv(f'{BASE}{f}', dtype=str, lineterminator='\n', on_bad_lines='skip', encoding_errors='ignore')
    wc_curr_chunk = chunk['text'].str.split().str.len()
    wc_list = pd.concat([wc_list, wc_curr_chunk])
    id_curr_chunk = chunk['path_id']
    id_list = pd.concat([id_list, id_curr_chunk])

res = pd.DataFrame({'path_id': id_list, 'word_count': wc_list})

print('saving csv now...')
res.to_csv(f'{BASE}wc_ocr_{i}.csv', index=False)
print(f'{datetime.now()} (to_csv done)')

t2 = datetime.now()
print(f'Time elapsed: {t2 - t1}')
