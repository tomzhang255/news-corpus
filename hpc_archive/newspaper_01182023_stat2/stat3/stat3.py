# using the meta data file:
# the distribution of the
# average number of pages per newspaper issue (a newspaper on a given day) across years


import pandas as pd
from datetime import datetime


t1 = datetime.now()


# read meta
meta = pd.read_csv('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt',
                    sep='|', encoding_errors='ignore',
                    dtype={'Publication_Date': str, 'Publication_Title': str, 'Page_Number': int},
                    usecols=['Publication_Date', 'Publication_Title', 'Page_Number'])
meta['Year'] = meta['Publication_Date'].str.slice(0, 4)
print('{} (meta loaded)'.format(datetime.now()))

# stat
res = meta.groupby(['Publication_Title', 'Publication_Date'])[['Page_Number']].count()  # combine pages of each issue
res.reset_index(inplace=True)
res['Year'] = res['Publication_Date'].str.slice(0, 4)
res = res.groupby('Year')[['Page_Number']].mean()  # answers the question
res.reset_index(inplace=True)
res.rename({'Page_Number': 'Avg_Page_Count_Per_Issue'}, axis=1, inplace=True)
print('{} (done stat); saving...'.format(datetime.now()))

# save
res.to_csv('/n/henrich_lab/Lab/clean/stat3.csv', index=False)

# done
t2 = datetime.now()
print('time elapsed: {}'.format(t2 - t1))
