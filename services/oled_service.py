# adapt the path values and the user and the display type in the script !!!

# this service prints stats
# if after staring of this service a file $HOME/oled.txt is preset, it will print this instead od stats
# /etc/systemd/system/oled.service 
'''
[Unit]
[Unit]
After=network.service
[Service]
ExecStart=/usr/bin/python3 /home/jetson/github/jetson-nano/services/oled_service.py SSD1306_128_32
User=jetson
WorkingDirectory=/home/jetson/github/jetson-nano/services/

[Install]
WantedBy=default.target
'''


# sudo systemctl enable oled.service  -> activate initial
# sudo systemctl daemon-reload        -> only needed after changes 
    # sudo systemctl start oled.service   -> only needed after daemon-reload
# systemctl status oled.service      -> show log

import sys, time, os, subprocess
from pathlib import Path
sys.path.append('../')
from utils.oled import Oled_display
from utils.cooling_fan import CoolingFan
from utils.battery import Battery

time.sleep(3)

# get display type from args
if len(sys.argv) > 1:
    if sys.argv[1] in ['SSD1306_128_32', 'SSD1306_128_64']: 
        disp = Oled_display(i2c_bus=1, oled_type=sys.argv[1])
    # default that is often installed on jetbots
    else:
        disp = Oled_display(i2c_bus=1, oled_type='SSD1306_128_32')
        
# check if battery and AD is connected
is_battery = True
battery = Battery()
try:
    battery.read_voltage()  
except:
    is_battery = False
        
# cusom file to show         
file_name = str(Path.home()) + '/oled.txt'
file_last_modified = 0

# helper function to get fan date and temperature
cooling_fan = CoolingFan()

def exec_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]
    except:
        return "-"

while True:
    
    if os.path.isfile(file_name):
        if (file_last_modified != os.path.getmtime(file_name)):
            file_last_modified = os.path.getmtime(file_name)
 
            # read rows from file
            f = open(file_name, "r")
            text_raws = []
            for text_row in f:
                text_raws.append(text_row)
            f.close()
            
            
            disp.draw_text(text_raws, len(text_raws))
            time.sleep(0.1)
        else:
            time.sleep(0.1)
    # stats         
    else:
        text_raws = []
        # network connection(s)
        for i, interface in enumerate(['eth0', 'wlan0']):
            operstate = exec_cmd(f'cat /sys/class/net/{interface}/operstate')
            if operstate == 'up' :  
                cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' \
                | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
                ip = exec_cmd(cmd)
            else:
                ip = ''
            text_raws.append(f'{interface} {ip}')
        # memory and swap
        cmd = "free -m | awk 'NR==2{printf \"mem %.0f%%\", $3*100/$2 }'"
        mem_usage = ip = exec_cmd(cmd)
        cmd = "free -m | awk 'NR==3{printf \"swap %.0f%%\", $3*100/$2 }'"
        swap_usage = ip = exec_cmd(cmd)
        text_raws.append(f'{mem_usage} % {swap_usage} %')
        # fan or battery and temperature
        if is_battery:
            fan_batt_temp = f'bat {battery.read_voltage() / 1000:0.1f}V temp {cooling_fan.get_temp()}°C'
        else:
            fan_batt_temp = f'fan {100 * cooling_fan.get_speed() // 255}% temp {cooling_fan.get_temp()}°C'
        
        text_raws.append(fan_batt_temp)
        
        disp.draw_text(text_raws)
        
        time.sleep(3)