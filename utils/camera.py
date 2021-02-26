import os
import time
import getpass
import atexit
import cv2


class Camera:

    def _init_cap(self):
        if self._debug is True:
            print(self._gst_str())
        self._cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)
        time.sleep(1)
        # not possible to change CV_CAP_PROP_BUFFERSIZE on jetson nano ?
        re, _ = self._cap.read()
        return re

    def __init__(self, capture_device=0, capture_fps=30, capture_width=640, capture_height=480,
                 width=224, height=224, flip_mode=0, debug=False):
        """
        init camera
        :param capture_device: 0 or 1 for internal cameras. usb cam is not implemented yet
        :param capture_fps:  fps that must be supported by camera
        :param capture_width: width must be supported by camera
        :param capture_height: height must be supported by camera
        :param width: with that will be returned in the getter
        :param height: height that will be returned in the getter
        :param flip_mode: 0=normal  -1=flipped
        :param debug: show debug messages
        """
        self._capture_width, self._capture_height, self._width, self._height = capture_width, capture_height, width, height
        self._capture_device, self._capture_fps, self._flip_mode = capture_device, capture_fps, flip_mode
        self._debug = debug

        if not self._init_cap():
            print('try to kill old camera processes. maybe enter password')
            password = getpass.getpass()
            # can be any command but don't forget -S as it enables input from stdin
            command = "sudo -S systemctl restart nvargus-daemon"
            os.system('echo %s | %s' % (password, command))
            time.sleep(2)
            if not self._init_cap():
                raise RuntimeError(
                    'init stream failed. try restart kernel after exceute "sudo systemctl restart nvargus-daemon"')

        atexit.register(self._cap.release)

    def _gst_str(self):
        return 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, \
                format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, \
                height=(int)%d, format=(string)BGRx ! videoconvert ! appsink drop=true sync=false' % (
            self._capture_device, self._capture_width, self._capture_height, self._capture_fps, self._width,
            self._height)

    def get_image_rgb(self):
        """
        grabs, decodes and returns the current video frame
        :return: array image rgb
        """
        return cv2.cvtColor(self.get_image_bgr(), cv2.COLOR_BGR2RGB)

    def get_image_bgr(self):
        """
        grabs, decodes and returns the current video frame
        :return: array image bgr
        """
        re, image = self._cap.read()
        if re:
            return cv2.flip(image, self._flip_mode)
        else:
            raise RuntimeError('read image failed')
