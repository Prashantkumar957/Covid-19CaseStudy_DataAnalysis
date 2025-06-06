# q8_1_highest_death_rates_2020.py

import pandas as pd

# load datasets
conf_fp = 'covid_19_confirmed_v1.csv'
deaths_fp = 'covid_19_deaths_v1.csv'
recov_fp = 'covid_19_recovered_v1.csv'

try:
    df_confirmed = pd.read_csv(conf_fp)
    df_deaths = pd.read_csv(deaths_fp, header=1)
    df_recovered = pd.read_csv(recov_fp, header=1)
    print("all datasets loaded for combined analysis.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

# func to transform and aggregate df
def transform_and_aggregate(df, value_col_name):
    id_vars = df.columns[:4].tolist()
    df_long = df.melt(id_vars=id_vars,
                      var_name='Date',
                      value_name=value_col_name)
    # convert date to datetime
    df_long['Date'] = pd.to_datetime(df_long['Date'], format='%m/%d/%y', errors='coerce') # added format
    df_long[value_col_name] = df_long.groupby(['Province/State', 'Country/Region'])[value_col_name].ffill()
    df_long[value_col_name] = df_long[value_col_name].fillna(0)
    df_aggregated = df_long.groupby(['Country/Region', 'Date'])[value_col_name].sum().reset_index()
    return df_aggregated

# apply transform to each dataset
df_confirmed_agg = transform_and_aggregate(df_confirmed, 'Confirmed')
df_deaths_agg = transform_and_aggregate(df_deaths, 'Deaths')
df_recovered_agg = transform_and_aggregate(df_recovered, 'Recovered')

# merge datasets
df_merged = df_confirmed_agg.copy()
df_merged = pd.merge(df_merged, df_deaths_agg, on=['Country/Region', 'Date'], how='outer')
df_merged = pd.merge(df_merged, df_recovered_agg, on=['Country/Region', 'Date'], how='outer')

# sort and fill nans
df_merged = df_merged.sort_values(by=['Country/Region', 'Date']).reset_index(drop=True)
df_merged[['Confirmed', 'Deaths', 'Recovered']] = df_merged[['Confirmed', 'Deaths', 'Recovered']].fillna(0)

# analysis for 2020 death rates
df_2020 = df_merged[(df_merged['Date'].dt.year == 2020)].copy()

# get latest cumulative data for each country in 2020
latest_date_2020_per_country = df_2020.groupby('Country/Region')['Date'].max().reset_index()
latest_date_2020_per_country.rename(columns={'Date': 'Latest_Date_2020'}, inplace=True)

df_2020_totals = pd.merge(df_2020, latest_date_2020_per_country,
                          left_on=['Country/Region', 'Date'],
                          right_on=['Country/Region', 'Latest_Date_2020'],
                          how='inner')

df_2020_totals = df_2020_totals[['Country/Region', 'Confirmed', 'Deaths']].copy()

# calculate death rate
df_2020_totals['Death_Rate'] = df_2020_totals.apply(
    lambda row: (row['Deaths'] / row['Confirmed']) * 100 if row['Confirmed'] > 0 else 0,
    axis=1
)

# sort by death rate
df_2020_totals_sorted = df_2020_totals.sort_values(by='Death_Rate', ascending=False)

# get top 3 countries
top_3_death_rate_countries = df_2020_totals_sorted.head(3) # completed this line

print("\n--- top 3 countries with highest death rates in 2020 ---")
print(top_3_death_rate_countries.to_string(index=False))

print("\n--- potential indications ---")
print("high death rate can mean several things:")
print("- health system was strained, few resources.")
print("- older population or more sick people in general.")
print("- not enough testing, so only severe cases counted.")
print("- gov response maybe not fast enough or effective.")
print("- new, more dangerous virus type.")