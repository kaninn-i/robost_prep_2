from module_a.config import Config

import numpy as np
import cv2

class VideoProcessor:
    def __init__(self):
        self.config = Config()

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # переводим фрейм в хсв
        # blurred = cv2.medianBlur(hsv, 5) #блюр
        blurred = cv2.GaussianBlur(hsv, (3, 3), 0)
        
        # словарь для кластеризации объектов
        detected_objects = {color['name']: [] for color in self.config.COLOR_RANGES}

        for color in self.config.COLOR_RANGES:
            # создание маски для цвета
            masks = []
            for l, u in zip(color['lower'], color['upper']):
                mask = cv2.inRange(blurred, np.array(l), np.array(u))
                masks.append(mask)
            combined_mask = cv2.bitwise_or(*masks) if len(masks) > 1 else masks[0]

            # Морфологические операции
            processed_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, self.config.KERNEL)
            processed_mask = cv2.morphologyEx(processed_mask, cv2.MORPH_OPEN, self.config.KERNEL)

            # Поиск контуров
            contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) < self.config.MIN_CONTOUR_AREA:
                    continue
                
                # Аппроксимация контура
                epsilon = 0.04 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                vertices = len(approx)
                
                # Определение характеристик
                shape = self._determine_shape(vertices, approx)
                color_name = color['name']
                
                # Сохранение объекта
                detected_objects[color_name].append({
                    'contour': approx,
                    'shape': shape,
                    'area': cv2.contourArea(contour),
                    'perimeter': cv2.arcLength(contour, True)
                })

                # Визуализация
                self._draw_object_info(frame, approx, color_name, shape)
        
        return frame, detected_objects, shape

    def _determine_shape(self, vertices, approx):
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

    def _draw_object_info(self, frame, contour, color, shape):
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"]) if M["m00"] != 0 else 0
        cY = int(M["m01"] / M["m00"]) if M["m00"] != 0 else 0
        
        # Рисование контура
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        
        # Текст с информацией
        cv2.putText(frame, f"{color} {shape}", (cX, cY),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


# from module_a.config import Config
# import numpy as np
# import cv2

# class VideoProcessor:
#     def __init__(self):
#         self.config = Config()

#     def process_frame(self, frame):
#         # Конвертация в HSV и размытие
#         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#         blurred = cv2.GaussianBlur(hsv, (3, 3), 0)
        
#         detected_objects = []  # Единый список для всех объектов

#         for color in self.config.COLOR_RANGES:
#             # Создаем маску для текущего цвета
#             mask = self._create_color_mask(blurred, color)
#             processed_mask = self._apply_morphology(mask)
            
#             # Находим и обрабатываем контуры
#             contours = self._find_valid_contours(processed_mask)
#             for contour in contours:
#                 approx = self._approximate_contour(contour)
#                 shape = self._determine_shape(approx)
                
#                 # Создаем объект с информацией
#                 obj_info = {
#                     'color': color['name'],
#                     'shape': shape,
#                     'contour': approx,
#                     'area': cv2.contourArea(contour),
#                     'perimeter': cv2.arcLength(contour, True),
#                     'position': self._calculate_centroid(approx)
#                 }
#                 detected_objects.append(obj_info)
                
#                 # Визуализация
#                 self._draw_object_info(frame, approx, obj_info['color'], shape)
        
#         return frame, detected_objects

#     def _create_color_mask(self, image, color):
#         mask = np.zeros(image.shape[:2], dtype=np.uint8)
#         for lower, upper in zip(color['lower'], color['upper']):
#             mask = cv2.bitwise_or(mask, cv2.inRange(image, np.array(lower), np.array(upper)))
#         return mask

#     def _apply_morphology(self, mask):
#         mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.config.KERNEL)
#         return cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.config.KERNEL)

#     def _find_valid_contours(self, mask):
#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         return [cnt for cnt in contours if cv2.contourArea(cnt) >= self.config.MIN_CONTOUR_AREA]

#     def _approximate_contour(self, contour):
#         epsilon = 0.04 * cv2.arcLength(contour, True)
#         return cv2.approxPolyDP(contour, epsilon, True)

#     def _determine_shape(self, approx):
#         vertices = len(approx)
#         if vertices == 3:
#             return "triangle"
#         elif vertices == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             aspect_ratio = w / float(h)
#             return "square" if 0.9 <= aspect_ratio <= 1.1 else "rectangle"
#         else:
#             area = cv2.contourArea(approx)
#             (_, _), radius = cv2.minEnclosingCircle(approx)
#             circle_area = np.pi * (radius ** 2)
#             return "circle" if abs(area - circle_area) / circle_area < 0.2 else f"polygon-{vertices}"

#     def _calculate_centroid(self, contour):
#         M = cv2.moments(contour)
#         if M["m00"] == 0:
#             return (0, 0)
#         return (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

#     def _draw_object_info(self, frame, contour, color, shape):
#         center = self._calculate_centroid(contour)
#         cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
#         cv2.putText(frame, f"{color} {shape}", center, 
#                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)