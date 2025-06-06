import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load file
confirmed_cases_filepath = 'covid_19_confirmed_v1.csv'
try:
    df_confirmed = pd.read_csv(confirmed_cases_filepath)
except FileNotFoundError as e:
    print(f"error: file not found - {e}. make sure the csv is in same folder")
    exit()

# reshape data (dates to rows)
df_confirmed_long = df_confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                      var_name='Date', value_name='Confirmed_Cases')

# change date col to datetime
df_confirmed_long['Date'] = pd.to_datetime(df_confirmed_long['Date'])

# group by country + date
df_confirmed_country_daily = df_confirmed_long.groupby(['Country/Region', 'Date'])['Confirmed_Cases'].sum().reset_index()

# get top 5 countries by total cases
total_cases_by_country = df_confirmed_country_daily.groupby('Country/Region')['Confirmed_Cases'].max().sort_values(ascending=False)
top_countries = total_cases_by_country.head(5).index.tolist()

# filter only top countries
df_top_countries = df_confirmed_country_daily[df_confirmed_country_daily['Country/Region'].isin(top_countries)]

# plot it
plt.figure(figsize=(15, 8))
sns.lineplot(data=df_top_countries, x='Date', y='Confirmed_Cases', hue='Country/Region', marker='o', markersize=4, linestyle='-', alpha=0.8)

# labels n title
plt.title('confirmed cases over time for top countries', fontsize=16, color='darkblue')
plt.xlabel('date', fontsize=12, color='gray')
plt.ylabel('confirmed cases', fontsize=12, color='gray')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title='country/region', title_fontsize='13', fontsize='10', frameon=True, shadow=True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_countries_confirmed_cases.png')
plt.show()
