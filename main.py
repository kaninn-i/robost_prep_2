from module_a.gui import RobotControlGUI
from module_b.gui import AutomaticGUI
from module_c.gui import CvGui
from module_d.gui import FinalGui

import sys
from PyQt5.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    executable_module = str(input('Введите букву модуля, который вы хотите запустить (А, Б, В или Г):')).lower()
    if executable_module == 'а':
        window = RobotControlGUI()
    elif executable_module == 'б':
        window =  AutomaticGUI()
    elif executable_module == 'в':
        window =  CvGui()
    elif executable_module == 'г':
        window = FinalGui()
    else:
        print('Введите корректную букву модуля')
        
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()