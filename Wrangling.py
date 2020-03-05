import pandas as pd
import numpy as np
import requests
import os
import zipfile
import shutil

########################## START: Data Gathering ###############################

address = 'https://s3.amazonaws.com/baywheels-data/202001-baywheels-tripdata.csv.zip'
fileName = '202001-baywheels-tripdata.csv.zip'
def downloadFile(address, fileName):
    r = requests.get(address)
    with open(os.path.join(fileName), mode='wb') as file:
        file.write(r.content)
    with zipfile.ZipFile(fileName, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())

addresses = ['https://s3.amazonaws.com/baywheels-data/201901-fordgobike-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201902-fordgobike-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201903-fordgobike-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201904-fordgobike-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201905-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201906-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201907-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201908-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201909-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201910-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201911-baywheels-tripdata.csv.zip',
'https://s3.amazonaws.com/baywheels-data/201912-baywheels-tripdata.csv.zip']

fileNames = []
for s in addresses:
    fileNames.append(s[s.rfind('/')+1:])

def downloadAllFiles():
    for f, n in zip(addresses,fileNames):
        downloadFile(f,n)


csv = []
def mergeAllFiles():
   
   #Get csv file names
    for f in fileNames:
        csv.append(f[:len(f)-4])

    df_all = []
    l = 0
    #Merge files
    for c in csv:
        df = pd.read_csv(c, low_memory=False)
        l += len(df)
        df_all.append(df)

    df_all = pd.concat(df_all, ignore_index=True, sort=False)

    if os.path.isfile('All.csv'):
        os.remove('All.csv')
    df_all.to_csv('All.csv')

    #Remove downloaded files
    for f in fileNames:
            os.remove(f)
            os.remove(f[:len(f)-4])
    if os.path.exists('__MACOSX'):
        shutil.rmtree('__MACOSX')

########################## END: Data Gathering ###############################

########################## START: DATA ASSESSMENT ############################

# Data issues that needs to be fixed 
# Quality issues:
# 1. Station id type id float.
# 2. There are some locations with latitude and longitude equal to zero.
# 3. Station name and station id columns have many NaN values (less tha 4% of the data).
# 4. 95% values for rental_access_method is NaN
# 5. Start and end date of the trip is string.

# Tidyness issues:
# 1. Data of stations and trips are stored in the same table.

########################## END: DATA ASSESSMENT ##############################

########################## START: DATA CLEANING ##############################

def clean():
    # Read the data
    df = pd.read_csv('All.csv', index_col=0, low_memory=False)

    # 1. Define: Remove all the trips without a station Id
    # code
    df = df[(~df['start_station_id'].isna()) & (~df['end_station_id'].isna())]

    # test
    #df[(df['start_station_id'].isna())].shape
    #df[(df['end_station_id'].isna())].shape

    # 2. Remove rental_access_method column (as 96% of the column is null and we won't use it we can remove it)
    # code
    df.drop('rental_access_method', inplace=True, axis=1)
    #Test 
    #df.info()

    # 3. Remove all the locations with latitude and longitude equal of zero. (When bikes have error on reporting the location they retuen zero)
    # code
    df = df[(df['start_station_latitude'] != 0) & (df['start_station_longitude'] != 0) & (df['end_station_latitude'] != 0) & (df['end_station_longitude'] != 0)]

    # test
    #df[(df['start_station_latitude'] == 0) | (df['start_station_longitude'] == 0) | (df['end_station_latitude'] == 0) | (df['end_station_longitude'] == 0)].shape[0]

    # 4. Conver Station_id to int
    # Code
    df['start_station_id'] = df['start_station_id'].astype(int)
    df['end_station_id'] = df['end_station_id'].astype(int)

    # test
    #df.info()

    # 5. Conver dates from string to datetime
    # Code
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    # test
    #df.info()

    # 6. Devide the stations and trips data

    # Code: Seperate station data
    start_stations = df.groupby(['start_station_id','start_station_latitude','start_station_longitude','start_station_name' ]).size().reset_index()
    end_stations = df.groupby(['end_station_id','end_station_latitude','end_station_longitude','end_station_name']).size().reset_index()

    start_stations.drop(0, axis=1, inplace = True)
    start_stations.columns = ['station_id','latitude','longitude','name']
    end_stations.drop(0, axis=1, inplace = True)
    end_stations.columns = ['station_id','latitude','longitude','name']

    stations = start_stations.append(end_stations)
    stations.drop_duplicates(['station_id','latitude','longitude'], keep='first', inplace=True)

    stations.to_csv('stations.csv')

    # Remove station details from trip data
    df = df[['duration_sec', 'start_time', 'end_time', 'start_station_id','end_station_id', 'bike_id','user_type', 'bike_share_for_all_trip']]
    df.drop_duplicates(['duration_sec', 'start_time', 'end_time', 'start_station_id','end_station_id', 'bike_id','user_type', 'bike_share_for_all_trip'], keep='first', inplace=True)
    df.to_csv('trips.csv')

    if os.path.isfile('All.csv'):
        os.remove('All.csv')

########################## END: DATA CLEANING ##############################



