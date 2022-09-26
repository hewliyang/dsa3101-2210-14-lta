import os
import pandas as pd
import json
import requests
import urllib.request
from dotenv import load_dotenv

env_loc = os.path.abspath(os.path.join(os.getcwd(), '..'))
load_dotenv(os.path.join(env_loc, '.env'))

KEY = os.getenv('PROJECT_API_KEY')

def get_json(key):
    url = "http://datamall2.mytransport.sg/"
    path = "ltaodataservice/TrafficSpeedBandsv2"
    headers = {'AccountKey': key,
        'accept': 'application/json'}
    response = requests.get(url + path, headers=headers)
    return json.loads(response.text)

def get_attributes(response):
    linkIDs = []
    roadNames = []
    roadCats = []
    speedBands = []
    minSpeeds = []
    maxSpeeds = []
    latStart, latEnd, longStart, longEnd = [], [], [], []

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

if __name__ == "__main__":
    get_attributes(get_json(KEY)).to_csv("data/speed.csv")