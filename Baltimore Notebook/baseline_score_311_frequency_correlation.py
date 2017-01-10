import pandas as pd
import json
import scipy.stats

df_baseline = pd.read_csv("baseline_model.csv")
normalized_complaint_frequency = json.load(open(
    "/root/Development/CSE519/BaltimoreRanking-519/Data/data_311/311_num_complaints_by_neighborhood_normalized.json"))

score = []
normalized_311_frequency = []
art_score = []
for row_num, series in df_baseline.iterrows():
    score.append(series["Score"])
    normalized_311_frequency.append(
        normalized_complaint_frequency[series["CSA2010"]])

corr, p = scipy.stats.pearsonr(score, normalized_311_frequency)

print(corr, p)
