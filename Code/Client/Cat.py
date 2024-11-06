import os
import sys
import cv2
import numpy as np
from Command import COMMAND as cmd

class Cat:
    def __init__(self):
        self.net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")
        
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
            
    def detect_cat(frame):
        height, width = frame.shape[:2]
        
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        boxes = []
        confidences = []
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > 0.5: 
                class_id = int(detections[0, 0, i, 1])
                if classes[class_id] == "cat": 
                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                    (x, y, x1, y1) = box.astype("int")
                    boxes.append([x, y, x1 - x, y1 - y])
                    confidences.append(float(confidence))
        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        if len(indexes) > 0:
            for i in indexes.flatten():
                (x, y, w, h) = boxes[i]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'Cat', (x + 5, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                print(f"Gato detectado en coordenadas: {x}, {y}, {w}, {h}")
                return (x, y, w, h)
        else:
            return None