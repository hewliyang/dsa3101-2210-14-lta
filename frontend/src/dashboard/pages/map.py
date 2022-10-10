import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import folium
import json
import folium_map as fm
# from components import header, nav

app = dash.Dash(__name__)

dash.register_page(
	__name__,
	path='/map',
	title='Map'
)

dat = fm.get_data()
fm.make_map(dat)

map1 = html.Div(
    [
        dbc.Row(
            [
                html.P("The Map"),
                html.Iframe(id = "map", srcDoc = open('folium_map.html','r').read(), width = '90%', height = '650')
                
            ]
        )
    ]
)


app.layout = dbc.Container(
    [
        #header func,
        html.Br(),
        html.H1('title'),
        html.Br(),
        #nav func,
        map1,
        html.Br(),
        #footer func
        html.Div(id='dummy_input')
    ]
)

@app.callback(Output('map', 'srcDoc'), 
              Input('dummy_input', 'children'))
              
def refresh_map(children):
    dat = fm.get_data()
    fm.make_map(dat)
    return open('folium_map.html','r').read()
    

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')