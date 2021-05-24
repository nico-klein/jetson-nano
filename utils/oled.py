import time, os, sys, subprocess
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class Oled_display(object):
  
    def __init__(self, i2c_bus, oled_type):
        if oled_type == 'SSD1306_128_64':
            self._disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=i2c_bus, gpio=1)
        elif oled_type == 'SSD1306_128_32':
            self._disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=i2c_bus, gpio=1)
        else:
            print('unknown display type')
            return
        
        self._disp.begin()
        self._disp.clear()
        self._disp.display()
        
        # create blank image for drawing
        self._image = Image.new('1', (self._disp.width, self._disp.height))
        # drawing object
        self._draw = ImageDraw.Draw(self._image)

        # load bigger fonts
        try:
            self._fonts = {i : ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf', i) 
                       for i in [9, 10, 12, 16, 21, 32, 64]}
        except:   
            self._fonts = {}
        
        # default font
        self._fonts[8] = ImageFont.load_default() 
        
    def get_display(self):
        return self._disp
    
    def clear(self):
        self._draw.rectangle((0, 0 , self._disp.width, self._disp.height), outline=0, fill=0) 
        self._disp.image(self._image)
        self._disp.display()
            
    def draw_text(self, texts, rows=None):
        self._draw.rectangle((0 ,0 ,self._disp.width, self._disp.height), outline=0, fill=0) 
        # default font
        if rows is None:
            fontsize = 8
            
        # calculate font    
        else:
            fontsize = self._disp.height // rows
            
            #default if not found
            if fontsize not in list(self._fonts.keys()):
                fontsize = 8
            
        for i, text_row in enumerate(texts):
            self._draw.text((0, fontsize * i), text_row,  font=self._fonts[fontsize], fill=255)
        self._disp.image(self._image)
        self._disp.display()