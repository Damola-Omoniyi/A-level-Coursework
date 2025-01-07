# ----------------------------------------------------------------------------------------------------------------------
# Import section
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from gui import GUI
from controls import Controller
from panda3d.core import *
from crypto import Crypto
from knight import Knight

loadPrcFile("config/Config.prc")

''' loadPrcFileData("", """
    fullscreen true
    win-size 1920 1080
    aspect-ratio auto
""") '''
# TODO - DO NOT USE A COLLISION WALL TOO COMPLEX INSTEAD CREATE A POINT OF ORIGIN IF PLAYERS HAVE X VALUE 100 UNITS AWAY THEN SPEED
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

        self.gamepad_nums = {"gamepad1": 0, "gamepad2": 1, "keyboard": 2, "CPU": 3}

        self.characters = {"Crypto": Crypto, "Knight": Knight}
        self.player1 = None
        self.player2 = None


# ----------------------------------------------------------------------------------------------------------------------

    def check_start_game(self, task):
        # print(self.player_data)
        if self.game_started is True:
            self.start_game()
            self.taskMgr.remove("START") # Remove this task after game starts so as not to waste processing power
        return task.cont

    def start_game(self):
        self.UI.frm_current.hide()
        self.UI.model.hide()  # hide model
        self.load_scene(self.scene_id)
        self.UI.in_game_gui()
        player1_character = self.characters[self.player_data[0][1]]
        print(player1_character)
        player2_character = self.characters[self.player_data[1][1]]

        self.player1 = player1_character(self.player_data[0][0], self)
        self.player2 = player2_character(self.player_data[1][0], self)

        self.player1.enemy = self.player2
        self.player2.enemy = self.player1
        self.player2.setCollision(self.player1.sphere_name)
        self.player1.setCollision(self.player2.sphere_name)

        self.pusher = CollisionHandlerPusher()
        self.handler = CollisionHandlerEvent()
        self.trav = CollisionTraverser()
        self.cTrav = self.trav
        self.pusher.addInPattern('%fn-into-%in')
        self.pusher.addOutPattern('%fn-out-%in')

        self.handler.addInPattern('%fn-into-%in')
        self.handler.addAgainPattern('%fn-again-%in')
        self.handler.addOutPattern('%fn-out-%in')

        # self.pusher.addCollider(self.player2.sphere_nodepath, self.player2.player)
        self.trav.addCollider(self.player2.sphere_nodepath, self.handler)
        self.trav.addCollider(self.player1.sphere_nodepath, self.handler)
        self.player1.start()
        self.player2.start()

        self.taskMgr.add(self.update_cam, "update-camera")

    def update_cam(self, task):
        # print(self.camera.getPos())
        self.cam.setX((self.player1.character.getX() + self.player2.character.getX())/2)
        return task.cont


    def update_music(self, task):
            #print(f"Total-length: {self.current_song.length()}  Current-time {self.current_song.getTime()}")

            for song in self.music:
                if self.can_play_song:
                    #print(song)
                    #self.can_play_song = False
                    self.current_song = self.loader.loadMusic(song)
                    # YOU ARE SO SILLY!!! RESET VALUES RESET VALUE WE HAVE BEEN HERE FOR OVER 2 HOURS FOR JUST ONE LINE
                    self.current_song.play()

                    self.current_song.length()
                    self.current_song.getTime()
                    # if self.current_song.length() > self.current_song.getTime():
                    #    self.can_play_song = False
                    # else:
                    #    self.can_play_song = True
            return  task.cont

    def load_scene(self, scene_id):
        if scene_id == 1:
            self.scene = self.loader.loadModel("models/moonsurface/moonsurface.egg")
            self.scene.reparentTo(self.render)
            self.scene.setPos(0, -750, -150)
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
            pier.setPos(0, -3000, -800)
            # pier.setH(0)

            self.scene.reparentTo(self.render)
            self.scene.setPos(400, 1000, -1000)
            self.scene.setScale(75)
            self.set_background_color(0.53, 0.81, 0.98)





base = Main()
base.run()