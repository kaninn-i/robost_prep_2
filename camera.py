import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # 0 — индекс камеры (может быть 0, 1, 2 и т. д.)

min_contour_area = 500       # Минимальная площадь контура
color_ranges = [             # Диапазоны цветов в HSV
    {'name': 'red',    'lower': [(0, 120, 70), (160, 120, 70)], 'upper': [(10, 255, 255), (180, 255, 255)]},
    {'name': 'green',  'lower': [(35, 50, 50)],                 'upper': [(85, 255, 255)]},
    {'name': 'blue',   'lower': [(100, 120, 70)],               'upper': [(130, 255, 255)]},
    {'name': 'yellow', 'lower': [(20, 100, 100)],              'upper': [(30, 255, 255)]}
]
kernel = np.ones((5,5), np.uint8)  # Ядро для морфологических операций


def process_frame(frame):
    # Предобработка
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    blurred = cv2.medianBlur(hsv, 5)
    
    # Словарь для кластеризации объектов
    detected_objects = {color['name']: [] for color in color_ranges}

    for color in color_ranges:
        # Создание маски для цвета
        masks = []
        for l, u in zip(color['lower'], color['upper']):
            mask = cv2.inRange(blurred, np.array(l), np.array(u))
            masks.append(mask)
        combined_mask = cv2.bitwise_or(*masks) if len(masks) > 1 else masks[0]

        # Морфологические операции
        processed_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)
        processed_mask = cv2.morphologyEx(processed_mask, cv2.MORPH_OPEN, kernel)

        # Поиск контуров
        contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            if cv2.contourArea(contour) < min_contour_area:
                continue
            
            # Аппроксимация контура
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            vertices = len(approx)
            
            # Определение характеристик
            shape = determine_shape(vertices, approx)
            color_name = color['name']
            
            # Сохранение объекта
            detected_objects[color_name].append({
                'contour': approx,
                'shape': shape,
                'area': cv2.contourArea(contour),
                'perimeter': cv2.arcLength(contour, True)
            })

            # Визуализация
            draw_object_info(frame, approx, color_name, shape)
    
    return frame

def determine_shape(vertices, approx):
    if vertices == 3:
        return "triangle"
    elif vertices == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        return "square" if 0.9 <= aspect_ratio <= 1.1 else "rectangle"
    else:
        area = cv2.contourArea(approx)
        (x,y), radius = cv2.minEnclosingCircle(approx)
        if abs(area - (np.pi * (radius**2))) / area < 0.2:
            return "circle"
        return f"polygon-{vertices}"

def draw_object_info(frame, contour, color, shape):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
    cY = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
    
    # Рисование контура
    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
    
    # Текст с информацией
    cv2.putText(frame, f"{color} {shape}", (cX, cY),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# обновление кадров
# def update_frames():
#     # 1й фрейм
#     ret1, frame1 = cap1.read()
#     if ret1:
#         frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
#         img1 = QImage(frame1, frame1.shape[1], frame1.shape[0], QImage.Format_RGB888)
#         self.video_label1.setPixmap(QPixmap.fromImage(img1))
    
#     # 2й фрейм
#     if self.cap2.isOpened():
#         ret2, frame2 = self.cap2.read()
#         if ret2:
#             frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
#             img2 = QImage(frame2, frame2.shape[1], frame2.shape[0], QImage.Format_RGB888)
#             self.video_label2.setPixmap(QPixmap.fromImage(img2))

#     # 3ий фрейм
#     if self.cap3.isOpened():
#         ret3, frame3 = self.cap3.read()
#         if ret3:
#             frame3 = self.process_frame(frame3)
#             # frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
#             # img3 = QImage(frame3, frame3.shape[1], frame3.shape[0], QImage.Format_RGB888)
#             img3 = QImage(frame3.data, frame3.shape[1], frame3.shape[0], 
#                     QImage.Format_RGB888).rgbSwapped()
#             self.video_label3.setPixmap(QPixmap.fromImage(img3))

# освобождение ресурсов при закрытии
# def closeEvent(self, event):
#     self.cap1.release()
#     self.cap2.release()
#     self.cap3.release()
#     event.accept()


while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка чтения камеры!")
        break
    frame = process_frame(frame)
    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()