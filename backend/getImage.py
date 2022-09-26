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
    path = "ltaodataservice/Traffic-Imagesv2"
    headers = {'AccountKey': key,
        'accept': 'application/json'}
    response = requests.get(url + path, headers=headers)
    return json.loads(response.text)

def get_attributes(response):
    cameraIDs = []
    latitudes = []
    longitudes = []
    imageLinks = []
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

def download(dataframe, folder):
    for i in range(len(dataframe)):
        urllib.request.urlretrieve(
            dataframe['Image Link'].values[i],
            os.path.join(folder, str(dataframe['CameraID'].values[i])+'.jpg')
        )
    return None

if __name__ == "__main__":
    download(get_attributes(get_json(KEY)), "images")