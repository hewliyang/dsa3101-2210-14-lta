# Backend Documentation

## API 

**Follow the steps to run the API on your local computer**

1. Docker

Make sure the ```.env``` file is in this directory. Then simply run  

```docker build -t api .```  
```docker run -d -p 5000:5000 api```

2. Virtual Environment

- Create a virtual environment of your choice; eg: 
```virtualenv venv```
- Activate virtual environment & Install dependencies
```source venv/Scripts/activate```
```pip install -r requirements.txt```
- Run ```mim install mmcv-full```
- Run the Flask app
```python app.py```

The app is hosted on ```localhost``` at port ```5000``` and available endpoints are
- ```/api/v1/cam_metadata```
- ```/api/v1/cam_images```
- ``` /api/v1/speed_bands```
- ```/api/v1/traffic_incidents```
- ```/api/v1/density```
- ```/api/v1/batch_inference```

Only ```density``` requires you to specify a parameter (```cameraID```, ```prob```) when you make a request.

Specific usage examples can be found in the [api_demo notebook](https://github.com/hewliyang/dsa3101-2210-14-lta/blob/main/backend/api_demo.ipynb)

Example request :

```python
import requests
import pandas as pd
url = "http://127.0.0.1:5000/api/v1/density"
args = {"cameraID":1702}
r = requests.get(url, params=args)
output = r.json()
df = pd.DataFrame(output)
```

Please also note that the timestamp is returned in UNIX format. An example is ```1665939900000``` which translates to ```2022-10-16T17:05:00```. You may do the conversion as follows using the ```datetime``` module:

```python
from datetime import datetime
from time import strftime

ts = 1665939900000
ts = ts/1000
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S'))
```

## File Descriptions

### utils.py

Contains helper functions which help pre-process and generate new features for data retrieved from
LTA API. Also serves as to export one instance of data locally. Calling

```
python utils.py
```

Will export speed band data and traffic incidents to CSV files, while images are downloaded.

### crop.py

Two distinct uses:
1) Auto Cropping  
- Using pre-coded coordinates, crop images into 2.

2) Store cropping coordinates to be used as the coords in auto cropping  
Used to crop traffic images into their 2 distinct directions using OpenCV.  
Outputs an array of coordinates representing the cropped polygon which can be saved.  

Cropped Coordinates:
- In the case of there being only 1 direction in image: leave the second list BLANK!
- The auto cropping code checks for a blank list: will not be enough to put 0 in distance

How To Crop:
1) Ensure the images you want to crop are in images folder
2) go cmd and cd to this folder:
- py crop.py
- Enter image id
- An Image should pop up
- Click the image to "crop" the image into just 1 side of the road.
- Press Enter
- Image will close and a new cropped image will show up
- Check to see if cropped correctly
- Press Enter
- Original Image should pop up
- Click the image to "crop" the image for the other side of the road.
- Press Enter
- Image will close and a new cropped image will show up
- Check to see if cropped correctly
- Press Enter
- If both sides cropped correctly --> Copy the coords outputed on ur cmd


### find_density.py  
Takes in functions from crop, utils, count to combine and find the latest density from images taken from lta
Given the density data, perform data preprocessing including removing 0s and outliers. Afterwards, scale and normalise the processed data and plot the values.


## Design Decisions

**Omitting the use of speed band data**

Observe the following plot of camera locations vs observed speed band locations plotted using the following code :

```python
import folium
# create base map
m = folium.Map(location=[1.3521, 103.8198], zoom_start = 12)
# add camera locations to map
for id, lat, lng in zip(image_data.CameraID, image_data.Latitude, image_data.Longitude):
     marker = folium.Marker([lat, lng], popup = f"id: {id}")
     marker.add_to(m)
# add speedband locations to map
for road_name, lat1, lng1, lat2, lng2 in zip(speed_band_data.RoadName, speed_band_data.latitude1, speed_band_data.longitude1, speed_band_data.latitude2, speed_band_data.longitude2):
    points = [(float(lat1),float(lng1)), (float(lat2),float(lng2))]
    folium.PolyLine(points, popup = str(road_name), weight = 5, opacity = 1, color = "red").add_to(m)
```
![](./assets/map_road_plot.JPG)

Speed band data returned by LTA's sensors are typically 
1. Heavily clustered in the south 
2. Not relevant to the locations of their traffic cameras which are on **highways** only

The interactive plot is available at this [link](https://hewliyang.github.io/)

## Models Used

**Vehicle Counting**

We use a pre-trained YOLO V4 model to count the number of vehicles that can be seen from the traffic cameras.

The weights are not included in this repository, but can be retrieved from [AlexeyAB's](https://github.com/AlexeyAB/darknet/wiki/YOLOv4-model-zoo) repository. This file should be included under the ```models``` folder along with its associated ```.cfg``` file. 

An example of a detection can be seen in the following image :

![](./assets/sample_detection.jpg)
