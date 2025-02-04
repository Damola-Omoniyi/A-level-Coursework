from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.music = ["models/Music/AOT.mp3", "models/Music/KNY.mp3"]
        self.current_song_index = 0
        self.load_next_song()

    def load_next_song(self):
        song = self.music[self.current_song_index]
        self.current_song = self.loader.loadMusic(song)
        self.current_song.setFinishedEvent('song-finished')
        self.accept('song-finished', self.on_song_finished)
        self.current_song.play()
        self.current_song.setPlayRate(2.5)

    def on_song_finished(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.music)
        self.load_next_song()


base = Main()
base.run()
