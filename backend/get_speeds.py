from deta import Deta
from utils import *
from tqdm import tqdm
from detector import Detector

db_key = "c02vlv6g_FTeny6UiDCzQs2QX1AUZrQg6UoZRin8h"
deta = Deta(db_key)

db = deta.Base('density_speed_records')
detector = Detector()

cam_id_list = [
 '6708',
 '6710',
]

def scrape_data():
    for cam_id in tqdm(cam_id_list):
        cam_id = int(cam_id)
        record = retrieve_density(cam_id, detector)
        record["timestamp"] = record["timestamp"].astype(str)
        df = retrieve_speedbands()
        if cam_id == 6708:
            record["speedband"] = df[df['LinkID'] == str(103000078)]['MinimumSpeed'].astype(str).astype(int).values
        elif cam_id == 6710:
            record["speedband"] = df[df['LinkID'] == str(103000080)]['MinimumSpeed'].astype(str).astype(int).values
        record = record.to_dict('records')
        db.insert({"id":cam_id, "record":record})
        print(f"Done: {cam_id}")


if __name__ == "__main__":
    scrape_data()
