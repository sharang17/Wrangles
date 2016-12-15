"""
Interface versus Phone? Does that correlate with wealth? One assumption would be that phone would be more popular for less wealthy individuals.

Compare difference in time to close an issue between different neighborhoods of the city

"""

import datetime
import pandas as pd
import os
import statistics
import copy
import json
import ipdb
import scipy.stats
import math


def status_date(string):
    return datetime.datetime.strptime(string, "%d/%m/%Y %I:%M:%S %p %z")


def create_date(string):
    return datetime.datetime.strptime(string, "%m/%d/%Y %I:%M:%S %p %z")


# open every file
# create dataframe for each

df_list = []
for f_string in os.listdir("./Data/data_311/"):
    if "311" in f_string:
        continue
    else:
        # tuple containing dataframe, neighborhood name.
        df_list.append((pd.read_csv("./Data/data_311/" +
                                    f_string), f_string.split(".")[0]))

# How should we deal with "Open" requests?
# What if the create and status date are the same?
# OK, so before I was using status date under the assumption that status
# date would be enough. Now I think I should only observe "Closed" cases
# Another important point -- seconds is probably the wrong resolution to calculate the variance on.
# If something differs by only 1 second is that really a difference in service?
# Perhaps we should do minutes?

group_statistics_all = {}
group_statistics_neighborhood = {}
for df, neighborhood in df_list:
    grouped = df.groupby("SRType").groups

    for group, values in grouped.items():
        deltas = []
        for value in values:
            row = df.iloc[value]
            if row["SRStatus"] != "CLOSED":
                continue
            our_created_date = create_date(row["CreatedDate"])
            our_status_date = status_date(row["StatusDate"])

            deltas.append(our_status_date - our_created_date)

        seconds_list = [delta.seconds for delta in deltas]
        # No closed cases
        if not seconds_list:
            continue

        # compute median, mean, count for each neighborhood
        # should I compute minutes here?
        # I think we can preserve the resolution up until we have to calculate
        # the variance
        group_statistics_neighborhood[group] = {}
        group_statistics_neighborhood[group][
            "median"] = statistics.median(seconds_list)
        group_statistics_neighborhood[group][
            "mean"] = statistics.mean(seconds_list)
        group_statistics_neighborhood[group][
            "count"] = len(seconds_list)

    group_statistics_all[neighborhood.lower()] = copy.deepcopy(
        group_statistics_neighborhood)


# One thing that I can do now is compute the variance for a particular
# SRType
# One problem is that not all categories may exist in any foparticular
# Neighborhood.
# So I should first compute the set of unique categories.

categories = set()
for neighborhood in group_statistics_all.keys():
    categories.update(group_statistics_all[neighborhood].keys())


variance_dict = {}
for category in categories:
    median_list = []
    mean_list = []
    count_list = []

    for neighborhood in group_statistics_all:
        try:
            median_list.append(group_statistics_all[
                               neighborhood][category]["median"])
            mean_list.append(group_statistics_all[
                             neighborhood][category]["mean"])
            count_list.append(group_statistics_all[
                              neighborhood][category]["count"])
        except:
            # dont add values if they don't exist
            pass

    # Compute the variance of the median and mean values across all
    # neighborhoods
    # If we compute in hours the variance goes down even more...
    # Variance looks pretty low at that resolution...
    variance_dict[category] = {}
    variance_dict[category]["median"] = statistics.variance(
        [x / 3600 for x in median_list])
    variance_dict[category]["mean"] = statistics.variance(
        [x / 3600 for x in mean_list])
    variance_dict[category]["count-aggregate"] = sum(count_list)
    variance_dict[category]["counts"] = copy.deepcopy(count_list)


# Rank the variance so as to get an idea of categories where variance is
# high and where variance is low

# Easy to sort and compute other statistics if its in a dataframe
df = pd.DataFrame.from_dict(variance_dict, orient='index')

# Compute the correlation and p value for HCD-Sanitation Property
sanitation_dict = {}
for key in group_statistics_all:
    for key2 in group_statistics_all[key]:
        if key2 == "HCD-Sanitation Property":
            sanitation_dict[key] = (group_statistics_all[key][key2][
                                    "median"], group_statistics_all[key][key2]["count"])

df_baseline = pd.DataFrame.read_csv("./baseline_model.csv")

score = []
sanitation_medians = []
for row_num, series in df_baseline.iterrows():
    score.append(series["Score"])
    sanitation_medians.append(
        sanitation_dict[series["CSA2010"].split("/")[0].lower()][0])

corr, p = scipy.stats.pearsonr(score, sanitation_medians)

# Calculate the correlation and the pvalue over all of the 311 categories

median_corr_dict = {}
category_dict_all = {}
# {neighborhood:
#        {
#          category:
#              {
#                mean:
#                ....
#}}}
for category in categories:
    # {neighborhood: median, count}
    category_dict = {}
    for neighborhood in group_statistics_all:
        try:
            category_dict[neighborhood] = (group_statistics_all[neighborhood][category][
                "median"], group_statistics_all[neighborhood][category]["count"])
        except:
            # category does not exist for particular neighborhood
            pass

    category_dict_all[category] = copy.deepcopy(category_dict)

    score = []
    medians = []
    for row_num, series in df_baseline.iterrows():
        score.append(series["Score"])
        try:
            medians.append(
                category_dict[series["CSA2010"].split("/")[0].lower()][0])
        except Exception as e:
            score.pop()

    median_corr_dict[category] = scipy.stats.pearsonr(
        score, medians)

# clean NaN values
median_corr_dict = {k: v for k,
                    v in median_corr_dict.items() if not math.isnan(v[0])}

# sort by absolute p value
sorted_list = sorted(median_corr_dict.items(),
                     key=lambda x: abs(x[1][0]), reverse=True)


# Top three versus bottom three
top_neighborhoods = ["inner harbor", "south baltimore", "north baltimore"]
bottom_neighborhoods = ["madison", "greenmount east", "dickeyville"]


corr_dict_small = {}
for category in category_dict_all:
    scores = []
    medians = []
    for i, neighborhood in enumerate(top_neighborhoods):
        try:
            medians.append(category_dict_all[category][neighborhood][0])
        except:
            break
        scores.append(df_baseline.iloc[i]["Score"])
    for i, neighborhood in enumerate(bottom_neighborhoods):
        try:
            medians.append(category_dict_all[category][neighborhood][0])
        except:
            break
        scores.append(df_baseline.iloc[54 - i]["Score"])
    corr_dict_small[category] = scipy.stats.pearsonr(scores, medians)
