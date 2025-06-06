# q5_1_peak_daily_new_cases.py

import pandas as pd

# load data
try:
    df = pd.read_csv('covid_19_confirmed_v1.csv')
    print("data loaded ok for peak case check")
except FileNotFoundError as e:
    print(f"err: file missing - {e}. put csv in same folder plz")
    exit()

# make long format
df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
             var_name='Date', value_name='Confirmed_Cases')
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')


# only check few countries
countries = ['Germany', 'France', 'Italy']
df = df[df['Country/Region'].isin(countries)]

# group by date and country
daily = df.groupby(['Country/Region', 'Date'])['Confirmed_Cases'].sum().reset_index()

print("\n-- checking daily rise --")

peaks = {}

for c in countries:
    d = daily[daily['Country/Region'] == c].sort_values('Date')
    d['Daily_New'] = d['Confirmed_Cases'].diff().fillna(d['Confirmed_Cases'])
    d['Daily_New'] = d['Daily_New'].apply(lambda x: max(0, x))

    peak_val = d['Daily_New'].max()
    peak_day = d[d['Daily_New'] == peak_val]['Date'].iloc[0]

    peaks[c] = {'val': int(peak_val), 'day': peak_day.strftime('%Y-%m-%d')}
    print(f"{c.lower()}: peak {int(peak_val)} on {peak_day.strftime('%Y-%m-%d')}")

# who had max surge
max_country = max(peaks, key=lambda x: peaks[x]['val'])
max_val = peaks[max_country]['val']
max_day = peaks[max_country]['day']

print("\n-- result --")
print(f"{max_country.lower()} had max 1-day rise: {max_val} on {max_day}")
