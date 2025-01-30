# ----------------------------------------------------------------------------------------------------------------------
# Import section
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor
from panda3d.core import *

# ----------------------------------------------------------------------------------------------------------------------


class GUI:
    def __init__(self, base):
        self.base = base  # base refers to the Main class in which a GUI object is instantiated.
        self.frm_current = DirectFrame()  # Keeps track of the Frame currently being displayed.
        self.base.is_game_mode_single_player = True  # Holds the value of the game mode, True for single player

        self.Knight = Actor("models/Knight/knight.bam", {"Idle": "models/Knight/knight_Idle.bam"})  # knight model
        self.Crypto = Actor("models/Crypto/Crypto.bam", {"Idle": "models/Crypto/Crypto_Idle.bam"})  # Crypto model

        self.models = {"Knight": self.Knight, "Crypto": self.Crypto}  # dictionary of characters
        # makes accessing character models easier
        self.model = self.Knight # current model default set to knight

        # sets the default character to knight
        self.characters = ("Knight", "Crypto") # List of character names
        self.character = self.characters[0]

        # These are attributes of the class and not local variables of a method as they shall be frequently updated
        # over the course of gameplay.
        self.lbl_time = DirectLabel(text="0", scale=0.25, pos=(0, 0, 0.85))
        self.bar_health_player1 = DirectWaitBar(text="Player1", value=100, pos=(-1.15, 0, 0.9), scale=0.85)
        self.bar_health_player2 = DirectWaitBar(text="Player2", value=100, pos=(1.15, 0, 0.9), scale=0.85)

        self.bar_power_player1 = DirectWaitBar(value=0, pos=(-1.15, 0, -0.9), scale=(0.45, 1, 0.85),
                                               barColor=(0, 0, 1, 1))
        self.bar_power_player2 = DirectWaitBar(value=0, pos=(1.15, 0, -0.9), scale=(0.45, 1, 0.85),
                                               barColor=(0, 0, 1, 1))
        self.lbl_time.hide()
        self.bar_health_player1.hide()
        self.bar_health_player2.hide()
        self.bar_power_player1.hide()
        self.bar_power_player2.hide()

        self.controls = ("keyboard", "gamepad1", "gamepad2")  # List of available controls
        self.lbl_error = DirectLabel() # Label that displays an error message when selecting invalid controls


    def start(self):
        # This function is called at the start of the game to load the game's GUI
        self.title_menu()

# ----------------------------------------------------------------------------------------------------------------------

    def title_menu(self):
        frm_title = DirectFrame(frameSize=(-2, 2, -1, 1),
                                frameColor=(0, 0, 0, 1))
        self.frm_current.hide()
        self.frm_current = frm_title

        lbl_title = DirectLabel(text="GAME-NAME",
                                parent=frm_title,
                                text_fg=(1, 0, 0, 1),
                                pos=(0, 0, 0.2),
                                scale=(0.5, 0.5, 0.5),
                                text_scale=(0.7, 0.7),
                                text_bg=(0, 0, 0, 0),
                                frameColor=(0, 0, 0, 0)
                                )

        btn_start = DirectButton(text="START",
                                 parent=frm_title,
                                 scale=0.15,
                                 pos=(0, 0, -0.5),
                                 text_fg=(1, 0, 0, 1),
                                 frameColor=(1, 1, 1, 1),
                                 relief="flat",
                                 command=self.main_menu)

    def main_menu(self):

        frm_main_menu = DirectFrame(frameSize=(-2, 2, -1, 1),
                                    frameColor=(0, 0, 0, 1))
        self.frm_current.hide()
        self.frm_current = frm_main_menu

        btn_play = DirectButton(text="PLAY",
                                parent=frm_main_menu,
                                scale=0.15,
                                pos=(0, 0, 0.5),
                                text_fg=(1, 0, 0, 1),
                                frameColor=(1, 1, 1, 1),
                                relief="flat",
                                command=self.game_mode_menu)

        '''btn_credits = DirectButton(text="CREDITS",
                                   parent=frm_main_menu,
                                   scale=0.15,
                                   pos=(0, 0, 0.2),
                                   text_fg=(1, 0, 0, 1),
                                   frameColor=(1, 1, 1, 1),
                                   relief="flat",
                                   command=None)'''

        btn_settings = DirectButton(text="SETTINGS",
                                    parent=frm_main_menu,
                                    scale=0.15,
                                    pos=(0, 0, 0.2),
                                    text_fg=(1, 0, 0, 1),
                                    frameColor=(1, 1, 1, 1),
                                    relief="flat",
                                    command= self.settings_menu)

        btn_back = DirectButton(text="BACK",
                                parent=frm_main_menu,
                                scale=0.15,
                                pos=(0, 0, -0.1),
                                text_fg=(1, 0, 0, 1),
                                frameColor=(1, 1, 1, 1),
                                relief="flat",
                                command=self.title_menu)

    def game_mode_menu(self):
        self.base.player_data = [[], []]
        self.base.controls.reset()  # reset controls after back button brings you here

        frm_game_mode_menu = DirectFrame(frameSize=(-2, 2, -1, 1),
                                         frameColor=(0, 0, 0, 1))
        self.frm_current.hide()

        self.frm_current = frm_game_mode_menu

        btn_single_player = DirectButton(text="SINGLE PLAYER",
                                         parent=frm_game_mode_menu,
                                         scale=0.15,
                                         pos=(0, 0, 0.5),
                                         text_fg=(1, 0, 0, 1),
                                         frameColor=(1, 1, 1, 1),
                                         relief="flat",
                                         command=self.set_game_mode,
                                         extraArgs=[True]
                                         )

        btn_multi_player = DirectButton(text="PLAYER VS PLAYER",
                                        parent=frm_game_mode_menu,
                                        scale=0.15,
                                        pos=(0, 0, 0.2),
                                        text_fg=(1, 0, 0, 1),
                                        frameColor=(1, 1, 1, 1),
                                        relief="flat",
                                        command=self.set_game_mode,
                                        extraArgs=[False]) # states that the game mode is not single player

        btn_back = DirectButton(text="BACK",
                                parent=frm_game_mode_menu,
                                scale=0.15,
                                pos=(0, 0, -0.2),
                                text_fg=(1, 0, 0, 1),
                                frameColor=(1, 1, 1, 1),
                                relief="flat",
                                command=self.main_menu)

    def set_game_mode(self, is_single_player=True):
        # Sets the state of the game e.g. if the match is single or multiplayer.
        self.base.is_game_mode_single_player = is_single_player

        self.select_character1_menu()  # load the next menu

