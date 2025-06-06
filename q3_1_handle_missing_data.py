# q3_1_handle_missing_data.py

import pandas as pd

# load files
confirmed_cases_filepath = 'covid_19_confirmed_v1.csv'
deaths_filepath = 'covid_19_deaths_v1.csv'
recovered_cases_filepath = 'covid_19_recovered_v1.csv'

try:
    df_confirmed = pd.read_csv(confirmed_cases_filepath)
    df_deaths = pd.read_csv(deaths_filepath, header=1) #
    df_recovered = pd.read_csv(recovered_cases_filepath, header=1) # 
    print("data loaded ok.")
except FileNotFoundError as e:
    print(f"file missing - {e}. check file path again.")
    exit()

print("\n--- before filling missing ---")

# check missing vals
def identify_missing(df, name):
    print(f"missing in {name}:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print("-" * 30)

identify_missing(df_confirmed, 'confirmed')
identify_missing(df_deaths, 'deaths')
identify_missing(df_recovered, 'recovered')

print("\n--- filling missing using ffill ---")

# melt + fill for confirmed
df_confirmed_long = df_confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                      var_name='Date', value_name='Confirmed_Cases')
df_confirmed_long['Date'] = pd.to_datetime(df_confirmed_long['Date'], format='%m/%d/%y', errors='coerce') # Added format for robustness
df_confirmed_long['Confirmed_Cases'] = df_confirmed_long.groupby(['Province/State', 'Country/Region'])['Confirmed_Cases'].ffill()
df_confirmed_long['Confirmed_Cases'] = df_confirmed_long['Confirmed_Cases'].fillna(0)
print("confirmed cases filled.")

# melt + fill for deaths
df_deaths_long = df_deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                var_name='Date', value_name='Deaths')
df_deaths_long['Date'] = pd.to_datetime(df_deaths_long['Date'], format='%m/%d/%y', errors='coerce') # Added format for robustness
df_deaths_long['Deaths'] = df_deaths_long.groupby(['Province/State', 'Country/Region'])['Deaths'].ffill()
df_deaths_long['Deaths'] = df_deaths_long['Deaths'].fillna(0)
print("deaths data filled.")

# melt + fill for recovered
df_recovered_long = df_recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                      var_name='Date', value_name='Recovered_Cases')
df_recovered_long['Date'] = pd.to_datetime(df_recovered_long['Date'], format='%m/%d/%y', errors='coerce') # Added format for robustness
df_recovered_long['Recovered_Cases'] = df_recovered_long.groupby(['Province/State', 'Country/Region'])['Recovered_Cases'].ffill()
df_recovered_long['Recovered_Cases'] = df_recovered_long['Recovered_Cases'].fillna(0)
print("recovered data filled.")

# check again
print("\n--- after filling ---")
print("confirmed missing:", df_confirmed_long.isnull().sum().sum())
print("deaths missing:", df_deaths_long.isnull().sum().sum())
print("recovered missing:", df_recovered_long.isnull().sum().sum())

print("\nnote: missing vals are filled using last known value (ffill)")
print("if start of data is missing, we put 0")
print("\nfirst few rows of confirmed data after clean:")
print(df_confirmed_long.head())