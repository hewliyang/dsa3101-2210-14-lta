import ast
import urllib
import pandas as pd
import numpy as np
import cv2

import sys
import cv2
from detector import Detector

from utils import retrieve_images
from utils import retrieve_speedbands
from crop import auto_crop
from count import getVehicleCount
from find_density import find_density
from find_minspeed import find_speedband
from utils import retrieve_density



# Q = D * V
def flow1(df):
    
    flow_1 = []
    flow_2 = []
    density08 = find_density(df, 6708)
    density10 = find_density(df, 6710)
    speed = find_speedband(retrieve_speedbands())
    flow_1.append(density08[0] * speed[0][0])
    flow_2.append(density08[1] * speed[0][0])
    flow_1.append(density10[0] * speed[1][0])
    flow_2.append(density10[1] * speed[1][0])
    return [flow_1, flow_2]

# vehicle count will be underestimated
def flow2(df):

    flow_1 = []
    flow_2 = []
    
    density08 = find_density(df, 6708)
    density10 = find_density(df, 6710)
    flow_1.append(density08[0])
    flow_2.append(density08[1])
    flow_1.append(density10[0])
    flow_2.append(density10[1])
    
    return [flow_1, flow_2]


if __name__ == "__main__":
    flow1(retrieve_images())
    flow2(retrieve_images())
    
    
        
        
