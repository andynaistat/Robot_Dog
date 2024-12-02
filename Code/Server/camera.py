from picamera2 import Picamera2
import time
picam2 = Picamera2()
# Puedes probar capturar una vista previa antes de tomar la imagen
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
# Espera un poco para que la camara se estabilice
time.sleep(2)
picam2.capture_file("image.jpg")
picam2.stop()
