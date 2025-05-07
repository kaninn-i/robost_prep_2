import sys
import numpy as np
import cv2
from PyQt5.QtWidgets import QComboBox, QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QMainWindow, QGridLayout
from PyQt5 import QtCore
from smart_prom_sim.mcx.mcx_control import *
import time
from gui import Ui_Form



class GuiLogs:
    def __init__(self):
        self.logs = []
        self.file_logs = []
    
    def add_log(self, log, to_file=False):
        self.logs.append(log)
        if to_file:
            self.file_logs.append(log)
    
    def get_logs(self):
        return self.logs
    
    def save_to_file(self):
        with open(".log", "w") as f:
            f.writelines([ i + "\n" for i in self.file_logs])

logs = GuiLogs()

class State:
    def __init__(self):
        self.states_list = {
            'OFF':'Выключен',
            'ON':'В работе',
            'WAIT':'Ожидает',
            'EMERGENCY':'Аварийная остановка'
        }
        #максимальная дистанция робота 0.95
        #если вводить точку [0.95, 0, 0]
        #соответсвенно если брать 3-х мероное пространство, то нужно вычислять дистанцию
        self.current_state = self.states_list['ON']

    def switch_state(self, new_state):
        self.current_state = self.states_list[new_state]
        if self.current_state == 'Аварийная остановка':
            logs.add_log(f'Состояние робота: {self.current_state}', True)
        else:
            logs.add_log(f'Состояние робота: {self.current_state}')


class RobotControlGUI(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.robot = MCX()
        self.robot.connect('192.168.2.100')
        logs.add_log('Робот подключен')
        self.robot.move_to_start()
        time.sleep(1)
        logs.add_log('Робот находится на стартовой позиции')
        self.robot_state = State()
        self.motors_list_joint = list(self.robot.get_joint_pos())
        self.motors_list_cart = list(self.robot.get_cart_pos())
        self.motor_list_actual = list()
        logs.add_log('Текущее положение:')
        logs.add_log(f"".join((str(i) for i in self.motors_list_joint)))
        self.move_variant = "J"
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.On_button.clicked.connect(self.changeOnOffState)
        self.ui.Pause_button.clicked.connect(self.changePauseState)
        self.ui.Stop_button.clicked.connect(self.changeEmergencyState)
        self.ui.gripper_button.clicked.connect(self.change_gripper_status)
        self.ui.move_cords_button.clicked.connect(self.changeRobotPosition)

        self.motors_list_auto = []
        
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

        self.Qtimer = QtCore.QTimer()
        self.Qtimer.setInterval(200)
        self.Qtimer.timeout.connect(self.update_logs)
        self.Qtimer.start()

    def testfunc():
        print('test')
        
    def update_logs(self):
        self.model_1 = QtCore.QStringListModel(self)
        self.model_1.setStringList(logs.get_logs())
        self.ui.logs_data.setModel(self.model_1)

    def update_cords(self, motor_number, x):
        if self.move_variant == "J":
            self.motors_list_actual = self.motors_list_joint
            self.motors_list_actual[motor_number-1] += x
            logs.add_log('Текущее положение:')
            logs.add_log(f" ".join(str(i) for i in self.motors_list_actual)) 
        elif self.move_variant == "L":
            self.motors_list_actual[motor_number-1] += x
            logs.add_log('Текущее положение:')
            logs.add_log(f" ".join(str(i) for i in self.motors_list_actual)) 
        
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
            logs.add_log('Режим выполнения: MoveL') 
        elif self.move_variant == "L":
            self.motors_list_actual = list(self.robot.get_joint_pos())
            self.move_variant = "J"
            logs.add_log('Режим выполнения: MoveJ')

    def change_gripper_status(self):
        _translate = QtCore.QCoreApplication.translate
        if self.robot.gripper_state == 0.0:
            self.robot.gripper_state = 1.0
            self.ui.gripper_button.setText(_translate("Form", "Отпустить"))
            logs.add_log('Захват активен')
        else:
            self.robot.gripper_state = 0.0
            self.ui.gripper_button.setText(_translate("Form", "Схватить"))
            logs.add_log('Захват отпущен')


    def changeOnOffState(self):
        _translate = QtCore.QCoreApplication.translate
        if self.robot_state.current_state == 'Выключен' or self.robot_state.current_state == 'Ожидает':
            self.ui.On_button.setText(_translate("Form", "Выкл"))
            self.robot_state.switch_state('ON')
            self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
            self.robot.move_to_start()
            time.sleep(1)
            logs.add_log('Робот включен и находится на стартовой позиции')
        else:
            self.ui.On_button.setText(_translate("Form", "Вкл"))
            self.robot_state.switch_state('OFF')
            self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
            self.robot.move_to_start()
            time.sleep(1)
            logs.add_log('Робот выключен')

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

        logs.add_log('Данные для перемещения получены')

        self.motors_list_actual = self.motors_list_auto
        self.robot.MoveL(self.motors_list_actual) # другая переменная??

        time.sleep(1)

        logs.add_log('Робот перемещён на заданную позицию')
        logs.add_log('Текущее положение:')
        logs.add_log(f" ".join(str(i) for i in self.motors_list_actual)) 

    # 3+ - навернх
    # 3- - вниз

    # def show_first_camera(self):
    #     cap = cv2.VideoCapture(2)

    #     if not cap.isOpened():
    #         print("Ошибка: камера не доступна!")
    #         exit()

    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #     cap.set(cv2.CAP_PROP_FPS, 30)

    #     import os 
    #     os.makedirs("video_frame", exist_ok=True)

    #     frame_count = 0
    #     try:
    #         while True:
    #             # Захват кадра
    #             ret, frame = cap.read()
                
    #             if not ret:
    #                 print("Ошибка: не удалось получить кадр!")
    #                 break

    #             # frame_path = f"video_frame/video.jpg"
    #             # cv2.imwrite(frame_path, frame)
    #             # frame_count +=1 

    #             time.sleep(0.1) #теперь можешь брать картинку из папки video_frame и вставлять
    #             #ее в свою гуи спасибо попробую

    #             rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             h, w, ch = rgbImage.shape
    #             bytesPerLine = ch * w
    #             convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
    #             p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
    #             self.changePixmap.emit(p)

    #             cv2.waitKey(28)

    #     except KeyboardInterrupt:
    #         print("Стриминг остановлен")


            
    #     finally:
    #         # Освобождение ресурсов
    #         cap.release()



def main():
    app = QApplication(sys.argv)
    window = RobotControlGUI()
    window.show()
    app.exec_()
    logs.save_to_file()


if __name__ == '__main__':
    main()




# label.setText()
# value/stateChanged