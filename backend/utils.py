import requests
import pandas as pd
from geopy import distance
import datetime
import re
from dotenv import load_dotenv
import os
import urllib
from find_density import find_density, normaliseDensity, find_density_with_link
import deta
from deta import Deta
import json

load_dotenv()

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

def avg_distance(start, end, loc):
    return (distance.distance(start, loc).km + distance.distance(end, loc).km)/2

def find_closest(cam, speed):
    closest_dist = []
    closest = []
    for i in range(len(speed.LinkID)):
        minDist = 1000
        minLoc = 0
        for j in range(len(cam.Latitude)):
            start = (speed["Lat Start"][i], speed["Long Start"][i])
            end = (speed["Lat End"][i], speed["Long End"][i])
            loc = (cam["Latitude"][j], cam["Longitude"][j])
            dist = avg_distance(start, end, loc)
            if (dist < minDist):
                minDist = dist
                minLoc = j
        closest_dist.append(minDist * 1000)
        closest.append(cam["CameraID"][minLoc])

    s2 = speed.copy()
    s2["Closest Cam"] = closest
    s2["dist (m)"] = closest_dist
    return s2

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

# retrieiving historical data from DB
def fetch_all_from_deta(db: deta.Base, id: int):
    res = db.fetch({'id':id})
    all_items = res.items

    while res.last:
        res = db.fetch({'id':id}, last=res.last)
        all_items += res.items

    return all_items

# convert unix time (int) to string
def convert_time(ts: int):
    ts = ts/1000 + 28800
    return(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S'))

# process data retrieved from DB for easy plotting on client-side
def proc_data(data: dict) -> pd.DataFrame:
    li = [json.loads(d["value"])[0] for d in data]
    df = pd.DataFrame(li)
    df["timestamp"] = df.apply(lambda x: convert_time(x["timestamp"]), axis = 1)
    return df.sort_values(by="timestamp").reset_index(drop=True)

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

# returns a DataFrame of one row concerning the specified cameraID and its traffic density
def retrieve_density(cameraID, detector):
    img_data = retrieve_images()
    # filter for the specified camera
    img_data = img_data[img_data['CameraID']==str(cameraID)]
    # extract the img download link
    d1, d2 = find_density(img_data, cameraID, detector)
    img_data = img_data.assign(density1=[d1], density2=[d2])
    return img_data

def retrieve_density_normalised(cameraID, detector):
    img_data = retrieve_images()
    # filter for the specified camera
    img_data = img_data[img_data['CameraID']==str(cameraID)]
    # extract the img download link
    d1, d2 = find_density(img_data, cameraID, detector)
    img_data = img_data.assign(density1=[normaliseDensity(d1)], density2=[normaliseDensity(d2)])
    return img_data

def retrieve_density_both(cameraID, detector):
    img_data = retrieve_images()
    # filter for the specified camera
    img_data = img_data[img_data['CameraID']==str(cameraID)]
    # extract the img download link
    d1, d2 = find_density(img_data, cameraID, detector)
    img_data = img_data.assign(density1=[d1], density2=[d2], prob1=[normaliseDensity(d1)], prob2=[normaliseDensity(d2)])
    return img_data

# add batch predict function for density
def batch_retrieve_dense_prob(detector):
    img_data = retrieve_images()
    
    dense_arr1 = []
    dense_arr2 = []
    prob_arr1 = []
    prob_arr2 = []

    for camID, img_link in zip(img_data.CameraID, img_data.ImageLink):
        d1, d2 = find_density_with_link(img_link, camID, detector)
        dense_arr1.append(d1)
        dense_arr2.append(d2)
        prob_arr1.append(normaliseDensity(d1))
        prob_arr2.append(normaliseDensity(d2))
    
    img_data = img_data.assign(density1=dense_arr1, density2=dense_arr2, prob1=prob_arr1, prob2=prob_arr2)
    return img_data


if __name__ == "__main__":
    retrieve_images().to_csv("data/images.csv")
    retrieve_speedbands().to_csv("data/speedbands.csv")
    retrieve_incidents().to_csv("data/incidents.csv")
    download_images(retrieve_images(), "images")
