import time
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT

class Motor():
        
    def __init__(self, channel, alpha=0.5, offset=0.2, i2c_bus=1, debug=False):
        self.i2c_bus, self.alpha, self.offset = i2c_bus, alpha, offset
        self.driver = Adafruit_MotorHAT(i2c_bus=self.i2c_bus)
        self.motor = self.driver.getMotor(channel)
        self._debug = debug
        self._channel = channel
        self._old_speed = -1
        
        if(channel == 1):
            self.ina, self.inb = 1, 0 
        else:
            self.ina, self.inb = 2, 3
        atexit.register(self.stop)
    
    def drive(self, value):
        # sets motor value between [-1, 1]
        if value > 0.0:
            mapped_value = int(255.0 * (self.alpha * value + self.offset))
        elif value < 0.0:
            mapped_value = int(255.0 * (self.alpha * value - self.offset))
        else:
             mapped_value = 0
        speed = min(max(abs(mapped_value), 0), 255)
        
        # debug : write changed speed
        if self._debug and self._old_speed != speed:
            print(f'channel {self._channel} speed:{speed}')
            self._old_speed = speed
            
        self.motor.setSpeed(speed)

        if mapped_value < 0:
            self.motor.run(Adafruit_MotorHAT.FORWARD)
            self.driver._pwm.setPWM(self.ina, 0, 0)
            self.driver._pwm.setPWM(self.inb, 0, speed*16)
        else:
            self.motor.run(Adafruit_MotorHAT.BACKWARD)
            self.driver._pwm.setPWM(self.ina, 0, speed*16)
            self.driver._pwm.setPWM(self.inb, 0, 0)
        
    def stop(self):
        self.motor.run(Adafruit_MotorHAT.RELEASE)
        self.driver._pwm.setPWM(self.ina, 0, 0)
        self.driver._pwm.setPWM(self.inb, 0, 0)  