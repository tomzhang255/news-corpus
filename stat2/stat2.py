# using the meta data file:
# the distributions of the overall number of pages and number of newspapers across years


import pandas as pd
from datetime import datetime


t1 = datetime.now()

# read meta
meta = pd.read_csv('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt',
                    sep='|', encoding_errors='ignore',
                    usecols=['Publication_Title', 'Publication_Date', 'Page_Number'],
                    dtype={'Publication_Title': str, 'Publication_Date': str, 'Page_Number': int})
meta['Year'] = meta['Publication_Date'].str.slice(0, 4)
print('{} (meta loaded)'.format(datetime.now()))

# stat
res = meta.groupby(['Publication_Title', 'Publication_Date'])[['Page_Number']].count()  # combine pages of each issue
res.reset_index(inplace=True)
res['Year'] = res['Publication_Date'].str.slice(0, 4)
res = res.groupby('Year')[['Page_Number']].agg(['sum', 'count'])  # answers the question
res.reset_index(inplace=True)
res.columns = ['Year', 'Sum_Pages', 'Count_Newspapers']
print('{} (done stat); saving...'.format(datetime.now()))

# save
res.to_csv('/n/henrich_lab/Lab/clean/stat2.csv', index=False)

# done
t2 = datetime.now()
print('time elapsed: {}'.format(t2 - t1))
