import ast
import urllib
import pandas as pd
import numpy as np
import cv2

from utils import retrieve_images
from crop import auto_crop
from count import getVehicleCount

def density(img, cam, i, dir):
    count = getVehicleCount(img)
    distance = cam["Dir" + dir + "Distance"][i] / 1000
    lanes = cam["Dir" + dir + "Lanes"][i]
    return count / distance / lanes;


def find_density(df):
    cam = pd.read_csv("cam.csv")
    density_1 = []
    density_2 = []
    for i in range(1, len(df) + 1):
        DirCoords = ast.literal_eval(cam["DirCoords"][i])
        resp = urllib.request.urlopen(df["ImageLink"][i-1])
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        cropped_images = auto_crop(img, DirCoords)
        density_1.append(density(cropped_images[0], cam, i, "1"))

        if len(cropped_images[1]) != 0:
            density_2.append(density(cropped_images[1], cam, i, "2"))
        else:
            density_2.append(0)
        print(density_1, density_2)
    return [density_1, density_2]
    

if __name__ == "__main__":
    find_density(retrieve_images())