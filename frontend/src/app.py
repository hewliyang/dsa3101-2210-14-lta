"""
This file is for the main dash application
"""
# TODO: UNSURE WHY CONNECTION IS REFUSED WHEN TRYING TO RUN RESULT_GENERATOR
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dcc
from dash.dependencies import Input, Output
from flask import Flask
from components import sidebar, navbar
import redis
import pickle

server = Flask(__name__)
app = dash.Dash(
	__name__,
	server=server,
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
			navbar,
			sidebar,
			dbc.Container([
				dash.page_container
				],
				id="page-content",
				fluid=True,
				style={"height":"90vh", "transition": "margin-right .5s", "width":"auto", "padding":0, "margin":0, 'max-height':"90vh"}
			),
			dcc.Interval(id='update-predictions', interval=180000, n_intervals=0), # Every 3mins check
			dcc.Store(id='current-predictions', storage_type='local', clear_data=True)
		]
	)

app.layout = serve_layout

@app.callback(Output('current-predictions', 'data'), Input('update-predictions', 'n_intervals'), prevent_initial_call = True) 
def generate_predictions(n):
	redisConnection = redis.Redis(host='redis-cache', port=6379, db=0)
	predictions_df = pickle.loads(redisConnection.get("currDisplay"))
	return predictions_df.to_json(date_format='iso', orient = 'split')

if __name__ == "__main__":
	app.run_server(debug=True, dev_tools_hot_reload=False, use_reloader=False)
