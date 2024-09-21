import os
import sys
import cv2
import numpy as np

class Cat:
    def __init__(self):
        # Utiliza el modelo de detección de gatos
        self.detector = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")
    
    def detect_cat(self, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cats = self.detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
            if len(cats) > 0:
                for (x, y, w, h) in cats:
                    # Dibujar un rectángulo alrededor del gato detectado
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    # Se puede agregar lógica para mover el robot hacia el gato
                    print("Gato detectado en coordenadas: ", x, y)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    cat_detector = Cat()

    # Iniciar captura de video para probar la detección
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if ret:
            cat_detector.detect_cat(frame)
            cv2.imshow('Gato Detector', frame)
        
        # Presionar 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
