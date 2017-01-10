import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("Data/housing.csv", header=1, index_col="CSA2010")
construction = df[
    "Number of New Construction Permits per 1,000 Residential Properties (2014)"]

plt.bar(range(len(df["Number of New Construction Permits per 1,000 Residential Properties (2014)"])), sorted(df["Number of New Construction Permits per 1,000 Residential Properties (2014)"],
                                                                                                             reverse=True), tick_label=sorted(df.index, key=lambda x: df.loc[x]["Number of New Construction Permits per 1,000 Residential Properties (2014)"], reverse=True))


locs, labels = plt.xticks()
plt.xticks(locs, labels, rotation="vertical")
plt.xlabel("Neighborhoods", fontsize=22)
plt.ylabel("Construction Permits Per Thousand", fontsize=22)
plt.title("Construction Permits Per Thousand Per Neighborhood",
          weight="heavy", fontsize=22)
plt.show()
