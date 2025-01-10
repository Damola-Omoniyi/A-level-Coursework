# Controls module handles most logic related to in game controls and controller validation
from panda3d.core import InputDevice
# ----------------------------------------------------------------------------------------------------------------------


class Controller:
    def __init__(self, base):
        self.base = base
        self.controls_availability = {"keyboard": True, "gamepad1": True, "gamepad2": True, "CPU": True}
        # This dictionary stores the state of control availability if a control method is already in use or free to use

        self.gamepad = "Keyboard"
        self.gamepads = self.base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        self.base.taskMgr.add(self.update_controls_task, "UPdate controls ")
        # The list of all external game pads detected
        self.error_msg = ""

    def update_controls_task(self, task):
        self.gamepads = self.base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        return task.cont

    def check_valid_controls(self, controller):
        # This method checks if a control is valid for use by ensuring it is connected and available (not already being
        # used)
        connected = True

        if controller == "gamepad1" and len(self.gamepads) < 1:
            # If there is over one game pad detected then gamepad one is connected
            # There are no external gamepads connected
            connected = False

        elif controller == "gamepad2" and len(self.gamepads) < 2:
            # If there is over two game pads detected then gamepad two is connected
            connected = False

        if connected and self.controls_availability[controller]:
            return True
        elif not connected:
            self.error_msg = f"{controller} not found"
        elif not self.controls_availability[controller]:
            self.error_msg = f"{controller} already in use"
        return False

    def reset(self):
        # When the user leaves the character selection menu we should reset the control availability status
        self.controls_availability = {"keyboard": True, "gamepad1": True, "gamepad2": True, "CPU": True}
        self.gamepad = "Keyboard"

    def set_game_controls(self, gamepad_no):
        self.gamepad = self.gamepads[gamepad_no]
        gamepad_name = f"gamepad{gamepad_no}"
        self.base.attachInputDevice(self.gamepad, prefix=gamepad_name)
