import dash
from dash.dependencies import Input, Output, State
from dash import html, callback
import os
import dash_bootstrap_components as dbc
import folium
from folium import IFrame
import pandas as pd
import base64

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
    
    for camID,img_src,lat,lon,d1,den1,pro1,d2,den2,pro2 in list_data:
        img = rf'src/assets/imageCurrShown/{img_src}'
        
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
        
        #html for popup markers
        html = '<img src="data:image/jpeg;base64,{}", style="width:85%; height:65%; margin:0px 8px">'.format
        encoded = base64.b64encode(open(img, 'rb').read()).decode('UTF-8')
        
        full =  ''' <html>
                    <head>The location is {}, {}</head>
                    </br>
                    {}
                    </br>
                    <section style = "background-color:#C0D6DF; display: inline-block; padding: 20px">
                    direction towards {}</br>
                    density is {} </br>
                    probability of traffic jam is {:.3f}
                    </section>
                    <section style = "background-color:#6bf766; display: inline-block; padding: 20px">
                    direction towards {}</br>
                    density is {} </br>
                    probability of traffic jam is {:.3f}
                    </section>
                    <html/>'''.format(lat,lon,html(encoded),d1,den1,pro1,d2,den2,pro2)
        
        iframe = IFrame(full)
        folium.Marker([lat, lon],
            popup=folium.Popup(iframe
            , max_width=650,min_width=600),
            icon=folium.Icon(color=c)
            ).add_to(m)
        
    if os.path.exists("folium_map.html"):
        os.remove("folium_map.html")

    m.save("folium_map.html")

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
        map1
    ],fluid=True, style={'padding':0, 'margin':0}
)

@callback(Output('map', 'srcDoc'), 
        Input(component_id='current-predictions', component_property='data'))         
def refresh_map(json_data):
    if json_data is not None:
        df = pd.read_json(json_data, orient = "split")
    else:
        df = pd.read_csv(r"src/assets/backup.csv")
    make_map(df)
    return open('folium_map.html','r').read()