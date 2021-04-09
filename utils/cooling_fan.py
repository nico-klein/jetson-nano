class CoolingFan():
    def __init__(self):
        pass
        
    def get_temp(self):
        with open("/sys/devices/virtual/thermal/thermal_zone0/temp","r") as file:
            temp = int(file.read()) /1000
        return temp
    
    # only possible with root rights (e.g. in service)
    def set_speed(self, speed):
        with open("/sys/devices/pwm-fan/target_pwm","w") as file:
            file.write(f"{speed}")
    
    def get_speed(self):
        with open("/sys/devices/pwm-fan/target_pwm","r") as file:
            temp = int(file.read())
            return temp
