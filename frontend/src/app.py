"""
This file is for the main dash application
"""
import os
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dcc
from dash.dependencies import Input, Output
from flask import Flask
from components import sidebar, navbar
#import urllib
#import requests

#function to download images, named by the camera id
#def download_images(dataframe, folder):
#
#    for i in range(len(dataframe)):
#        urllib.request.urlretrieve(
#            dataframe['ImageLink'].values[i],
#            os.path.join(folder, str(dataframe['CameraID'].values[i])+'.jpg')
#        )
#    return None

#TODO: REQUEST API FROM BACKEND IMAGES
server = Flask(__name__)
app = dash.Dash(
	__name__,
	#server=server,
	use_pages=True,
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
            dcc.Location(id="url"),
            navbar,
            sidebar,
            dbc.Container([
                dash.page_container
                ],
                id="page-content",
                fluid=True,
                style={"height":"90vh", "transition": "margin-right .5s", "width":"auto", "padding":0, "margin":0, 'max-height':"90vh"}
            )
        ]
    )

app.layout = serve_layout

if __name__ == "__main__":
	app.run_server(host="0.0.0.0", debug=True)
