import pandas as pd

dic = pd.read_csv('data/dic.csv')
dic['count'] = 0
dic = dic.set_index('word').to_dict()['count']
print(dic)


dic = pd.read_csv('data/dic.csv')
print(dic.word.to_list())
