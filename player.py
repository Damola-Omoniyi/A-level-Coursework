class Player():
    def __init__(self, player_num, base, character="Crypto"):
        self.base = base
        self.player_num = player_num
        #self.character = character
        self.enemy = None

        self.gamepad_no = self.base.gamepad_nums[self.base.player_data[self.player_num - 1][2]]

    def start(self):
        self.set_controls()

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

