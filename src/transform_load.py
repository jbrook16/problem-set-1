'''
PART 2: Merge and transform the data
- Read in the two datasets from /data into two separate dataframes
- Profile, clean, and standardize date fields for both as needed
- Merge the two dataframe for the date range 10/1/2024 - 10/31/2025
- Conduct EDA to understand the relationship between weather and transit ridership over time
-- Create a line plot of daily transit ridership and daily average temperature over the whole time period
-- For February 2025, create a scatterplot of daily transit ridership vs. precipitation
-- Create a correlation heatmap of all numeric features in the merged dataframe
-- Load the merged dataframe as a CSV into /data
-- In a print statement, summarize any interesting trends you see in the merged dataset

'''

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def merge_and_transform():

    weather_df = pd.read_csv(os.path.join(DATA_DIR, "weather_raw.csv"))
    transit_df = pd.read_csv(os.path.join(DATA_DIR, "transit_raw.csv"))


    weather_df["date"] = pd.to_datetime(weather_df["datetime"])
    weather_df = weather_df.drop(columns=["datetime"])

    
    transit_df["date"] = pd.to_datetime(transit_df["service_date"])

    
    start_date = "2024-10-01"
    end_date = "2025-10-31"

    weather_df = weather_df[
        (weather_df["date"] >= start_date) &
        (weather_df["date"] <= end_date)
    ]

    transit_df = transit_df[
        (transit_df["date"] >= start_date) &
        (transit_df["date"] <= end_date)
    ]

    
    transit_daily = (
        transit_df
        .groupby("date")["rides"]
        .sum()
        .reset_index()
    )

    merged_df = pd.merge(weather_df, transit_daily, on="date", how="inner")

    merged_df.insert(0, "id", range(1, len(merged_df) + 1))

    
    merged_df.to_csv(os.path.join(DATA_DIR, "merged_weather_transit.csv"), index=False)

    print("Merged and transformed data.")
    

  
    plt.figure()
    plt.plot(merged_df["date"], merged_df["rides"])
    plt.plot(merged_df["date"], merged_df["temp"])
    plt.title("Daily Transit Ridership and Average Temperature")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(DATA_DIR, "lineplot_ridership_temp.png"))
    plt.close()

    feb_2025 = merged_df[
        (merged_df["date"] >= "2025-02-01") &
        (merged_df["date"] <= "2025-02-28")
    ]

    plt.figure()
    plt.scatter(feb_2025["precip"], feb_2025["rides"])
    plt.title("Feb 2025: Ridership vs Precipitation")
    plt.xlabel("Precipitation")
    plt.ylabel("Ridership")
    plt.tight_layout()
    plt.savefig(os.path.join(DATA_DIR, "scatter_feb2025.png"))
    plt.close()

    
    numeric_df = merged_df.select_dtypes(include="number")

    plt.figure()
    sns.heatmap(numeric_df.corr(), annot=True)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(DATA_DIR, "correlation_heatmap.png"))
    plt.close()


    correlation = numeric_df["rides"].corr(numeric_df["temp"])

    print("\n----- Trend Summary -----")
    print(f"Correlation between temperature and ridership: {round(correlation, 3)}")

    if correlation > 0:
        print("Ridership tends to increase as temperature increases.")
    else:
        print("Ridership tends to decrease as temperature increases.")

    print("Further analysis may reveal seasonal and precipitation-related patterns.\n")

    return merged_df