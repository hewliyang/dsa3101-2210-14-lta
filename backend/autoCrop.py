import numpy as np
import cv2

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