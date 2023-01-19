# simple summary stat on word count
# (average word count per publisher per year)


import pandas as pd
from datetime import datetime


t1 = datetime.now()

# read meta
meta = pd.read_csv('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt',
                    sep='|', dtype=str, encoding_errors='ignore',
                    usecols=['State_Name', 'City_Name', 'Publication_Title', 'Publication_Date', 'File_Path'])
meta['Year'] = meta['Publication_Date'].str.slice(0, 4)
print('{} (meta loaded)'.format(datetime.now()))

# read word count
BASE = '/n/henrich_lab/Lab/clean/'
wc = pd.read_csv('{}wc_all.csv'.format(BASE))
wc.rename({'path_id': 'File_Path', 'word_count': 'Word_Count'}, axis=1, inplace=True)
print('{} (wc loaded). Joining...'.format(datetime.now()))

# join
df = pd.merge(meta, wc, how='left', on='File_Path')
print('{} (joined)'.format(datetime.now()))

# stat
df.drop('File_Path', axis=1, inplace=True)
res = df.groupby(['State_Name', 'City_Name', 'Publication_Title', 'Year'])[['Word_Count']].mean()
res.reset_index(inplace=True)
res.rename({'Word_Count': 'Avg_Word_Count'}, axis=1, inplace=True)
res['Avg_Word_Count'] = res['Avg_Word_Count'].round()
print('{} (stat done)'.format(datetime.now()))

# save
print('{} (saving...)'.format(datetime.now()))
res.to_csv('{}stat.csv'.format(BASE), index=False)
print('{} (saved)'.format(datetime.now()))

# done
t2 = datetime.now()
print('Total time elapsed: {}'.format(t2 - t1))
