# q5_3_canada_death_rates_by_province.py

import pandas as pd
import numpy as np # np for general numerical ops, not strictly needed here but good to have

# load files
conf_fp = 'covid_19_confirmed_v1.csv'
deaths_fp = 'covid_19_deaths_v1.csv'

try:
    df_conf = pd.read_csv(conf_fp)
    # use header=1 for deaths data if headers are on 2nd row
    df_deaths = pd.read_csv(deaths_fp, header=1) # added header=1
    print("conf and deaths loaded.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

# process conf data
df_conf_long = df_conf.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                            var_name='Date', value_name='Confirmed_Cases')
df_conf_long['Date'] = pd.to_datetime(df_conf_long['Date'], format='%m/%d/%y', errors='coerce') # added format
df_conf_canada = df_conf_long[df_conf_long['Country/Region'] == 'Canada'].copy()

# process deaths data
df_deaths_long = df_deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                var_name='Date', value_name='Deaths')
df_deaths_long['Date'] = pd.to_datetime(df_deaths_long['Date'], format='%m/%d/%y', errors='coerce') # added format
df_deaths_canada = df_deaths_long[df_deaths_long['Country/Region'] == 'Canada'].copy()

# find latest common date for canada
latest_date_conf = df_conf_canada['Date'].max()
latest_date_deaths = df_deaths_canada['Date'].max()
latest_common_date = min(latest_date_conf, latest_date_deaths)

print(f"analysing data as of: {latest_common_date.strftime('%Y-%m-%d')}")

# filter data for latest common date
df_conf_canada_latest = df_conf_canada[df_conf_canada['Date'] == latest_common_date].copy()
df_deaths_canada_latest = df_deaths_canada[df_deaths_canada['Date'] == latest_common_date].copy()

# aggregate by province/state
conf_by_prov = df_conf_canada_latest.groupby('Province/State')['Confirmed_Cases'].sum().reset_index()
deaths_by_prov = df_deaths_canada_latest.groupby('Province/State')['Deaths'].sum().reset_index()

# merge and calc death rate
df_canada_rates = pd.merge(conf_by_prov, deaths_by_prov, on='Province/State', how='left')
df_canada_rates['Death_Rate'] = df_canada_rates.apply(
    lambda row: (row['Deaths'] / row['Confirmed_Cases']) * 100 if row['Confirmed_Cases'] > 0 else 0,
    axis=1
)

# sort for highest/lowest
df_canada_rates_sorted = df_canada_rates.sort_values(by='Death_Rate', ascending=False)

print("\n--- death rates (deaths/conf) in canada provinces ---")
print(df_canada_rates_sorted[['Province/State', 'Confirmed_Cases', 'Deaths', 'Death_Rate']].to_string(index=False))

# identify highest and lowest
if not df_canada_rates_sorted.empty:
    highest_rate_prov = df_canada_rates_sorted.iloc[0]
    lowest_rate_prov = df_canada_rates_sorted.iloc[-1]

    print("\n--- results ---")
    print(f"prov with highest death rate: {highest_rate_prov['Province/State']} ({highest_rate_prov['Death_Rate']:.2f}%)")
    print(f"prov with lowest death rate: {lowest_rate_prov['Province/State']} ({lowest_rate_prov['Death_Rate']:.2f}%)")
else:
    print("no data for canada or provinces to calc rates.")