import cv2

def test_camera(camera_index=0):
    # Создаем объект для захвата видео с камеры
    cap = cv2.VideoCapture(camera_index)
    
    # Проверяем, удалось ли открыть камеру
    if not cap.isOpened():
        print(f"Ошибка: Не удалось открыть камеру с индексом {camera_index}")
        return
    
    print(f"Камера с индексом {camera_index} успешно открыта")
    print("Нажмите 'q' чтобы выйти из просмотра")
    
    while True:
        # Захватываем кадр
        ret, frame = cap.read()
        
        # Если кадр не получен, выходим из цикла
        if not ret:
            print("Ошибка: Не удалось получить кадр")
            break
        
        # Показываем кадр
        cv2.imshow('Camera Test', frame)
        
        # Выход по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()

# Проверяем камеру с индексом 0 (обычно это встроенная камера)
test_camera()