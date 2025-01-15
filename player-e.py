# Player Class
# ----------------------------------------------------------------------------------------------------------------------
# This python file contains the Player class for our code which handles most attributes and functions relating to in
# game characters, such as their appearances, move sets and overall in-game features and behaviour.
# ----------------------------------------------------------------------------------------------------------------------
# Basic Imports Required
from direct.fsm.FSM import FSM
from panda3d.core import *
from direct.actor.Actor import Actor
import random
import ai as AI
# ----------------------------------------------------------------------------------------------------------------------
# this is an abstract class provides structure to programme but is not instantiated directly but is inherited from.
class Player(FSM):
    def __init__(self, player_num, character, base, AI_enabled=None ):
        # The player_num value determines if this is player1 or player 2 which decides the position a character faces
        # and their movement.
        # The character argument represents the actor or character a player is using.
        # Base refers to our main game class this is the class in our main file.

        FSM.__init__(self, "player-FSM")
        self.player_num = player_num
        self.player = character
        self.is_moving = False  # value that determines if our actor is moving or not
        self.base = base
        self.distance = 0  # The distance attribute measures the distance between both players in each frame
        self.enemy = None  # The opponent/opposition object to the player

        self.can_hit = False  # value that determines if a hit is possible or valid
        self.direction = 0  # This variable determines the direction our actor moves in forward or backward
        self.speed = 90

        self.sum_distance = 0
        self.power = 0
        self.atk_sound =self.base.loader.loadSfx("models/sword_sfx.wav")
        self.ai_enabled = AI_enabled

# ----------------------------------------------------------------------------------------------------------------------
        self.c_sphere = CollisionSphere(0, 0, 1, 0.25)
        self.sphere_name = f"cnode{self.player_num}"  # player1's name would be cnode1
        self.sphere_nodepath = self.player.attachNewNode(CollisionNode(self.sphere_name))

        '''This section has a lot of issues and may be potentially redundant will get back to it in due time'''
# ----------------------------------------------------------------------------------------------------------------------

        # The ranges dictionary contains the appropriate striking distance for each move, unique to all players and not
        # included here in the Super class
        self.ranges = {}

        self.health = 100 # Players health
        self.time = 0
        self.is_blocking = False  # Value that determines if a player is blocking or not
        # self.start_jump = False  # This value signifies that a jump is being activated
        self.is_jumping = False  # This value shows that a player is currently jumping

        if AI_enabled is not None:
            self.input_layer = [0, 0, 0, 0, 0, 0]
            self.sum_distance = 0
        elif AI_enabled is True:
            self.doing_action = False
            self.finished_action = False

