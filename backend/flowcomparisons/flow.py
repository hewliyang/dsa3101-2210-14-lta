import ast
import urllib
import pandas as pd
import numpy as np
import cv2

import sys
import cv2

def flowcombined():
    data = pd.read_csv("speedcombined.csv")
    density1 = []
    density2 = []
    speed = []
    flow1 = []
    flow2 = []
    cd = []
    count = 0

    for i in range(23):
        f1, f2, d1, d2, s = 0, 0, 0, 0, 0
        for j in range(24):
            f1 += data['density1'].iloc[count]
            f2 += data['density2'].iloc[count]
            s += data['speedband'].iloc[count]
            count += 1
        d1 = f1/12
        d2 = f2/12
        s = s/12
        density1.append(d1)
        density2.append(d2)
        speed.append(s)
        cd.append((d1+d2)/2)
        flow1.append(f1)
        flow2.append(f2)

    f1, f2, d1, d2, s = 0, 0, 0, 0, 0
    for i in range(18):
        f1 += data['density1'].iloc[count]
        f2 += data['density2'].iloc[count]
        s += data['speedband'].iloc[count]
        count += 1
    d1 = f1/9
    d2 = f2/9
    s = s/9
    density1.append(d1)
    density2.append(d2)
    speed.append(s)
    cd.append((d1+d2)/2)
    flow1.append(f1)
    flow2.append(f2)

    return [density1, density2, speed, cd, flow1, flow2]


# Q = D * V
def flow6708():
    data = pd.read_csv("speed6708.csv")
    density1 = []
    density2 = []
    speed = []
    flow1 = []
    flow2 = []
    cd = []
    count = 0

    for i in range(23):
        f1, f2, d1, d2, s = 0, 0, 0, 0, 0
        for j in range(12):
            f1 += data['density1'].iloc[count]
            f2 += data['density2'].iloc[count]
            s += data['speedband'].iloc[count]
            count += 1
        d1 = f1/12
        d2 = f2/12
        s = s/12
        density1.append(d1)
        density2.append(d2)
        speed.append(s)
        cd.append((d1+d2)/2)
        flow1.append(f1)
        flow2.append(f2)

    f1, f2, d1, d2, s = 0, 0, 0, 0, 0
    for i in range(9):
        f1 += data['density1'].iloc[count]
        f2 += data['density2'].iloc[count]
        s += data['speedband'].iloc[count]
        count += 1
    d1 = f1/9
    d2 = f2/9
    s = s/9
    density1.append(d1)
    density2.append(d2)
    speed.append(s)
    cd.append((d1+d2)/2)
    flow1.append(f1)
    flow2.append(f2)

    return [density1, density2, speed, cd, flow1, flow2]

def flow6710():
    data = pd.read_csv("speed6710.csv")
    density1 = []
    density2 = []
    speed = []
    flow1 = []
    flow2 = []
    cd = []
    count = 0

    for i in range(23):
        f1, f2, d1, d2, s = 0, 0, 0, 0, 0
        for j in range(12):
            f1 += data['density1'].iloc[count]
            f2 += data['density2'].iloc[count]
            s += data['speedband'].iloc[count]
            count += 1
        d1 = f1/12
        d2 = f2/12
        s = s/12
        density1.append(d1)
        density2.append(d2)
        speed.append(s)
        cd.append((d1+d2)/2)
        flow1.append(f1)
        flow2.append(f2)

    f1, f2, d1, d2, s = 0, 0, 0, 0, 0
    for i in range(9):
        f1 += data['density1'].iloc[count]
        f2 += data['density2'].iloc[count]
        s += data['speedband'].iloc[count]
        count += 1
    d1 = f1/9
    d2 = f2/9
    s = s/9
    density1.append(d1)
    density2.append(d2)
    speed.append(s)
    cd.append((d1+d2)/2)
    flow1.append(f1)
    flow2.append(f2)

    return [density1, density2, speed, cd, flow1, flow2]


if __name__ == "__main__":
    flow6708()
    flow6710()
