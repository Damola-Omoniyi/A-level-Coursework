# ----------------------------------------------------------------------------------------------------------------------
# Import section
from direct.showbase.ShowBase import ShowBase
from gui import GUI
from controls import Controller
from panda3d.core import *

loadPrcFile("config/Config.prc")

'''loadPrcFileData("", """
    fullscreen true
    win-size 1920 1080
    aspect-ratio auto
""")'''


# ----------------------------------------------------------------------------------------------------------------------

class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()  # Prevents user from moving camera

        self.UI = GUI(self)  # create an instance of the GUI class
        self.UI.start()
        self.controls = Controller(self)  # Controller class handles functions related to game controls

        self.is_game_mode_single_player = True  # Holds the value of the game mode True for single player

        # TODO: These are temporary lines of code only for testing to be removed
        self.accept("p",  self.UI.pause_menu)
        self.accept("x",  self.UI.end_round_menu)

        self.player_data = [[], []]
        self.game_started = False

        self.taskMgr.add(self.check_start_game, "START")
        #self.taskMgr.add(self.update_music, "music")

        self.scene = None # Scene model to be displayed
        self.scene_id = 1  # Scene selected by player

        self.music = ["models/Music/AOT.mp3", "models/Music/KNY.mp3"]
        self.current_song = self.loader.loadMusic(self.music[0])
        self.can_play_song = True
        #self.update_music()
        self.taskMgr.add(self.update_music, "music")

        self.gamepad_nums = {"gamepad1": 0, "gamepad2": 1, "keyboard": 5, "CPU": 5}



# ----------------------------------------------------------------------------------------------------------------------

    def check_start_game(self, task):
        if self.game_started is True:
            self.start_game()
            self.taskMgr.remove("START") # Remove this task after game starts so as not to waste processing power
        return task.cont

    def start_game(self):
        self.UI.frm_current.hide()
        self.UI.model.hide()  # hide model
        self.load_scene(self.scene_id)
        self.UI.in_game_gui()

    def update_music(self, task):
        #print(f"Total-length: {self.current_song.length()}  Current-time {self.current_song.getTime()}")

        for song in self.music:
            if self.can_play_song:
                print(song)
                #self.can_play_song = False
                self.current_song = self.loader.loadMusic(song)
                # YOU ARE SO SILLY!!! RESET VALUES RESET VALUE WE HAVE BEEN HERE FOR OVER 2 HOURS FOR JUST ONE LINE
                self.current_song.play()

                self.current_song.length()
                self.current_song.getTime()
                #if self.current_song.length() > self.current_song.getTime():
                #    self.can_play_song = False
                #else:
                #    self.can_play_song = True

        return  task.cont
    def load_scene(self, scene_id):
        if scene_id == 1:
            self.scene = self.loader.loadModel("models/moonsurface/moonsurface.egg")
            self.scene.reparentTo(self.render)
            self.scene.setPos(0, -750, -250)

            sun = self.loader.loadModel("models/jack.egg.pz")
            sun.reparentTo(self.render)
            sun.setPos(0, 4000, 500)
            sun.setScale(500)
            self.set_background_color(0.1, 0.1, 0.1125)
            # TODO: apply lighting and shading to scene
        elif scene_id == 2:
            self.scene = self.loader.loadModel("models/BeachTerrain/BeachTerrain.egg")
            pier = self.loader.loadModel("models/Pier/Pier.egg")
            pier.reparentTo(self.render)
            pier.setScale(150)
            pier.setPos(0, -2000, -850)
            # pier.setH(0)

            self.scene.reparentTo(self.render)
            self.scene.setPos(400, 1000, -1000)
            self.scene.setScale(75)
            self.set_background_color(0.53, 0.81, 0.98)


base = Main()
base.run()