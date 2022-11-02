import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output
import datetime
import os
import pandas as pd

dash.register_page(
	__name__,
	path='/gridDetailed',
	title='Grid Detailed View',
	description="Shows the detailed description version of the chosen image"
)

# Color border based on probability
def seriousness(probability):
	if probability > 0.7:
		return {"border":0, "outline":"4px solid red", "outline-offset":"-4px"}
	elif probability > 0.3:
		return {"border":0, "outline":"4px solid orange", "outline-offset":"-4px"}
	else:
		return {"border":0, "outline":"4px solid green", "outline-offset":"-4px"}

def create_card(img_src, cameraID, severity, main=False):
	image = f'./assets/imageCurrShown/{img_src}'
	if main:
		return dbc.Card(
			[
				dbc.CardImg(src=image, className = 'align-self-center', style={"max-height":"60vh", "height":"60vh"}),
				dbc.CardImgOverlay([html.H5(f"CAMERA_ID: {cameraID}", className="card-title", style={"color":"white", "background-color":"gray", "width":"50%", "opacity":0.7})])
			], style = severity
		)
	else: 
		return dbc.Card(
			[
				dbc.CardImg(src=image, className = 'align-self-center', style={"max-height":"25vh", "height":"auto"}),
				dbc.CardImgOverlay(
				[html.H5(f"CAMERA_ID: {cameraID}", className="card-title", style={"color":"white", "background-color":"gray", "width":"50%", "opacity":0.7}),
				dbc.Button(href=f"http://localhost:8050/gridDetailed?main_picture={img_src}", 
				style= {"opacity": 0, "height": "100%", "width": "100%", "margin":0, "padding":0, "border":0})
				], 
				style = {"padding":0, "margin":0})
			], style = severity
		)

def layout(main_picture=None, **other_unknown_query_strings):
	return html.Div(
	[
		# First Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					id='img_main_detailed',
					width=6
				),
				dbc.Col(
					[
						dbc.Row([
							html.H2("Camera ID", style={'textAlign':'center', 'padding':'0px', 'margin':0}),
							html.H4(id='camera-id', style={'textAlign':'center', 'color':'white', 'padding':'2px', 'margin':0}),
							html.H2(f"Location", style={'textAlign': 'center', 'padding':'0px', 'margin':0}), # , 'background-color': 'Yellow'
							html.H4(id='lat-long', style={'textAlign': 'center', 'color':'white', 'padding':'2px', 'margin':0})
						], style={'height': '20vh', 'background-color': '#4A6FA5', "padding":0, "margin":0}),
						dbc.Row([
							dbc.Col([
								html.H2("DIRECTION", style={'textAlign':'center'}),
								html.H4(id='dir1', style={'textAlign':'center', 'color':'white'}),
								html.H2("DENSITY", style={'textAlign':'center'}),
								html.H4(id='den1', style={'textAlign':'center', 'color':'white'}),
								html.H2("PROBABILITY", style={'textAlign':'center'}),
								html.H4(id='prob1', style={'textAlign':'center', 'color':'white'})
							], width = 6),
							dbc.Col([
								html.H2("DIRECTION", style={'textAlign':'center'}),
								html.H4(id='dir2', style={'textAlign':'center', 'color':'white'}),
								html.H2("DENSITY", style={'textAlign':'center'}),
								html.H4(id='den2', style={'textAlign':'center', 'color':'white'}),
								html.H2("PROBABILITY", style={'textAlign':'center'}),
								html.H4(id='prob2', style={'textAlign':'center', 'color':'white'})
							], width = 6)
						], style={'height': '40vh', 'background-color':"#166088", "padding":0, "margin":0})
					], 
					width=6,
					style={'max-height': '60vh', "height":"60vh", "padding":0, "margin":0}
				)
			],
			className="g-0",
			justify="evenly",
			style = {"padding":0, "margin":0}
		),
		# Next Top 4 Traffic Images
		dbc.Row(
			[
				dbc.Col(
					id='img_b1_detailed',
					width=3
				),
				dbc.Col(
					id='img_b2_detailed',
					width=3
				),
				dbc.Col(
					id='img_b3_detailed',
					width=3
				),
				dbc.Col(
					id='img_b4_detailed',
					width=3
				)
			],
			className="g-0",
			justify="evenly",
			style = {"padding":0, "margin":0}
		),
		html.Div(id="last_updated_detailed", style = {"float":"right", "padding-right":"10px", "padding-top":"0px"}),
		html.Div(id="time_detailed", style={"display":"None"}),
		html.Div([dcc.Input(value=main_picture, id="selected_img", style={"display":"None"})], style={"display":"None"})
	]
)

@callback(
	Output(component_id='last_updated_detailed', component_property='children'),
	Input(component_id='time_detailed', component_property='children'),
	Input(component_id='current-predictions', component_property='data')
)
# 2706_1143_20220105114554_d54810
def last_updated(time, json_data):
	if json_data is not None:
		df = pd.read_json(json_data, orient = "split")
	else:
		df = pd.read_csv(r"src/assets/backup.csv")	
	timestamp = df['imageFile'][0][5:-4]
	time = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S") #Mock Data
	return f'Last Updated: {time}'

@callback(
	[Output("img_main_detailed", "children"), #a1
	Output("img_b1_detailed", "children"), #a2
	Output("img_b2_detailed", "children"), #a3
	Output("img_b3_detailed", "children"), #a4
	Output("img_b4_detailed", "children"),
	Output("camera-id", "children"),
	Output("lat-long", "children"),
	Output("dir1", "children"),
	Output("den1", "children"),
	Output("prob1", "children"),
	Output("dir2", "children"),
	Output("den2", "children"),
	Output("prob2", "children")
	],
	Input("selected_img", "value"),
	Input(component_id='current-predictions', component_property='data')
) 
def update_images(selected_img, json_data):
	if json_data is not None:
		df = pd.read_json(json_data, orient = "split")
	else:
		df = pd.read_csv(r"src/assets/backup.csv")	
	imgSrcList = [[w, x, max(y, z)] for w, x, y, z in zip(df['imageFile'], df['CameraID'], df['prob1'], df['prob2'])]
	imgSrcList.sort(key= lambda x:x[2], reverse=True)

	row = 0
	main_value = 0
	for i in range(len(imgSrcList)):
		if imgSrcList[i][0] == selected_img:
			main_value = i
			row = df[df['CameraID'] == imgSrcList[i][1]]
			break
	# Main
	imgToDisplay = [create_card(imgSrcList[main_value][0], imgSrcList[main_value][1], seriousness(imgSrcList[main_value][2]), True)]
	detailed_data = [row['CameraID'].values[0], f'{row["Latitude"].values[0]}, {row["Longitude"].values[0]}',\
					row['dir1'].values[0], round(row['density1'].values[0], 3), row['prob1'].values[0],\
					row['dir2'].values[0], round(row['density2'].values[0], 3), row['prob2'].values[0]]
	
	# Top 4 aside from main
	for imgNum in range(len(imgSrcList)):
		if imgNum != main_value:
			imgToDisplay += [create_card(imgSrcList[imgNum][0], imgSrcList[imgNum][1], seriousness(imgSrcList[imgNum][2]))]
		if len(imgToDisplay) == 5:
			break
	imgToDisplay += detailed_data
	return imgToDisplay