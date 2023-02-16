# a script that reads in a subset of corpus html files, cleans them (extracts text)
# then saves to the "clean" folder while preserving the original directory structure

# preserve dir structure: ~60 days
# save to single csv file with path identifier column: ~20 days


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime


# read in a subset of meta data
# note: the entire meta data file alone is 30.5 GB (~230 million rows)
nrows = 10000
t1 = datetime.now()
print('{} (reading meta data, {} rows)'.format(t1, nrows))
meta = pd.read_table('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt', sep='|', nrows=nrows)
print('{} (done reading meta data, {} rows)'.format(datetime.now(), nrows))


# clean up file path from meta data
meta['File_Path1'] = meta['File_Path'].str.slice(11).str.replace('\\', '/', regex=False)

# for each corpus html file
paths = meta['File_Path']
paths1 = meta['File_Path1']

base_og = '/n/henrich_lab/Lab/newspaperarchive_corpus/'
base_clean = '/n/henrich_lab/Lab/clean/'


res = []

for i in range(len(paths)):
    path = paths[i]
    path1 = paths1[i]

    path_read = base_og + path1

    with open(path_read, 'rb') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        txt = soup.body.get_text()

        # save txt file to the "clean" directory
        # path_write = base_clean + path[:-5] + '.txt'

        # create subdirectories if not exist
        # outfile = Path(path_write)
        # outfile.parent.mkdir(parents=True, exist_ok=True)

        # with open(path_write, 'w') as f:
            # f.write(txt)
        
        res.append((path, txt))

    if i % 1000 == 0:  # progress log every once in awhile
        print(i)

res = pd.DataFrame(res, columns=['path_id', 'text'])
res.to_csv(base_clean + 'res.csv', index=False)


t2 = datetime.now()
print('{} (script finished)'.format(t2))
print('Total time elapsed: {}'.format(t2 - t1))
