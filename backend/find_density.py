import ast
import urllib
import pandas as pd
import numpy as np
import cv2
import json

from crop import auto_crop
from count import getVehicleCount

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

### Read in a dictionary translation of cam.csv 
cam_info = json.load(open("metadata/camera_info.txt"))

noJam = {"max" : 30, "min" : 0}
jam =  {"max" : 81.667, "min": 30}

# Calculate traffic density of an image (# vehicles per KM per lane)
def density(img, cameraID, dir, detector):
    count = getVehicleCount(img, detector)
    distance = cam_info["Dir1Distance"][str(cameraID)]/1000 if dir == 1 else \
        cam_info["Dir2Distance"][str(cameraID)]/1000
    lanes = cam_info["Dir1Lanes"][str(cameraID)] if dir == 1 else \
        cam_info["Dir2Lanes"][str(cameraID)]
    return round((count / distance / lanes), 3)

# Performs the crop before running density()
# # If any direction2's distance / lane are NaN, density = 0
def find_density(image_df, cameraID, detector):

    DirCoords = ast.literal_eval(cam_info["DirCoords"][str(cameraID)])
    resp = urllib.request.urlopen(image_df[image_df['CameraID']==str(cameraID)].iloc[0]["ImageLink"])
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    cropped_images = auto_crop(img, DirCoords)

    density1 = density(cropped_images[0], cameraID, 1, detector)

    if len(cropped_images[1]) != 0:
        density2 = density(cropped_images[1], cameraID, 2, detector)
    else:
        density2 = 0
        
    return (density1, density2)

def normaliseDensity(density):
    if density <= noJam["max"]:
        return 0.3 * (density - noJam["min"]) / (noJam["max"] - noJam["min"])
    
    else:
        if density > jam["max"]:
            return 1
        return 0.7 * (density - jam["min"]) / (jam["max"] - jam["min"]) + 0.3

#can try filtering or plot histogram to see what would be a good threshold
def remove_zeros(dat) :
    return dat[dat!=0]

#returns df with 3 types of scaling: min max, robust and standard
def scale(dat):
    dat = pd.DataFrame(dat)
    df1 = pd.DataFrame(MinMaxScaler().fit_transform(dat)).rename({0: 'min_max'}, axis=1)
    df2 = pd.DataFrame(StandardScaler().fit_transform(dat)).rename({0: 'std_scale'}, axis=1)
    df3 = pd.DataFrame(RobustScaler().fit_transform(dat)).rename({0: 'robust_scale'}, axis=1)
    return pd.DataFrame(pd.concat([df1, df2, df3], axis=1))

#normalises the features/columns
def normalise(dat):
    dat = pd.DataFrame(dat)
    return pd.DataFrame(sklearn.preprocessing.normalize(dat, axis=0, copy=True, return_norm=False))

def hist_plot(dat):
    fig, axes = plt.subplots(nrows=2,ncols=2,figsize=(15, 15))
    dat["min_max"].plot(ax = axes[0,0], subplots=True,kind="hist")
    axes[0,0].set_title("min max")
    dat["std_scale"].plot(ax = axes[0,1], subplots=True,kind="hist")
    axes[0,1].set_title("std scale")
    dat["robust_scale"].plot(ax = axes[1,0], subplots=True,kind="hist")
    axes[1,0].set_title("robust scale")

def remove_outliers(dat,perc):
    dat = pd.DataFrame(dat)
    iso = IsolationForest(contamination=perc)
    yhat = iso.fit_predict(dat)
    nonoutliers = dat[yhat != -1]
    outliers = dat[yhat == -1]
    num_outliers = np.size(outliers)
    return (nonoutliers,outliers,num_outliers)
