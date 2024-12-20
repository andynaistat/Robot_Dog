import os
import sys
import cv2
import numpy as np
from Command import COMMAND as cmd

class Cat:
    def __init__(self):
        # Utiliza el modelo de detección de gatos
        self.detector = cv2.CascadeClassifier("Cat/haarcascade_frontalcatface.xml")
    
    def detect_cat(self, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cats = self.detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            if len(cats) > 0:
                for (x, y, w, h) in cats:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, 'Cat', (x + 5, y + h + 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
                    print("Gato detectado en coordenadas: ", x, y)
                    return (x, y, w, h)
            return None 
        except Exception as e:
            print(e)
            return None 
