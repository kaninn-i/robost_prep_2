from module_b.gui import AutomaticGUI

import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

from module_c.video_processing import VideoProcessor


class CvGui(AutomaticGUI):
    def __init__(self):
        super().__init__()
        self.video_processor = VideoProcessor()
        self.init_cameras()


    def init_cameras(self):
        '''Инициализация камер и отображения видео'''

        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(0)
        self.cap3 = cv2.VideoCapture(0)
        
        # QLabel для отображения видео внутри фреймов
        self.video_label1 = QLabel(self.ui.videoframe_1)
        self.video_label1.resize(320, 180)
        self.video_label1.setScaledContents(True)

        self.video_label2 = QLabel(self.ui.videoframe_2)
        self.video_label2.resize(320, 180)
        self.video_label2.setScaledContents(True)

        self.video_label3 = QLabel(self.ui.videoframe_3)
        self.video_label3.resize(320, 180)
        self.video_label3.setScaledContents(True)

        # таймер для обновления видео
        self.video_timer = QtCore.QTimer()
        self.video_timer.timeout.connect(self.update_frames)
        self.video_timer.start(30)  # 30 ms интервал
    
    def update_frames(self):
        '''Ф-я для обновления кадров на камерах'''
        # 1й фрейм
        ret1, frame1 = self.cap1.read()
        if ret1:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            img1 = QImage(frame1, frame1.shape[1], frame1.shape[0], QImage.Format_RGB888)
            self.video_label1.setPixmap(QPixmap.fromImage(img1))

        # 2й фрейм
        if self.cap2.isOpened():
            ret2, frame2 = self.cap2.read()
            if ret2:
                frame2, shape, color_name = self.video_processor.process_frame(frame2)

                img2 = QImage(frame2.data, frame2.shape[1], frame2.shape[0], 
                        QImage.Format_RGB888).rgbSwapped()
                self.video_label2.setPixmap(QPixmap.fromImage(img2))

                self.ui.color_data.setText(color_name)
                self.ui.shape_data.setText(shape)
      

    # освобождение ресурсов при закрытии
    def closeEvent(self, event):
        self.cap1.release()
        self.cap2.release()
        self.cap3.release()
        event.accept()
