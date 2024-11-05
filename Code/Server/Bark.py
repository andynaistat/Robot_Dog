import pygame

class Bark:
    def __init__(self):
        # Inicializar el módulo de mezcla de pygame
        pygame.mixer.init()

    def run(self, archivo):
        """Carga y reproduce un archivo de audio."""
        try:
            pygame.mixer.music.load(archivo)
            pygame.mixer.music.play()

            # Esperar a que el audio termine de reproducirse
            while pygame.mixer.music.get_busy():
                continue

        except pygame.error as e:
            print(f"Error al reproducir el archivo de audio: {e}")

