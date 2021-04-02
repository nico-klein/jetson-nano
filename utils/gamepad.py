from evdev import InputDevice

# TODO docstrings
# '/dev/input/event4'

class Gamepad():
    def __init__(self, device_name):
        self._device_name = device_name
        self._gamepad = InputDevice(self._device_name)
        
    def get_active_keys(self):
        return self._gamepad.active_keys()
        
    def get_analog_value(self, id):
        return self._gamepad.absinfo(id).value


# works with model #1914 (2020=
class XBoxController (Gamepad):
    BUTTON_B = 305
    BUTTON_A = 304
    BUTTON_X = 207
    BUTTON_Y = 308
    BUTTON_OPTIONS = 315
    BUTTON_MAP = 314
    BUTTON_RB = 311
    BUTTON_LB = 310
    BUTTON_R = 318
    BUTTON_L = 317
    BUTTON_XBOX = 316
    ANALOG_LT = 2
    ANALOG_RT = 5
    ANALOG_L_SIDE = 0
    ANALOG_L_UPDOWN = 1
    ANALOG_L_SIDE = 3
    ANALOG_L_UPDOWN = 4
    
    pass


# works with PS 5 controller (2020)
class PS5DualSense (Gamepad):       
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
    
    pass