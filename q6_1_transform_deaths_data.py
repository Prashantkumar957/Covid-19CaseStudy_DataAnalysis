# q6_1_transform_deaths_data.py

import pandas as pd

# load deaths dataset
deaths_fp = 'covid_19_deaths_v1.csv'

try:
    # use header=1 for deaths data
    df_deaths = pd.read_csv(deaths_fp, header=1) 
    print("deaths dataset loaded.")
except FileNotFoundError as e:
    print(f"err: file not found - {e}.")
    exit()

print("\n--- original 'deaths' head (wide format) ---")
print(df_deaths.head())

# identify id variables (first 4 columns)
id_vars = df_deaths.columns[:4].tolist()

# melt to long format
df_deaths_long = df_deaths.melt(id_vars=id_vars,
                                var_name='Date',
                                value_name='Deaths_Count')

# convert date to datetime objects
df_deaths_long['Date'] = pd.to_datetime(df_deaths_long['Date'], format='%m/%d/%y', errors='coerce') 

print("\n--- transformed 'deaths' head (long format) ---")
print(df_deaths_long.head())

print("\n--- transformed 'deaths' info (check dtypes) ---")
df_deaths_long.info()

print("\ndataset transformed successfully.")