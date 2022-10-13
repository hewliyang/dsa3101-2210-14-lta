import dash
from dash.dependencies import Input, Output, State
from dash import html, callback
import os
import dash_bootstrap_components as dbc
import folium
import json
# from components import header, nav
dash.register_page(
	__name__,
	path='/map',
	title='Map'
)

def get_data():
    #load JSON to dict
    #url = ''
    #r1 = requests.get(url) 
    #data = json.loads(js)

    #dummy data
    data = {1:{"latitude": 1.290270,"longitude": 103.851959,"density": 35, "speed": 60, "prob": 0.7},
            2:{"latitude": 1.292270,"longitude": 103.852959,"density": 35, "speed": 60, "prob": 0.8},
            3:{"latitude": 1.280270,"longitude": 103.861959,"density": 35, "speed": 60, "prob": 0.2},
            4:{"latitude": 1.280170,"longitude": 103.851659,"density": 35, "speed": 60, "prob": 0.6},}
    return data

def make_map(data):
    m = folium.Map(location= [1.3521, 103.8198], zoom_start= 12)
    for i in data.values():
        c = "green"
        if i['prob'] > 0.7:
            c = "red"
        elif i['prob'] > 0.3:
            c = "orange"
        den = i['density']
        pro = i['prob']
        lat = i['latitude']
        lon = i['longitude']
        #still need include img tag in pop_html
        pop_html = f'''<html> 
                    <head>The location is {lat}, {lon}</head>
                    density is {den} </br>
                    probability of traffic jam is {pro}
                    </html>'''
        iframe = folium.IFrame(pop_html)
        folium.Marker([lat, lon],
            popup=folium.Popup(iframe
            , max_width=250,min_width=300),
            icon=folium.Icon(color=c)
            ).add_to(m)
    if os.path.exists("folium_map.html"):
        os.remove("folium_map.html")

    m.save("folium_map.html")
    
dat = get_data()
make_map(dat)

map1 = html.Div(
    [
        dbc.Row(
            [
                html.P("The Map"),
                html.Iframe(id = "map", srcDoc = 'folium_map.html', width = '90%', height = '650')
                
            ]
        )
    ]
)


layout = dbc.Container(
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

@callback(Output('map', 'srcDoc'), 
              Input('dummy_input', 'children'))         
def refresh_map(children):
    dat = get_data()
    make_map(dat)
    return open('folium_map.html','r').read()