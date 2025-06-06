# q7_3_monthly_summary_us_italy_brazil.py

import pandas as pd

# load datasets
conf_fp = 'covid_19_confirmed_v1.csv'
deaths_fp = 'covid_19_deaths_v1.csv'
recov_fp = 'covid_19_recovered_v1.csv'

try:
    df_confirmed = pd.read_csv(conf_fp)
    # use header=1 for deaths and recovered data
    df_deaths = pd.read_csv(deaths_fp, header=1)
    df_recovered = pd.read_csv(recov_fp, header=1)
    print("all datasets loaded for specific country monthly summary.")
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

# monthly sum for specific countries
df_merged['Month_Year'] = df_merged['Date'].dt.to_period('M')

target_countries = ['US', 'Italy', 'Brazil'] # define target countries
df_filtered_countries = df_merged[df_merged['Country/Region'].isin(target_countries)].copy()

monthly_summary_filtered = df_filtered_countries.groupby(['Country/Region', 'Month_Year'])[
    ['Confirmed', 'Deaths', 'Recovered']
].sum().reset_index()

monthly_summary_filtered['Month_Year'] = monthly_summary_filtered['Month_Year'].astype(str) # convert to string
monthly_summary_filtered = monthly_summary_filtered.sort_values(by=['Country/Region', 'Month_Year']) # sort

print("\n--- monthly sum of confirmed, deaths, recov for us, italy, brazil ---")
print(monthly_summary_filtered.to_string(index=False))

print("\nnote: analysis provides monthly cumulative totals for specified countries.")