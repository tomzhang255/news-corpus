# concatenate all ocr0_* files in ocr/

import pandas as pd
from os import walk
from datetime import datetime


i = 2


all_filenames = next(walk('/n/henrich_lab/Lab/ocr/'), (None, None, []))[2]
curr_chunk_filenames = list(filter(lambda x: x.startswith(f'ocr{i}_'), all_filenames))
# convert ocr0_0.csv into ocr0_00.csv to make sorting easier
curr_chunk_filenames_clean = list(map(lambda x: f'{x[:5]}0{x[5]}{x[6:]}' if len(x) == 10 else x, curr_chunk_filenames))
files_zip = list(zip(curr_chunk_filenames_clean, curr_chunk_filenames))
files_zip.sort()
files = [x[1] for x in files_zip]
print(files)
print(len(files))
