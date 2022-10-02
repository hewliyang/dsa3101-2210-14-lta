import os
import re
import pandas as pd
import datetime
import json
import requests
import urllib.request
from dotenv import load_dotenv

env_loc = os.path.abspath(os.path.join(os.getcwd(), '..'))
load_dotenv(os.path.join(env_loc, '.env'))

KEY = os.getenv('PROJECT_API_KEY')
PATHS = ["ltaodataservice/Traffic-Imagesv2", "ltaodataservice/TrafficSpeedBandsv2", "ltaodataservice/TrafficIncidents"]

def get_json(key, path):
    url = "http://datamall2.mytransport.sg/"
    path = path
    headers = {'AccountKey': key,
        'accept': 'application/json'}
    response = requests.get(url + path, headers=headers)
    return json.loads(response.text)

def to_date(date):
    date = re.split('\/|\:|\(|\)', date)
    return datetime.datetime(2022, int(date[2]), 
        int(date[1]), int(date[3]), int(date[4]))

def cam_attributes():
    cameraIDs = []
    latitudes = []
    longitudes = []
    imageLinks = []
    response = get_json(KEY, PATHS[0])
    
    if 'value' not in response:
        raise Exception("Error: Cannot find value key in json response")
    
    for camera in response['value']:
        latitudes.append(camera['Latitude'])
        longitudes.append(camera['Longitude'])
        cameraIDs.append(camera['CameraID'])
        imageLinks.append(camera['ImageLink'])
    
    dataframe = pd.DataFrame({
        'CameraID': cameraIDs,
        'Latitude': latitudes,
        'Longitude': longitudes,
        'Image Link': imageLinks})
    
    return dataframe

def speed_attributes():
    linkIDs = []
    roadNames = []
    roadCats = []
    speedBands = []
    minSpeeds = []
    maxSpeeds = []
    latStart, latEnd, longStart, longEnd = [], [], [], []
    response = get_json(KEY, PATHS[1])

    if 'value' not in response:
        raise Exception("Error: Cannot find value key in json response")
    
    for speed in response['value']:
        linkIDs.append(speed['LinkID'])
        roadNames.append(speed['RoadName'])
        roadCats.append(speed['RoadCategory'])
        speedBands.append(speed['SpeedBand'])
        minSpeeds.append(speed['MinimumSpeed'])
        maxSpeeds.append(speed['MaximumSpeed'])
        latStart.append(speed['Location'].split(" ")[0])
        latEnd.append(speed['Location'].split(" ")[2])
        longStart.append(speed['Location'].split(" ")[1])
        longEnd.append(speed['Location'].split(" ")[3])
    
    dataframe = pd.DataFrame({
        'LinkID': linkIDs,
        'Road Names': roadNames,
        'Road Categories': roadCats,
        'Speed Bands': speedBands,
        'Min Speed': minSpeeds,
        'Max Speed': maxSpeeds,
        'Lat Start': latStart,
        'Lat End': latEnd,
        'Long Start': longStart,
        'Long End': longEnd})
    
    return dataframe

def traffic_attributes():
    types = []
    latitudes = []
    longitudes = []
    times = []
    messages = []
    response = get_json(KEY, PATHS[2])

    if 'value' not in response:
        raise Exception("Error: Cannot find value key in json response")
    
    for incident in response['value']:
        types.append(incident['Type'])
        latitudes.append(incident['Latitude'])
        longitudes.append(incident['Longitude'])
        times.append(to_date(incident['Message'][0:11]))
        messages.append(incident['Message'][11:])
    
    dataframe = pd.DataFrame({
        'Type': types,
        'Latitude': latitudes,
        'Longitude': longitudes,
        'Time': times,
        'Message': messages})
    return dataframe

def download(dataframe, folder):
    for i in range(len(dataframe)):
        urllib.request.urlretrieve(
            dataframe['Image Link'].values[i],
            os.path.join(folder, str(dataframe['CameraID'].values[i])+'.jpg')
        )
    return None

if __name__ == "__main__":
    download(cam_attributes(), "images")
    speed_attributes().to_csv("data/speed.csv")
    traffic_attributes().to_csv("data/incidents.csv")