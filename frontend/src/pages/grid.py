import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output
import datetime
import random
import requests
import os

dash.register_page(
	__name__,
	path='/grid',
	title='Grid View',
	description="Grid view of traffic"
)

# Color border based on probability
def seriousness(probability):
	if probability > 0.7:
		return {"border":0, "outline":"4px solid red", "outline-offset":"-4px"}
	elif probability > 0.3:
		return {"border":0, "outline":"4px solid orange", "outline-offset":"-4px"}
	else:
		return {"border":0, "outline":"4px solid green", "outline-offset":"-4px"}


def create_card(img_src, severity):
	image = f'./assets/sampleImg/{img_src}'
	return dbc.Card(
		[
			#html.H4("Placeholder", style={'textAlign': 'center'}),
			dbc.CardImg(src=image, className = 'align-self-center', style={"max-height":"25vh", "height":"auto"}),
			dbc.CardImgOverlay(
				[dbc.Button(href=f"http://localhost:8050/gridDetailed?main_picture={img_src}", 
				style= {"opacity": 0, "height": "100%", "width": "100%", "margin":0, "padding":0, "border":0})
				], 
				style = {"padding":0, "margin":0})
		], style = severity
	)

def get_pictures():
	#metadata_url = "https://localhost:5000/api/v1/cam_metadata"
	#density_url = "https://localhost:5000/api/v1/density"
	pass

random.seed(1)
imgSrcList = [(file, round(random.uniform(0, 1), 2)) for file in os.listdir("src/assets/sampleImg/") if file.endswith(".jpg")]
imgSrcList.sort(key= lambda x:x[1], reverse=True)
#imgSrcList = get_pictures()

def layout():
	return html.Div(
	[
		# First Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					id='img_a1',
					width = 3
				),
				dbc.Col(
					id='img_a2',
					width = 3
				),
				dbc.Col(
					id='img_a3',
					width = 3
				),
				dbc.Col(
					id='img_a4',
					width = 3
				)
			],
			class_name = "g-0", # No gaps between images
			justify="evenly"
		),
		# Second Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					id='img_b1',
					width = 3
					#[create_card(f'{img_b1}')]
				),
				dbc.Col(
					id='img_b2',
					width = 3
				),
				dbc.Col(
					id='img_b3',
					width = 3
				),
				dbc.Col(
					id='img_b4',
					width = 3
				)
			],
			class_name = "g-0", # No gaps between images
			justify="evenly"
		),
		# Third Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					id='img_c1',
					width = 3
				),
				dbc.Col(
					id='img_c2',
					width = 3
				),
				dbc.Col(
					id='img_c3',
					width = 3
				),
				dbc.Col(
					id='img_c4',
					width = 3
				)
			],
			class_name = "g-0", # No gaps between images
			justify="evenly"
		),
		html.Div(id="last_updated", style = {"float":"right", "padding-right":"10px", "padding-top":"5px"}),
		html.Div([
		html.Div("Select a page", id = "pagination-contents", style={"margin":0, "padding":0}),
		dbc.Pagination(id="pagination", max_value=8, fully_expanded=False, first_last=True),
		html.Div(id="time", style={"display":None})
		], style = {"float": "left", "padding-left":"10px", "padding-top":"5px"})
	]
)

@callback(
	Output(component_id='last_updated', component_property='children'),
	Input(component_id='time', component_property='children')
) 
def last_updated(time):
	pic = imgSrcList[0][0][10:22]
	time = datetime.datetime.strptime(pic, "%Y%m%d%H%M") #Mock Data
	return f'Last Updated: {time}'

@callback(
    Output("pagination-contents", "children"),
    [Input("pagination", "active_page")],
)
def change_page(page):
    if page:
        return f"Page selected: {page}"
    return "Select a page"

@callback(
	[Output("img_a1", "children"), #a1
	Output("img_a2", "children"), #a2
	Output("img_a3", "children"), #a3
	Output("img_a4", "children"), #a4
	Output("img_b1", "children"), #b1
	Output("img_b2", "children"), #b2
	Output("img_b3", "children"), #b3
	Output("img_b4", "children"), #b4
	Output("img_c1", "children"), #c1
	Output("img_c2", "children"), #c2
	Output("img_c3", "children"), #c3
	Output("img_c4", "children")], #c4
	Input("pagination", "active_page")
)
def update_images(page):
	if not page:
		page = 1
	startIndex = (page-1)*12
	endIndex = startIndex + 12
	if endIndex >= len(imgSrcList):
		endIndex = len(imgSrcList) - 1
	imgToDisplay = [create_card(imgSrcList[imgNum][0], seriousness(imgSrcList[imgNum][1])) for imgNum in range(startIndex, endIndex)]
	imgToDisplay += [[]] * (12 - len(imgToDisplay))
	return imgToDisplay