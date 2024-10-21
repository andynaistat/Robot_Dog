from PyQt5.QtCore import QTimer
from Command import COMMAND as cmd
from ui_client import Ui_client
from Client import *

class Sonic(Ui_client):
    _instance = None  # Atributo de clase para almacenar la instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:  # Si no existe una instancia
            cls._instance = super(Sonic, cls).__new__(cls)  # Crear una nueva instancia
        return cls._instance  # Retornar la instancia existente

    def __init__(self, client):
        self.client = client
        self.distance = 0  # Inicializa la distancia
        self.timer_sonic = QTimer()  # Inicializa el QTimer para Sonic

    def sonic(self):
        if self.Button_Sonic.text() == 'Sonic':
            self.timer_sonic.start(100)
            self.Button_Sonic.setText('Close')
        else:
            self.timer_sonic.stop()
            self.Button_Sonic.setText('Sonic')

    def getSonicData(self):
        command = cmd.CMD_SONIC + '\n'
        self.client.send_data(command)

    def getDistance(self):
        return self.distance

    def setDistance(self, d):
        self.distance = d

    def getTimerSonic(self):
        return self.timer_sonic  # Devuelve el timer correctamente inicializado
