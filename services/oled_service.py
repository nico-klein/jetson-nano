# adapt the path values and the user and the display type in the script !!!

# this service prints stats
# if after staring of this service a file $HOME/oled.txt is preset, it will print this instead od stats
# /etc/systemd/system/oled.service 
'''
[Unit]
[Unit]
After=network.service
[Service]
ExecStart=/usr/bin/python3 /home/jetson/jetson-nano/services/oled_service.py SSD1306_128_32
User=jetson
WorkingDirectory=/home/jetson/jetson-nano/services/

[Install]
WantedBy=default.target
'''


# sudo systemctl enable oled.service  -> activate initial
# sudo systemctl daemon-reload        -> only needed after changes 
# sudo systemctl start oled.service   -> only needed after daemon-reload
# systemctl status oled.service      -> show log

import time, os, sys, subprocess
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
sys.path.append('../')
from utils.cooling_fan import CoolingFan
from utils.battery import Battery

time.sleep(3)

# get display type from args
if len(sys.argv) > 1:
    if sys.argv[1] == 'SSD1306_128_32':
        disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)
    elif sys.argv[1] == 'SSD1306_128_64':
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
    else:
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
else:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
        
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

# initialize library and clear display
disp.begin()
disp.clear()
disp.display()

# create blank image for drawing
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# drawing object
draw = ImageDraw.Draw(image)

# load default font and bigger fonts
font = ImageFont.load_default()
fonts = {
    64 :ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf', 64),
    32: ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf', 32),
    16: ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf', 16),
    8: ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf', 8)
}


def exec_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]
    except:
        return "-"

while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    if os.path.isfile(file_name):
        if (file_last_modified != os.path.getmtime(file_name)):
            file_last_modified = os.path.getmtime(file_name)
 
            # read rows from file
            f = open(file_name, "r")
            rows = []
            for text_row in f:
                rows.append(text_row)
            f.close()
            
            # calculate best font
            fontsize = height / max(len(rows), 1)
            fontsize = max(fontsize, 8)
            
            for i, text_row in enumerate(rows):
                draw.text((0, fontsize * i),text_row,  font=fonts[fontsize], fill=255)
            disp.image(image)
            disp.display()
            time.sleep(0.1)
            
        else:
            time.sleep(0.1)
    # stats         
    else:
        # network connection(s)
        for i, interface in enumerate(['eth0', 'wlan0']):
            operstate = exec_cmd(f'cat /sys/class/net/{interface}/operstate')
            if operstate == 'up' :  
                cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' \
                | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
                ip = exec_cmd(cmd)
            else:
                ip = ''
            draw.text((0, 8 * i), f'{interface} {ip}',  font=font, fill=255)
        # memory and swap
        cmd = "free -m | awk 'NR==2{printf \"mem %.0f%%\", $3*100/$2 }'"
        mem_usage = ip = exec_cmd(cmd)
        cmd = "free -m | awk 'NR==3{printf \"swap %.0f%%\", $3*100/$2 }'"
        swap_usage = ip = exec_cmd(cmd)
        draw.text((0, 8 * 2),    
                  f'{mem_usage} % {swap_usage} %',  
                  font=font, 
                  fill=255)
        # fan or battery and temperature
        if is_battery:
            fan_batt_temp = f'bat {battery.read_voltage() / 1000:0.1f}V temp {cooling_fan.get_temp()}°C'
        else:
            fan_batt_temp = f'fan {100 * cooling_fan.get_speed() // 255}% temp {cooling_fan.get_temp()}°C'
        
        draw.text((0, 8 * 3),    
                  fan_batt_temp,  font=font,
                  fill=255)
        

        disp.image(image)
        disp.display()
        time.sleep(3)