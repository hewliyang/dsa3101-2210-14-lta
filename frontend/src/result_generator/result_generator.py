import os
import pandas as pd
import requests
import urllib
import redis
from datetime import datetime
from time import strptime, sleep

url = "http://127.0.0.1:5000/api/v1/" #http://localhost:5000/api/v1/

# Insufficient computing resources version
# Generate next predictions
def generate_new_set():
	folder = r'src/assets/imageToBeUpdated/'
	# Empty all images in the toBeUpdated folder
	if os.listdir(folder) != []:
		for file in os.listdir(folder):
			if file.endswith(".jpg"):
				os.remove(f'{folder}{file}')

	direction_label = pd.read_csv(r"src/assets/direction_label.csv")
	# Band_Aid solution
	density_url = f"{url}density"
	predictions = []
	for i in range(len(direction_label['CameraID'])):
		CID = direction_label.iloc[i, 0]
		params = {"cameraID":CID, "prob":True} # To obtain Probability and density
		r1 = requests.get(density_url, params=params)
		if r1.status_code == 200:
			data = r1.json()[0]
			# Download the picture
			picTime = datetime.utcfromtimestamp(data['timestamp']/1000).strftime('%Y%m%d%H%M%S')
			urllib.request.urlretrieve(
					data['ImageLink'],
					os.path.join(folder, f'{CID}_{picTime}.jpg')
			)
			predictions += [[CID, data['ImageLink'], f'{CID}_{picTime}.jpg', data['Latitude'], data['Longitude'], direction_label.iloc[i, 1], data['density1'], data['prob1'],\
							direction_label.iloc[i, 2], data['density2'], data['prob2']]]
	result = pd.DataFrame(predictions, columns=['CameraID', 'imageLink', 'imageFile', 'Latitude', 'Longitude', 'dir1', 'density1', 'prob1', 'dir2', 'density2', 'prob2'])
	result.to_csv(r"src/assets/backup.csv", index=False)
	currDisplayFolder = r'src/assets/imageCurrShown/'
	if os.listdir(currDisplayFolder) != []: # Remove Current showing photos
		for file in os.listdir(currDisplayFolder):
			if file.endswith(".jpg"):
				os.remove(f'{currDisplayFolder}{file}')
	for file in os.listdir(folder): # Move files from toBeUpdated to Current showing photos
		if file.endswith(".jpg"):
			os.rename(f'{folder}{file}', f'{currDisplayFolder}{file}')
	return result

if __name__ == "__main__":
	redisConnection = redis.Redis(host='redis-cache', port=6379, db=0)
	while True:
		df = pd.read_msgpack(redisConnection.get("currDisplay"))
		if df is not None: # Check to see if predicting for the same set of data
			images_url = f'{url}cam_images'
			data = requests.get(images_url).json()[0]
			if data['ImageLink'][0] != df['imageLink'][0]:
				new_prediction = generate_new_set()
				redisConnection.set("currDisplay", new_prediction.to_msgpack(compress='zlib'))
		else: 
			new_prediction = generate_new_set()
			redisConnection.set("currDisplay", new_prediction.to_msgpack(compress='zlib'))
		sleep(10)

# With sufficient computing resources version
#function to download images, named by the cameraID_datetime.jpy
#def download_images(folder, barrier):
#	# Empty all images in the toBeUpdated folder
#	if os.listdir(folder) != []:
#		for file in os.listdir('frontend/src/assets/imageToBeUpdated/'):
#			if file.endswith(".jpg"):
#				os.remove(file)
#	req = requests.get(f'{url}cam_images')
#	df = pd.DataFrame(req.json())
#	# Downloads only if the folder is cleared -> Pictures are moved to imageCurrShown <=> Predictions are all made
#	for i in range(len(df)):
#		picTime = datetime.utcfromtimestamp(df['timestamp'].values[i]/1000).strftime('%Y%m%d%H%M%S')
#		urllib.request.urlretrieve(
#			df['ImageLink'].values[i],
#			os.path.join(folder, f'{df["CameraID"].values[i]}_{picTime}.jpg')
#		)
#	barrier.wait()

# Generate next predictions
#def get_predictions(barrier):
#	direction_label = pd.read_csv(r"src/assets/direction_label.csv")
#	## Insufficient Computing Resources to run this
#	density_url = f"{url}batch_inference" #http://localhost:5000/api/v1/
#	r = requests.get(density_url)
#	result = pd.DataFrame(r.json())
#	result['dir1'] = [x for x in direction_label['direction1'].values]
#	result['dir2'] = [x for x in direction_label['direction2'].values]
#	barrier.wait()
#	return result

#def backgroundProcesses():
#	barrier = Barrier(3)
#	Process(target=download_images, args = ('./assets/imageToBeUpdated',barrier))
#	result = Process(target=get_predictions, args = (barrier))
#	barrier.wait()
#	currDisplayFolder = r'src/assets/imageCurrShown/'
#	if os.listdir(currDisplayFolder) != []: # Remove Current showing photos
#		for file in os.listdir(currDisplayFolder):
#			if file.endswith(".jpg"):
#				os.remove(f'{currDisplayFolder}{file}')
#	for file in os.listdir(folder): # Move files from toBeUpdated to Current showing photos
#		if file.endswith(".jpg"):
#			os.rename(f'{folder}{file}', f'{currDisplayFolder}{file}')
#	return result
			


