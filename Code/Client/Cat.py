import os
import sys
import cv2
import numpy as np
from Command import COMMAND as cmd

class Cat:
    def __init__(self):
        self.net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
    
    def detect_cat(self, img):
        height, width, channels = img.shape
        
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if self.classes[class_id] == "cat" and confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Calcular las coordenadas del rectángulo
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        if len(indexes) > 0:
            i = indexes[0][0]
            x, y, w, h = boxes[i]
            
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, 'Cat', (x + 5, y + h + 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
            print(f"Gato detectado en coordenadas: {x}, {y}, {w}, {h}")
            
            return (x, y, w, h)
        else:
            return None
