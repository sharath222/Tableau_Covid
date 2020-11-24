# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 13:04:40 2020

@author: narayana-pc
"""


# import libraries
# ================

# for date and time opeations
from datetime import datetime
# for file and folder operations
import os
# for regular expression opeations
import re
# for listing files in a folder
import glob
# for getting web contents
import requests 
# storing and analysing data
import pandas as pd
# for scraping web contents
from bs4 import BeautifulSoup
# regular expression
import re
# for numerical analysis
import numpy as np
# get data
# ========

# link at which web data recides
link = 'https://www.mohfw.gov.in/'
# get web data
req = requests.get(link)
# parse web data
soup = BeautifulSoup(req.content, "html.parser")
print(soup)
# find the table
# ==============
# our target table is the last table in the page

# get the table head
# table head may contain the column names, titles, subtitles
thead = soup.find_all('thead')[-1]
print(thead)

# get all the rows in table head
# it usually have only one row, which has the column names
head = thead.find_all('tr')
print(head)

# get the table tbody
# it contains the contents
tbody = soup.find_all('tbody')[-1]
print(tbody)

# get all the rows in table body
# each row is each state's entry
body = tbody.find_all('tr')
print(body)
# get the table contents
# ======================

# container for header rows / column title
head_rows = []
# container for table body / contents
body_rows = []

# loop through the head and append each row to head
for tr in head:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    head_rows.append(row)
# print(head_rows)

# loop through the body and append each row to body
for tr in body:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    body_rows.append(row)
# print(head_rows)
    
# save contents in a dataframe
# ============================
    
# skip last 3 rows, it contains unwanted info
# head_rows contains column title
df_bs = pd.DataFrame(body_rows[:len(body_rows)-6], 
                     columns=head_rows[0])         

# Drop 'S. No.' column
df_bs.drop('S. No.', axis=1, inplace=True)

# there are 36 states+UT in India
df_bs.head(36)

# date-time information
# =====================

# today's date
now  = datetime.now()
# format date to month-day-year
df_bs['Date'] = now.strftime("%m/%d/%Y") 

# add 'Date' column to dataframe
df_bs['Date'] = pd.to_datetime(df_bs['Date'], format='%m/%d/%Y')

# df_bs.head(36)

# remove extra characters from 'Name of State/UT' column
df_bs['Name of State / UT'] = df_bs['Name of State / UT'].str.replace('#', '')

# latitude and longitude information
# ==================================

# latitude of the states
lat = {'Delhi':28.7041, 'Haryana':29.0588, 'Kerala':10.8505, 'Rajasthan':27.0238,
       'Telengana':18.1124, 'Telangana':18.1124, 'Uttar Pradesh':26.8467, 'Ladakh':34.2996, 'Tamil Nadu':11.1271,
       'Jammu and Kashmir':33.7782, 'Punjab':31.1471, 'Karnataka':15.3173, 'Maharashtra':19.7515,
       'Andhra Pradesh':15.9129, 'Odisha':20.9517, 'Uttarakhand':30.0668, 'West Bengal':22.9868, 
       'Puducherry': 11.9416, 'Chandigarh': 30.7333, 'Chhattisgarh':21.2787, 'Gujarat': 22.2587, 
       'Himachal Pradesh': 31.1048, 'Madhya Pradesh': 22.9734, 'Bihar': 25.0961, 'Manipur':24.6637, 
       'Mizoram':23.1645, 'Goa': 15.2993, 'Andaman and Nicobar Islands': 11.7401, 'Assam' : 26.2006, 
       'Jharkhand': 23.6102, 'Arunachal Pradesh': 28.2180, 'Tripura': 23.9408, 'Nagaland': 26.1584, 
       'Meghalaya' : 25.4670, 'Dadar Nagar Haveli' : 20.1809, 'Sikkim':27.5330, 
       'Dadra and Nagar Haveli and Daman and Diu': 20.1809}

# longitude of the states
long = {'Delhi':77.1025, 'Haryana':76.0856, 'Kerala':76.2711, 'Rajasthan':74.2179,
        'Telengana':79.0193, 'Telangana':79.0193, 'Uttar Pradesh':80.9462, 'Ladakh':78.2932, 'Tamil Nadu':78.6569,
        'Jammu and Kashmir':76.5762, 'Punjab':75.3412, 'Karnataka':75.7139, 'Maharashtra':75.7139,
        'Andhra Pradesh':79.7400, 'Odisha':85.0985, 'Uttarakhand':79.0193, 'West Bengal':87.8550, 
        'Puducherry': 79.8083, 'Chandigarh': 76.7794, 'Chhattisgarh':81.8661, 'Gujarat': 71.1924, 
        'Himachal Pradesh': 77.1734, 'Madhya Pradesh': 78.6569, 'Bihar': 85.3131, 'Manipur':93.9063, 
        'Mizoram':92.9376, 'Goa': 74.1240, 'Andaman and Nicobar Islands': 92.6586, 'Assam' : 92.9376, 
        'Jharkhand': 85.2799, 'Arunachal Pradesh': 94.7278, 'Tripura': 91.9882, 'Nagaland': 94.5624,
        'Meghalaya' : 91.3662, 'Dadar Nagar Haveli' : 73.0169, 'Sikkim':88.5122,
        'Dadra and Nagar Haveli and Daman and Diu': 73.0169}

# add latitude column based on 'Name of State / UT' column
df_bs['Latitude'] = df_bs['Name of State / UT'].map(lat)

# add longitude column based on 'Name of State / UT' column
df_bs['Longitude'] = df_bs['Name of State / UT'].map(long)

# df_bs.head(36)
# unique state names
df_bs['Name of State / UT'].unique()

# number of missing values 
df_bs.isna().sum()
# number of unique values 
df_bs.nunique()
# saving data
# ===========

# file names as year-month-day.csv format
file_name = now.strftime("%Y_%m_%d")+'.csv'

# location for saving the file
file_loc = 'D:\\Capgemini\\Tableau_covid\\'

# save file as a scv file
df_bs.to_csv(file_loc + file_name, index=False)

df_bs.head(36)
# column names 
# df_bs.columns
# list of all files available
# ! ls C:\Users\imdevskp\Documents\github\covid_india\.day_by_day_data
# location of the file
loc = "D:\\Capgemini\\Tableau_covid\\"

# list of all files
files = glob.glob(loc+'2020*.csv')
   
# container for each day's data's dataframe
dfs = []

# loop through the files and append to the dfs list
for i in files:
    # read data
    df_temp = pd.read_csv(i)
    
    # rename columns
    
    try:
        df_temp = df_temp.drop(['Total Confirmed cases (Indian National)', 
                                'Total Confirmed cases ( Foreign National )'], axis=1)
    except:
        pass
        
    d = {'^Cured.*': 'Cured/Discharged/Migrated', 
         'Total Confirmed cases.*': 'Total Confirmed cases', 
         'Death.*': 'Death'}
    
    df_temp.columns = df_temp.columns.to_series().replace(d, regex=True)


#     df_temp = df_temp.rename(columns={'Cured':'Cured/Discharged'})
#     df_temp = df_temp.rename(columns={'Cured/Discharged':'Cured/Discharged/Migrated', 
#                                       'Total Confirmed cases *': 'Total Confirmed cases', 
#                                       'Total Confirmed cases ': 'Total Confirmed cases', 
#                                       'Total Confirmed cases* ': 'Total Confirmed cases'})
#     df_temp = df_temp.rename(columns=lambda x: re.sub('Total Confirmed cases \(Including .* foreign Nationals\) ',
#                                                       'Total Confirmed cases',x))
#     df_temp = df_temp.rename(columns=lambda x: re.sub("Death.*", "Death", x))

    
    # append to the df_s
    dfs.append(df_temp)
    
# print(dfs)

# concat dataframes
complete_data = pd.concat(dfs, ignore_index=True).sort_values(['Date'], ascending=True).reset_index(drop=True)

# get just numbers
complete_data['Death'] = complete_data['Death'].astype('str').str.extract('(\d+)').astype('int')

# few sample rows
complete_data.sample(10)
# fix datatype
complete_data['Date'] = pd.to_datetime(complete_data['Date'])

# sort rows
complete_data = complete_data.sort_values(['Date', 'Name of State / UT']).reset_index(drop=True)

# fill missing values with 0
cols = ['Cured/Discharged/Migrated', 'Death']
complete_data[cols] = complete_data[cols].fillna(0).astype('int')
# rename state/UT names
complete_data['Name of State / UT'].replace('Chattisgarh', 'Chhattisgarh', inplace=True)
complete_data['Name of State / UT'].replace('Pondicherry', 'Puducherry', inplace=True) 
# select only rows with more than 1 case
complete_data = complete_data[complete_data['Total Confirmed cases']>0]
# drop extra columns
complete_data = complete_data.drop(['Active Cases*'], axis=1)
# rearrange columns
complete_data = complete_data[['Date', 'Name of State / UT', 'Latitude', 'Longitude', 
                               'Total Confirmed cases', 'Death', 'Cured/Discharged/Migrated']]
# rename state names
complete_data['Name of State / UT'] = complete_data['Name of State / UT'].replace('Dadar Nagar Haveli', 'Dadra and Nagar Haveli and Daman and Diu')
complete_data['Name of State / UT'] = complete_data['Name of State / UT'].replace('Daman & Diu', 'Dadra and Nagar Haveli and Daman and Diu')
# New cases
# =========

# temp dataset
temp = complete_data.groupby(['Name of State / UT', 'Date', ])['Total Confirmed cases', 'Death', 'Cured/Discharged/Migrated']
temp = temp.sum().diff().reset_index()

mask = temp['Name of State / UT'] != temp['Name of State / UT'].shift(1)

temp.loc[mask, 'Total Confirmed cases'] = np.nan
temp.loc[mask, 'Death'] = np.nan
temp.loc[mask, 'Cured/Discharged/Migrated'] = np.nan

temp = temp[['Date', 'Name of State / UT', 'Total Confirmed cases', 'Death', 'Cured/Discharged/Migrated']]
temp.columns = ['Date', 'Name of State / UT', 'New cases', 'New deaths', 'New recovered']

# merging new values
complete_data = pd.merge(complete_data, temp, on=['Name of State / UT', 'Date'])

# filling na with 0
complete_data = complete_data.fillna(0)

# fixing data types
cols = ['New cases', 'New deaths', 'New recovered']
complete_data[cols] = complete_data[cols].astype('int')

# remove negative values
complete_data['New cases'] = complete_data['New cases'].apply(lambda x: 0 if x<0 else x)

# final data
complete_data.head()
# random rows
complete_data.sample(3)
# complete data info
complete_data.info()
# save data in a csv file
complete_data.to_csv('complete.csv', index=False)
# complete_data.groupby('Date').count()
# complete_data.sort_values('Death', ascending=False)
complete_data[complete_data['Date']==max(complete_data['Date'])]