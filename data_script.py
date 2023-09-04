# proxies_list = open("tested_proxies", "r").read().strip().split("\n")
import pandas as pd
import numpy as np


df = pd.read_pickle(r"C:\Users\dmcfa\Desktop\cEDH_Decks.pk1")
f = open('competitive_decks', "r").read().strip().split("\n")
lst = open('list', 'r').read().strip().split('\n')
# print(df.value_counts(['Card_Name']))
for i in f:
    if i not in lst:
        print(i)
"""df['Status'] = np.where(df['Deck_Link'].item in f, 'Competitive', 'Outdated')

for j, k in df.iterrows():
    print(j, k)"""