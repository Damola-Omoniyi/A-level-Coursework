# Imports Required
from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from panda3d.core import *
import ai as ai
from direct.showbase import DirectObject
import random
from direct.showbase.ShowBase import ShowBase


class Player(FSM, DirectObject.DirectObject):
    def __init__(self, player_num, base):
        FSM.__init__(self, "character-FSM")
        self.base = base  # Used to reference the main class
        self.player_num = player_num  # Unique player number attribute for each player
        self.enemy = None  # The player object of the opposing player
        self.character = None  # The Actor model for the character
        self.gamepad_no = self.base.gamepad_nums[self.base.player_data[self.player_num - 1][2]]
        self.is_moving = False
        self.is_blocking = False  # Value that determines if a player is blocking or not
        self.is_jumping = False  # This value shows that a player is currently jumping
        self.speed = 0
        self.direction = 0
        self.power = 0
        self.health = 100  # Players health
        self.is_dead = False
        self.distance = 0  # The distance attribute measures the distance between both players in each frame
        # The ranges dictionary contains the appropriate striking distance for each move, unique to all players and not
        # included here in the Super class
        self.ranges = {}
        self.c_sphere = CollisionSphere(0, 0, 1, 0.25)
        self.sphere_name = f"cnode{self.player_num}"  # player1's name would be cnode1
        self.sphere_nodepath = None
        self.atk_sound =self.base.loader.loadSfx("models/sword_sfx.wav")
        self.is_AI = False
        if self.base.is_game_mode_single_player and self.gamepad_no != 3:
            self.is_AI = False
            self.input_layer = [0, 0, 0, 0, 0, 0]
            self.total_distance = 0
        else:
            self.is_AI = True
            self.ai = ai.AI()


    def start(self):
        # Method called at the start of the game to setup the player objects
        if self.gamepad_no < 2:
            # Connect gamepad controllers
            self.base.controls.set_game_controls(self.gamepad_no)
        self.set_controls()
        self.character.reparentTo(self.base.render)
        self.character.setScale(200)
        self.base.cam.setZ(50)
        self.character.setPos(0, 1000, -150)
        self.set_light()
        if self.player_num == 1:
            self.character.setX(-200)
            self.character.setH(90)
        elif self.player_num == 2:
            self.character.setH(270)
            self.character.setX(200)
        self.request("Idle")
        self.base.taskMgr.add(self.move_task, "move_task")
        self.base.taskMgr.add(self.attack_task, "attack_task")
        self.base.taskMgr.add(self.death_task, f"death_task{self.player_num}")
        if not self.is_AI and self.base.is_game_mode_single_player:
            # self.accept('spam', self.on_spam, ['eggs', 'sausage'])

            self.base.taskMgr.add(self.calc_ai_input, "AIStuff")
            self.base.taskMgr.add(self.average_distance, "AIdist")
        if self.is_AI:
            self.accept("walk-f", self.walk_forward)
            self.accept("walk-b", self.walk_backward)
            self.accept('idle', self.stop_walk)
            self.accept('jump', self.jump)
            self.accept("block", self.block, [True])
            self.accept("special move", self.block, [False])
            self.accept("attack", self.Attack, [random.choice(['Attack1', 'Attack2', 'Attack3', 'Attack4'])])


    def set_controls(self):
        if self.gamepad_no == 2:
            self.accept("arrow_right", self.walk_forward)
            self.base.accept("arrow_left", self.walk_backward)
            self.accept('arrow_left-up', self.stop_walk)
            self.accept('arrow_right-up', self.stop_walk)
            self.accept('arrow_up', self.jump)
            self.accept("arrow_down", self.block, [True])
            self.accept("arrow_down-up", self.block, [False])
            self.accept("w", self.Attack, ['Attack1'])
            self.accept("a", self.Attack, ['Attack2'])
            self.accept('s', self.Attack, ['Attack3'])
            self.accept('d', self.Attack, ['Attack4'])
            self.accept('x', print, ["x"])
            self.accept('y', print, ["y"])

        elif self.gamepad_no < 2:
            # If gamepad number is less than 2 that means our user is using a pc controller not the keyboard or AI
            gamepad_name = f"gamepad{self.gamepad_no}"
            self.accept(f"{gamepad_name}-face_x", self.Attack, ['Attack1'])
            self.accept(f"{gamepad_name}-face_a", self.Attack, ['Attack2'])
            self.accept(f"{gamepad_name}-face_b", self.Attack, ['Attack3'])
            self.accept(f"{gamepad_name}-face_y", self.Attack, ['Attack4'])
            self.accept(f"{gamepad_name}-dpad_up",self.jump)
            self.accept(f"{gamepad_name}-dpad_down", self.block, [True])
            self.accept(f"{gamepad_name}-dpad_down-up", self.block, [False])
            self.accept(f"{gamepad_name}-dpad_left", self.walk_backward)
            self.accept(f"{gamepad_name}-dpad_left-up", self.stop_walk)
            self.accept(f"{gamepad_name}-dpad_right", self.walk_forward)
            self.accept(f"{gamepad_name}-dpad_right-up", self.stop_walk)
    def set_light(self):
        # np stands for node path
        d_light = DirectionalLight('d_light')
        a_light = AmbientLight('a_light')
        d_light_np = self.character.attachNewNode(d_light)
        d_light_np.setZ(100)
        a_light_np = self.character.attachNewNode(a_light)
        d_light.setColor((2.5, 2.5, 2.5, 1))
        a_light.setColor((2.5, 2.5, 2.5, 1))
        d_light_np.setHpr(-60, -30, 10)
        self.character.setLight(d_light_np)
        self.character.setLight(a_light_np)
        point_light = PointLight("point_light")
        point_light_node_path = self.character.attachNewNode(point_light)
        point_light_node_path.setScale(500)
        point_light_node_path.setPos(self.character.getPos())
        point_light_node_path.setZ(self.character.getZ() + 30)
        point_light_node_path.setY(self.character.getY() + 100)
        point_light.setColor((5, 5, 5, 1))
        self.character.setLight(point_light_node_path)

