'''
This file creates a file listing all unique newspaper titles.

Last update: February 20th, 2023 / MP
'''

#%%
## LIBRARIES ------------------
import os
import pandas as pd

#%%
## PATHS ------------------
os.chdir("/n/henrich_lab/Lab")
path_srcdata = os.path.join("newspaperarchive_metadata", "Harvard_FileDetails.txt")

#%%
## SCRIPT ------------------
meta = pd.read_table(path_srcdata, sep='|')
distinct_meta = meta[['State_Name', 'City_Name',
                      'Publication_Title', 'Publication_Date']].drop_duplicates()
distinct_meta['Publication_Date'] = pd.to_datetime(distinct_meta['Publication_Date'], format='%Y-%m-%d')
distinct_meta['Publication_Year'] = distinct_meta['Publication_Date'].dt.year
distinct_meta = distinct_meta[['State_Name', 'City_Name', 'Publication_Title', 'Publication_Year']].drop_duplicates()
distinct_titles = distinct_meta[['State_Name', 'City_Name', 'Publication_Title']].drop_duplicates()
distinct_title_years = distinct_meta.copy()

### Save -----
distinct_titles.to_csv(os.path.join("clean", "unique_titles.csv"), index=False)
distinct_title_years.to_csv(os.path.join("clean", "unique_title_years.csv"), index=False)
