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

    def chase_cat(self, img):
        cat_position = self.detect_cat(img)  # Solo obtenemos la posición del primer gato
        if cat_position:
            x, y, w, h = cat_position
            center_x = x + w // 2  # Coordenada X del centro del gato
            center_y = y + h // 2  # Coordenada Y del centro del gato
            
            # Tamaño de la imagen (ajusta estos valores según la resolución de tu cámara)
            img_width = img.shape[1]
            img_height = img.shape[0]

            # Parámetros para el movimiento
            move_speed = 50  # Velocidad de movimiento, ajústalo según sea necesario
            threshold_x = 20  # Umbral para determinar si girar o avanzar
            threshold_y = 50  # Umbral para determinar si detenerse o avanzar
            
            # Calculamos la distancia desde el centro de la imagen
            error_x = center_x - (img_width // 2)  # Error en la dirección X
            error_y = center_y - (img_height // 2)  # Error en la dirección Y

            # Movemos el robot según la posición del gato
            if abs(error_x) > threshold_x:
                if error_x > 0:
                    command = cmd.CMD_TURN_RIGHT + "#" + str(move_speed) + '\n'
                else:
                    command = cmd.CMD_TURN_LEFT + "#" + str(move_speed) + '\n'
            else:
                if abs(error_y) > threshold_y:
                    command = cmd.CMD_MOVE_FORWARD + "#" + str(move_speed) + '\n'
                else:
                    command = cmd.CMD_MOVE_STOP + "#" + str(move_speed) + '\n'

            self.send_data(command)  # Enviamos el comando para mover el robot
        else:
            command = cmd.CMD_MOVE_STOP + "#" + str(move_speed) + '\n'
            self.send_data(command)  # Detenemos el robot si no hay gato
    