from pydub import AudioSegment
from pydub.playback import play

class AudioPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def play(self):
        sound = AudioSegment.from_file(self.audio_file)
        play(sound)

# Uso
if __name__ == "__main__":
    player = AudioPlayer('../Audios/small-dog-barking.mp3')
    player.play()

