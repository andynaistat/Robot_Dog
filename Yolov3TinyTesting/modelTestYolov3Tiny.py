import cv2
import numpy as np
import os

# Cargar los archivos del modelo YOLO

current_dir = os.path.dirname(os.path.abspath(__file__))
weights_path = os.path.join(current_dir, "yolov3-tiny.weights")
cfg_path = os.path.join(current_dir, "yolov3-tiny.cfg")
coco_names_path = os.path.join(current_dir, "coco.names")

net = cv2.dnn.readNet(weights_path, cfg_path)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Cargar las etiquetas (coco.names contiene las clases entrenadas)
with open(coco_names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

def detect_cat(frame):
    height, width, channels = frame.shape
    
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    class_ids = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if classes[class_id] == "cat" and confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Cat', (x + 5, y + h + 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
            print(f"Gato detectado en coordenadas: {x}, {y}, {w}, {h}")
            return (x, y, w, h)
    else:
        return None

def run_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("No se pudo recibir el frame (stream terminado?). Saliendo ...")
            break

        detect_cat(frame)

        cv2.imshow('Detección de Gato', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera()
