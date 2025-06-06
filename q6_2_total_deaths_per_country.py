# q6_2_total_deaths_per_country.py

import pandas as pd

# load deaths data
deaths_fp = 'covid_19_deaths_v1.csv'

try:
    # use header=1 for deaths data
    df_deaths = pd.read_csv(deaths_fp, header=1) 
    print("deaths dataset loaded.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

# melt to long format
id_vars = df_deaths.columns[:4].tolist()
df_deaths_long = df_deaths.melt(id_vars=id_vars,
                                var_name='Date',
                                value_name='Deaths_Count')

# convert date to datetime
df_deaths_long['Date'] = pd.to_datetime(df_deaths_long['Date'], format='%m/%d/%y', errors='coerce') # added format

# get latest death count per country/province
df_latest_deaths = df_deaths_long.groupby(['Country/Region', 'Province/State'])['Date'].max().reset_index()
df_latest_deaths = pd.merge(df_latest_deaths, df_deaths_long, on=['Country/Region', 'Province/State', 'Date'], how='left')

# sum total deaths per country
total_deaths_per_country = df_latest_deaths.groupby('Country/Region')['Deaths_Count'].sum().reset_index()
total_deaths_per_country.rename(columns={'Deaths_Count': 'Total_Deaths'}, inplace=True)

# sort descending
total_deaths_per_country_sorted = total_deaths_per_country.sort_values(by='Total_Deaths', ascending=False)

print("\n--- total deaths per country (top 20) ---")
print(total_deaths_per_country_sorted.head(20).to_string(index=False))

print("\nnote: 'current date' is latest available date in dataset for each country.")