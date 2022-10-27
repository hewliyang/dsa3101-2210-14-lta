"""
This file is for the main dash application
"""
# TODO: Downloading pictures and making predictions together using in the same\
# function result in inconsistency and repeat downloads of the same photos
# TODO: Predictions and downloading images are not running in the background
# TODO: Changing page refreshes the app and causes the prediction to run again,\
# preventing anything from working until prediction is done ->  Need to somehow save the current state
import os
import requests
import pandas as pd
import urllib
from datetime import datetime
from time import strftime, sleep
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dcc, DiskcacheManager
from dash.dependencies import Input, Output
from flask import Flask
from components import sidebar, navbar
import diskcache
# from multiprocessing import Process, Barrier

url = "http://127.0.0.1:5000/api/v1/" #http://localhost:5000/api/v1/
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

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

server = Flask(__name__)
app = dash.Dash(
	__name__,
	server=server,
	use_pages=True,
	background_callback_manager=background_callback_manager,
	meta_tags=[
				{"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1.2, minimum-scale=0.5"}
			],
	external_stylesheets=[dbc.themes.BOOTSTRAP]
	)

def serve_layout():
	'''Define the layout of the application'''
	return html.Div(
		[
			dcc.Store(id='side_click'),
			navbar,
			sidebar,
			dbc.Container([
				dash.page_container
				],
				id="page-content",
				fluid=True,
				style={"height":"90vh", "transition": "margin-right .5s", "width":"auto", "padding":0, "margin":0, 'max-height':"90vh"}
			),
			dcc.Interval(id='update-predictions', interval=600000, n_intervals=0), # Every 10mins refresh
			dcc.Store(id='current-predictions', storage_type='local', clear_data=True)
		]
	)

app.layout = serve_layout

@app.callback(Output('current-predictions', 'data'), Input('update-predictions', 'n_intervals'),\
	Input('current-predictions', 'data'), background=True, prevent_initial_call = True)
# TODO:Currently preventing initial to at least load the pages
def generate_predictions(n, json_data):
	if json_data is not None:
		df = pd.read_json(json_data, orient = "split")
		images_url = f'{url}cam_images'
		data = requests.get(images_url).json()[0]
		if data['ImageLink'][0] == df['imageLink'][0]: # Same ImageLink means not refreshed yet
			return dash.no_update
	predictions_df = generate_new_set()
	return predictions_df.to_json(date_format='iso', orient = 'split')

if __name__ == "__main__":
	app.run_server(host="0.0.0.0", debug=True, dev_tools_hot_reload=False, use_reloader=False)
