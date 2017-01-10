import pandas as pd
import scipy
import os

standard_weight_vector = {
    "price": .25,
    "hotness": .15,
    "crime": .15,
    "nightlife": .10,
    "education": .10,
    "diversity": .10,
    "creative": .10,
    "art": .05
}

"""
Final Model


Try/Except will fill in worst value for column if for some reason key is not present in dictionary
"""


def ranking_function(df_housing, df_div, df_edu, df_create, df_night, df_cr,  weight_vector):
    ranking_dict = {}
    for csa in df_div.index:
        try:
            art_score = df_div.loc[csa]["art_score"]
        except:
            art_score = df_div["art_score"].min()
        try:
            diversity_score = df_div.loc[csa]["diversity_score"]
        except:
            diversity_score = df_div["diversity_score"].min()
        try:
            education_score = df_edu.loc[csa]["zscore"]
        except:
            education_score = df_edu["zscore"].min()
        try:
            creative_score = df_create.loc[csa]['Creative Z Score']
        except:
            creative_score = df_create['Creative Z Score'].min()
        try:
            nightlife_score = df_night.loc[csa]["Count_per_pop_zscore"]
        except:
            nightlife_score = df_night["Count_per_pop_zscore"].min()
        try:
            crime_score = df_cr.loc[csa]["zscore"]
        except:
            crime_score = df_cr["zscore"].min()
        try:
            price_score = df_housing.loc[csa]["Median Prices Z Score"]
        except:
            price_score = df_housing["Median Prices Z Score"].min()
        try:
            hotness_score = df_housing.loc[csa]["Median Days Z Score"]
        except:
            hotness_score = df_housing["Median Days Z Score"].min()

        ranking_dict[csa] = ((weight_vector["art"] * art_score) + (weight_vector["diversity"] * diversity_score) +
                             (weight_vector["education"] * education_score) + (weight_vector["creative"] * creative_score) +
                             (weight_vector["nightlife"] * nightlife_score) + (weight_vector["crime"] * crime_score) +
                             (weight_vector["price"] * price_score) + (weight_vector['hotness'] * hotness_score))

    return pd.DataFrame.from_dict(ranking_dict, orient="index")


df_art_diversity = pd.read_csv(
    "./Rankings/baseline_art_diversity.csv", index_col="CSA2010")
df_education = pd.read_csv("./Rankings/education.csv", index_col="Community")
df_creative = pd.read_csv(
    "./Rankings/Creative+Art Rankings.csv", index_col="Community")
df_nightlife = pd.read_csv(
    "./Rankings/final_res_count.csv", index_col="Neighborhood")
df_crime = pd.read_csv(
    "./Rankings/art_rankings.csv", index_col="Community")
df_housing_cost = pd.read_csv(
    "./Rankings/baseline_model.csv", index_col="CSA2010")


df = ranking_function(df_housing_cost, df_art_diversity, df_education,
                      df_creative, df_nightlife, df_crime, standard_weight_vector)
df=df.sort_values(0, ascending=False)
df.to_csv("Final Ranks.csv")
