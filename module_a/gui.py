from design import Ui_Form
from config import Config
from robot_control import RobotController, RobotState
from mcx.mcx_control import *


import numpy as np
import cv2
import time

from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap

from logging_handler import setup_logger
logger = setup_logger(__name__)


class RobotControlGUI(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.robot_controller = RobotController(self.config.ROBOT_IP)
        self.robot_state = RobotState()
        self.robot = MCX()
        self.init_ui()
        self.init_cameras()


        self.motors_list_joint = list(self.robot.get_joint_pos())
        self.motors_list_cart = list(self.robot.get_cart_pos())
        self.motor_list_actual = list() # запихнуть в стейт?
        logger.debug(f'Текущее положение:'+ ''.join(str(i) for i in self.motors_list_joint))
        self.move_variant = "J"


    def init_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.On_button.clicked.connect(self.changeOnOffState)
        self.ui.Pause_button.clicked.connect(self.changePauseState)
        self.ui.Stop_button.clicked.connect(self.changeEmergencyState)
        self.ui.gripper_button.clicked.connect(self.change_gripper_status)
        self.ui.move_cords_button.clicked.connect(self.changeRobotPosition)

        self.motors_list_auto = [] # не должно быть тут??
        
        self.ui.comboBox.currentIndexChanged.connect(self.updateMoveVariant)
        self.ui.motor_1_minus.clicked.connect(lambda: self.update_cords(1, -0.05))
        self.ui.motor_1_plus.clicked.connect(lambda: self.update_cords(1, 0.05))
        self.ui.motor_2_minus.clicked.connect(lambda: self.update_cords(2, -0.05))
        self.ui.motor_2_plus.clicked.connect(lambda: self.update_cords(2, 0.05))
        self.ui.motor_3_minus.clicked.connect(lambda: self.update_cords(3, -0.05))
        self.ui.motor_3_plus.clicked.connect(lambda: self.update_cords(3, 0.05))
        self.ui.motor_4_plus.clicked.connect(lambda: self.update_cords(4, -0.05))
        self.ui.motor_5_plus.clicked.connect(lambda: self.update_cords(4, 0.05))
        self.ui.motor_5_minus.clicked.connect(lambda: self.update_cords(5, -0.05))
        self.ui.motor_4_minus.clicked.connect(lambda: self.update_cords(5, 0.05))
        self.ui.motor_6_minus.clicked.connect(lambda: self.update_cords(6, -0.05))
        self.ui.motor_6_plus.clicked.connect(lambda: self.update_cords(6, 0.05))

        # self.Qtimer = QtCore.QTimer()
        # self.Qtimer.setInterval(200)
        # self.Qtimer.timeout.connect(self.update_logs)
        # self.Qtimer.start()
        
        
    def init_cameras(self):
        # #  -------------------- камеры ------------
        self.cap1 = cv2.VideoCapture(0)  # Первая камера
        self.cap2 = cv2.VideoCapture(0)  # Вторая камера (если есть)
        self.cap3 = cv2.VideoCapture(0)  # Третья камера (если есть)
        
        # QLabel для отображения видео внутри фреймов
        self.video_label1 = QLabel(self.ui.videoframe_1)
        self.video_label1.resize(340, 260)
        self.video_label1.setScaledContents(True)

        self.video_label2 = QLabel(self.ui.videoframe_2)
        self.video_label2.resize(340, 260)
        self.video_label2.setScaledContents(True)

        self.video_label3 = QLabel(self.ui.videoframe_3)
        self.video_label3.resize(340, 260)
        self.video_label3.setScaledContents(True)

        # таймер для обновления видео
        self.video_timer = QtCore.QTimer()
        self.video_timer.timeout.connect(self.update_frames)
        self.video_timer.start(30)  # 30 ms интервал

    def testfunc():
        print('test')
        
    # def update_logs(self):
    #     self.model_1 = QtCore.QStringListModel(self)
    #     self.model_1.setStringList(logs.get_logs())
    #     self.ui.logs_data.setModel(self.model_1)

    def update_cords(self, motor_number, x):
        if self.move_variant == "J":
            self.motors_list_actual = self.motors_list_joint
            self.motors_list_actual[motor_number-1] += x
            logger.debug(f'Текущее положение:'+ ''.join(str(i) for i in self.motors_list_actual))
        elif self.move_variant == "L":
            self.motors_list_actual[motor_number-1] += x
            logger.debug(f'Текущее положение:'+ ''.join(str(i) for i in self.motors_list_actual))

        self.move_hand()   

    def move_hand(self):
        if self.move_variant == "J":
            self.robot.MoveJ(self.motors_list_actual)
        elif self.move_variant == "L":
            self.robot.MoveL(self.motors_list_actual)


    def updateMoveVariant(self):
        if self.move_variant == "J":
            self.motors_list_actual = list(self.robot.get_cart_pos())
            self.move_variant = "L"
         
        elif self.move_variant == "L":
            self.motors_list_actual = list(self.robot.get_joint_pos())
            self.move_variant = "J"

        logger.debug(f'Режим выполнения: Move{self.move_variant}')

    def change_gripper_status(self):
        _translate = QtCore.QCoreApplication.translate
        if self.robot.gripper_state == 0.0:
            self.robot.gripper_state = 1.0
            self.ui.gripper_button.setText(_translate("Form", "Отпустить"))
            
            logger.debug('Захват активен')
        else:
            self.robot.gripper_state = 0.0
            self.ui.gripper_button.setText(_translate("Form", "Схватить"))
            logger.debug('Захват отпущен')


    def changeOnOffState(self):
        _translate = QtCore.QCoreApplication.translate
        if self.robot_state.current_state == 'Выключен' or self.robot_state.current_state == 'Ожидает':
            self.ui.On_button.setText(_translate("Form", "Выкл"))
            self.robot_state.switch_state('ON')
            self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
            self.robot.move_to_start()
            time.sleep(1)
            logger.debug('Робот включен и находится на стартовой позиции')

        else:
            self.ui.On_button.setText(_translate("Form", "Вкл"))
            self.robot_state.switch_state('OFF')
            self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
            self.robot.move_to_start()
            time.sleep(1)
            logger.debug('Робот выключен')

    def changePauseState(self):
        _translate = QtCore.QCoreApplication.translate
        self.robot_state.switch_state('WAIT')
        self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
        self.ui.On_button.setText(_translate("Form", "Вкл"))

    def changeEmergencyState(self):
        _translate = QtCore.QCoreApplication.translate
        self.robot_state.switch_state('EMERGENCY')
        self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))

    def changeRobotPosition(self):
        for row in range(self.ui.move_cords_table.rowCount()):
            for column in range(self.ui.move_cords_table.columnCount()):
                self.motors_list_auto.append(self.ui.move_cords_table.item(row, column).data(2))
        for i, l in enumerate(self.motors_list_auto):
            self.motors_list_auto[i] = float(l)

        logger.debug('Данные для перемещения получены')

        self.motors_list_actual = self.motors_list_auto
        self.robot.MoveL(self.motors_list_actual) # другая переменная??

        time.sleep(1)


        logger.debug('Робот перемещён на заданную позицию')
        logger.debug(f'Текущее положение:'+ ''.join(str(i) for i in self.motors_list_actual)) 

    def update_frames(self):
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
                frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                img2 = QImage(frame2, frame2.shape[1], frame2.shape[0], QImage.Format_RGB888)
                self.video_label2.setPixmap(QPixmap.fromImage(img2))

        # 3ий фрейм
        if self.cap3.isOpened():
            ret3, frame3 = self.cap3.read()
            if ret3:
                frame3 = self.process_frame(frame3)
                # frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
                # img3 = QImage(frame3, frame3.shape[1], frame3.shape[0], QImage.Format_RGB888)
                img3 = QImage(frame3.data, frame3.shape[1], frame3.shape[0], 
                        QImage.Format_RGB888).rgbSwapped()
                self.video_label3.setPixmap(QPixmap.fromImage(img3))

    # освобождение ресурсов при закрытии
    def closeEvent(self, event):
        self.cap1.release()
        self.cap2.release()
        self.cap3.release()
        event.accept()

    