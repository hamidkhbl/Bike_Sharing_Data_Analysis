import pandas as pd
import numpy as np
import requests
import os
import zipfile

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

########################## END: Data Gathering ###############################



