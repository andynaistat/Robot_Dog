import cv2
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
prototxt_path = os.path.join(current_dir, "MobileNetSSD_deploy.prototxt")
deploy_path = os.path.join(current_dir, "MobileNetSSD_deploy.caffemodel")
coco_names_path = os.path.join(current_dir, "coco.names")

# Cargar el modelo MobileNet SSD
net = cv2.dnn.readNetFromCaffe(prototxt_path, deploy_path)

# Cargar las etiquetas de clases
with open(coco_names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Función para detectar gatos
def detect_cat(frame):
    height, width = frame.shape[:2]
    
    # Preprocesar la imagen
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Inicializar listas para las detecciones
    boxes = []
    confidences = []
    
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])
        
        # Filtrar por confianza y clase de gato
        if confidence > 0.6 and class_id == 15:  # 15 es el índice de "cat"
            print(f"Detected {classes[class_id]} with confidence {confidence}")
            # Coordenadas del bounding box
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (x, y, x1, y1) = box.astype("int")
            boxes.append([x, y, x1 - x, y1 - y])
            confidences.append(float(confidence))
    
    # Aplicar Non-Maxima Suppression
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
