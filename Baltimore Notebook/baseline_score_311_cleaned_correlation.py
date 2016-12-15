"""
Corr: -0.25456007830189198
P: 0.060719440709136235


"""


import json
import pandas as pd
import scipy.stats


df = pd.read_csv("./Data/311.csv")
df_baseline = pd.read_csv("baseline_model.csv")
data_cleaned = json.load(open("./Data/311_data_cleaned.json"))
neighborhood_map = json.load(open("Data/csa_to_neighborhood_map.json"))

incident_frequencies_by_neighborhood = {}
found = False
for row_num, series in df.iterrows():
    if series["SRType"] in data_cleaned.keys():
        neighborhood = series["Neighborhood"]
        for key, value in neighborhood_map.items():
            for subneighborhood in value:
                if neighborhood.lower() in subneighborhood.lower():
                    try:
                        incident_frequencies_by_neighborhood[key] += 1
                    except Exception as e:
                        incident_frequencies_by_neighborhood[key] = 1
                    found = True
                    break
            if found == True:
                found = False
                break
score = []
frequency = []
for row_num, series in df_baseline.iterrows():
    score.append(series["Score"])
    frequency.append(
        incident_frequencies_by_neighborhood[series["CSA2010"]])

corr, p = scipy.stats.pearsonr(score, frequency)
