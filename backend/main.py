import fastapi
import json
from fastapi.responses import HTMLResponse, ORJSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils import *
from detector import Detector

# initialise Detector object
global detector
detector = Detector()

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
        return Response(retrieve_density_both(cameraID, detector).
        to_json(orient="records"),
        media_type="application/json")
    return None

@app.get("/api/v1/batch_inference")
async def get_batch_inference():
    return Response(batch_retrieve_dense_prob(detector).
    to_json(orient="records"),
    media_type="application/json")
