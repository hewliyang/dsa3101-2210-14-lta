import os
import folium
import json

def get_data():
    #load JSON to dict
    #url = ''
    #r1 = requests.get(url) 
    #data = json.loads(js)

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
        folium.Marker([i['latitude'], i['longitude']],
            popup=folium.Popup(f"density is {i['density']}" 
            f"speed band is {i['speed']}" 
            f"probability of traffic jam is {i['prob']}"
            , max_width=200,min_width=200),
            icon=folium.Icon(color=c)
            ).add_to(m)
    if os.path.exists("folium_map.html"):
        os.remove("folium_map.html")

    m.save("folium_map.html")