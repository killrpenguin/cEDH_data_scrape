# proxies_list = open("tested_proxies", "r").read().strip().split("\n")
import pandas as pd


df1 = pd.read_pickle(r"C:\Users\dmcfa\Desktop\cedh_webscrape1.pk1")
print(df1.value_counts())
# df2 = df1.pivot_table(index = ['Card_names'], aggfunc ='size')
# df3 = df2.sort_values(by='col1', ascending=False, na_position='first')
