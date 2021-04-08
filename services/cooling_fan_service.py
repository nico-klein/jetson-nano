# /etc/systemd/system/cooling_fan.service 
'''
[Unit]
After=network.service
[Service]
ExecStart=/usr/bin/python3 /home/jetson/notebooks/jetson-nano/services/cooling_fan_service.py
User=jetson
WorkingDirectory=/home/jetson/notebooks/jetson-nano/services

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

cooling_fan = CoolingFan()

# switch fan on for 2 seconds
cooling_fan.set_speed(255)
time.sleep(2)
cooling_fan.set_speed(0)
sys.stdout.write('cooling_fan service started with speed:'+ str(cooling_fan.calculate_cooling_speed())+  '\n')
sys.stdout.write('current temperature:' + str(cooling_fan.get_temp()) + '\n')

# forever loop
while True:
    current_speed = cooling_fan.get_speed()
    target_speed = cooling_fan.calculate_cooling_speed()
    
    ## change if difference > 10
    if abs(current_speed - target_speed) > 10:
        cooling_fan.set_speed(target_speed)
        # debug only : print(target_speed)
    time.sleep(10)
