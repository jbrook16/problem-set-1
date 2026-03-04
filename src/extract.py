'''
PART 1: EXTRACT WEATHER AND TRANSIT DATA

Pull in data from two dataset
1. Weather data from visualcrossing's weather API (https://www.visualcrossing.com/weather-api)
- You will need to sign up for a free account to get an API key
-- You only get 1000 rows free per day, so be careful to build your query correctly up front
-- Though not best practice, include your API key directly in your code for this assignment
- Write code below to get weather data for Chicago, IL for the date range 10/1/2024 - 10/31/2025
- The default data fields should be sufficient
2. Daily transit ridership data for the Chicago Transit Authority (CTA)
- Here is the URL: ttps://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

Load both as CSVs into /data
- Make sure your code is line with the standards we're using in this class 
'''

import os
import requests
import pandas as pd


DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)



def extract_weather_data():

    api_key = "4SRAQRSJ22YYXFCQBJLQF8LPC"  

    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    location = "Chicago,IL"
    start_date = "2024-10-01"
    end_date = "2025-10-31"

    url = f"{base_url}/{location}/{start_date}/{end_date}"

    params = {
        "unitGroup": "us",
        "include": "days",
        "key": api_key,
        "contentType": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Weather API request failed: {response.status_code}")

    weather_json = response.json()


    weather_data = pd.DataFrame(weather_json["days"])


    output_path = os.path.join(DATA_DIR, "weather_raw.csv")
    weather_data.to_csv(output_path, index=False)

    print("Weather data extracted successfully.")

    return weather_data


def extract_transit_data():

    transit_url = "https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

    transit_data = pd.read_csv(transit_url)

    output_path = os.path.join(DATA_DIR, "transit_raw.csv")
    transit_data.to_csv(output_path, index=False)

    print("Transit data extracted successfully.")

    return transit_data




def extract_transit_data():
    transit_url = "https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

    transit_data = pd.read_csv(transit_url)

    output_path = os.path.join(DATA_DIR, "transit_raw.csv")
    transit_data.to_csv(output_path, index=False)

    print("Transit data extracted.")

    return transit_data
