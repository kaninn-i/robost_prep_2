import cv2
import numpy as np
from ultralytics import YOLO
import torch

# model = YOLO(path)

from ultralytics import YOLO
import cv2

from module_a.logging_handler import setup_logger
logger = setup_logger(__name__)

class YoloProcessor:
    def __init__(self, model_path='module_d/runs/detect/yolov8s_3epo/weights/best.pt'):
        """
        Инициализация YOLO модели
        :param model_path: путь к файлу модели .pt
        """
        self.model = YOLO(model_path)  # Загрузка модели
        self.model.fuse()
        self.class_names = self.model.names  # Получение названий классов

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f'Используемое устройство для модели: {self.device}')
        self.model.to(self.device)
    
    def process_frame(self, frame):
        """
        Обработка кадра с помощью YOLO
        :param frame: входной кадр (numpy array)
        :return: обработанный кадр с bounding boxes, список обнаруженных объектов
        """
        # Выполнение предсказания
        results = self.model.predict(frame, conf=0.5, verbose=False)
        
        # Визуализация результатов
        annotated_frame = results[0].plot()
        
        # Сбор информации об обнаруженных объектах
        detected_objects = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls.item())
                confidence = box.conf.item()
                bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                
                detected_objects.append({
                    'class': self.class_names[class_id],
                    'confidence': confidence,
                    'bbox': bbox
                })
        
        return annotated_frame, detected_objects