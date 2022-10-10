import ast
import urllib
import pandas as pd
import numpy as np
import cv2
import json

from crop import auto_crop
from count import getVehicleCount

### Read in a dictionary translation of cam.csv 
cam_info = json.load(open("camera_info.txt"))

# Calculate traffic density of an image (# vehicles per KM per lane)
def density(img, cameraID, dir):
    count = getVehicleCount(img)
    distance = cam_info["Dir1Distance"][str(cameraID)]/1000 if dir == 1 else \
        cam_info["Dir2Distance"][str(cameraID)]/1000
    lanes = cam_info["Dir1Lanes"][str(cameraID)] if dir == 1 else \
        cam_info["Dir2Lanes"][str(cameraID)]
    return round((count / distance / lanes), 3)

# Performs the crop before running density()
# # If any direction2's distance / lane are NaN, density = 0
def find_density(image_df, cameraID):

    DirCoords = ast.literal_eval(cam_info["DirCoords"][str(cameraID)])
    resp = urllib.request.urlopen(image_df[image_df['CameraID']==str(cameraID)].iloc[0]["ImageLink"])
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    cropped_images = auto_crop(img, DirCoords)

    density1 = density(cropped_images[0], cameraID, 1)

    if len(cropped_images[1]) != 0:
        density2 = density(cropped_images[1], cameraID, 2)
    else:
        density2 = 0
        
    return (density1, density2)