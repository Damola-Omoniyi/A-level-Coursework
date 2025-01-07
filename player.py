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
        self.character = Actor("models/Knight/knight.bam",
                               {"Attack1": "models/Knight/knight_Attack1.bam",
                             "Attack2": "models/Knight/knight_Attack2.bam",
                             "Attack3": "models/Knight/knight_Attack3.bam",
                             "Attack4": "models/Knight/knight_Attack4.bam",
                             "Attack5": "models/Knight/knight_Attack5.bam",
                             "Block1": "models/Knight/knight_Block1.bam",
                             "Death1": "models/Knight/knight_Death1.bam",
                             "Death2": "models/Knight/knight_Death2.bam",
                             "Idle": "models/Knight/knight_Idle.bam",
                             "Impact1": "models/Knight/knight_Impact1.bam",
                             "Impact2": "models/Knight/knight_Impact2.bam",
                             "Intro1": "models/Knight/knight_Intro1.bam",
                             "Outro1": "models/Knight/knight_Outro1.bam",
                             "Special1": "models/Knight/knight_Special1.bam",
                             "Special2": "models/Knight/knight_Special2.bam",
                             "Special3": "models/Knight/knight_Special3.bam",
                             "Walk": "models/Knight/knight_Walk.bam",
                             "Jump": "models/Knight/knight_Jump.bam"
                             })

        self.gamepad_no = self.base.gamepad_nums[self.base.player_data[self.player_num - 1][2]]
        self.is_moving = False
        self.speed = 0
        self.direction = 0
        self.c_sphere = CollisionSphere(0, 0, 1, 0.25)
        self.sphere_name = f"cnode{self.player_num}"  # player1's name would be cnode1
        self.sphere_nodepath = self.character.attachNewNode(CollisionNode(self.sphere_name))

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


    def set_controls(self):
        self.base.accept("p", self.print_x)
        if self.gamepad_no == 2:
            self.base.accept("arrow_right", self.walk_forward)
            self.base.accept("arrow_left", self.walk_backward)
            self.base.accept('arrow_left-up', self.stop_walk)
            self.base.accept('arrow_right-up', self.stop_walk)
            self.base.accept('arrow_up', print, ["arrow-up"])
            self.base.accept("arrow_down", print, ["arrow-down"])
            self.base.accept("arrow_down-up", print, ["arrow-down-up"])
            self.base.accept("w", print, ["w"])
            self.base.accept("a", print, ["a"])
            self.base.accept('s', print, ["s"])
            self.base.accept('d', print, ["d"])
            self.base.accept('x', print, ["x"])
            self.base.accept('y', print, ["y"])

        elif self.gamepad_no < 2:
            self.base.controls.set_game_controls(self.gamepad_no)
            gamepad_name = f"gamepad{self.gamepad_no}"
            print(gamepad_name)
            self.base.accept(f"{gamepad_name}-face_x", print, ["x"])
            self.base.accept(f"{gamepad_name}-face_a", print, ["a"])
            self.base.accept(f"{gamepad_name}-face_b", print, ["b"])
            self.base.accept(f"{gamepad_name}-face_y", print, ["y"])
            self.base.accept(f"{gamepad_name}-dpad_up", print, ["up"])
            self.base.accept(f"{gamepad_name}-dpad_down", print, ["down"])
            self.base.accept(f"{gamepad_name}-dpad_down-up", print, ["down-up"])
            self.base.accept(f"{gamepad_name}-dpad_left", self.walk_backward)
            self.base.accept(f"{gamepad_name}-dpad_left-up", self.stop_walk)
            self.base.accept(f"{gamepad_name}-dpad_right", self.walk_forward)
            self.base.accept(f"{gamepad_name}-dpad_right-up", self.stop_walk)

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
                self.no_speed()
        
        if self.character.getX() >= 650:
            if self.direction == 1:
                self.no_speed()
            
        return task.cont

    def print_x(self):
        print(f"character {self.player_num} : {self.character.getX()}")

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

    def no_speed(self, a=0):
        self.is_moving = False
        self.speed = 0

    def set_speed(self, a=0):
        self.speed = 90
        self.enemy.speed = 90

    def setCollision(self, name):
        # name is the name (cnode2) of our opponents collision capsule.
        self.sphere_nodepath.node().addSolid(self.c_sphere)
        # Uncomment this line to show the collision solid
        # self.sphere_nodepath.show()

        self.base.accept(f'{self.sphere_name}-into-{name}', self.no_speed)
        self.base.accept(f'{self.sphere_name}-again-{name}', self.no_speed)
        self.base.accept(f'{self.sphere_name}-out-{name}', self.set_speed)


