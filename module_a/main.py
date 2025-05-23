from gui import RobotControlGUI

import sys
from PyQt5.QtWidgets import QApplication

# -------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    window = RobotControlGUI()
    window.show()
    app.exec_()
    # logs.save_to_file()


if __name__ == '__main__':
    main()