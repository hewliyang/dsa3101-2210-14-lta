import requests
import pandas as pd
from geopy import distance
import datetime
import re
from dotenv import load_dotenv
import os
import urllib

env_loc = os.path.abspath(os.path.join(os.getcwd(), '..'))
load_dotenv(os.path.join(env_loc, '.env'))

API_KEY = os.getenv('PROJECT_API_KEY')

lta_url = "http://datamall2.mytransport.sg/ltaodataservice"
lta_images = lta_url + "/Traffic-Imagesv2"
lta_incidents = lta_url + "/TrafficIncidents"
lta_speedbands = lta_url + "/TrafficSpeedBandsv2"
header = {'AccountKey':API_KEY, 'accept':'application/json'}

# HELPER FUNCTIONS

# calculates the geodesic distance between two points in kilometers (km)
def get_distance(lat1, long1, lat2, long2):
    return distance.distance((lat1, long1), (lat2, long2)).km

def get_datetime(message):
    s = re.search(r"\(\d+\/\d+\)\d+\:\d+", message).group()
    dt = datetime.datetime.strptime(s, "(%d/%m)%H:%M")
    dt = dt.replace(year=datetime.date.today().year)
    return dt

def get_message(message):
    s = re.split(r"\(\d+\/\d+\)\d+\:\d+", message)
    return s[1]

# function to download images, named by the camera id
def download_images(dataframe, folder):
    for i in range(len(dataframe)):
        urllib.request.urlretrieve(
            dataframe['ImageLink'].values[i],
            os.path.join(folder, str(dataframe['CameraID'].values[i])+'.jpg')
        )
    return None

# functions to retrieve data from LTA API

def retrieve(endpoint, header):
    req_out = requests.get(endpoint, headers=header)
    if req_out.status_code != 200:
        raise Exception("API Key not setup properly OR LTA API Service is offline")
    return req_out.json()["value"]

def retrieve_images():
    df = pd.DataFrame(retrieve(lta_images, header))
    df["timestamp"] = datetime.datetime.now().replace(microsecond=0,second=0)
    return df
    
# returns a DataFrame with the distance of the respective stretch of road
def retrieve_speedbands():
    df = pd.DataFrame(retrieve(lta_speedbands, header))
    df[['latitude1', 'longitude1', 'latitude2', 'longitude2']] = df['Location'].str.split(' ', expand = True)
    df = df.drop('Location', axis=1)
    df["distance"] = df.apply(lambda x: get_distance(x['latitude1'],x['longitude1'],x['latitude2'],x['longitude2']), axis = 1)
    df["timestamp"] = datetime.datetime.now().replace(microsecond=0, second=0)
    return df

# can do some regex here
def retrieve_incidents():
    df = pd.DataFrame(retrieve(lta_incidents, header))
    df["timestamp"] = df.apply(lambda x: get_datetime(x["Message"]), axis = 1)
    df["Message"] = df.apply(lambda x: get_message(x["Message"]), axis = 1)
    return df

if __name__ == "__main__":
    retrieve_speedbands().to_csv("data/speedbands.csv")
    retrieve_incidents().to_csv("data/incidents.csv")
    download_images(retrieve_images(), "images")
