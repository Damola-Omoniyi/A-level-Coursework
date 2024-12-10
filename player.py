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

