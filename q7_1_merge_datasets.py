# q7_1_merge_datasets.py

import pandas as pd

# load datasets
conf_fp = 'covid_19_confirmed_v1.csv'
deaths_fp = 'covid_19_deaths_v1.csv'
recov_fp = 'covid_19_recovered_v1.csv'

try:
    df_conf = pd.read_csv(conf_fp)
    # use header=1 for deaths and recovered data
    df_deaths = pd.read_csv(deaths_fp, header=1)
    df_recov = pd.read_csv(recov_fp, header=1)
    print("all datasets loaded for merging.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

# func to transform and clean df
def transform_and_clean(df, value_col_name):
    # identify id vars
    id_vars = df.columns[:4].tolist()

    # melt to long format
    df_long = df.melt(id_vars=id_vars,
                      var_name='Date',
                      value_name=value_col_name)

    # convert date to datetime
    df_long['Date'] = pd.to_datetime(df_long['Date'], format='%m/%d/%y', errors='coerce') # added format

    # ffill then fillna 0 for value col
    df_long[value_col_name] = df_long.groupby(['Province/State', 'Country/Region'])[value_col_name].ffill()
    df_long[value_col_name] = df_long[value_col_name].fillna(0)

    # aggregate by country/region and date
    df_aggregated = df_long.groupby(['Country/Region', 'Date'])[value_col_name].sum().reset_index()

    return df_aggregated

# apply transform to each dataset
df_conf_agg = transform_and_clean(df_conf, 'Confirmed')
df_deaths_agg = transform_and_clean(df_deaths, 'Deaths')
df_recov_agg = transform_and_clean(df_recov, 'Recovered')

print("\n--- datasets transformed and aggregated ---")
print("confirmed head:")
print(df_conf_agg.head())
print("\ndeaths head:")
print(df_deaths_agg.head())
print("\nrecovered head:")
print(df_recov_agg.head())

# merge datasets
df_merged = df_conf_agg.copy() # start with confirmed

df_merged = pd.merge(df_merged, df_deaths_agg, on=['Country/Region', 'Date'], how='outer') # merge with deaths
df_merged = pd.merge(df_merged, df_recov_agg, on=['Country/Region', 'Date'], how='outer') # merge with recovered

# sort and reset index
df_merged = df_merged.sort_values(by=['Country/Region', 'Date']).reset_index(drop=True)

# fill remaining nans from outer join
df_merged[['Confirmed', 'Deaths', 'Recovered']] = df_merged[['Confirmed', 'Deaths', 'Recovered']].fillna(0)

print("\n--- merged dataset head ---")
print(df_merged.head())

print("\n--- merged dataset info ---")
df_merged.info()

print("\ndatasets successfully merged.")