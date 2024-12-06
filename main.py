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
        self.is_game_mode_single_player = True  # Holds the value of the game mode True for single player
        self.UI.start()
        self.controls = Controller(self)  # Controller class handles functions related to game controls

        self.accept("p",  self.UI.pause_menu)
        self.accept("x",  self.UI.end_round_menu)
        self.player_data = [[], []]

        self.scene = None  # Scene selected by player

        # self.start_game()

    def start_game(self):
        self.UI.frm_current.hide()  # not permanent code
        self.UI.model.hide()  # not permanent code
        self.load_scene(2)
        self.UI.in_game_gui()

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
            # apply lighting and shading to scene
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
            print(self.scene.getScale())
            self.set_background_color(0.53, 0.81, 0.98)


base = Main()
base.run()