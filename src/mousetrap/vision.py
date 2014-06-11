'''
All things computer vision. Isolates OpenCV from the rest of the system.
If you see another file using OpenCV directly, it should probably be using
this module instead.
'''

import cv2
import cv


S_CAPTURE_OPEN_ERROR = 'Device #%d does not support video capture interface'
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

class ImageConverter(object):

    @staticmethod
    def rgb_to_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


class HaarLoader(object):
    _haar_files = {
        "face": "haars/haarcascade_frontalface_default.xml",
        "nose": "haars/haarcascade_mcs_nose.xml",
    }

    _haar_cache = {}

    @staticmethod
    def from_name(name):
        if not name in HaarLoader._haar_files:
            # TODO: Throw an exception
            pass

        haar_file = HaarLoader._haar_files[name]

        haar = HaarLoader.from_file(haar_file, name)

        return haar

    @staticmethod
    def from_file(file, cache_name=None):
        import os

        if cache_name in HaarLoader._haar_cache:
            return HaarLoader._haar_cache[name]

        current_dir = os.path.dirname(os.path.realpath(__file__))

        haar_file = os.path.join(current_dir, file)

        haar = cv2.CascadeClassifier(haar_file)

        if not cache_name is None:
            if not cache_name in HaarLoader._haar_cache:
                HaarLoader._haar_cache[cache_name] = haar

        return haar
