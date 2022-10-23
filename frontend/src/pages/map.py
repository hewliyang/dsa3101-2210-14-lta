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
            4:{"latitude": 1.280170,"longitude": 103.851659,"density": 35, "speed": 60, "prob": 0.6},
            5:{"latitude": 1.3521,"longitude": 103.8198,"density": 35, "speed": 60, "prob": 0.6}}
    return data

def make_map(data):
    m = folium.Map(location= [1.3621, 103.8198], 
                   zoom_start= 12, 
                   max_zoom = 12, 
                   min_zoom =12, 
                   zoom_control=False)
    for i in data.values():
        #change to each direction
        den = i['density']
        pro = i['prob']
        lat = i['latitude']
        lon = i['longitude']
        
        c = "green"
        if pro > 0.7:
            c = "red"
        elif pro > 0.3:
            c = "orange"
        
        #still need include img tag in pop_html
        pop_html = f'''<html> 
                    <head>The location is {lat}, {lon}</head>
                    </br>
                    <img src = "", alt = "camera image"/>
                    </br>
                    <section style = "background-color:#C0D6DF; display: inline-block; padding: 30px">
                    density is {den} </br>
                    probability of traffic jam is {pro}
                    </section>
                    <section style = "background-color:#6bf766; display: inline-block; padding: 30px">
                    density is {den} </br>
                    probability of traffic jam is {pro}
                    </section>
                    </html>'''
        iframe = folium.IFrame(pop_html)
        folium.Marker([lat, lon],
            popup=folium.Popup(iframe
            , max_width=550,min_width=600),
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
                html.Iframe(id = "map", srcDoc = 'folium_map.html', width = '100%', height = '100%')
                
            ],style={"height": "85vh"}
        )
    ]
)


layout = dbc.Container(
    [
        html.Div(id='dummy_input'),
        html.Br(),
        map1,
        html.Br()
    ],fluid=True
)

@callback(Output('map', 'srcDoc'), 
        Input('dummy_input', 'children'))         
def refresh_map(children):
    dat = get_data()
    make_map(dat)
    return open('folium_map.html','r').read()