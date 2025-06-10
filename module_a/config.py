import numpy as np

class Config:
    ROBOT_IP = '192.168.2.100'


    MIN_CONTOUR_AREA = 500       # Минимальная площадь контура
    COLOR_RANGES = [             # Диапазоны цветов в HSV
        {'name': 'red',    'lower': [(0, 120, 70), (160, 120, 70)], 'upper': [(10, 255, 255), (180, 255, 255)]},
        {'name': 'green',  'lower': [(35, 50, 50)],                 'upper': [(85, 255, 255)]},
        {'name': 'blue',   'lower': [(100, 120, 70)],               'upper': [(130, 255, 255)]},
        {'name': 'yellow', 'lower': [(20, 100, 100)],              'upper': [(30, 255, 255)]}
    ]
    KERNEL = np.ones((5,5), np.uint8)  # Ядро для морфологических операций
    CAMERA_INDEXES = [0, 0, 0]