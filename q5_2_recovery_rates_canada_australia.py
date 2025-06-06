# q5_2_recovery_rates_canada_australia.py

import pandas as pd

# try to load files
try:
    df_c = pd.read_csv('covid_19_confirmed_v1.csv')
    df_r = pd.read_csv('covid_19_recovered_v1.csv', header=1) # <--- ADDED header=1
    print("confirmed + recovered data loaded fine")
except FileNotFoundError as e:
    print(f"err: file not found - {e}")
    exit()

# date to check
date = '2020-12-31'

# melt both dfs
df_c = df_c.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                 var_name='Date', value_name='Confirmed')
# Specify format for robustness in date parsing
df_c['Date'] = pd.to_datetime(df_c['Date'], format='%m/%d/%y', errors='coerce')

df_r = df_r.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                 var_name='Date', value_name='Recovered')
df_r['Date'] = pd.to_datetime(df_r['Date'], format='%m/%d/%y') 

# filter both
countries = ['Canada', 'Australia']
df_c = df_c[(df_c['Country/Region'].isin(countries)) & (df_c['Date'] == date)]
df_r = df_r[(df_r['Country/Region'].isin(countries)) & (df_r['Date'] == date)]

# total up
df_c = df_c.groupby('Country/Region')['Confirmed'].sum().reset_index()
df_r = df_r.groupby('Country/Region')['Recovered'].sum().reset_index()

# merge + calc rate
df = pd.merge(df_c, df_r, on='Country/Region', how='left')
df['Recovery_Rate'] = df.apply(
    lambda row: (row['Recovered'] / row['Confirmed']) * 100 if row['Confirmed'] > 0 else 0, axis=1
)

print(f"\n-- recovery % as of {date} --")
print(df)

# compare
if not df.empty:
    c_rate = df[df['Country/Region'] == 'Canada']['Recovery_Rate'].iloc[0]
    a_rate = df[df['Country/Region'] == 'Australia']['Recovery_Rate'].iloc[0]

    print("\n-- result --")
    if c_rate > a_rate:
        print(f"canada better: {c_rate:.2f}% vs australia {a_rate:.2f}%")
    elif a_rate > c_rate:
        print(f"australia better: {a_rate:.2f}% vs canada {c_rate:.2f}%")
    else:
        print(f"both same rate: {c_rate:.2f}%")
else:
    print("no data to compare, check csvs or date again")