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
        self._current_state = self.STATES['ON']
        # self.current_cords_cords = coordinates ?
 
    @property
    def current_state(self):
        return self._current_state
    
    @property
    def current_cords(self):
        pass
    
    def set_state(self, new_state):
        self._current_state = self.STATES[new_state]