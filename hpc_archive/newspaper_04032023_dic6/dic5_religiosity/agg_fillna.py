import pandas as pd

df = pd.read_csv('/n/henrich_lab/Lab/dic5_religiosity/dic5_agg.csv')
df.fillna(0.0, inplace=True)
df.to_csv('/n/henrich_lab/Lab/dic5_religiosity/dic5_agg_fillna.csv', index=False)
