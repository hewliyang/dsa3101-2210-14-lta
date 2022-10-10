import ast
import urllib
import pandas as pd
import numpy as np
import cv2

from utils import retrieve_images
from crop import auto_crop
from count import getVehicleCount


CAM = pd.read_csv("cam.csv")
CAM_DICT = {1001: 1, 1002: 2, 1003: 3, 1004: 4, 1005: 5, 1006: 6, 1501: 7, 1502: 8, 1503: 9, 1504: 10, 1505: 11, 1701: 12, 1702: 13,
            1703: 14, 1704: 15, 1705: 16, 1706: 17, 1707: 18, 1709: 19, 1711: 20, 2701: 21, 2702: 22, 2703: 23, 2704: 24, 2705: 25,
            2706: 26, 2707: 27, 2708: 28, 3702: 29, 3704: 30, 3705: 31, 3793: 32, 3795: 33, 3796: 34, 3797: 35, 3798: 36, 4701: 37, 
            4702: 38, 4703: 39, 4704: 40, 4705: 41, 4706: 42, 4707: 43, 4708: 44, 4709: 45, 4710: 46, 4712: 47, 4713: 48, 4714: 49, 
            4716: 50, 4798: 51, 4799: 52, 5794: 53, 5795: 54, 5797: 55, 5798: 56, 5799: 57, 6701: 58, 6703: 59, 6704: 60, 6705: 61, 
            6706: 62, 6708: 63, 6710: 64, 6711: 65, 6712: 66, 6713: 67, 6714: 68, 6715: 69, 6716: 70, 7791: 71, 7793: 72, 7794: 73, 
            7795: 74, 7796: 75, 7797: 76, 7798: 77, 8701: 78, 8702: 79, 8704: 80, 8706: 81, 9701: 82, 9702: 83, 9703: 84, 9704: 85, 
            9705: 86, 9706: 87}

def density(img, cam, i, dir):
    count = getVehicleCount(img)
    distance = cam["Dir" + dir + "Distance"][i] / 1000
    lanes = cam["Dir" + dir + "Lanes"][i]
    return count / distance / lanes;


def find_all_density(df):
    cam = pd.read_csv("cam.csv")
    densities = []

    for i  in range(len(df)):
        densities.append(find_density(df, int(df["CameraID"][i])))
        print(df["CameraID"][i])

            

    return densities

def find_density(df, index):
    id = CAM_DICT[index]-1
    
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