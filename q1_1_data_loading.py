# q1_1_data_loading.py

import pandas as pd

# here i am define all file paths 
confirmed_cases_filepath = 'covid_19_confirmed_v1.csv'
deaths_filepath = 'covid_19_deaths_v1.csv'
recovered_cases_filepath = 'covid_19_recovered_v1.csv'

# here i am loadign all the datasets
try:
    df_confirmed = pd.read_csv(confirmed_cases_filepath)
    df_deaths = pd.read_csv(deaths_filepath)
    df_recovered = pd.read_csv(recovered_cases_filepath)
    print("datasets loaded successfully!")
except FileNotFoundError as e:
    print(f"Error loading file: {e}. make sure the csv files are in the correct directory.")