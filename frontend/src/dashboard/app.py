"""
This file is for the main dash application
"""

import os
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dependencies import Input, Output
#from flask import Flask

from components import button, footer, header, nav

#server = Flask(__name__)
app = dash.Dash(
	__name__,
	#server=server,
	use_pages=True
	)

def serve_layout():
    '''Define the layout of the application'''
    return html.Div(
        [
            nav,
            dbc.Container(
                dash.page_container
            ),
            footer
        ]
    )

app.layout = serve_layout

if __name__ == "__main__":
	app.run_server(debug=True, host= '0.0.0.0')
