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

def get_json(key):
    url = "http://datamall2.mytransport.sg/"
    path = "ltaodataservice/TrafficIncidents"
    headers = {'AccountKey': key,
        'accept': 'application/json'}
    response = requests.get(url + path, headers=headers)
    return json.loads(response.text)

def to_date(date):
    date = re.split('\/|\:|\(|\)', date)
    return datetime.datetime(2022, int(date[2]), 
        int(date[1]), int(date[3]), int(date[4]))



def get_attributes(response):
    types = []
    latitudes = []
    longitudes = []
    times = []
    messages = []

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

if __name__ == "__main__":
    get_attributes(get_json(KEY)).to_csv("data/incidents.csv")