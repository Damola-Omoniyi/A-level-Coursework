from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.music_list = [self.loader.loadMusic("models/Music/AOT.mp3"), self.loader.loadMusic("models/Music/KNY.mp3")]
        self.music_active = 0
        self.play_song = False

        self.taskMgr.add(self.music_task, "music-task")

        self.my_play(0)

    def my_play(self, number):
        self.music_list[number].play()
        self.music_active = number
        self.play_song = True
        print(self.music_list[number].getName())

    def music_task(self, task):
        if self.music_list[self.music_active].status() == 1:
            if self.play_song == True:
                self.play_song = False
                if self.music_active < len(self.music_list)-1:
                    self.music_active += 1
                else:
                    self.music_active = 0

                self.my_play(self.music_active)

        return task.cont


base = Main()
base.run()