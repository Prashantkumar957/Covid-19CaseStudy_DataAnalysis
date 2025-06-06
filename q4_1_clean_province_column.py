# q4_1_clean_province_column.py

import pandas as pd
import numpy as np

# Load the datasets.
# Assuming 'covid_19_confirmed_v1.csv', 'covid_19_deaths_v1.csv',
# and 'covid_19_recovered_v1.csv' are in the same directory.
confirmed_cases_filepath = 'covid_19_confirmed_v1.csv'
deaths_filepath = 'covid_19_deaths_v1.csv'
recovered_cases_filepath = 'covid_19_recovered_v1.csv'

try:
    df_confirmed = pd.read_csv(confirmed_cases_filepath)
    df_deaths = pd.read_csv(deaths_filepath)
    df_recovered = pd.read_csv(recovered_cases_filepath)
    print("datasets loaded successfully for cleaning 'Province/State' column.")
except FileNotFoundError as e:
    print(f"ERROR: file not found - {e}. PLEASE ENSURE THE CSV FILES ARE IN THE CORRECT DIRECTORY.")
    exit()

print("\\n--- before cleaning 'province/state' column (sample of missing values) ---")
print("confirmed cases 'province/state' missing values:")
print(df_confirmed['Province/State'].isnull().sum())
print("deaths 'province/state' missing values:")
print(df_deaths['Province/State'].isnull().sum())
print("recovered cases 'province/state' missing values:")
print(df_recovered['Province/State'].isnull().sum())

# Replace blank values (NaN or empty strings) in 'Province/State' with "All Provinces"
def clean_province_column(df):
    # Replace NaN values
    df['Province/State'] = df['Province/State'].fillna('All Provinces')
    # Replace empty strings if any
    df['Province/State'] = df['Province/State'].replace('', 'All Provinces')
    return df

df_confirmed = clean_province_column(df_confirmed)
df_deaths = clean_province_column(df_deaths)
df_recovered = clean_province_column(df_recovered)

print("\\n--- after cleaning 'province/state' column (sample of missing values) ---")
print("confirmed cases 'province/state' missing values:")
print(df_confirmed['Province/State'].isnull().sum())
print("deaths 'province/state' missing values:")
print(df_deaths['Province/State'].isnull().sum())
print("recovered cases 'province/state' missing values:")
print(df_recovered['Province/State'].isnull().sum())

print("\\n'province/state' column cleaned successfully in all datasets.")
print("\\nexample of 'province/state' column after cleaning (confirmed cases dataset):")
print(df_confirmed[['Country/Region', 'Province/State']].head(10))
print("\\nnotice how some 'province/state' entries might have changed to 'all provinces' if they were blank.")