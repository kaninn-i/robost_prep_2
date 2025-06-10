from module_c.gui import CvGui
import cv2
from PyQt5.QtGui import QImage, QPixmap
from module_d.yolo_processing import YoloProcessor


class FinalGui(CvGui):
    def __init__(self):
        super().__init__()
        self.yolo_processor = YoloProcessor()


    def update_frames(self):
        super().update_frames()

        if self.cap3.isOpened():
            ret3, frame3 = self.cap3.read()
            if ret3:
                # Обработка кадра YOLO
                frame3, yolo_objects = self.yolo_processor.process_frame(frame3)
                
                # Конвертация для отображения
                frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
                img3 = QImage(frame3, frame3.shape[1], frame3.shape[0], 
                             QImage.Format_RGB888)
                self.video_label3.setPixmap(QPixmap.fromImage(img3))
                
                # Обновление информации об объектах
                if yolo_objects:
                    # Формируем строку с информацией
                    obj_info = "\n".join([
                        f"{obj['class']} ({obj['confidence']:.2f})" 
                        for obj in yolo_objects
                    ])
                    self.ui.model_data.setText(obj_info)