# adapt the path values and the user in the script !!!

# this service prints stats
# if after staring of this service a file $HOME/oled.txt is preset, it will print this instead od stats
# during start of service an existing file $HOME/oled.txt will be deleted

# /etc/systemd/system/oled.service 
'''
[Unit]
[Unit]
After=network.service
[Service]
ExecStart=/usr/bin/python3 /home/jetson/jetson-nano/services/oled_service.py 
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

if len(sys.argv) > 1:
    if sys.argv[1] == 'SSD1306_128_32':
        disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)
    elif sys.argv[1] == 'SSD1306_128_64':
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
    else:
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
else:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
        
# Initialize library.
disp.begin()

file_name = str(Path.home()) + '/oled.txt'
if os.path.isfile(file_name):
    os.remove(file_name)

#file1 = open(file_name,"w")
#file1.write("Hello \n")
#file1.write(str(sys.argv))
#file1.close() #to change file access modes
    
    
# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()
#font = ImageFont.truetype("arial.ttf", 15)

cooling_fan = CoolingFan()

space = 8

file_last_modified = 0


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
        
            f = open(file_name, "r")
            row = 0
            for text in f:
                draw.text((x, top + 8 * row),text,  font=font, fill=255)
                row += 1
            f.close()
            # Display image.
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
            draw.text((x, top + space * i), f'{interface} {ip}',  font=font, fill=255)
        
        #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        #cpu_load = ip = exec_cmd(cmd)
        cmd = "free -m | awk 'NR==2{printf \"mem %.0f%%\", $3*100/$2 }'"
        mem_usage = ip = exec_cmd(cmd)
        cmd = "free -m | awk 'NR==3{printf \"swap %.0f%%\", $3*100/$2 }'"
        swap_usage = ip = exec_cmd(cmd)
        fan = f'fan {100 * cooling_fan.get_speed() // 255}%  temp {cooling_fan.get_temp()}°C'
    
        draw.text((x, top + space * 2),    
                  f'{mem_usage} % {swap_usage} %',  
                  font=font, 
                  fill=255)
        draw.text((x, top + space * 3),    
                  fan,  font=font,
                  fill=255)
        #draw.text((x, top + space * 4),    
        #          f'check {file_name}',  font=font,
        #          fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(5)