# ----------------------------------------------------------------------------------------------------------------------
    '''The group of methods below are dedicated to the FSM which handles the character states.
     Mostly in the format enter-state and exit-state'''
        
    def enterIdle(self):
        self.character.loop("Idle")

    def exitIdle(self):
        self.character.stop()

    def enterWalk(self):
        self.character.loop("Walk")
        self.character.setPlayRate(1.5, "Walk")

    def exitWalk(self):
        self.character.stop()

    def enterWalkback(self):
        self.character.loop("Walk")
        self.character.setPlayRate(-1.5, "Walk")

    def exitWalkback(self):
        self.character.stop()

    def enterImpact(self):
        self.character.play("Impact1")

    def exitImpact(self):
        self.character.stop()

    def enterAttack1(self):
        self.character.play("Attack1")
        self.character.setPlayRate(1.75, "Attack1")

    def exitAttack1(self):
        self.character.stop()

    def enterAttack2(self):
        self.character.play("Attack2")
        self.character.setPlayRate(1.75, "Attack2")

    def exitAttack2(self):
        self.character.stop()

    def enterAttack3(self):
        self.character.play("Attack3")
        self.character.setPlayRate(1.75, "Attack3")

    def exitAttack3(self):
        self.character.stop()

    def enterAttack4(self):
        self.character.play("Attack4")
        self.character.setPlayRate(1.75, "Attack4")

    def exitAttack4(self):
        self.character.stop()

    def enterBlock(self):
        self.character.loop("Block1")

    def exitBlock(self):
        self.character.stop()

    def enterJump(self):
        self.character.play("Jump")

    def exitJump(self):
        self.character.stop()

    def enterDeath(self):
        self.character.play("Death1")

    def exitDeath(self):
        self.character.stop()

    def enterSpecial1(self):
        self.character.play("Special1")

    def enterSpecial2(self):
        self.character.play("Special2")
   
    def exitSpecial1(self):
        self.character.stop()
   
    def exitSpecial2(self):
        self.character.stop()

# ----------------------------------------------------------------------------------------------------------------------
    def null_speed(self, a=0):
        self.is_moving = False
        self.speed = 0

    def set_speed(self, a=0):
        self.speed = 90
        self.enemy.speed = 90

    def move_task(self, task):
        # MOVEMENT: Forward and backward
        dt = self.base.clock.dt  # delta time
        self.speed = 100  # This value determines how fast our player moves

        if self.is_moving:
            self.character.setX(self.character.getX() + self.direction * self.speed * dt)
            # Update the position of the character with each frame
        else:
            self.speed = 0

        # If a character has reached end the screen they can no longer move to prevent them going off screen
        if self.character.getX() <= -650: 
            if self.direction == -1:
                self.null_speed()
        
        if self.character.getX() >= 650:
            if self.direction == 1:
                self.null_speed()
        return task.cont

    def walk_forward(self):
        self.is_moving = True
        self.direction = 1
        self.request("Walk")
        # Here add the walk task

    def walk_backward(self):
        self.is_moving = True
        self.direction = -1
        self.request("Walkback")
        # Here remove the walk task might be more efficient as task is not running always.

    def stop_walk(self):
        # Activated when a player takes their hand off the movement buttons
        self.is_moving = False
        self.direction = 0
        self.request("Idle")

