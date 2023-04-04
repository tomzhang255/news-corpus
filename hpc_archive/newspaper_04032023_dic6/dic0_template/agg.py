# aggregating dicitonary word counting results

# Populist data: you obtained keyword frequencies for the "populist" dictionary I sent you
# a few weeks ago. At the the end are a few lines of code that concat the csv files,
# add meta data, and save the output as one csv file that is then ready for our analysis.
# could you please review my code, edit if necessary, save and run it on the cluster?


## LIBRARIES ------------------
import os
import pandas as pd
import glob
import json

## CONFIG ------------------
with open('config.json') as f:
    config = json.load(f)

## PATHS ------------------
os.chdir("/n/henrich_lab/Lab")

## SCRIPT ------------------
df = pd.DataFrame(columns=['path_id'])

for file_name in glob.glob(f"{config['name']}/dic{config['index']}-"+'*.csv'):
    x = pd.read_csv(file_name)
    try:
        x.drop(['Unnamed: 0'], axis=1, inplace=True)
    except:
        pass
    df = pd.concat([df,x], ignore_index=True)

df.fillna(0.0, inplace=True)

f = os.path.join("newspaperarchive_metadata", "Harvard_FileDetails.txt")
meta = pd.read_table(f, sep='|', encoding_errors='ignore')

f = os.path.join("clean", "geocode.csv")
geocode = pd.read_csv(f)

meta_geocode = pd.merge(meta, geocode, how='left', on=['State_Name','City_Name'])
del meta 
del geocode

meta_geocode = meta_geocode[["File_Path", "Publication_Title", "State_Name", "City_Name", "Publication_Date", "Page_Number", "fips", "state_fips"]]
meta_geocode = meta_geocode.rename(columns = {'File_Path':'path_id'})

df = pd.merge(df, meta_geocode, how='left', on=['path_id'])
df.to_csv(f'{config["name"]}/dic{config["index"]}_agg.csv', index=False)
