import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output


dash.register_page(
	__name__,
	path='/grid',
	title='Grid View'
)
def seriousness(probability):
	if probability > 0.75:
		return {"border":0, "outline":"4px solid red", "outline-offset":"-4px"}
	elif probability > 0.5:
		return {"border":0, "outline":"4px solid orange", "outline-offset":"-4px"}
	else:
		return {"border":0, "outline":"4px solid green", "outline-offset":"-4px"}

def create_card(img_src, severity):
	img_src = "./assets/sampleImg/1001_1143_20220105114948_a72916.jpg"
	return dbc.Card(
		[
			#html.H4("Placeholder", style={'textAlign': 'center'}),
			dbc.CardImg(src=img_src, className = 'align-self-center', style={"max-height":"30vh", "height":"auto"}),
			dbc.CardImgOverlay(
				[dbc.Button(href="http://127.0.0.1:8050/gridDetailed", 
				style= {"opacity": 0, "height": "100%", "width": "100%", "margin":0, "padding":0, "border":0})
				], 
				style = {"padding":0, "margin":0})
		], style = severity
	)

def update_images(imgSrcList, page):
	startIndex = (page-1)*12
	endIndex = startIndex + 12
	imgToDisplay = [imgSrcList[imgNum] for imgNum in range(startIndex, endIndex)]
	return imgToDisplay

# TODOs: Callbacks for list of images and page number
# img_a1, img_a2, img_a3, img_a4, img_b1, img_b2, img_b3, img_b4, img_c1, img_c2, img_c3, img_c4 = update_images(imgSrcList, page)
# TODOs: Color borders based on traffic jam probability 

layout = html.Div(
	[
		# First Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					[create_card("Placeholder", seriousness(0.9))],
					width = 3
					#[create_card(f{img_a1}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.8))],
					width = 3
					#[create_card(f'{img_a2}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.75))],
					width = 3
					#[create_card(f'{img_a3}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.5))],
					width = 3
					#[create_card(f'{img_a4}')]
				)
			],
			class_name = "g-0", # No gaps between images
			justify="evenly"
		),
		# Second Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					[create_card("Placeholder", seriousness(0.5))],
					width = 3
					#[create_card(f'{img_b1}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.3))],
					width = 3
					#[create_card(f'{img_b2}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.2))],
					width = 3
					#[create_card(f'{img_b3}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.2))],
					width = 3
					#[create_card(f'{img_b4}')]
				)
			],
			class_name = "g-0", # No gaps between images
			justify="evenly"
		),
		# Third Row of Traffic Images
		dbc.Row(
			[
				dbc.Col(
					[create_card("Placeholder", seriousness(0.2))],
					width = 3
					#[create_card(f'{img_c1}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.4))],
					width = 3,
					#[create_card(f'{img_c2}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.5))],
					width = 3
					#[create_card(f'{img_c3}')]
				),
				dbc.Col(
					[create_card("Placeholder", seriousness(0.4))],
					width = 3
					#[create_card(f'{img_c4}')]
				)
			],
			class_name = "g-0", # No gaps between images
			justify="evenly"
		)
	]
)

