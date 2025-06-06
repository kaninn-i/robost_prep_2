from module_b.gui import AutomaticGUI
# from module_a.gui import RobotControlGUI

import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window =  AutomaticGUI()
    # window = RobotControlGUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()