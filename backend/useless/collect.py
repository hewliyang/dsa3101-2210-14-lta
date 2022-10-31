import requests
import pandas as pd
from geopy import distance
import datetime
import re
from dotenv import load_dotenv
import os
import urllib
from find_density import find_density
from utils import retrieve_speedbands
from utils import retrieve_images
from flow import flow1
from flow import flow2
from utils import retrieve_images

# returns a DataFrame of one row concerning the specified cameraID and its traffic density
def retrieve_density(cameraID):
    img_data = retrieve_images()
    # filter for the specified camera
    img_data = img_data[img_data['CameraID']==str(cameraID)]
    # extract the img download link
    d1, d2 = find_density(img_data, cameraID)
    img_data = img_data.assign(density1=[d1], density2=[d2])
    return img_data

print(retrieve_density(6708))
print(retrieve_density(6710))

def find_speedband(df):
    minspeed6708 = df[df['LinkID'] == str(103000078)]['MinimumSpeed'].astype(str).astype(int).values/12
    minspeed6710 = df[df['LinkID'] == str(103000080)]['MinimumSpeed'].astype(str).astype(int).values/12
    print(minspeed6708, minspeed6710)
    return [minspeed6708, minspeed6710]



def proportion(df):
    if flow1(df)[0][0] != 0:
        p108 = flow2(df)[0][0]/flow1(df)[0][0]
    else:
        p108 = 0
    if flow1(df)[0][1] != 0:
        p110 = flow2(df)[0][1]/flow1(df)[0][1]
    else:
        p110 = 0
    if flow1(df)[1][0] != 0:
        p208 = flow2(df)[1][0]/flow1(df)[1][0]
    else:
        p208 = 0
    if flow1(df)[1][1] != 0:
        p210 = flow2(df)[1][1]/flow1(df)[1][1]
    else:
        p210 = 0

    print(p108, p110, p208, p210)
    return [p108, p110, p208, p210]

if __name__ == "__main__":
    find_speedband(retrieve_speedbands())
    proportion(retrieve_images())

