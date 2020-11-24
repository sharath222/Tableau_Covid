# to get web contents
import requests
# to parse json contents
import json
# to parse csv files
import csv

# for numerical operations
import numpy as np
# to store and analysis data in dataframes
import pandas as pd

# # first few rows
# full_data.head()

# # read data
day_wise = pd.read_csv('https://api.covid19india.org/csv/latest/case_time_series.csv')
day_wise = day_wise.drop(['Date'],axis=1)
dayDate = []

from datetime import date, timedelta, datetime

sdate = date(2020, 1, 30)   # start date
edate = datetime.now().date()
delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    dayDate.append(day)

dayDate =  dayDate[0:-1]

day_wise['date'] = dayDate    
# save as a .csv file
day_wise.to_csv('nation_level_daily.csv', index=False)
 
# first few rows
# day_wise.head()
# https://api.covid19india.org/csv/latest/state_wise.csv
    # 
# read data
latest = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')

# save as a .csv file`
latest.to_csv('state_level_latest.csv', index=False)

# first few rows
latest.head()

# read data
state_wise_daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
# state_wise_daily.to_csv('state_level_daily.csv')

# melt dataframe
state_wise_daily = state_wise_daily.melt(id_vars=['Date', 'Status'], value_vars=state_wise_daily.columns[3:], var_name='State', value_name='Count')

# pivot table
state_wise_daily = state_wise_daily.pivot_table(index=['Date', 'State'], columns=['Status'], values='Count').reset_index()

# map state names to state codes
state_codes = {code:state for code, state in zip(latest['State_code'], latest['State'])}
state_codes['DD'] = 'Daman and Diu'
state_wise_daily['State_Name'] = state_wise_daily['State'].map(state_codes)

# save as a .csv file
state_wise_daily.to_csv('state_level_daily.csv')

# first few rows
state_wise_daily.head()

# read data
district_wise = pd.read_csv('https://api.covid19india.org/csv/latest/district_wise.csv')

district_wise = district_wise[district_wise.District != 'Unassigned']
district_wise = district_wise[district_wise.District != 'Foreign Evacuees']
district_wise = district_wise[district_wise.District != 'Others']
district_wise = district_wise[district_wise.District != 'Other State']
district_wise = district_wise[district_wise.District != 'Airport Quarantine']
district_wise = district_wise[district_wise.District != 'Italians']
district_wise = district_wise[district_wise.District != 'CAPF Personnel']
district_wise = district_wise[district_wise.District != 'State Pool']
district_wise = district_wise[district_wise.District != 'BSF Camp']
district_wise = district_wise[district_wise.District != 'Unknown']
district_wise = district_wise[district_wise.District != 'Other Region']
district_wise = district_wise[district_wise.District != 'Evacuees']
district_wise = district_wise[district_wise.District != 'Railway Quarantine']
                   

# save as .csv file
district_wise.to_csv('district_level_latest.csv', index=False)

# first few rows
district_wise.head()
# read data
tests_day_wise = pd.read_csv('https://api.covid19india.org/csv/latest/tested_numbers_icmr_data.csv')

# save as .csv file
tests_day_wise.to_csv('tests_day_wise.csv', index=False)

# first few rows
tests_day_wise.head()

# read data
tests_state_wise = pd.read_csv('https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv')

# save as .csv file
tests_state_wise.to_csv('tests_state_wise.csv', index=False)

# first few rows
tests_state_wise.head(3)