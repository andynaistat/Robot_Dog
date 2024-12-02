# bark.py
from pydub import AudioSegment
from pydub.playback import play
import threading
import time

class AudioPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.is_playing = False  
        self.last_played_time = 0
        self.cooldown = 5

    def play_sound(self):
        self.is_playing = True
        sound = AudioSegment.from_file(self.audio_file)
        play(sound)
        self.is_playing = False
        self.last_played_time = time.time()

    def play(self):
        if self.is_playing:
            print("Audio ya en reproducción, ignorando la nueva llamada.")
            return

        # Calcula el tiempo transcurrido desde la última reproducción
        time_since_last_play = time.time() - self.last_played_time
        if time_since_last_play < self.cooldown:
            print("Audio en cooldown. Espera 5 segundos antes de volver a reproducir.")
            return

        # Ejecuta la reproducción en un hilo separado si se cumplen las condiciones
        threading.Thread(target=self.play_sound, daemon=True).start()

# Uso
if __name__ == "__main__":
    player = AudioPlayer('../Audios/small-dog-barking.mp3')
    player.play()
