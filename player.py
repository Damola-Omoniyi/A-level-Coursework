from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from panda3d.core import *


class Player(FSM):
    def __init__(self, player_num, base):
        FSM.__init__(self, "character-FSM")
        self.base = base
        self.player_num = player_num
        self.enemy = None
        self.character = None
        self.gamepad_no = self.base.gamepad_nums[self.base.player_data[self.player_num - 1][2]]
        self.is_moving = False  #
        self.is_blocking = False  # Value that determines if a player is blocking or not
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

    def start(self):
        if self.gamepad_no < 2:
            self.base.controls.set_game_controls(self.gamepad_no)
        self.set_controls()
        self.character.reparentTo(self.base.render)
        self.character.setScale(200)
        self.set_light()
        self.base.cam.setZ(50)
        self.character.setPos(0, 1000, -150)
        if self.player_num == 1:
            self.character.setX(-200)
            self.character.setH(90)
        elif self.player_num == 2:
            self.character.setH(270)
            self.character.setX(200)
        self.request("Idle")
        self.base.taskMgr.add(self.move_task, "move_task")
        self.base.taskMgr.add(self.attack_task, "attack_task")
        self.base.taskMgr.add(self.death_task, "death_task")

    def set_controls(self):
        if self.gamepad_no == 2:
            self.accept("arrow_right", self.walk_forward)
            self.accept("arrow_left", self.walk_backward)
            self.accept('arrow_left-up', self.stop_walk)
            self.accept('arrow_right-up', self.stop_walk)
            self.accept('arrow_up', print, ["arrow-up"])
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
            self.accept(f"{gamepad_name}-dpad_up", print, ["up"])
            self.accept(f"{gamepad_name}-dpad_down", self.block, [True])
            self.accept(f"{gamepad_name}-dpad_down-up", self.block, [False])
            self.accept(f"{gamepad_name}-dpad_left", self.walk_backward)
            self.accept(f"{gamepad_name}-dpad_left-up", self.stop_walk)
            self.accept(f"{gamepad_name}-dpad_right", self.walk_forward)
            self.accept(f"{gamepad_name}-dpad_right-up", self.stop_walk)

    # The group of methods below are dedicated to the FSM 
    # enter-state and exit-state
        
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

    def move_task(self, task):
        # MOVEMENT: Forward and backward
        dt = self.base.clock.dt  # delta time
        self.speed = 100  # This value determines how fast our player moves

        if self.is_moving:
            self.character.setX(self.character.getX() + self.direction * self.speed * dt)
        else:
            self.speed = 0

        # If a character has reached end the screen they can no longer move
        if self.character.getX() <= -650: 
            if self.direction == -1:
                self.null_speed()
        
        if self.character.getX() >= 650:
            if self.direction == 1:
                self.null_speed()
        return task.cont

    def attack_task(self, task):
        dt = self.base.clock.dt  # delta time
        current_anim = self.character.getCurrentAnim()  # Variable holds the current animation being played
        self.record()  # Records the distance between the 2 players

        if current_anim in ['Attack1', 'Attack2', 'Attack3', 'Attack4']:
            self.ignoreAll()
            #   # If an attack has been engaged some controls are ignored till the attack is complete
            if self.speed != 0:
                self.speed -= 90  # Players speed is reduced to 0 so no movement until attack complete
        elif current_anim in ["Idle", "Walk"]:
            self.set_controls()  # Allow controls if player is idle or just walking
            # print("unlock")
        return task.cont

    def death_task(self, task):
        if self.character.getCurrentAnim() is None:
            if self.health <= 0 and not self.is_dead:
                self.request('Death')
                self.is_dead = True
                # self.base.taskMgr.remove("death_task")
                # self.character.hide()
                # If no animation is playing and health is empty hide actor
            else:
                if not self.is_dead:
                    self.request("Idle")

        return task.cont

    def record(self):
        pos1 = self.character.getX()  # Player's position
        pos2 = self.enemy.character.getX()  # Enemy's position
        self.distance = abs(pos2 - pos1)

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

    def null_speed(self, a=0):
        self.is_moving = False
        self.speed = 0

    def set_speed(self, a=0):
        self.speed = 90
        self.enemy.speed = 90

    def setCollision(self, name):
        self.sphere_nodepath = self.character.attachNewNode(CollisionNode(self.sphere_name))
        # name is the name (cnode2) of our opponents collision capsule.
        self.sphere_nodepath.node().addSolid(self.c_sphere)
        # Uncomment this line to show the collision solid
        # self.sphere_nodepath.show()
        self.base.accept(f'{self.sphere_name}-into-{name}', self.null_speed)
        self.base.accept(f'{self.sphere_name}-again-{name}', self.null_speed)
        self.base.accept(f'{self.sphere_name}-out-{name}', self.set_speed)

    def Attack(self, attack):
        # Load an MP3 file as sound effect
        # self.atk_sound.play()
        # Load an MP3 file as background music
        self.request(attack)  # Play animation
        self.is_moving = False  # Stop movement
        if self.distance <= self.ranges[attack][0] and self.enemy.is_blocking is False:
            # An attack is valid if enemy is not blocking and within range
            self.enemy.health -= 5
            self.power += 12.5
            self.base.taskMgr.doMethodLater(self.ranges[attack][1], self.react, 'reaction time')
            # Calls the React function after an appropriate time has elapsed

    def block(self, state):
        self.is_blocking = state
        self.is_moving = False
        if state:
            self.request("Block")
        else:
            self.request("Idle")

    def react(self, task):
        dt = self.base.clock.dt
        self.enemy.request("Impact")  # Plays animation for when a hit is registered
        # sound = self.base.loader.loadSfx("models/gruntsound.wav")
        # sound.play()
        # self.enemy.player.setX(self.player.getX() + 1 * 20 * dt)
        return task.done


