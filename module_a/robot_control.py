from mcx.mcx_control import *

from logging_handler import setup_logger
logger = setup_logger(__name__)

import time

#максимальная дистанция робота 0.95
#если вводить точку [0.95, 0, 0]
#соответсвенно если брать 3-х мероное пространство, то нужно вычислять дистанцию


class RobotState:
    STATES = {
        'OFF':'Выключен',
        'ON':'В работе',
        'WAIT':'Ожидает',
        'EMERGENCY':'Аварийная остановка'
    }

    def __init__(self):    
        self._current = self.STATES['ON']

    @property
    def current(self):
        return self._current
    
    def set_state(self, new_state):
        self._current = self.STATES[new_state]


class RobotController:
    def __init__(self, ip_adress):
        self.ip = ip_adress
        self.robot = MCX()
        self.state = RobotState()
        self.connect()
        

    def connect(self):
        try:
            self.robot.connect(self.ip)
            logger.debug('Робот подключен')

        except Exception as e:
            logger.debug(f'Ошибка подключения: {str(e)}')

    def move_to_start(self):
        try:
            self.robot.move_to_start()
            time.sleep(1)
        except Exception as e:
            logger.debug(f'Ошибка перемещения: {str(e)}')
        

    # def switch_state(self, new_state):
    #     self.current_state = self.states_list[new_state]
    #     if self.current_state == 'Аварийная остановка':
    #         logs.add_log(f'Состояние робота: {self.current_state}', True)
    #     else:
    #         logs.add_log(f'Состояние робота: {self.current_state}')

