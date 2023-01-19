# a script that reads in a subset of corpus html files, cleans them (extracts text)
# then saves content in a single csv file of two columns: original file path and text
# note: we actually need to break the result csv file into several pieces to not exceed memory


import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool
from gc import collect  # garbage collector


# read in a subset of meta data
# note: the entire meta data file alone is 30.5 GB (~230 million rows)
# nrows = 1000000
nrows = 'all'
t1 = datetime.now()
print('{} (reading meta data, {} rows)'.format(t1, nrows))
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

    with open(path_read, 'rb') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'lxml')
        obj = soup.body

        if obj is None:
            obj = soup
        
        txt = obj.get_text()

    # if i % 10000 == 0:  # log progress once in awhile
        # print(i)

    return path, txt

# need to break result into several pieces as to not exceed memory
SINGLE_LIMIT = 20000000  # size limit of a single result csv file - 20 million rows
CORPUS_SIZE = len(paths)  # how many files in total

start = 0  # start index
end = SINGLE_LIMIT  # end index
i = 0  # counter
res = None

while start < CORPUS_SIZE:
    # garbage colleciton
    del res
    collect()

    # run for-loop but parallelized
    print('{}, on {} - {}'.format(datetime.now(), start, end))
    res = Pool(None).map(process, range(start, end))  # None <- os.cpu_count() <- use all

    # save final csv
    print('{} (saving csv {}: {} - {})'.format(datetime.now(), i, start, end))
    res = pd.DataFrame(res, columns=['path_id', 'text'])
    res.to_csv(base_clean + 'res' + str(i) + '.csv', index=False)

    # increment
    start = end
    if CORPUS_SIZE - end >= SINGLE_LIMIT:
        end += SINGLE_LIMIT
    else:
        end = CORPUS_SIZE
    i += 1


t2 = datetime.now()
print('{} (script finished)'.format(t2))
print('Total time elapsed: {}'.format(t2 - t1))