# ----------------------------------------------------------------------------------------------------------------------
    def set_model_light(self, x_position):
        point_light = PointLight("point_light")
        point_light.setColor((2, 2, 2, 1))
        point_light_node_path = self.base.render.attachNewNode(point_light)
        point_light_node_path.setPos(x_position, 95, -10)
        point_light_node_path.setScale(500)
        self.model.setLight(point_light_node_path)

    def set_model(self, x_position=35):
        # positions the model being displayed
        self.model.loop("Idle")
        self.model.setScale(25)
        # self.model.setScale(25)

        self.model.setPos(x_position, 120, -25)
        self.model.reparentTo(self.base.render)
        self.set_model_light(x_position)
        self.model.show()

    def select_character1_menu(self):
        self.base.set_background_color(0.2, 0.2, 0.2)
        self.frm_current.hide()
        frm_main = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(-2, 0, -1, 1))
        self.frm_current = frm_main
        self.set_model(35)

        lbl_character = DirectLabel(text=self.character, parent=frm_main, pos=(-1, 0, -0.15),
                                    frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.2)

        btn_previous_character = DirectButton(text="<", parent=frm_main, pos=(-1.75, 0, -0.15),
                                              frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.25,
                                              command=self.change_character,
                                              extraArgs=[-1, lbl_character, 35])

        btn_next_character = DirectButton(text=">", parent=frm_main, pos=(-0.25, 0, -0.15),
                                          command=self.change_character,
                                          extraArgs=[1, lbl_character, 35],
                                          frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.25)

        lbl_controls = DirectLabel(text="keyboard", parent=frm_main, pos=(-1, 0, 0.45),
                                   frameSize = (-2.5, 2.5, -0.5 ,1),
                                   frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15)

        btn_change_controls = DirectButton(text="change controller", parent=frm_main, pos=(-1, 0, 0.75),
                                           frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15,
                                           command=self.change_controls,
                                           extraArgs=[lbl_controls],)

        btn_next_menu = DirectButton(text="NEXT", parent=frm_main, pos=(-0.5, 0, -0.65),
                                     command=self.next_menu,
                                     extraArgs=[1, lbl_character, lbl_controls],
                                     frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15,)
        btn_back = DirectButton(text="BACK", parent=frm_main, pos=(-1.5, 0, -0.65), command=self.game_mode_menu,
                                frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15)


    def select_character2_menu(self):
        self.base.set_background_color(0.2, 0.2, 0.2)
        self.frm_current.hide()
        frm_main = DirectFrame(frameColor=(0, 0, 0, 1), frameSize=(0, 2, -1, 1))
        self.frm_current = frm_main
        self.set_model(-35)
        lbl_character = DirectLabel(text=self.character, parent=frm_main, pos=(1, 0, -0.15),
                                 frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.2)

        btn_previous_character = DirectButton(text=">", parent=frm_main, pos=(1.75, 0, -0.15),
                                              command=self.change_character,
                                              extraArgs=[-1, lbl_character, -35],
                                              frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.25)

        btn_next_character = DirectButton(text="<", parent=frm_main, pos=(0.25, 0, -0.15),
                                          command=self.change_character,
                                          extraArgs=[1, lbl_character, -35],
                                          frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.25)
        lbl_controls = DirectLabel(text="keyboard", parent=frm_main, pos=(1, 0, 0.45),
                                   frameSize = (-2.5, 2.5, -0.5 ,1),
                                   frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15)

        btn_change_controls = DirectButton(text="change controller", parent=frm_main, pos=(1, 0, 0.75),
                                    frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15,
                                    command=self.change_controls, extraArgs=[lbl_controls])
        if self.base.is_game_mode_single_player:
            # hide these widgets if playing single player mode
            lbl_controls["text"] = "CPU"
            lbl_controls.hide()
            btn_change_controls.hide()

        btn_next_menu = DirectButton(text="NEXT", parent=frm_main, pos=(1.5, 0, -0.65),
                                     command=self.next_menu,
                                     extraArgs=[2, lbl_character, lbl_controls],
                                     frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15)
        btn_back = DirectButton(text="BACK", parent=frm_main, pos=(0.5, 0, -0.65),  command=self.game_mode_menu,
                                frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15)

