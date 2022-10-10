import ast
import urllib
import pandas as pd
import numpy as np
import cv2

from utils import retrieve_images
from crop import auto_crop
from count import getVehicleCount

### Read in cam.csv and create a dictionary to find all camera ids in cam
CAM = pd.read_csv("cam.csv")
CAM_DICT = {1001: 0, 1002: 1, 1003: 2, 1004: 3, 1005: 4, 1006: 5, 1501: 6, 1502: 7, 1503: 8, 1504: 9, 1505: 10, 1701: 11, 1702: 12,
            1703: 13, 1704: 14, 1705: 15, 1706: 16, 1707: 17, 1709: 18, 1711: 19, 2701: 20, 2702: 21, 2703: 22, 2704: 23, 2705: 24,
            2706: 25, 2707: 26, 2708: 27, 3702: 28, 3704: 29, 3705: 30, 3793: 31, 3795: 32, 3796: 33, 3797: 34, 3798: 35, 4701: 36,
            4702: 37, 4703: 38, 4704: 39, 4705: 40, 4706: 41, 4707: 42, 4708: 43, 4709: 44, 4710: 45, 4712: 46, 4713: 47, 4714: 48,
            4716: 49, 4798: 50, 4799: 51, 5794: 52, 5795: 53, 5797: 54, 5798: 55, 5799: 56, 6701: 57, 6703: 58, 6704: 59, 6705: 60,
            6706: 61, 6708: 62, 6710: 63, 6711: 64, 6712: 65, 6713: 66, 6714: 67, 6715: 68, 6716: 69, 7791: 70, 7793: 71, 7794: 72,
            7795: 73, 7796: 74, 7797: 75, 7798: 76, 8701: 77, 8702: 78, 8704: 79, 8706: 80, 9701: 81, 9702: 82, 9703: 83, 9704: 84,
            9705: 85, 9706: 86}


# Calculate density of image
def density(img, cam, i, dir):
    count = getVehicleCount(img)
    distance = cam["Dir" + dir + "Distance"][i] / 1000
    lanes = cam["Dir" + dir + "Lanes"][i]
    return count / distance / lanes;

# Calculate density of all images in df
def find_all_density(df):
    cam = pd.read_csv("cam.csv")
    densities = []

    for i  in range(len(df)):
        densities.append(find_density(df, int(df["CameraID"][i])))
        print(df["CameraID"][i])

        
    return densities

# Calculate density of both directions of a CameraID
def find_density(df, index):
    id = CAM_DICT[index]
    
    DirCoords = ast.literal_eval(CAM["DirCoords"][id])
    resp = urllib.request.urlopen(df["ImageLink"][id])
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    cropped_images = auto_crop(img, DirCoords)

    density1 = density(cropped_images[0], CAM, id, "1")

    if len(cropped_images[1]) != 0:
        density2 = density(cropped_images[1], CAM, id, "2")
    else:
        density2 = "NA"
            

    return [density1, density2]
    

if __name__ == "__main__":
    print(find_all_density(retrieve_images()))