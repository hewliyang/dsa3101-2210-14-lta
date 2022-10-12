import sys
import cv2
from detector import Detector

# Make sure to have opencv pip installed
# python count.py path_to_img

# returns the number of vehicles in the image
def getVehicleCount(img):
    detector = Detector()
    bbs = detector.detect_vehicles(img)
    return len(bbs)

if __name__ == "__main__":

    detector = Detector()
    filepath = sys.argv[1]
    img = cv2.imread(filepath)

    # get bounding boxes
    bb = detector.detect_vehicles(img)
    count = len(bb)

    for box in bb:
        x, y, w, h = box
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

        cv2.putText(img, "vehicle_count: " + str(count), (50,50), cv2.FONT_HERSHEY_COMPLEX, 2, (0,255,0), 3)

    cv2.imshow("test", img)
    cv2.waitKey(0)
