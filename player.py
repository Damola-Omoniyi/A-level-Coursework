class Player():
    def __init__(self, player_num, base, character="Crypto"):
        self.base = base
        self.player_num = player_num
        #self.character = character
        self.enemy = None

        self.gamepad_no = self.base.gamepad_nums[self.base.player_data[self.player_num - 1][2]]
        # if self.gamepad_no is not False or self.gamepad_no != 2:

    def start(self):
        self.set_controls()

    def set_controls(self):
        if self.gamepad_no == 2:
            self.accept("arrow_right", print, ["arrow-right"])
            self.accept("arrow_left", print, ["arrow-left"])
            self.accept('arrow_left-up', print, ["arrow-right-up"])
            self.accept('arrow_right-up', print, ["arrow-left-up"])
            self.accept('arrow_up', print, ["arrow-up"])
            self.accept("arrow_down", print, ["arrow-down"])
            self.accept("arrow_down-up", ["arrow-down-up"])
            self.accept("w", print, ["w"])
            self.accept("a", print, ["a"])
            self.accept('s', print, ["s"])
            self.accept('d', print, ["d"])
            self.accept('x', print, ["x"])
            self.accept('y', print, ["y"])

        else:
            self.base.controls.set_game_controls(self.gamepad_no)
            gamepad_name = f"gamepad{self.gamepad_no}"
            print(gamepad_name)
            self.accept(f"{gamepad_name}-face_x", print, ["x"])
            self.accept(f"{gamepad_name}-face_a", print, ["a"])
            self.accept(f"{gamepad_name}-face_b", print, ["b"])
            self.accept(f"{gamepad_name}-face_y", print, ["y"])
            self.accept(f"{gamepad_name}-dpad_up", print, ["up"])
            self.accept(f"{gamepad_name}-dpad_down", print, ["down"])
            self.accept(f"{gamepad_name}-dpad_down-up", print, ["down-up"])
            self.accept(f"{gamepad_name}-dpad_left", print, ["left"])
            self.accept(f"{gamepad_name}-dpad_left-up", print, ["left-up"])
            self.accept(f"{gamepad_name}-dpad_right", print, ["right"])
            self.accept(f"{gamepad_name}-dpad_right-up", print, ["right-up"])