# ----------------------------------------------------------------------------------------------------------------------
        self.base.gamepad_nums = {"gamepad1": 0, "gamepad2": 1, "keyboard": False, "CPU": False}
        self.gamepad_no = self.base.gamepad_nums[self.base.player_data[self.player_num - 1][2]]
        if self.gamepad_no is not False:
            self.base.controls.set_game_controls(self.gamepad_no)
            gamepad_name = f"gamepad{self.gamepad_no}"
    # The start function loads the player into the scene graph and sorts out player positioning and controls
    def start(self):
        self.base.taskMgr.add(self.move_task, "move_task")
        self.base.taskMgr.add(self.attack_task, "attack_task")
        self.base.taskMgr.add(self.auto_align, "autotask")
        self.base.taskMgr.add(self.timer, "timer")
        if self.ai_enabled:
            self.base.taskMgr.add(self.calc_ai_input, "AIStuff")
            self.base.taskMgr.add(self.avg_distance, "AIdist")
            self.base.taskMgr.add(self.check_doing_action, "action-check")

        self.player.reparentTo(self.base.render)
        # self.player.setScale(200)
        self.request("Idle")  # Start off with an Idle animation
        self.set_light()
        self.set_controls()
        #self.inGameGUI()
        #self.accept("b", self.pause_screen)
        if self.player_num == 1:
            self.player.setX(-100)
            self.player.setH(90)
        elif self.player_num == 2:
            self.player.setH(270)
            self.player.setX(300)


    def set_controls(self):
        # BASIC CONTROLS
        # PLAYER1 USES THE KEYBOARD
        # PLAYER2 USES A GAME-PAD
        if self.player_num == 1:
            self.accept("arrow_right", self.walk_forward)
            self.accept("arrow_left", self.walk_backward)
            self.accept('arrow_left-up', self.stop_walk)
            self.accept('arrow_right-up', self.stop_walk)
            self.accept('arrow_up', self.jump)
            self.accept("arrow_down", self.block, [True])
            self.accept("arrow_down-up", self.block, [False])
            self.accept("w", self.Attack, ['Attack1'])
            self.accept("a", self.Attack, ['Attack2'])
            self.accept('s', self.Attack, ['Attack3'])
            self.accept('d', self.Attack, ['Attack4'])
            self.accept('x', self.special)
        elif self.player_num == 2:
            self.accept("l", self.walk_forward)
            self.accept("j", self.walk_backward)
            self.accept("l-up", self.stop_walk)
            self.accept("j-up", self.stop_walk)
            self.accept("k", self.block, [True])
            self.accept("k-up", self.block, [False])
            self.accept("i", self.jump)
            self.accept("t", self.Attack, ['Attack1'])
            self.accept("f", self.Attack, ['Attack2'])
            self.accept('g', self.Attack, ['Attack3'])
            self.accept('h', self.Attack, ['Attack4'])  # come to this on a special knight class and add motion
            self.accept('y', self.special)
            '''THIS SHALL REVOLUTIONIZE OUR AI 
             class Test(DirectObject):
    def __init__(self):
        self.accept('spam', self.on_spam, ['eggs', 'sausage'])

    def on_spam(self, a, b, c, d):
        print(a, b, c, d)

test = Test()
messenger.send('spam', ['foo', 'bar'])
base.run()'''

        #print(self.base.player_data[0][2])
        #print("controls should set up")
        gamepad_name = f"gamepad{self.gamepad_no}"
        self.accept("gamepad0-face_x", print, [2])
        self.accept(f"{gamepad_name}-face_x", self.Attack, ['Attack1'])
        self.accept(f"{gamepad_name}-face_a", self.Attack, ['Attack2'])
        self.accept(f"{gamepad_name}-face_b", self.Attack, ['Attack3'])
        self.accept(f"{gamepad_name}-face_y", self.Attack, ['Attack4'])
        self.accept(f"{gamepad_name}-dpad_up", self.jump)
        self.accept(f"{gamepad_name}-dpad_down", self.block, [True])
        self.accept(f"{gamepad_name}-dpad_down-up", self.block, [False])
        self.accept(f"{gamepad_name}-dpad_left", self.walk_backward)
        self.accept(f"{gamepad_name}-dpad_left-up", self.stop_walk)
        self.accept(f"{gamepad_name}-dpad_right", self.walk_forward)
        self.accept(f"{gamepad_name}-dpad_right-up", self.stop_walk)
        #elif self.base.player_data[0][2] == "gamepad1":
 # This method locks the controls and prevents actions from being carried out. Useful for cutscenes and after a game
    # has ended
    def ignore_some(self):
        if self.player_num == 1:
            self.ignore("w")
            self.ignore("a")
            self.ignore("s")
            self.ignore("d")
            self.ignore('x')
        elif self.player_num == 2:
            self.ignore("t")
            self.ignore("f")
            self.ignore("g")
            self.ignore("h")
            self.ignore('y')

# ----------------------------------------------------------------------------------------------------------------------
    # This is the FSM section which contains all the possible states of the player for example an Idle state or an
    # Attack state.
    def enterIdle(self):
        self.player.loop("Idle")

    def exitIdle(self):
        self.player.stop()

    def enterWalk(self):
        self.player.loop("Walk")
        self.player.setPlayRate(1.5, "Walk")

    def exitWalk(self):
        self.player.stop()

    def enterWalkback(self):
        self.player.loop("Walk")
        self.player.setPlayRate(-1.5, "Walk")

    def exitWalkback(self):
        self.player.stop()

    def enterImpact(self):
        self.player.play("Impact1")

    def exitImpact(self):
        self.player.stop()

    def enterAttack1(self):
        self.player.play("Attack1")
        self.player.setPlayRate(1.75, "Attack1")

    def exitAttack1(self):
        self.player.stop()

    def enterAttack2(self):
        self.player.play("Attack2")
        self.player.setPlayRate(1.75, "Attack2")

    def exitAttack2(self):
        self.player.stop()

    def enterAttack3(self):
        self.player.play("Attack3")
        self.player.setPlayRate(1.75, "Attack3")

    def exitAttack3(self):
        self.player.stop()

    def enterAttack4(self):
        self.player.play("Attack4")
        self.player.setPlayRate(1.75, "Attack4")

    def exitAttack4(self):
        self.player.stop()

    def enterBlock(self):
        self.player.loop("Block1")

    def exitBlock(self):
        self.player.stop()

    def enterJump(self):
        self.player.play("Jump")

    def exitJump(self):
        self.player.stop()

    def enterDeath(self):
        self.player.play("Death1")

    def exitDeath(self):
        self.player.stop()

    def enterSpecial1(self):
        self.player.play("Special1")
    def enterSpecial2(self):
        self.player.play("Special2")
    def exitSpecial1(self):
        self.player.stop()
    def exitSpecial2(self):
        self.player.stop()

