import sys
import cv2
from sahi.utils.cv import read_image_as_pil
from sahi.predict import get_sliced_prediction
from detector import Detector

# returns the number of vehicles in the image
def getVehicleCount(img):
    detector = Detector()
    obj_pred_list = detector.detect_vehicles(img)
    count = 0
    for obj in obj_pred_list:
        id = obj.category.id
        if (id == 2 or id == 3 or id == 5 or id == 7):
            count += 1
    return count

if __name__ == "__main__":

    detector = Detector()
    filepath = sys.argv[1]
    img = cv2.imread(filepath)

    # get predictions
    result = get_sliced_prediction(
        img,
        detector.model,
        slice_height = 512,
        slice_width = 512,
        overlap_height_ratio = 0.2,
        overlap_width_ratio = 0.2
        )
    result.export_visuals(export_dir='.')


