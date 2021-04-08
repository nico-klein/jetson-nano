# sudo chmod 777 /sys/devices/pwm-fan/target_pwm

class CoolingFan():
    def __init__(self):
        self.TEMP_FAN_OFF = 25
        self.TEMP_FAN_MAX = 50
        
    def get_temp(self):
        with open("/sys/devices/virtual/thermal/thermal_zone0/temp","r") as file:
            temp = int(file.read()) /1000
        return temp
    
    def set_speed(self, speed):
        with open("/sys/devices/pwm-fan/target_pwm","w") as file:
            file.write(f"{speed}")
    
    def get_speed(self):
        with open("/sys/devices/pwm-fan/target_pwm","r") as file:
            temp = int(file.read())
            return temp
            
    def calculate_cooling_speed(self):
        temp = self.get_temp()
        if temp < self.TEMP_FAN_OFF:
            return 0
        elif temp > self.TEMP_FAN_MAX:
            return 255
        else:
            return int(255 * (temp - self.TEMP_FAN_OFF) / (self.TEMP_FAN_MAX - self.TEMP_FAN_OFF))
   