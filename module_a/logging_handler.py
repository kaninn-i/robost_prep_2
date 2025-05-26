import logging
from logging.handlers import RotatingFileHandler
import os

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
    file_handler.setFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter('%(levelname)s - %(message)s')

    logger.handlers.clear()
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger






# class GuiLogs:
#     def __init__(self):
#         self.logs = []
#         self.file_logs = []
    
#     def add_log(self, log, to_file=False):
#         self.logs.append(log)
#         if to_file:
#             self.file_logs.append(log)
    
#     def get_logs(self):
#         return self.logs
     
#     def save_to_file(self):
#         with open(".log", "w") as f:
#             f.writelines([ i + "\n" for i in self.file_logs])


# logs = GuiLogs()