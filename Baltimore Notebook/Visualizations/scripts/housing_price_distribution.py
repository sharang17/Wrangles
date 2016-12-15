import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("baseline_model.csv",  index_col="CSA2010")
plt.bar(range(len(df["Median Price of Homes Sold (2014)"])), sorted(df[
        "Median Price of Homes Sold (2014)"], reverse=True), tick_label=sorted(df.index, key=lambda x: df.loc[x]["Median Price of Homes Sold (2014)"], reverse=True))


locs, labels = plt.xticks()
plt.xticks(locs, labels, rotation="vertical")
plt.title(
    "Distribution of Median Home Prices Throughout Baltimore Neighborhoods", fontsize=22, weight="heavy")
plt.xlabel("Neighborhood", fontsize=22)
plt.ylabel("Median Home Price", fontsize=22)
plt.show()
