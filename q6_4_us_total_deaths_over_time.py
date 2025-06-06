# q6_4_us_total_deaths_over_time.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load deaths data
deaths_fp = 'covid_19_deaths_v1.csv'

try:
    # use header=1 for deaths data
    df_deaths = pd.read_csv(deaths_fp, header=1) # added header=1
    print("deaths dataset loaded for us total deaths analysis.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

# melt to long format
df_deaths_long = df_deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                var_name='Date',
                                value_name='Cumulative_Deaths')

# convert date to datetime
df_deaths_long['Date'] = pd.to_datetime(df_deaths_long['Date'], format='%m/%d/%y', errors='coerce') # added format

# filter for us
df_us_deaths = df_deaths_long[df_deaths_long['Country/Region'] == 'US'].copy()

# aggregate total deaths by date for us
df_us_total_deaths_daily = df_us_deaths.groupby('Date')['Cumulative_Deaths'].sum().reset_index()

# generate plot
plt.figure(figsize=(12, 7))
sns.lineplot(data=df_us_total_deaths_daily, x='Date', y='Cumulative_Deaths',
             marker='o', markersize=3, linestyle='-', color='purple', alpha=0.8)

# add titles and labels
plt.title('total deaths over time in the united states', fontsize=16, color='darkmagenta')
plt.xlabel('date', fontsize=12, color='gray')
plt.ylabel('cumulative deaths', fontsize=12, color='gray')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()

# save plot
plt.savefig('us_total_deaths_over_time.png')

# show plot
plt.show()

print("\nnote: plot shows cumulative deaths in us over time.")