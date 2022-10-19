from deta import Deta
from utils import *
from tqdm import tqdm
from detector import Detector

db_key = "c0io5s5q_dMf99nepUqTFKxFXzyswF1rHDPFK4vDe"
deta = Deta(db_key)

db = deta.Base('density_records')
detector = Detector()

cam_id_list = ['1001',
 '1002',
 '1003',
 '1004',
 '1005',
 '1006',
 '1501',
 '1502',
 '1503',
 '1504',
 '1505',
 '1701',
 '1702',
 '1703',
 '1704',
 '1705',
 '1706',
 '1707',
 '1709',
 '1711',
 '2701',
 '2702',
 '2703',
 '2704',
 '2705',
 '2706',
 '2707',
 '2708',
 '3702',
 '3704',
 '3705',
 '3793',
 '3795',
 '3796',
 '3797',
 '3798',
 '4701',
 '4702',
 '4703',
 '4704',
 '4705',
 '4706',
 '4707',
 '4708',
 '4709',
 '4710',
 '4712',
 '4713',
 '4714',
 '4716',
 '4798',
 '4799',
 '5794',
 '5795',
 '5797',
 '5798',
 '5799',
 '6701',
 '6703',
 '6704',
 '6705',
 '6706',
 '6708',
 '6710',
 '6711',
 '6712',
 '6713',
 '6714',
 '6715',
 '6716',
 '7791',
 '7793',
 '7794',
 '7795',
 '7796',
 '7797',
 '7798',
 '8701',
 '8702',
 '8704',
 '8706',
 '9701',
 '9702',
 '9703',
 '9704',
 '9706'] # 9705 was removed for some reason by LTA

def scrape_data():
    for cam_id in tqdm(cam_id_list):
        cam_id = int(cam_id)
        record = retrieve_density(cam_id, detector)
        record["timestamp"] = record["timestamp"].astype(str)
        record = record.to_dict('records')
        db.insert({"id":cam_id, "record":record})
        print(f"Done: {cam_id}")
    

if __name__ == "__main__":
    scrape_data()
