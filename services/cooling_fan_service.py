# /etc/systemd/system/cooling_fan.service 
# adapt the path values in the script !!!

'''
[Unit]
After=network.service
[Service]
ExecStart=/usr/bin/python3 /home/jetson/jetson-nano/services/cooling_fan_service.py
User=root
WorkingDirectory=/home/jetson/jetson-nano/services
ExecStop=/bin/echo "0" > /sys/devices/pwm-fan/target_pwm

[Install]
WantedBy=default.target
'''

# sudo systemctl enable cooling_fan.service  -> activate initial
# sudo systemctl daemon-reload               -> only needed after changes 
# sudo systemctl start cooling_fan.service   -> only needed after daemon-reload
# systemctl status cooling_fan.service       -> show log


import sys, time
sys.path.append('../')
from utils.cooling_fan import CoolingFan

MIN_SPEED = 35
TEMP_FAN_OFF = 35
TEMP_FAN_MAX = 55
    
cooling_fan = CoolingFan()

# switch fan on for 1 second
cooling_fan.set_speed(200)
time.sleep(1)
cooling_fan.set_speed(0)

# forever loop
while True:
    # calculate target speed
    temp = cooling_fan.get_temp()
    if temp < TEMP_FAN_OFF:
        target_speed = 0
    elif temp > TEMP_FAN_MAX:
        target_speed =  255
    else:
        target_speed = MIN_SPEED + int((255 - MIN_SPEED) * (temp - TEMP_FAN_OFF) / (TEMP_FAN_MAX - TEMP_FAN_OFF))
    
    # get current speed
    current_speed = cooling_fan.get_speed()
    
    # change if difference > 5
    if abs(current_speed - target_speed) > 10:
        cooling_fan.set_speed(target_speed)
        # debug only : print(target_speed)
    time.sleep(10)
