"""
Filter 311 rows into neighborhood buckets

We can then tabulate: 

What are the most common types of calls per neighborhood
What is the time between opening and closing a call per neighborhood? Do some neighborhoods receive bettter service?


"""


import json
import pandas as pd
import copy
import ipdb

mapping = json.load(open("./Data/data_311/311_mapping.json"))
df_311 = pd.read_csv("./Data/data_311/311.csv")

df_neighborhoods = []
for key, value in mapping.items():
    row_list = []
    for row_num in value:
        row_list.append(df_311.iloc[row_num].to_dict())

    df_neighborhoods.append((pd.DataFrame(row_list), key))

for df, neighborhood in df_neighborhoods:
    if "/" in neighborhood:
        neighborhood = neighborhood.split("/")
        neighborhood = neighborhood[0]
    df.to_csv("Data/data_311/" + neighborhood + ".csv")
