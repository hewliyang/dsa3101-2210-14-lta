import dash
from dash.dependencies import Input, Output, State
from dash import html, callback
import os
import dash_bootstrap_components as dbc
import folium
import json
import pandas as pd
# from components import header, nav
dash.register_page(
	__name__,
	path='/map',
	title='Map'
)

# def get_data():

#     #columns=['CameraID', 'imageFile', 'Latitude', 'Longitude', 'dir1', 'density1', 'prob1', 'dir2', 'density2', 'prob2']
#     #dummy data
#     data = {1:{"CameraID": 1701, "latitude": 1.290270,"longitude": 103.851959,"ImageLink":"some link","timestamp": 1,"density1": 35, "density2": 60, "prob1": 0.3, "prob2":0.71},
#             2:{"CameraID": 1702,"latitude": 1.292270,"longitude": 103.852959,"ImageLink":"some link","timestamp": 1,"density1": 45, "density2": 40, "prob1": 0.5, "prob2":0.6},
#             3:{"CameraID": 1703,"latitude": 1.280270,"longitude": 103.861959,"ImageLink":"some link","timestamp": 1,"density1": 35, "density2": 10, "prob1": 0.3, "prob2":0.1},
#             4:{"CameraID": 1704,"latitude": 1.280170,"longitude": 103.851659,"ImageLink":"some link","timestamp": 1,"density1": 25, "density2": 45, "prob1": 0.2, "prob2":0.71},
#             5:{"CameraID": 1705,"latitude": 1.3521,"longitude": 103.8198,"ImageLink":"some link","timestamp": 1,"density1": 55, "density2": 62, "prob1": 0.6, "prob2":0.7}
#             }
#     return data

def make_map(df):
    #columns=['CameraID', 'imageFile', 'Latitude', 'Longitude', 'dir1', 'density1', 'prob1', 'dir2', 'density2', 'prob2']
    m = folium.Map(location= [1.3621, 103.8198], 
                   zoom_start= 12, 
                   max_zoom = 12, 
                   min_zoom =12, 
                   zoom_control=False)
    
    list_data = list(zip(df['CameraID'],df['imageFile'],df['Latitude'],df['Longitude'],df['dir1'],df['density1'],df['prob1'],df['dir2'],df['density2'],df['prob2']))
    
    for camID,img,lat,lon,d1,den1,pro1,d2,den2,pro2 in list_data:
        #change to each direction
        # camID = i['CameraID']
        # img = i['imageFile']
        # den1 = i['density1']
        # den2 = i['density2']
        # pro1 = i['prob1']
        # pro2 = i['prob2']
        # lat = i['latitude']
        # lon = i['longitude']
        
        #take higher probability
        pro = pro1
        if pro < pro2:
            pro = pro2
        
        #colour-coding based on probability
        c = "green"
        if pro > 0.7:
            c = "red"
        elif pro > 0.3:
            c = "orange"
        
        
        #still need include img tag in pop_html
        pop_html = f'''<html> 
                    <head>The location is {lat}, {lon}</head>
                    </br>
                    <img src = {img}, alt = "camera image"/>
                    </br>
                    <section style = "background-color:#C0D6DF; display: inline-block; padding: 30px">
                    upwards facing direction </br>
                    density is {den1} </br>
                    probability of traffic jam is {pro1:.3f}
                    </section>
                    <section style = "background-color:#6bf766; display: inline-block; padding: 30px">
                    downwards facing direction </br>
                    density is {den2} </br>
                    probability of traffic jam is {pro2:.3f}
                    </section>
                    </html>'''
        iframe = folium.IFrame(pop_html)
        folium.Marker([lat, lon],
            popup=folium.Popup(iframe
            , max_width=650,min_width=600),
            icon=folium.Icon(color=c)
            ).add_to(m)
        
    if os.path.exists("folium_map.html"):
        os.remove("folium_map.html")

    m.save("folium_map.html")
    
# dat = get_data()
# make_map(dat)

map1 = html.Div(
    [
        dbc.Row(
            [
                html.Iframe(id = "map", srcDoc = 'folium_map.html', width = '100%', height = '100%')
                
            ],style={"height": "90vh", 'padding':'2.5vh'}
        )
    ]
)


layout = dbc.Container(
    [
        html.Div(id='dummy_input', style={'display':"None"}),
        map1
    ],fluid=True, style={'padding':0, 'margin':0}
)

@callback(Output('map', 'srcDoc'), 
        Input('dummy_input', 'children'),
        Input(component_id='current-predictions', component_property='data'))         
def refresh_map(children,json_data):
    df = pd.read_json(json_data, orient = "split")
    make_map(df)
    return open('folium_map.html','r').read()