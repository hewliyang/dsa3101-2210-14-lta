import os
import numpy as np
import pandas as pd
import cv2
import ast
import urllib

from utils import retrieve_images, download_images

def crop(img, coord):
    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    points = np.array([coord])
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    res = cv2.bitwise_and(img,img,mask = mask)
    rect = cv2.boundingRect(points)
    wbg = np.ones_like(img, np.uint8)*255
    cv2.bitwise_not(wbg,wbg, mask=mask)
    dst = wbg+res
    return dst

def auto_crop(img, coords):
    dir1 = crop(img, coords[0])
    if (coords[1]):
        dir2 = crop(img, coords[1])
    else:
        dir2 = 0
    return [dir1, dir2]

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