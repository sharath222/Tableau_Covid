import pandas as pd
tests_day_wise = pd.read_csv('https://www.kaggle.com/imdevskp/covid19-corona-virus-india-dataset/download/state_level_latest.csv')

# save as .csv file
tests_day_wise.to_csv('state_level_latest.csv', index=False)

# first few rows
tests_day_wise.head()