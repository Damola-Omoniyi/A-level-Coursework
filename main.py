# ----------------------------------------------------------------------------------------------------------------------
# Import section
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.task.Task import Task
from gui import GUI
from controls import Controller
from panda3d.core import *
from crypto import Crypto
from knight import Knight
import complexpbr
# mySound.setVolume(0.5)
loadPrcFile("config/Config.prc")

# ----------------------------------------------------------------------------------------------------------------------

class Main(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()  # Prevents user from moving camera

        self.UI = GUI(self)  # create an instance of the GUI class and start the game
        self.UI.start()
        self.controls = Controller(self)  # Controller class handles functions related to game controls

        self.is_game_mode_single_player = True  # Holds the value of the game mode True for single player

        # TODO: These are temporary lines of code only for testing to be removed

        self.player_data = [[], []] # Data about each player,  player number, character used and controller
        self.game_started = False # Set to true when main game loop starts

        self.taskMgr.add(self.check_start_game, "START")

        self.scene = None  # Scene model to be displayed
        self.prop = self.loader.loadModel("models/Pier/Pier.egg")
        self.scene_id = 1  # Scene selected by player

        # complexpbr.apply_shader(self.render)
        # self.set_scene_light()
        # self.render.setShaderAuto()

        self.music = ["models/Music/AOT.mp3", "models/Music/KNY.mp3"]
        self.current_song_index = 0
        self.load_next_song()


        self.gamepad_nums = {"gamepad1": 0, "gamepad2": 1, "keyboard": 2, "CPU": 3}
        # CPU is used for single player against an AI

        self.characters = {"Crypto": Crypto, "Knight": Knight}
        
        self.player1 = None
        self.player2 = None

        self.handler = CollisionHandlerEvent()
        self.trav = CollisionTraverser()
        self.cTrav = self.trav

        self.round_info = {"player1": 0, "player2":0}
        self.game_ending = False
        self.round = 1  # Rounds 1, 2 or 3
        self.winner = ""
        self.taskMgr.add(self.settings_task, "settings")


# ----------------------------------------------------------------------------------------------------------------------

    def check_start_game(self, task):
        if self.game_started is True:
            self.start_game()
            self.taskMgr.remove("START")  # Remove this task after game starts so as not to waste processing power
        return task.cont



    def timer(self, task):
        self.time = int(task.time) // 1
        if self.time > 120:
            a = ("time to end game")
            # Call an end game function
        return task.cont

    def start_game(self):
        self.UI.frm_current.hide()
        self.UI.model.hide()  # hide model
        self.load_scene(self.scene_id)
        self.UI.in_game_gui()
        player1_character = self.characters[self.player_data[0][1]]
        player2_character = self.characters[self.player_data[1][1]]

        self.player1 = player1_character(self.player_data[0][0], self)
        self.player2 = player2_character(self.player_data[1][0], self)

        self.player1.enemy = self.player2
        self.player2.enemy = self.player1
        self.set_collisions()
        self.player1.start()
        self.player2.start()
        self.UI.bar_power_player1.hide()
        self.UI.bar_power_player2.hide()
        self.UI.lbl_time.hide()
        self.accept("space", self.pause_game)
        self.taskMgr.add(self.timer, "time_task")
        self.taskMgr.add(self.update_cam, "update-camera")
        self.taskMgr.add(self.update_gui, "update")
        self.taskMgr.add(self.check_end_game, "end_game_task")

    def pause_game(self):
        self.player1.ignoreAll()
        self.player2.ignoreAll()
        self.ignoreAll()
        self.UI.pause_menu()

    def unpause_game(self):
        self.UI.frm_current.hide()
        self.player1.set_controls()
        self.player2.set_controls()
        self.accept("space", self.pause_game)
        self.UI.lbl_time.show()
        self.UI.bar_health_player1.show()
        self.UI.bar_health_player2.show()
        self.UI.bar_power_player1.show()
        self.UI.bar_power_player2.show()

    def end_game(self):
        self.player1.end_player()
        self.player2.end_player()
        del self.player1
        del self.player2
        # print('I occur')
        self.scene.hide()
        self.prop.hide()
        self.taskMgr.remove("time_task")
        self.taskMgr.remove("update-camera")
        self.taskMgr.remove("update")
        self.set_background_color(0.2, 0.2, 0.2)
        self.cam.setPos(0, 0, 0)  # Move it back to default position
        self.ignoreAll()
        # self.camera.setHpr(0, 0, 0)  # Reset rotation

    def check_end_game(self, task):
        if self.game_ending:
            self.end_game()
            self.UI.end_round_menu()
            self.game_ending = False

            self.taskMgr.remove("end_game_task")
        return task.cont


    def set_collisions(self):
        self.player2.setCollision(self.player1.sphere_name)
        self.player1.setCollision(self.player2.sphere_name)

        self.handler.addInPattern('%fn-into-%in')
        self.handler.addAgainPattern('%fn-again-%in')
        self.handler.addOutPattern('%fn-out-%in')

        self.trav.addCollider(self.player2.sphere_nodepath, self.handler)
        self.trav.addCollider(self.player1.sphere_nodepath, self.handler)

    def update_cam(self, task):
        self.cam.setX((self.player1.character.getX() + self.player2.character.getX())/2)
        # Sets the camera right between both players
        return task.cont

    # TODO: Fix this please
    def load_next_song(self):
        song = self.music[self.current_song_index]
        self.current_song = self.loader.loadMusic(song)
        self.current_song.setFinishedEvent('song-finished')
        self.accept('song-finished', self.on_song_finished)
        self.current_song.play()

    def on_song_finished(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.music)
        self.load_next_song()

    def update_gui(self, task):
        # time = f"{int(task.time)}"
        # self.UI.lbl_time["text"] = time
        self.UI.bar_health_player1["value"] = self.player1.health
        self.UI.bar_health_player2["value"] = self.player2.health

        self.UI.bar_power_player1["value"] = self.player1.power
        self.UI.bar_power_player2["value"] = self.player2.power
        self.UI.lbl_time["text"] = f"{120-self.time}"

        return task.cont

    def set_scene_light(self):
        # np stands for node path
        d_light = DirectionalLight('d_light')
        a_light = AmbientLight('a_light')
        d_light_np = self.render.attachNewNode(d_light)
        d_light_np.setZ(100)
        a_light_np = self.render.attachNewNode(a_light)
        d_light.setColor((10,10, 10, 1))
        a_light.setColor((2.5, 2.5, 2.5, 1))
        d_light_np.setHpr(-60, -30, 10)
        self.render.setLight(d_light_np)
        self.render.setLight(a_light_np)


    def load_scene(self, scene_id, close = False):
        if scene_id == 1:

            self.scene = self.loader.loadModel("models/moonsurface/moonsurface.egg")
            self.scene.reparentTo(self.render)
            self.scene.setPos(0, -750, -150)
            self.prop = self.loader.loadModel("models/jack.egg.pz")
            self.prop.reparentTo(self.render)
            self.prop.setPos(0, 4000, 500)
            self.prop.setScale(500)
            self.set_background_color(0.1, 0.1, 0.1125)
            # TODO: apply lighting and shading to scene

        elif scene_id == 2:

            self.scene = self.loader.loadModel("models/BeachTerrain/BeachTerrain.egg")
            self.prop = self.loader.loadModel("models/Pier/Pier.egg")
            self.prop.reparentTo(self.render)
            self.prop.setScale(150)
            self.prop.setPos(0, -3000, -800)

            self.scene.reparentTo(self.render)
            self.scene.setPos(400, 1000, -1000)
            self.scene.setScale(75)
            self.set_background_color(0.53, 0.81, 0.98)

    def settings_task(self, task):
        self.current_song.setVolume(self.UI.slider_music["value"]/50)
        return task.cont


base = Main()
base.run()