# ----------------------------------------------------------------------------------------------------------------------
    def change_controls(self, widget):
        controller = widget["text"]
        controller_index = self.controls.index(controller)+1  # When button clicked increment index
        if controller_index+1 > len(self.controls):  # If end of tuple reached cycle back to first item
            widget["text"] = self.controls[0]
        else:
            widget["text"] = self.controls[controller_index]  # Change text of label

    def change_character(self, direction, widget, x_position=35):
        self.model.hide()
        current = self.characters.index(self.character)
        character_index = current + direction
        if character_index < len(self.characters) - 1:
            self.character = self.characters[character_index]
        else:
            character_index = character_index % len(self.characters)
            self.character = self.characters[character_index]
        widget["text"] = self.character
        self.model = self.models[self.character]
        self.set_model(x_position)

    def next_menu(self, player_num, player, controller):
        if self.base.controls.check_valid_controls(controller["text"]): # First check if control selected is valid
            if player_num == 1:
                self.select_character2_menu()
                # Go to next character selection menu if for player 1
            elif player_num == 2:
                self.select_scene_menu()
                # If for player 2 go to scene menu
            self.base.player_data[player_num-1] = [player_num, player["text"], controller["text"]]
            # Update player data from main class. List in  main class is 0-indexed hence the subtraction

            if self.base.controls.controls_availability[controller["text"]]:
                self.base.controls.controls_availability[controller["text"]] = False
                # If a controller has been selected it is no longer available
        else:
            # If the controls selected were invalid
            self.lbl_error.hide()
            self.lbl_error = DirectLabel(text=self.base.controls.error_msg, scale=0.1)

            self.base.taskMgr.add(self.show_error_msg, "error message")

    def show_error_msg(self, task):
        if task.time < 1.5:
            self.lbl_error.show()
            # Display error message for 1.5 seconds
        else:
            # Hide message after 1.5 seconds remove task and finish
            self.lbl_error.hide()
            self.base.taskMgr.remove("error message")
            return task.done
        return task.cont
# ----------------------------------------------------------------------------------------------------------------------

    def select_scene_menu(self):
        self.model.hide()
        frm_main = DirectFrame(frameSize=(-2, 2, -1, 1), frameColor=(0, 0, 0, 1))
        self.frm_current.hide()
        self.frm_current = frm_main
        btn_select_scene1 = DirectButton(parent=frm_main, scale=0.35, image="models/moonSurface.png",
                                         pos=(-0.5, 0, 0), command=self.set_scene,
                                         extraArgs=[1])
        btn_select_scene2 = DirectButton(parent=frm_main, scale=0.35, image="models/Pier.png",
                                         pos=(0.5, 0, 0), command=self.set_scene,
                                         extraArgs=[2])
        lbl_select_scene = DirectLabel(text="select a stage", parent=frm_main, pos=(0, 0, 0.75),
                                       frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1), scale=0.15)
        btn_start_game = DirectButton(text="Start Game", parent=frm_main, pos=(0, 0, -0.85),
                                      command= self.base.start_game,frameColor=(1, 0, 0, 1), text_fg=(0, 0, 0, 1),
                                      scale=0.15)

    def set_scene(self, scene):
        self.base.scene_id = scene
