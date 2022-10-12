import cv2

class Detector:

    def __init__(self):
        net = cv2.dnn.readNet("models/yolov4.weights", "models/yolov4.cfg")
        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(832, 832), scale=1/255)
        self.classes_allowed = {2,3,5,6,7} # vehicles only

    def detect_vehicles(self, img):
        vehicles_boxes = []
        class_ids, scores, boxes = self.model.detect(img, confThreshold = 0.2, nmsThreshold=0.4)
        for class_id, box in zip(class_ids, boxes):
            if class_id in self.classes_allowed:
                vehicles_boxes.append(box)
        return vehicles_boxes
