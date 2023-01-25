# plots stat4.csv

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('stat4.csv')

df['year'] = df['year'].astype('int')
df['nonword_error_rate'] = df['error_counts'] / df['word_counts']

agg1 = df.groupby('year')[['word_counts']].median().reset_index()
agg2 = df.groupby('year')[['error_counts']].median().reset_index()
agg3 = df.groupby('year')[['nonword_error_rate']].median().reset_index()

plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.lineplot(data=agg1, x='year', y='word_counts')
plt.ylabel('median word count')

plt.subplot(1, 3, 2)
sns.lineplot(data=agg2, x='year', y='error_counts')
plt.ylabel('median non-word error count')

plt.subplot(1, 3, 3)
sns.lineplot(data=agg3, x='year', y='nonword_error_rate')
plt.ylabel('median non-word error rate')

plt.suptitle('Statistics for Stratified OCR Sample on Non-word Errors')
plt.tight_layout()
plt.savefig('stat4.png')
plt.show()