# ----------------------------------------------------------------------------------------------------------------------

    def in_game_gui(self):
        self.lbl_time.show()
        self.bar_health_player1.show()
        self.bar_health_player2.show()
        self.bar_power_player1.show()
        self.bar_power_player2.show()

    def pause_menu(self):
        self.lbl_time.hide()
        self.bar_health_player1.hide()
        self.bar_health_player2.hide()
        self.bar_power_player1.hide()
        self.bar_power_player2.hide()
        frm_main = DirectFrame(frameSize=(-2, 2, -1, 1),
                                frameColor=(0, 0, 0, 1))
        self.frm_current.hide()
        self.frm_current = frm_main

        lbl_title = DirectLabel(text="PAUSE MENU",
                                parent=frm_main,
                                text_fg=(1, 0, 0, 1),
                                pos=(0, 0, 0.2),
                                scale=(0.5, 0.5, 0.5),
                                text_scale=(0.7, 0.7),
                                text_bg=(0, 0, 0, 0),
                                frameColor=(0, 0, 0, 0)
                                )

        btn_resume = DirectButton(text="RESUME",
                                 parent=frm_main,
                                 scale=0.15,
                                 pos=(0, 0, -0.5),
                                 text_fg=(1, 0, 0, 1),
                                 frameColor=(1, 1, 1, 1),
                                 relief="flat",
                                  command = self.base.unpause_game)

        def quit_command():
            self.base.end_game()
            self.main_menu()

        btn_quit = DirectButton(text="QUIT",
                                 parent=frm_main,
                                 scale=0.15,
                                 pos=(0, 0, -0.75),
                                 text_fg=(1, 0, 0, 1),
                                 frameColor=(1, 1, 1, 1),
                                 relief="flat",
                                command = quit_command)

    def end_round_menu(self):
        self.lbl_time.hide()
        self.bar_health_player1.hide()
        self.bar_health_player2.hide()
        self.bar_power_player1.hide()
        self.bar_power_player2.hide()

        frm_title = DirectFrame(frameSize=(-2, 2, -1, 1),
                                frameColor=(0, 0, 0, 1))
        self.frm_current.hide()
        self.frm_current = frm_title

        lbl_title = DirectLabel(text=f"{self.base.winner} WINS",
                                parent=frm_title,
                                text_fg=(1, 0, 0, 1),
                                pos=(0, 0, 0.2),
                                scale=(0.5, 0.5, 0.5),
                                text_scale=(0.7, 0.7),
                                text_bg=(0, 0, 0, 0),
                                frameColor=(0, 0, 0, 0)
                                )

        btn_next = DirectButton(text="NEXT",
                                 parent=frm_title,
                                 scale=0.15,
                                 pos=(0, 0, -0.5),
                                 text_fg=(1, 0, 0, 1),
                                 frameColor=(1, 1, 1, 1),
                                 relief="flat",
                                 command = self.title_menu )
    def settings_menu(self):
        frm_main = DirectFrame(frameSize=(-2, 2, -1, 1),
                               frameColor=(0, 0, 0, 1))
        self.frm_current.hide()
        self.frm_current = frm_main

        slider_music = DirectSlider(range=(0, 100), value=50, pageSize=1, pos=(-0.75, 0, 0.75), parent=frm_main)
        lbl_music = DirectLabel(text="Music", scale=0.1, pos=(0.75, 0, 0.7), parent=frm_main)

        slider_sound = DirectSlider(range=(0, 100), value=50, pageSize=1, pos=(-0.75, 0, 0.25), parent=frm_main)
        lbl_sound = DirectLabel(text="Sounds", scale=0.1, pos=(0.75, 0, 0.22), parent=frm_main)

        slider_brightness = DirectSlider(range=(0, 100), value=50, pageSize=1, pos=(-0.75, 0, -0.25), parent=frm_main)
        lbl_brightness = DirectLabel(text="Brightness", scale=0.1, pos=(0.75, 0, -0.27), parent=frm_main)

        btn_back = DirectButton(text="BACK",
                                parent=frm_main,
                                scale=0.15,
                                pos=(0, 0, -0.75),
                                text_fg=(1, 0, 0, 1),
                                frameColor=(1, 1, 1, 1),
                                relief="flat",
                                command=self.title_menu)


