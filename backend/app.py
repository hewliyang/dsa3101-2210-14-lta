from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
import json
import pandas as pd
from utils import *

app = Flask(__name__)
api = Api(app)

# returns camera metadata for each cameraID
# consists of {Latitude, Longitude,Dir1Distance, Dir2Distance, Dir1Lanes, Dir2Lanes, DirCoords}
class CameraMetadata(Resource):
    def get(self):
        return json.load(open("metadata/camera_info.txt"))

# returns links to all camera images along with the time fetched
# schema : {CameraID, Latitude, Longitude, ImageLink, timestamp}
# TO FIX : timestamp (datetime) object is not serializable in JSON. need to convert it to ISO format string
class CameraImages(Resource):
    def get(self):
        return Response(retrieve_images().to_json(orient="records"),
            mimetype='application/json')

# returns speed band information for all 500 observed road sections
# schema : {LinkID,RoadName,RoadCategory,SpeedBand,MinimumSpeed,MaximumSpeed,latitude1,longitude1,latitude2,longitude2,distance,timestamp}
class SpeedBands(Resource):
    def get(self):
        return Response(retrieve_speedbands().to_json(orient="records"),
            mimetype='application/json')

# returns all traffic incidents at time of requests
# schema : {Type,Latitude,Longitude,Message,timestamp}
class TrafficIncidents(Resource):
    def get(self):
        return Response(retrieve_incidents().to_json(orient="records"),
            mimetype='application/json')

# returns the traffic density for 2 directions for a given CameraID at time of request
# Typically, dir1 = North and dir2 = South
# this functions performs alot of image pre-processing and running a YOLOv4 model, so expect some time lag
# schema : {CameraID, Latitude, Longitude, ImageLink, timestamp, density1, density2}
class TrafficDensity(Resource):
    def get(self):
        cameraID = request.args.get('cameraID')
        return Response(retrieve_density(cameraID).to_json(orient="records"),
            mimetype='application/json')


api.add_resource(CameraMetadata, '/api/v1/cam_metadata')
api.add_resource(CameraImages, '/api/v1/cam_images')
api.add_resource(SpeedBands, '/api/v1/speed_bands')
api.add_resource(TrafficIncidents, '/api/v1/traffic_incidents')
api.add_resource(TrafficDensity, '/api/v1/density')

if __name__ == '__main__':
    app.run(debug=True)