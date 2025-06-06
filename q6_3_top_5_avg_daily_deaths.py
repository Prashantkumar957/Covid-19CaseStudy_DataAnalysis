# q6_3_top_5_avg_daily_deaths.py

import pandas as pd

# load deaths data
deaths_fp = 'covid_19_deaths_v1.csv'

try:
    df_deaths = pd.read_csv(deaths_fp, header=1) 
    print("deaths dataset loaded for avg daily deaths analysis.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

# melt to long format
df_deaths_long = df_deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                var_name='Date',
                                value_name='Cumulative_Deaths')

# convert date to datetime
df_deaths_long['Date'] = pd.to_datetime(df_deaths_long['Date'], format='%m/%d/%y', errors='coerce') # added format

# aggregate cumulative deaths by country and date
df_country_daily_deaths = df_deaths_long.groupby(['Country/Region', 'Date'])['Cumulative_Deaths'].sum().reset_index()

# calc daily new deaths
df_country_daily_deaths = df_country_daily_deaths.sort_values(by=['Country/Region', 'Date'])
df_country_daily_deaths['Daily_New_Deaths'] = df_country_daily_deaths.groupby('Country/Region')['Cumulative_Deaths'].diff()

# handle nans and negative values
df_country_daily_deaths['Daily_New_Deaths'] = df_country_daily_deaths['Daily_New_Deaths'].fillna(0)
df_country_daily_deaths['Daily_New_Deaths'] = df_country_daily_deaths['Daily_New_Deaths'].apply(lambda x: max(0, x))

# calc average daily new deaths
average_daily_deaths = df_country_daily_deaths.groupby('Country/Region')['Daily_New_Deaths'].mean().reset_index()
average_daily_deaths.rename(columns={'Daily_New_Deaths': 'Average_Daily_Deaths'}, inplace=True)

# get top 5 countries
top_5_avg_daily_deaths = average_daily_deaths.sort_values(by='Average_Daily_Deaths', ascending=False).head(5)

print("\n--- top 5 countries with highest avg daily deaths ---")
print(top_5_avg_daily_deaths.to_string(index=False))

print("\nnote: avg daily deaths from daily increments.")