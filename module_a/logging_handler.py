import logging
from logging.handlers import RotatingFileHandler
import os

from PyQt5.QtCore import QObject, pyqtSignal

class QtLogHandler(QObject, logging.Handler):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(msg)


def setup_logger(name):
    os.makedirs('logs', exist_ok = True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        'logs/.log',
        maxBytes=1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(message)s')
        )
    
    qt_handler = QtLogHandler()

    logger.handlers.clear()
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(qt_handler)

    return logger

# --------------------------------------------
