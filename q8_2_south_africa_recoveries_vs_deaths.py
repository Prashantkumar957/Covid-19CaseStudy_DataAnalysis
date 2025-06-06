# q8_2_south_africa_recoveries_vs_deaths.py

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
    print("all datasets loaded for south africa analysis.")
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

# compare recoveries to deaths in south africa
df_sa = df_merged[df_merged['Country/Region'] == 'South Africa'].copy()

# get total recovered and total deaths for sa
total_recov_sa = df_sa['Recovered'].max()
total_deaths_sa = df_sa['Deaths'].max()

print(f"\n--- comparison: south africa recoveries vs. deaths ---")
print(f"total recovered cases in south africa: {int(total_recov_sa):,}")
print(f"total deaths in south africa: {int(total_deaths_sa):,}")

print("\n--- what this can tell us ---")
if total_recov_sa > total_deaths_sa:
    print(f"recoveries ({int(total_recov_sa):,}) are higher than deaths ({int(total_deaths_sa):,}) in south africa.")
    print("suggests majority of cases resulted in recovery.")
    print("indicates effective health measures or young pop.")
elif total_deaths_sa > total_recov_sa:
    print(f"deaths ({int(total_deaths_sa):,}) are higher than recoveries ({int(total_recov_sa):,}) in south africa.")
    print("concerning sign, potentially overwhelmed healthcare.")
else:
    print(f"recoveries ({int(total_recov_sa):,}) are equal to deaths ({int(total_deaths_sa):,}) in south africa.")
    print("challenging situation or delayed recovery.")

print("\nnote: high-level comparison. more analysis needed for detailed insights.")