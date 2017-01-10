import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Data/census.csv", header=1, index_col="CSA2010")
less_25 = df["Percent of Households Earning Less than $25,000 (2010-2014)"]
betw_25_40 = df["Percent of Households Earning $25,000 to $40,000 (2010-2014)"]
betw_40_60 = df["Percent of Households Earning $40,000 to $60,000 (2010-2014)"]
betw_60_75 = df["Percent of Households Earning $60,000 to $75,000 (2010-2014)"]
more_75 = df["Percent of Households Earning More than $75,000 (2010-2014)"]
# med_income = df["Median Household Income (2010-2014)"]
df2 = pd.DataFrame({"less_25": less_25, "betw_25_40": betw_25_40,
                    "betw_40_60": betw_40_60, "betw_60_75": betw_60_75, "more_75": more_75})

poorest_neighborhood = df2.loc["Oldtown/Middle East"]
richest_neighborhood = df2.loc["Greater Roland Park/Poplar Hill"]
baltimore_city = df2.loc["Baltimore City"]


plt.subplot(1, 3, 1)
plt.bar([0, 1, 2, 3, 4, ], [poorest_neighborhood["less_25"], poorest_neighborhood["betw_25_40"],
                            poorest_neighborhood["betw_40_60"], poorest_neighborhood["betw_60_75"], poorest_neighborhood["more_75"]], tick_label=["< 25k", "25-40", "40-60", "60-75", "75 < "], align="center")
plt.ylabel("Percentage of Residents", fontsize=22)
plt.xlabel("Income Bracket", fontsize=22)
plt.title("Poorest Neighborhood", fontsize=22)
# plt.xticks(range(5), ("< 25k", "25-40" "40-60", "60-75", "75 < "))

plt.subplot(1, 3, 2)
plt.bar([0, 1, 2, 3, 4], [baltimore_city["less_25"], baltimore_city["betw_25_40"],
                          baltimore_city["betw_40_60"], baltimore_city["betw_60_75"], baltimore_city["more_75"]], tick_label=["< 25k", "25-40", "40-60", "60-75", "75 < "], align="center")
plt.ylim([0, 70])
plt.ylabel("Percentage of Residents", fontsize=22)
plt.xlabel("Income Bracket", fontsize=22)
plt.title("Baltimore Average", fontsize=22)

plt.subplot(1, 3, 3)
plt.bar([0, 1, 2, 3, 4], [richest_neighborhood["less_25"], richest_neighborhood["betw_25_40"],
                          richest_neighborhood["betw_40_60"], richest_neighborhood["betw_60_75"], richest_neighborhood["more_75"]], tick_label=["< 25k", "25-40", "40-60", "60-75", "75 < "], align="center")
plt.ylabel("Percentage of Residents", fontsize=22)
plt.xlabel("Income Bracket", fontsize=22)
plt.title("Richest Neighborhood", fontsize=22)


plt.suptitle("Income Distribution", fontsize=30, weight="heavy")
plt.show()
