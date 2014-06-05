'''
All things computer vision. Isolates OpenCV from the rest of the system.
If you see another file using OpenCV directly, it should probably be using
this module instead.
'''

import cv2
from cv2 import cv


S_CAPTURE_OPEN_ERROR = 'Device #%s does not support video capture interface'
S_CAPTURE_READ_ERROR = 'Error while capturing. Camera disconnected?'


class Camera(object):
    def __init__(self, device_index, width, height):
        self.device = self._new_capture_device(device_index)
        self._set_dimensions(width, height)

    @staticmethod
    def _new_capture_device(device_index):
        capture = cv2.VideoCapture(device_index)
        if not capture.isOpened():
            capture.release()
            raise IOError(S_CAPTURE_OPEN_ERROR % device_index)
        return capture

    def _set_dimensions(self, width, height):
        self.device.set(cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.device.set(cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    def read_image(self):
        ret, image = self.device.read()
        if not ret:
            raise IOError(S_CAPTURE_READ_ERROR)
        return image

