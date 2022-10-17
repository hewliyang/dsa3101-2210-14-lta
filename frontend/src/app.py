"""
This file is for the main dash application
"""
import os
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from flask import Flask
from components import sidebar, navbar

# from components import button, footer, header, nav

server = Flask(__name__)
app = dash.Dash(
	__name__,
	#server=server,
	use_pages=True,
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
            fluid=True,
            style={"height":"90vh", 'margin':0, 'padding':0}
            )
        ]
    )

app.layout = serve_layout

if __name__ == "__main__":
	app.run_server(debug=True)
