import cv2
from ultralytics import YOLO
from typing import List


class ObjectDetector:
    """Класс для обнаружения объектов на изображениях.
    Использует модели YOLO, по дефолту модель yolo11s-seg"""
    def __init__(self, model="yolo11s-seg.pt") -> None:
        self.model = YOLO(model)

    async def detect_objects(self, image_path: str) -> List[str]:
        """Обнаружение объектов на изображении"""
        image = cv2.imread(image_path)

        if image is None:
            print(f"Ошибка загрузки изображения: {image_path}")
            return []

        results = self.model(image)[0]

        classes_ids = results.boxes.cls.cpu().numpy().astype(int)

        classes_names = results.names
        detected_objects = [classes_names[class_id] for class_id in classes_ids]

        return detected_objects


