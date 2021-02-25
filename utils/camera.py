import os
import json
import time
import getpass
import atexit
import cv2

class Camera():

    def _init_cap(self):
        if self.debug is True:
            print(self._gst_str())
        self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)
        time.sleep(1)
        # not possible to change CV_CAP_PROP_BUFFERSIZE on jetson nano ?
        re, _ = self.cap.read()
        return re

    def __init__(self, capture_device=0, capture_fps=30, capture_width=640, capture_height=480,
                 width=224, height=224, flip_mode=0, debug=False):

        self.capture_width, self.capture_height, self.width, self.height = capture_width, capture_height, width, height
        self.capture_device, self.capture_fps, self.flip_mode = capture_device, capture_fps, flip_mode
        self.debug=debug

        if not self._init_cap():
            print('try to kill old camera processes. maybe enter password')
            password = getpass.getpass()
            # can be any command but don't forget -S as it enables input from stdin
            command = "sudo -S systemctl restart nvargus-daemon"
            os.system('echo %s | %s' % (password, command))
            time.sleep(2)
            if not self._init_cap():
                raise RuntimeError('init stream failed. try restart kernel after exceute "sudo systemctl restart nvargus-daemon"')

        atexit.register(self.cap.release)

    def _gst_str(self):
        return 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, \
                format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, \
                height=(int)%d, format=(string)BGRx ! videoconvert ! appsink drop=true sync=false' % (
            self.capture_device, self.capture_width, self.capture_height, self.capture_fps, self.width, self.height)

    def get_image_rgb(self):
        return cv2.cvtColor(self.get_image_bgr(), cv2.COLOR_BGR2RGB)
        
    def get_image_bgr(self):
        re, image = self.cap.read()
        if re:
            return cv2.flip(image, self.flip_mode)
        else:
            raise RuntimeError('read image failed')
