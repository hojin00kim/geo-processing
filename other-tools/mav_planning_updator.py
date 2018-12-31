"""
This is very crude tool to help image acquisition planning .

Read master spreadsheet and update six different csv files for planning weekly aerial acquisition
"""
import datetime
import os

import csv
import numpy as np
import pandas as pd


# set input directory
filedir = "/Users/hojin.kim/update"
os.chdir(filedir)

# open data files
master_file = 'maxter_file.xlsx'
t1_file = 'Base Polygons - 20170825.csv'
t2_file = 'Base  - 20170825.csv'
t3_file = 'Code 1 - 20170825.csv'
t4_file = 'Code 2 Field Boundaries - 20170825.csv'
t5_file = 'Code 6 - 20170825.csv'
t6_file = 'ILCU - 20170825.csv'

# read excel and csv file and convert it to pandas dataframe
master_df = pd.ExcelFile(master_file).parse('2017 Imaging Projections')

t1_df = pd.read_csv(t1_file)
t2_df = pd.read_csv(t2_file)
t3_df = pd.read_csv(t3_file)
t4_df = pd.read_csv(t4_file)
t5_df = pd.read_csv(t5_file)
t6_df = pd.read_csv(t6_file)

# clean out "Planned" before updating
t1_df = t1_df.replace('Planned', ' ')
t2_df = t2_df.replace('Planned', ' ')
t3_df = t3_df.replace('Planned', ' ')
t4_df = t4_df.replace('Planned', ' ')
t5_df = t5_df.replace('Planned', ' ')
t6_df = t6_df.replace('Planned', ' ')


master_df = master_df[(master_df['Platform'] == '')]
# master_df = master_df[(master_df['Platform'] == ')') & (master_df['Start'] > today)]
# master_df = master_df[(master_df['Platform'] == '') | (master_df['Platform'] == 'Mav (G)') & (master_df['Start'] > today)]

# read "Task Name column/parse/obtain Site_ID
prefix = master_df['Task Name'].str.split(':', 1).str[0]
master_df['Site_ID'] = prefix.str.split('/').str[-1]

# define whether the task is either 'planned' or 'On-demand'
master_df['Task'] = master_df['Task Name'].str.split(':', 1).str[1]
#master_df.loc[master_df['Task'].str.contains('On-Demand', na=False), 'Task'] = 'On-Demand'
master_df.loc[~(master_df['Task'].str.contains('On-Demand', na=False)), 'Task'] = 'Planned'

# define "week of" values
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-05-07", "2017-05-13"))), 'WeekOf'] = 'WkOf07May'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-05-14", "2017-05-20"))), 'WeekOf'] = 'WkOf14May'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-05-21", "2017-05-27"))), 'WeekOf'] = 'WkOf21May'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-05-28", "2017-06-03"))), 'WeekOf'] = 'WkOf28May'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-06-04", "2017-06-10"))), 'WeekOf'] = 'WkOf04Jun'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-06-11", "2017-06-17"))), 'WeekOf'] = 'WkOf11Jun'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-06-18", "2017-06-24"))), 'WeekOf'] = 'WkOf18Jun'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-06-25", "2017-07-01"))), 'WeekOf'] = 'WkOf25Jun'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-07-02", "2017-07-08"))), 'WeekOf'] = 'WkOf02Jul'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-07-09", "2017-07-15"))), 'WeekOf'] = 'WkOf09Jul'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-07-16", "2017-07-22"))), 'WeekOf'] = 'WkOf16Jul'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-07-23", "2017-07-29"))), 'WeekOf'] = 'WkOf23Jul'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-07-30", "2017-08-05"))), 'WeekOf'] = 'WkOf30Jul'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-08-06", "2017-08-12"))), 'WeekOf'] = 'WkOf06Aug'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-08-13", "2017-08-19"))), 'WeekOf'] = 'WkOf13Aug'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-08-20", "2017-08-26"))), 'WeekOf'] = 'WkOf20Aug'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-08-27", "2017-09-02"))), 'WeekOf'] = 'WkOf27Aug'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-09-03", "2017-09-09"))), 'WeekOf'] = 'WkOf03Sep'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-09-10", "2017-09-16"))), 'WeekOf'] = 'WkOf10Sep'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-09-17", "2017-09-23"))), 'WeekOf'] = 'WkOf17Sep'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-09-24", "2017-09-30"))), 'WeekOf'] = 'WkOf24Sep'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-10-01", "2017-10-07"))), 'WeekOf'] = 'WkOf01Oct'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-10-08", "2017-10-14"))), 'WeekOf'] = 'WkOf08Oct'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-10-15", "2017-10-21"))), 'WeekOf'] = 'WkOf15Oct'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-10-23", "2017-10-28"))), 'WeekOf'] = 'WkOf23Oct'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-10-29", "2017-11-04"))), 'WeekOf'] = 'WkOf04Nov'
master_df.loc[(master_df["Start"].isin(pd.date_range("2017-12-31", "2018-01-06"))), 'WeekOf'] = 'WkOf31Dec'

#for row in master_df.itertuples(): # little fast
for index, row in master_df.iterrows():

    # check if it returns all rows
    #print row.Site_ID, row.TaskName, row.WeekOf, row.Task
    #print type(row.Site_ID)

    # update cell values of the target dataframe
    t1_df.loc[t1_df['Site_ID'] == row.Site_ID, row.WeekOf] = row.Task
    t2_df.loc[t2_df['Site_ID'] == row.Site_ID, row.WeekOf] = row.Task
    t3_df.loc[t3_df['Site_ID'] == row.Site_ID, row.WeekOf] = row.Task
    t4_df.loc[t4_df['Site_ID'] == row.Site_ID, row.WeekOf] = row.Task
    t5_df.loc[t5_df['Site_ID'] == row.Site_ID, row.WeekOf] = row.Task
    t6_df.loc[t6_df['Site_ID'] == row.Site_ID, row.WeekOf] = row.Task

# obtaion column names to check the updated dataframe contains correct information
t1_df_colnames = list(t1_df.columns.values)
print t1_df_colnames

# drop the last column
t1_df = t1_df.iloc[:, :-1]
t2_df = t2_df.iloc[:, :-1]
t3_df = t3_df.iloc[:, :-1]
t4_df = t4_df.iloc[:, :-1]
t5_df = t5_df.iloc[:, :-1]
t6_df = t6_df.iloc[:, :-1]


# save it to a csv file
# output name for Base_Corn_Polygons
t1 = t1_file.split('.')[0]
t1_pre = ''.join([i for i in t1 if not i.isdigit()])

# output name for Base_Soybean
t2 = t2_file.split('.')[0]
t2_pre = ''.join([i for i in t2 if not i.isdigit()])

# output name for Code6
t3_pre = t3_file.split('.')[0][:9]

# output name for Base_Soybean
t4_pre = t4_file.split('.')[0][:-8]

t5_pre = t5_file.split('.')[0][:9]

# output name for Base_Soybean
t6 = t6_file.split('.')[0]
t6_pre = ''.join([i for i in t6 if not i.isdigit()])

# update master dataframe based on today's date
d = datetime.date.today()
today = str(d.year) + str('{:02d}'.format(d.month)) + str('{:02d}'.format(d.day))

t1_df.to_csv(t1_pre + today + '.csv', index = False)
t2_df.to_csv(t2_pre + today + '.csv', index = False)
t3_df.to_csv(t3_pre + today + '.csv', index = False)
t4_df.to_csv(t4_pre + today + '.csv', index = False)
t5_df.to_csv(t5_pre + today + '.csv', index = False)
t6_df.to_csv(t6_pre + today + '.csv', index = False)
