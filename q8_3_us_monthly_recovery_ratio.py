# q8_3_us_monthly_recovery_ratio.py

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
    print("all datasets loaded for us monthly recovery ratio.")
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

# analyze recovery ratio for us monthly
start_date = pd.to_datetime('2020-03-01')
end_date = pd.to_datetime('2021-05-31')

df_us = df_merged[(df_merged['Country/Region'] == 'US') &
                  (df_merged['Date'] >= start_date) &
                  (df_merged['Date'] <= end_date)].copy()

df_us['Month_Year'] = df_us['Date'].dt.to_period('M') # create month_year

# group by month_year and sum confirmed and recovered
monthly_us_summary = df_us.groupby('Month_Year')[['Confirmed', 'Recovered']].sum().reset_index()

# calc recovery ratio
monthly_us_summary['Recovery_Ratio'] = monthly_us_summary.apply(
    lambda row: (row['Recovered'] / row['Confirmed']) * 100 if row['Confirmed'] > 0 else 0,
    axis=1
)

monthly_us_summary['Month_Year'] = monthly_us_summary['Month_Year'].astype(str) # convert to string
monthly_us_summary = monthly_us_summary.sort_values(by='Month_Year') # sort

print("\n--- monthly recovery ratio for us (mar 2020 - may 2021) ---")
print(monthly_us_summary.to_string(index=False))

# identify month with highest ratio
highest_ratio_month_info = monthly_us_summary.loc[monthly_us_summary['Recovery_Ratio'].idxmax()]

print(f"\n--- month with highest recovery ratio ---")
print(f"highest recovery ratio in us was in {highest_ratio_month_info['Month_Year']} ({highest_ratio_month_info['Recovery_Ratio']:.2f}%).")

print("\n--- potential reasons for highest recovery ratio ---")
print("high ratio could be due to:")
print("1. improved treatment.")
print("2. less severe variants.")
print("3. increased testing (more mild cases).")
print("4. lag in reporting.")
print("5. demographics of infected population.")
print("\nnote: ratio based on cumulative numbers. more precise analysis needs daily new cases/recoveries.")