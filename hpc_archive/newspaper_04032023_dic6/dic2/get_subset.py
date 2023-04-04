import pandas as pd
from datetime import datetime
from gc import collect  # garbage collector


df = pd.read_csv('/n/henrich_lab/Lab/clean/dic2.csv')
print(f'{datetime.now()}; dic2.csv read')

sub = df.loc[df.year == 1950]
sub.to_csv('dic2_1970.csv', index=False)
print(f'{datetime.now()}; 1950 done')
collect()

sub = df.loc[df.year == 1970]
sub.to_csv('dic2_1970.csv', index=False)
print(f'{datetime.now()}; 1970 done')
collect()

sub = df.loc[df.year == 1990]
sub.to_csv('dic2_1990.csv', index=False)
print(f'{datetime.now()}; 1990 done')
collect()

sub = df.loc[df.year == 2010]
sub.to_csv('dic2_2010.csv', index=False)
print(f'{datetime.now()}; 2010 done')
collect()