# ----------------------------------------------------------------------------------------------------------------------
    # This function handles the lighting of the player
    def set_light(self):
        # np stands for node path
        d_light = DirectionalLight('d_light')
        a_light = AmbientLight('a_light')
        d_light_np = self.base.render.attachNewNode(d_light)
        a_light_np = self.base.render.attachNewNode(a_light)

        d_light.setColor((2, 2, 2, 1))
        a_light.setColor((0.5, 0.5, 0.5, 1))
        d_light_np.setHpr(-60, -30, 10)
        self.base.render.setLight(d_light_np)
        self.base.render.setLight(a_light_np)
    def no_speed(self, a=0):
        #print("donein")
        self.is_moving = False
        self.speed = 0

        self.enemy.speed = 0
        self.enemy.is_moving = False

    def yes_speed(self, a=0):
        #print("notdonin")
        self.speed = 90
        self.enemy.speed = 90

    def setCollision(self, name):
        # name is the name (cnode2) of our opponents collision capsule.
        self.sphere_nodepath.node().addSolid(self.c_sphere)
        # Uncomment this line to show the collision solid
        #self.sphere_nodepath.show()

        self.accept(f'{self.sphere_name}-into-{name}', self.no_speed)
        self.accept(f'{self.sphere_name}-again-{name}', self.no_speed)
        self.accept(f'{self.sphere_name}-out-{name}', self.yes_speed)
# ----------------------------------------------------------------------------------------------------------------------
    # The move task is the key component of our player class it handles movement, jumping and gameplay and is split into
    # various sections representing each of these component
    def move_task(self, task):
        # MOVEMENT: Forward and backward
        dt = self.base.clock.dt  # delta time
        self.speed = 90  # This value determines how fast our player moves

        if self.is_moving:
            self.player.setX(self.player.getX() + self.direction * self.speed * dt)
        else:
            self.speed = 0
        return task.cont

# ----------------------------------------------------------------------------------------------------------------------
    # ATTACKS AND ANIMATIONS
# ----------------------------------------------------------------------------------------------------------------------
    # ATTACKS AND ANIMATIONS

    def attack_task(self, task):
        dt = self.base.clock.dt  # delta time
        current_anim = self.player.getCurrentAnim()  # Variable holds the current animation being played
        self.record(self.enemy)  # Records the distance between the 2 players
        if self.health <= 0:
            self.request('Death')
            self.player.hide()
            print("time to die")
        if current_anim is None:
            if self.health is None:
                if self.health <= 0:
                    self.request('Death')
                    self.player.hide()
                    # If no animation is playing and health is empty hide actor
            else:
                self.request("Idle")

        if current_anim in ['Attack1', 'Attack2', 'Attack3', 'Attack4']:
            self.ignoreAll()  # If an attack has been engaged some controls are ignored till the attack is complete
            if self.speed != 0:
                self.speed -= 90  # Players speed is reduced to 0 so no movement until attack complete

        elif current_anim in ["Idle", "Walk"]:
            self.set_controls()  # Allow controls if player is idle or just walking
        return task.cont

