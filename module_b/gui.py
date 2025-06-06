from module_a.gui import RobotControlGUI
import time


class AutomaticGUI(RobotControlGUI):
    def __init__(self):
        super().__init__()

        self.motors_list_auto = list()
        self.ui.move_cords_button.clicked.connect(self.changeRobotPosition)


    def changeRobotPosition(self):
        '''Автоматическое перемещение робота по заданным координатам'''
        for row in range(self.ui.move_cords_table.rowCount()):
            for column in range(self.ui.move_cords_table.columnCount()):
                self.motors_list_auto.append(self.ui.move_cords_table.item(row, column).data(2))
        for i, l in enumerate(self.motors_list_auto):
            self.motors_list_auto[i] = float(l)

        self.logger.debug('Данные для перемещения получены')

        self.motors_list_actual = self.motors_list_auto
        self.robot.MoveL(self.motors_list_actual) # другая переменная??

        time.sleep(1)

        self.logger.debug('Робот перемещён на заданную позицию')
        self.logger.debug(f'Текущее положение: '+ ' '.join(str(i) for i in self.motors_list_actual))