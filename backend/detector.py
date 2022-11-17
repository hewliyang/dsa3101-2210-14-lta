from mmdet.apis import init_detector, inference_detector
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction, predict
from sahi.utils.cv import read_image_as_pil

CONFIG_FILE_PATH = 'models/yolox_tiny_8x8_300e_coco.py'
MODEL_FILE_PATH = 'models/yolox_tiny_8x8_300e_coco_20211124_171234-b4047906.pth'

class Detector:

    def __init__(self):
        self.model = AutoDetectionModel.from_pretrained(
            model_type='mmdet',
            model_path = MODEL_FILE_PATH,
            config_path = CONFIG_FILE_PATH,
            confidence_threshold = 0.2,
            device = 'cpu'
        )

    def detect_vehicles(self, img):
        result = get_sliced_prediction(
        img,
        self.model,
        slice_height = 512,
        slice_width = 512,
        overlap_height_ratio = 0.2,
        overlap_width_ratio = 0.2
        )
        return result.object_prediction_list
