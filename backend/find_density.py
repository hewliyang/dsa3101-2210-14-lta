import ast
import urllib
import pandas as pd
import numpy as np
import cv2

from utils import retrieve_images
from autoCrop import auto_crop

def crop_images(df):
    cam = pd.read_csv("cam.csv")
    a = []
    for i in range(1, len(df)+1):
        DirCoords = ast.literal_eval(cam["DirCoords"][i])
        resp = urllib.request.urlopen(df["ImageLink"][i-1])
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        a.append(auto_crop(img, DirCoords))

    return a

if __name__ == "__main__":
    print(len(crop_images(retrieve_images())))