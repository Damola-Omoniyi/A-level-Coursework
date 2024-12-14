from direct.fsm.FSM import FSM
from direct.actor.Actor import Actor

class Player(FSM):
    def __init__(self, player_num, base):
        FSM.__init__(self, "character-FSM")

        self.base = base
        self.player_num = player_num
        self.enemy = None
        self.character =  Actor("models/Knight/knight.bam",
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

    def start(self):
        self.set_controls()
        self.character.reparentTo(self.base.render)
        self.character.setScale(150)
        self.character.setPos(0, 1000, -150)
        if self.player_num == 1:
            self.character.setX(-200)
            self.character.setH(90)
        elif self.player_num == 2:
            self.character.setH(270)
            self.character.setX(200)



    def set_controls(self):
        if self.gamepad_no == 2:
            self.base.accept("arrow_right", print, ["arrow-right"])
            self.base.accept("arrow_left", print, ["arrow-left"])
            self.base.accept('arrow_left-up', print, ["arrow-right-up"])
            self.base.accept('arrow_right-up', print, ["arrow-left-up"])
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
            self.base.accept(f"{gamepad_name}-dpad_left", print, ["left"])
            self.base.accept(f"{gamepad_name}-dpad_left-up", print, ["left-up"])
            self.base.accept(f"{gamepad_name}-dpad_right", print, ["right"])
            self.base.accept(f"{gamepad_name}-dpad_right-up", print, ["right-up"])
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



