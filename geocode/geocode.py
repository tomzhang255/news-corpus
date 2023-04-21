'''
This file creates a file assigning longitudes, latitudes, and fips 
codes to newspaper titles.

Last update: February 18th, 2023 / MP
'''

#%%
## LIBRARIES ------------------
import addfips
# !pip install geopy
import os
import pandas as pd
import requests
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.geocoders import Bing
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
from geopy.exc import GeocoderQuotaExceeded
from time import sleep

#%%
## PATHS ------------------
os.chdir("/n/henrich_lab/Lab")
path_srcdata = os.path.join("newspaperarchive_metadata", "Harvard_FileDetails.txt")
path_outdata = os.path.join("clean", "geocode.csv")


#%%
## FUNCTIONS ------------------
def do_nominatim(address):
    print("I'm getting {}".format(address))
    sleep(1)
    geolocator = Nominatim(user_agent="geocoder")
    try:
        return geolocator.geocode(address)
    except (GeocoderTimedOut, GeocoderServiceError, GeocoderQuotaExceeded) as x:
        print('geolocator failed, {}'.format(x.__class__.__name__))
        sleep(10)
        return do_nominatim(address)


def do_bing(address):
    print("I'm getting {}".format(address))
    sleep(1)
    geolocator = Bing(
        api_key='ApBu7s3uHCGMVIn0d8BYpKVLWGdSDkQzCNeZCbNQwTbdFQyWJoEPBIYjNP5maQHx')
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut as x:
        print('gelocator failed, {}'.format(x.__class__.__name__))
        return do_bing(address)
    except GeocoderServiceError as y:
        print('gelocator failed, {}'.format(y.__class__.__name__))
        sleep(10)
        return do_bing(address)


def do_google(address):
    print("I'm getting {}".format(address))
    geolocator = GoogleV3(api_key='AIzaSyBPIW2jWkv4ytc_Lbvj2Xoac0N1MpVJ9Mk')
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut as x:
        print('gelocator failed, {}'.format(x.__class__.__name__))
        return do_google(address)
    except GeocoderServiceError as y:
        print('gelocator failed, {}'.format(y.__class__.__name__))
        sleep(60)
        return do_google(address)

def eval_results(x):
    try:
        return (x.address, x.latitude, x.longitude)
    except:
        return (None, None, None)


def get_fips(row):
    sleep(1)
    url = 'https://geo.fcc.gov/api/census/block/find?latitude={}&longitude={}&censusYear=2020&format=json'
    request = url.format(row['latitude'], row['longitude'])
    response = requests.get(request)
    data = response.json()
    # return multiple values as a series - this will create a dataframe with multiple columns
    return pd.Series({'fips': data['County']['FIPS'], 'county': data['County']['name'], 'state_fips': data['State']['FIPS']})



#%%
## SCRIPT ------------------
meta = pd.read_table(path_srcdata, sep='|')
distinct_meta = meta[['State_Name', 'City_Name']].drop_duplicates()
distinct_meta.loc[:, 'address'] = distinct_meta['City_Name'].str.cat(
    distinct_meta['State_Name'], sep=', ') + ', USA'

### Nominatim -----
distinct_meta['geocode'] = distinct_meta['address'].apply(lambda x: do_nominatim(
    x) if x != None else None).apply(lambda x: eval_results(x))

temp = distinct_meta['geocode'].apply(pd.Series)
temp = temp.rename(columns={0 : 'geocode', 1 : "latitude", 2 : "longitude"})
temp.drop(['geocode'], axis=1, inplace=True)
distinct_meta = pd.concat([distinct_meta, temp], axis=1)

### Bing -----
failed = pd.DataFrame(
    distinct_meta['address'][pd.isnull(distinct_meta['latitude'])])
failed['geocode'] = failed['address'].apply(lambda x: do_bing(
    x) if x != None else None).apply(lambda x: eval_results(x))

temp = failed['geocode'].apply(pd.Series)
temp = temp.rename(columns={0 : 'geocode', 1 : "latitude", 2 : "longitude"})
temp.drop(['geocode'], axis=1, inplace=True)
failed = pd.concat([failed, temp], axis=1)
failed.drop(['address'], axis=1, inplace=True)
distinct_meta.loc[distinct_meta['latitude'].isnull(), ['geocode', 'latitude', 'longitude']] = failed


### Assign FIPS codes -----
fips = distinct_meta.apply(get_fips, axis=1)
distinct_meta = pd.concat([distinct_meta, fips], axis=1)
# distinct_meta.loc[distinct_meta['longitude'].isna()]
# distinct_meta.loc[distinct_meta['fips'].isna()]


### Save -----
distinct_meta = distinct_meta[['State_Name', 'City_Name', 'latitude', 'longitude', 'fips', 'county', 'state_fips']]
distinct_meta.to_csv(path_outdata, index=False)
