import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output


dash.register_page(
	__name__,
	path='/grid',
	title='Home'
)

def create_card(img_src):
	return dbc.Card(
		[
			dbc.CardImg(src=img_src)
		]
	)

def update_images(imgSrcList, page):
	startIndex = (page-1)*12
	endIndex = startIndex + 12
	imgToDisplay = [imgSrcList[imgNum] for imgNum in range(startIndex, endIndex)]
	return imgToDisplay

# TODOs: Callbacks for list of images and page number
img_a1, img_a2, img_a3, img_a4, img_b1, img_b2, img_b3, img_b4, img_c1, img_c2, img_c3, img_c4 = update_images(imgSrcList, page)
# TODOs: Color borders based on traffic jam probability 

layout = html.Div(
	[
		# First Row of Traffic Images
		dbc.Row(
			[
				dbc.Col([create_card(f'{img_a1}')]),
				dbc.Col([create_card(f'{img_a2}')]),
				dbc.Col([create_card(f'{img_a3}')]),
				dbc.Col([create_card(f'{img_a4}')])
			],
			class_name = "g-0" # No gaps between images
		),
		# Second Row of Traffic Images
		dbc.Row(
			[
				dbc.Col([create_card(f'{img_b1}')]),
				dbc.Col([create_card(f'{img_b2}')]),
				dbc.Col([create_card(f'{img_b3}')]),
				dbc.Col([create_card(f'{img_b4}')])
			],
			class_name = "g-0" # No gaps between images
		),
		# Third Row of Traffic Images
		dbc.Row(
			[
				dbc.Col([create_card(f'{img_c1}')]),
				dbc.Col([create_card(f'{img_c2}')]),
				dbc.Col([create_card(f'{img_c3}')]),
				dbc.Col([create_card(f'{img_c4}')])
			],
			class_name = "g-0" # No gaps between images
		)
	]
)

