from module_a.logging_handler import setup_logger
logger = setup_logger(__name__)

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

    MOVE_VARIANTS = {
        'J':'J',
        'L':'L',
        'C':'C'
    }

    def __init__(self):    
        self._current_state = self.STATES['OFF']
        self._move_variant = self.MOVE_VARIANTS['J']
 
    @property
    def current_state(self):
        return self._current_state
    
    @property
    def current_move_variant(self):
        return self._move_variant
    
    
    def set_state(self, new_state):
        self._current_state = self.STATES[new_state]

    def set_move_variant(self, new_move_variant):
        self._move_variant = self.MOVE_VARIANTS[new_move_variant]