# ----------------------------------------------------------------------------------------------------------------------
    def record(self):
        pos1 = self.character.getX()  # Player's position
        pos2 = self.enemy.character.getX()  # Enemy's position
        self.distance = abs(pos2 - pos1)

    def attack_task(self, task):
        dt = self.base.clock.dt  # delta time
        current_anim = self.character.getCurrentAnim()  # Variable holds the current animation being played
        self.record()  # Records the distance between the 2 players
        self.atk_sound.setVolume(self.base.UI.slider_sound["value"]/50)
        if current_anim in ['Attack1', 'Attack2', 'Attack3', 'Attack4']:
            self.ignoreAll()  # If an attack has been engaged some controls are ignored till the attack is complete
            self.null_speed()  # Players speed is reduced to 0 so no movement until attack complete
        elif current_anim in ["Idle", "Walk"]:
            self.set_controls()  # Allow controls if player is idle or just walking
        return task.cont

    def Attack(self, attack):
        # Load an MP3 file as sound effect
        self.atk_sound.play()
        # Load an MP3 file as background music
        self.request(attack)  # Play animation
        self.is_moving = False  # Stop movement
        if self.distance <= self.ranges[attack][0] and self.enemy.is_blocking is False and not self.is_jumping:
            # An attack is valid if enemy is not blocking and within range
            self.enemy.health -= 12.5
            self.power += 12.5
            self.base.taskMgr.doMethodLater(self.ranges[attack][1], self.react, 'reaction time')
            # Calls the React function after an appropriate time has elapsed
            if not self.is_AI and self.base.is_game_mode_single_player:
                self.input_layer[1] += 1

    def react(self, task):
        dt = self.base.clock.dt
        self.enemy.request("Impact")  # Plays animation for when a hit is registered
        sound = self.base.loader.loadSfx("models/gruntsound.wav")
        sound.play()
        sound.setVolume(self.base.UI.slider_sound["value"]/50)
        # self.enemy.player.setX(self.player.getX() + 1 * 20 * dt)
        return task.done

# ----------------------------------------------------------------------------------------------------------------------

    def death_task(self, task):
        current_anim = self.character.getCurrentAnim()  # Variable holds the current animation being played
        if current_anim is None:
            if self.health <= 0:
                self.base.winner = f"PLAYER{self.enemy.player_num}"
                self.request('Death')
                self.base.game_ending = True
                self.base.taskMgr.remove(f"death_task{self.player_num}")
            else:
                self.request("Idle")
        return task.cont


    def jump_task(self, task):
        dt = self.base.clock.dt  # delta time
        self.ignore_all()
        if task.time < 0.5:
            height = 500
            self.character.setZ(self.character.getZ() + height * dt)
        elif 0.5 < task.time < 1.0:
            height = -500
            self.character.setZ(self.character.getZ() + height * dt)
        elif task.time > 1.0:
            self.character.setZ(self.z_pos)
            self.base.taskMgr.remove(f"jump-task{self.player_num}")
            self.set_controls()
            self.is_jumping = False
            self.set_speed()
        return task.cont

    def jump(self):
        if not self.is_jumping:
            self.null_speed()
            # Prevents a player from jumping again while currently jumping
            self.is_jumping = True
            self.request("Jump")
            self.z_pos = self.character.getZ()
            self.base.taskMgr.add(self.jump_task,f"jump-task{self.player_num}")
            if not self.is_AI and self.base.is_game_mode_single_player:
                # print("I run")
                self.input_layer[2] += 1

    def end_player(self):
        self.ignoreAll()
        self.base.taskMgr.remove("move_task")
        self.base.taskMgr.remove("attack_task")
        self.character.hide()

    def setCollision(self, name):
        self.sphere_nodepath = self.character.attachNewNode(CollisionNode(self.sphere_name))
        # name is the name (cnode2) of our opponents collision capsule.
        self.sphere_nodepath.node().addSolid(self.c_sphere)
        # Uncomment this line to show the collision solid
        # self.sphere_nodepath.show()
        self.base.accept(f'{self.sphere_name}-into-{name}', self.null_speed)
        self.base.accept(f'{self.sphere_name}-again-{name}', self.null_speed)
        self.base.accept(f'{self.sphere_name}-out-{name}', self.set_speed)

    def block(self, state):
        self.is_blocking = state
        self.is_moving = False
        if state:
            self.request("Block")
            if not self.is_AI and self.base.is_game_mode_single_player:
                self.base.taskMgr.add(self.block_calculations, "AI-block")
        else:
            self.request("Idle")

# ----------------------------------------------------------------------------------------------------------------------
    def average_distance(self, task):
        pos1 = self.character.getX()  # Player's position
        pos2 = self.enemy.character.getX()  # Enemy's position
        distance = abs(pos2 - pos1)
        self.total_distance += distance
        return task.cont

    def block_calculations(self, task):
        if not self.is_blocking:
            self.input_layer[3] = int(task.time)
            self.base.taskMgr.remove("block-calc")
        return task.cont

    def calc_ai_input(self, task):
        self.input_layer[4] = self.health
        self.input_layer[5] = self.power
        # print(self.input_layer)
        if int(task.time) % 2.5 == 0:
            # reset after a minute
            avg = self.total_distance / (25 * 30)
            self.input_layer[0] = avg
            self.input_layer[0] = self.input_layer[0] / 100
            self.input_layer[3] = self.input_layer[3] / 20
            self.input_layer[4] = self.input_layer[4] / 100
            self.input_layer[5] = self.input_layer[5] / 100
            # print(self.input_layer)

            self.enemy.ai.input_layer = self.input_layer
            DirectObject.messenger.send('idle')
            DirectObject.messenger.send('special move')
            DirectObject.messenger.send(self.enemy.ai.perform())
            self.input_layer = [0, 0, 0, 0, 0, 0]


        return task.cont


