import pandas as pd
import matplotlib.pyplot as plt

# Renewable Energy Analytics per Country
# Using Pandas, Matplotlib to analyze growth and contribution of Solar, Wind, Hydro (2000-2024)

energy_df = pd.read_csv("renewable_energy_data.csv")

#Data Cleaning
for col in ["Solar_GWh", "Wind_GWh","Hydro_GWh"]:
    energy_df[col] = (energy_df.groupby("Country")[col]
                                     .transform(lambda x: x.ffill().bfill()))

energy_df["Total_Renewable_GWh"] = (energy_df["Total_Renewable_GWh"]
                                    .fillna(energy_df["Solar_GWh"] + energy_df["Wind_GWh"]
                                    + energy_df["Hydro_GWh"]))

energy_df = energy_df.drop_duplicates()

#Analysis
energy_df["GrowthRate"] = energy_df.groupby("Country")["Total_Renewable_GWh"].pct_change()
energy_df["SolarContribution(%)"] = (energy_df["Solar_GWh"] / energy_df["Total_Renewable_GWh"]
                                  * 100)
energy_df["WindContribution(%)"] = (energy_df["Wind_GWh"] / energy_df["Total_Renewable_GWh"]
                                  * 100)
energy_df["HydroContribution(%)"] = (energy_df["Hydro_GWh"] / energy_df["Total_Renewable_GWh"]
                                  * 100)


total_energy_growth = energy_df.groupby("Year")["Total_Renewable_GWh"].sum()
avg_growth_rate_per_country = energy_df.groupby("Country")["GrowthRate"].mean()
avg_solar_per_country = energy_df.groupby("Country")["SolarContribution(%)"].mean()
avg_wind_per_country = energy_df.groupby("Country")["WindContribution(%)"].mean()
avg_hydro_per_country = energy_df.groupby("Country")["HydroContribution(%)"].mean()
top_3_highest_growth = avg_growth_rate_per_country.sort_values(ascending=False).head(3)

contributions = pd.DataFrame({
    "Solar": avg_solar_per_country,
    "Wind": avg_wind_per_country,
    "Hydro": avg_hydro_per_country
})

fig, axs = plt.subplots(1, 3, figsize=(24, 6))

#Plot 1: Total Renewable Energy Growth per Year
axs[0].plot(total_energy_growth.index, total_energy_growth.values, color="teal")
axs[0].set_title("Renewable Energy Growth per Year")
axs[0].set_xlabel("Year")
axs[0].set_ylabel("Total Renewable Energy (GWh)")

#Plot 2: Top 3 Fastest Growing Countries
axs[1].bar(top_3_highest_growth.index, top_3_highest_growth.values, color="red")
axs[1].set_title("Top 3 Fastest Growing Countries")
axs[1].set_xlabel("Country")
axs[1].set_ylabel("Growth (%)")

#Plot 3: Relative Renewable Energy Contribution
contributions.plot(kind="bar", stacked=True, ax=axs[2], color=["gold", "gray", "blue"])
axs[2].tick_params(axis="x", rotation=45)
axs[2].set_title("Average Renewable Energy Contribution Per Country")
axs[2].set_xlabel("Country")
axs[2].set_ylabel("Relative Contribution (%)")
axs[2].legend(title="Energy Source")

plt.suptitle("Renewable Energy Analytics per Country")
plt.tight_layout(pad=3)
plt.savefig("renewable_energy_analysis.png", dpi=300)
plt.show()