import fastapi
import json
from fastapi.responses import HTMLResponse, ORJSONResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import *
from detector import Detector
from deta import Deta
from dotenv import load_dotenv
import os
import requests

#initialise API keys
load_dotenv()
DB_KEY = os.getenv('DB_KEY')

# initialise Detector object
global detector
detector = Detector()

# initialise DB object
deta = Deta(DB_KEY)

description = """
Available endpoints are as listed below.  

### Notice
**batch_inference** is unstable as the request takes a while. It may timeout depending on how
fast the host system is.
"""

app = fastapi.FastAPI(
    title = "Traffic Prediction API",
    description = description,
    version = "0.0.1"
    )

db = deta.Base("density")
bucket = deta.Drive("latest-images")

app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="assets")


@app.get("/", response_class=HTMLResponse)
async def root(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/cam_metadata")
async def get_cam_metadata():
    return ORJSONResponse(content = 
    json.load(open("metadata/camera_info.txt")))

@app.get("/api/v1/cam_images")
async def get_images():
    return Response(retrieve_images().to_json(orient="records"),
    media_type="application/json")

@app.get("/api/v1/speed_bands")
async def get_speed_bands():
    return Response(retrieve_speedbands().to_json(orient="records"),
    media_type="application/json")

@app.get("/api/v1/traffic_incidents")
async def get_traffic_incidents():
    return Response(retrieve_incidents().to_json(orient="records"),
    media_type="application/json")

@app.get("/api/v1/density")
async def get_density(cameraID: int):
    if cameraID:
        # push/update latest image into storage bucket(images), drive(json)
        data = retrieve_density_both(cameraID, detector)
        image_link = data["ImageLink"].iloc[0]
        image_bytes = requests.get(image_link).content
    
        d_data = data.to_json(orient="records")

        bucket.put(f"{cameraID}.jpg", data=image_bytes)
        db.put(d_data, key=str(cameraID))
        
        return Response(d_data, media_type="application/json")
    return None

@app.get("/api/v1/batch_inference")
async def get_batch_inference():
    return Response(batch_retrieve_dense_prob(detector).
    to_json(orient="records"),
    media_type="application/json")
    
@app.get("/api/v1/image")
async def get_image(cameraID: int):
    img = bucket.get(f"{cameraID}.jpg")
    if img:
        return StreamingResponse(img.iter_chunks(), media_type="image/jpg")
    else:
        return f"Inference has not yet been made for camera ID : {cameraID}. Call density first."

@app.get("/api/v1/record")
async def get_record(cameraID: int):
    record = db.get(f"{cameraID}")
    if record:
        return Response(record["value"], media_type="application/json")
    else:
        return f"Inference has not yet been made for camera ID : {cameraID}. Call density first."

@app.get("/api/v1/debug")
async def debug(cameraID: int):
    return Response(retrieve_density_both(cameraID, detector).
    to_json(orient="records"),
    media_type="application/json")