from module_a.gui import RobotControlGUI
from module_b.gui import AutomaticGUI
from module_c.gui import CvGui
from module_d.gui import FinalGui

import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    # window = RobotControlGUI()
    # window =  AutomaticGUI()
    # window =  CvGui()
    window = FinalGui()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()