# ----------------------------------------------------------------------------------------------------------------------
# MOVEMENT: Jumping
    def jump_task(self, task):
        dt = self.base.clock.dt  # delta time
        self.ignore_all()
        if task.time < 0.5:
            height = 850
            self.player.setZ(self.player.getZ() + height * dt)
        elif 0.5 < task.time < 1.0:
            height = -850
            self.player.setZ(self.player.getZ() + height * dt)
        elif task.time > 1.0:
            self.player.setZ(0)
            self.base.taskMgr.remove("jump-task")
            self.set_controls()
            self.is_jumping = False
        return task.cont
    def auto_align(self, task):
        #print("player-enemy", self.player.getPos() - self.enemy.player.getPos())
        if self.player.getPos() - self.enemy.player.getPos() < 0:
            self.player.setH(90)
            self.enemy.player.setH(270)
        return task.cont

    def timer(self, task):
        self.time = int(task.time)
        if self.time > 120:
            a = ("time to end game")
            # Call an end game function
        return task.cont

    def walk_forward(self):
        self.is_moving = True
        self.direction = 1
        self.request("Walk")

    def walk_backward(self):
        self.is_moving = True
        self.direction = -1
        self.request("Walkback")

    def stop_walk(self):
        # Activated when a player takes their hand off the move buttons
        self.is_moving = False
        self.direction = 0
        self.request("Idle")

    def Attack(self, attack):
        # Load an MP3 file as sound effect
        self.atk_sound.play()
        # Load an MP3 file as background music

        self.request(attack)  # Play animation
        self.is_moving = False  # Stop movement
        if self.distance <= self.ranges[attack][0] and self.enemy.is_blocking is False:
            # An attack is valid if enemy is not blocking and within range
            # print(self.ranges[attack][0])
            # print("hit is valid")
            self.enemy.health -= 5
            self.power += 12.5
            print(self.power)
            # print(self.health)
            # print(self.enemy.health)
            self.base.taskMgr.doMethodLater(self.ranges[attack][1], self.react, 'reaction time')
            # Calls the React function after an appropriate time has elapsed
        if self.ai_enabled:
            self.input_layer[1] += 1

    def react(self, task):
        dt = self.base.clock.dt
        self.enemy.request("Impact")  # Plays animation for when a hit is registered
        sound = self.base.loader.loadSfx("models/gruntsound.wav")
        sound.play()
        #self.enemy.player.setX(self.player.getX() + 1 * 20 * dt)
        return task.done

    def jump(self):
        if not self.is_jumping:
            # Prevents a player from jumping again while currently jumping
            self.is_jumping = True
            self.request("Jump")
            self.base.taskMgr.add(self.jump_task, "jump-task")
            # self.start_jump = True
            self.input_layer[2] += 1


    def block(self, state):
        self.is_blocking = state
        self.is_moving = False
        if state:
            self.request("Block")
        else:
            self.request("Idle")

    def check_doing_action(self, task):
        current_anim = self.player.getCurrentAnim()
        if current_anim in ['Idle']:
            self.doing_action = False
        else:
            self.doing_action = True
        return task.cont

    def avg_distance(self, task):
        p1 = self.player.getX()  # Player's position
        p2 = self.enemy.player.getX()  # Enemy's position
        distance = abs(p2 - p1)
        self.sum_distance += distance
        return task.cont
    def block_calc(self, task):
        a = task.time
        if self.is_blocking:
            a = task.time
            #print(a)
        else:
            self.input_layer[3] += task.time
            self.base.taskMgr.remove("block")
        return task.cont
    def calc_ai_input(self, task):
        self.input_layer[4] = self.health
        self.input_layer[5] = self.power
        if int(task.time)%25==0:
            # reset after a minute
            avg = self.sum_distance / (25 * 30)
            self.input_layer[0] = avg
            self.input_layer[0] = self.input_layer[0] / 20
            self.input_layer[4] = self.input_layer[4] / 20
            self.input_layer[5] = self.input_layer[5] / 20
            #self.input_layer = [0, 0, 0, 0, 0, 0]
    def calc_ai_input(self, task):
        self.input_layer[4] = self.health
        self.input_layer[5] = self.power
        #print(self.input_layer)
        self.ai_stuff()
        #print(self.has_AI)
        if int(task.time)%25==0:
            # reset after a minute
            avg = self.sum_distance / (25 * 30)
            self.input_layer[0] = avg
            self.input_layer[0] = self.input_layer[0] / 20
            self.input_layer[4] = self.input_layer[4] / 20
            self.input_layer[5] = self.input_layer[5] / 20
            #print(self.input_layer)
            #self.input_layer = [0, 0, 0, 0, 0, 0]
        if self.has_AI:

            #print(task.time - a)
            for action in self.ai.action_stack:
                if int(task.time) % 5 == 0 and not self.doing_action:
                    #print(action)
                    if action == 0:
                        rand = random.choice(['Attack1','Attack2','Attack3','Attack4'])
                        self.Attack(rand)
                    elif action == 1:
                        self.jump()
                    elif action == 2:
                        self.block(True)
                        self.base.taskMgr.doMethodLater(2, self.ai_unblock, 'reaction time')
                    elif action == 3:
                        self.walk_backward()
                        self.base.taskMgr.doMethodLater(2, self.ai_stop, 'reaction time')
                    elif action == 4:
                        self.walk_forward()
                        self.base.taskMgr.doMethodLater(2, self.ai_stop, 'reaction time')
                    elif action == 5:
                        pass
                        #special
                    elif action == 6:
                        pass
                        #idle
                self.ai.action_stack.remove(action)


        return task.cont

    def ai_unblock(self, task):
        self.block(False)
        return task.done

    def ai_stop(self, task):
        #self.block(False)
        self.stop_walk()
        return task.done
    def ai_stuff(self):
        if self.has_AI:
            self.ai = AI.AI()
            self.ai.input_layer = self.input_layer
            self.ai.perform()
    def record(self, enemy):
        p1 = self.player.getX()  # Player's position
        p2 = enemy.player.getX()  # Enemy's position
        self.distance = abs(p2 - p1)
    def special(self, num="2"):
        if self.power>=100:
            self.power = 0
            run_special = True
            self.request("Special1")
            #print("doing specialz")