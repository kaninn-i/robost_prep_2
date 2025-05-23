import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name):
    os.makedirls('logs', exist_ok = True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler()
    console_handler = logging.StreamHandler()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)







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