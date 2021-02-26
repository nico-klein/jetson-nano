from evdev import InputDevice

# TODO docstrings
# constants from PS 5 controller
# '/dev/input/event4'

class Gamepad():
        
    BUTTON_CROSS = 305
    BUTTON_SQUARE = 304
    BUTTON_TRIANGLE = 207
    BUTTON_CIRCLE = 306
    BUTTON_L1 = 308
    BUTTON_L2 = 310
    BUTTON_L3 = 314
    BUTTON_R1 = 309
    BUTTON_R2 = 311
    BUTTON_R3 = 315
    BUTTON_OPTIONS = 313
    BUTTON_CREATE = 312
    BUTTON_PS = 316
    BUTTON_TOUCHPAD = 317
    ANALOG_L_SIDE = 0
    ANALOG_L_UPDOWN = 1
    ANALOG_R_SIDE = 2
    ANALOG_R_UPDOWN = 5
    ANALOG_L2 = 3
    ANALOG_R2 = 4
              
    def __init__(self, device_name):
        self._device_name = device_name
        self._gamepad = InputDevice(self._device_name)
        
    def get_active_keys(self):
        return self._gamepad.active_keys()
        
    def get_analog_value(self, id):
        return self._gamepad.absinfo(id).value

