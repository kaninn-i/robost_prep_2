from module_a.design import Ui_Form
from module_a.config import Config
from module_a.robot_control import RobotState

from mcx.mcx_control import *

import time
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

from module_a.logging_handler import setup_logger, QtLogHandler

class RobotControlGUI(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.robot = MCX()
        self.robot_state = RobotState()

        self.robot.connect(self.config.ROBOT_IP)

        self.init_ui()
        self.setup_logging()

        self.logger.info(f'Текущее положение: '+ ' '.join(str(i) for i in self.robot.get_joint_pos()))
        self.motors_list_actual = list()

    def setup_logging(self):
        '''Подключение сигнала к виджету'''
        self.logger = setup_logger(__name__)
        
        for handler in self.logger.handlers:
            if isinstance(handler, QtLogHandler):
                handler.log_signal.connect(self.append_log)
                break

    def append_log(self, text):
        """Добавление логов в QPlainTextEdit"""
        self.ui.logs_plaintext.appendPlainText(text)
        # автопрокрутка к новому сообщению
        scrollbar = self.ui.logs_plaintext.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def init_ui(self):
        '''Подключение модуля с дизайном gui'''
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.On_button.clicked.connect(self.changeOnOffState)
        self.ui.Pause_button.clicked.connect(self.changePauseState)
        self.ui.Stop_button.clicked.connect(self.changeEmergencyState)
        self.ui.gripper_button.clicked.connect(self.change_gripper_status)

        self.ui.comboBox.currentIndexChanged.connect(self.updateMoveVariant)
        for motor_num in range(1, 7):  # Для моторов от 1 до 6
            
            minus_button = getattr(self.ui, f'motor_{motor_num}_minus')
            plus_button = getattr(self.ui, f'motor_{motor_num}_plus')
            
            minus_button.clicked.connect(lambda _, m=motor_num: self.update_cords(m, -0.05))
            plus_button.clicked.connect(lambda _, m=motor_num: self.update_cords(m, 0.05))
        
    def update_cords(self, motor_number, x):
        '''Ф-я, обновляющая координаты для их дальнейшего вывода или
          перемещения на них, в зависимости от стиля движения'''
        
        if self.robot_state.current_move_variant == "J":
            self.motors_list_actual = self.robot.get_joint_pos()
            self.motors_list_actual[motor_number-1] += x

        elif self.robot_state.current_move_variant == "L":
            self.motors_list_actual = self.robot.get_linear_pos()
            self.motors_list_actual[motor_number-1] += x

        elif self.robot_state.current_move_variant == "C":
            self.motors_list_actual = self.robot.get_cart_pos()
            self.motors_list_actual[motor_number-1] += x
            
        self.logger.info(f'Текущее положение: '+ ' '.join(str(i) for i in self.motors_list_actual))
        self.move_hand()   

    def move_hand(self):
        '''Движение робота в зависимости от текущего стиля движения'''
        if self.robot_state.current_move_variant == "J":
            self.robot.MoveJ(self.motors_list_actual)
        elif self.robot_state.current_move_variant == "L":
            self.robot.MoveL(self.motors_list_actual)
        elif self.robot_state.current_move_variant == "C":
            self.robot.MoveC(self.motors_list_actual)


    def updateMoveVariant(self):
        '''Ф-я для изменения стиля движения'''
        if self.robot_state.current_move_variant == "J":
            self.motors_list_actual = list(self.robot.get_cart_pos())
            self.robot_state.set_move_variant("L")
         
        elif self.robot_state.current_move_variant == "L":
            self.motors_list_actual = list(self.robot.get_joint_pos())
            self.robot_state.set_move_variant("J")

        self.logger.info(f'Режим выполнения: {self.robot_state.current_move_variant}')

    def change_gripper_status(self):
        '''Ф-я для изменения статуса гриппера (захвата)'''
        _translate = QtCore.QCoreApplication.translate
        if self.robot.gripper_state == 0.0:
            self.robot.gripper_state = 1.0
            self.ui.gripper_button.setText(_translate("Form", "Отпустить"))
            
            self.logger.info('Захват активен')
        else:
            self.robot.gripper_state = 0.0
            self.ui.gripper_button.setText(_translate("Form", "Схватить"))
            self.logger.info('Захват отпущен')


    def changeOnOffState(self):
        '''Ф-я для изменения статуса робота, вкл/выкл'''
        _translate = QtCore.QCoreApplication.translate
        if self.robot_state.current_state == self.robot_state.STATES['OFF'] or self.robot_state.current_state == self.robot_state.STATES['WAIT']:
            self.ui.On_button.setText(_translate("Form", "Выкл"))
            self.robot_state.set_state('ON')
            self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
            self.robot.move_to_start()
            time.sleep(1)
            self.logger.info('Робот включен и находится на стартовой позиции')

        else:
            self.ui.On_button.setText(_translate("Form", "Вкл"))
            self.robot_state.set_state('OFF')
            self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
            self.robot.move_to_start()
            time.sleep(1)
            self.logger.info('Робот выключен')

    def changePauseState(self):
        '''Ф-я для изменения статуса робота, пауза'''
        _translate = QtCore.QCoreApplication.translate
        self.robot_state.set_state('WAIT')
        self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
        self.ui.On_button.setText(_translate("Form", "Вкл"))
        self.logger.info('Робот приостановил свою работу')

    # не хватает нормальной экстренной остановки
    def changeEmergencyState(self):
        '''Ф-я для изменения статуса робота, экстренная остановка'''
        _translate = QtCore.QCoreApplication.translate
        self.robot_state.set_state('EMERGENCY')
        self.ui.State_data.setText(_translate("Form", self.robot_state.current_state))
        self.logger.error('Робот аварийно остановлен')