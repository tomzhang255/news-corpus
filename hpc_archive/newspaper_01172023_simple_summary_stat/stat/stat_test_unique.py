# simple summary stat on word count
# (average word count per publisher per year)


import pandas as pd


BASE = '/n/henrich_lab/Lab/clean/'

meta = pd.read_csv('/n/henrich_lab/Lab/newspaperarchive_metadata/Harvard_FileDetails.txt',
                    sep='|', usecols=['City_Name', 'Publication_Title'], dtype=str, nrows=1000000)
res = meta.groupby('Publication_Title')['City_Name'].value_counts().to_frame()
res.columns = ['count']
res.reset_index(inplace=True)
a = res['Publication_Title'].nunique()
b = res['City_Name'].nunique()
print(a, b, a==b)
