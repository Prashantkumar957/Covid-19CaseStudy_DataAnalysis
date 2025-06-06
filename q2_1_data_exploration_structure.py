# q2_1_data_exploration_structure.py

import pandas as pd

confirmed_cases_filepath = 'covid_19_confirmed_v1.csv'
deaths_filepath = 'covid_19_deaths_v1.csv'
recovered_cases_filepath = 'covid_19_recovered_v1.csv'

try:
    df_confirmed = pd.read_csv(confirmed_cases_filepath)
    df_deaths = pd.read_csv(deaths_filepath)
    df_recovered = pd.read_csv(recovered_cases_filepath)

    print("--- confirmed cases dataset structure ---")
    print("shape:", df_confirmed.shape)
    print("\ninfo:")
    df_confirmed.info()

    print("\n--- deaths dataset structure ---")
    print("shape:", df_deaths.shape)
    print("\ninfo:")
    df_deaths.info()

    print("\n--- recovered cases dataset structure ---")
    print("shape:", df_recovered.shape)
    print("\ninfo:")
    df_recovered.info()

except FileNotFoundError as e:
    print(f"error loading file: {e}. ensure the csv files are in the correct directory.")