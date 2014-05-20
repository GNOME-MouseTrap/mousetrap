import cv2


class Camera(object):

    def __init__(self, device_id=0):
        self._device_id = device_id
        self._capture = None

    def start_camera(self):
        self._capture = cv2.VideoCapture(self._device_id)

    def get_image(self):
        if not self.is_started():
            raise CameraError("Camera has not been started.")
        return self._read_image()

    def is_started(self):
        return self._capture is not None and self._capture.isOpened()

    def _read_image(self):
        read_was_successful, image = self._capture.read()
        if not read_was_successful:
            raise CameraError("Read was not successful.")
        return image


class CameraError(Exception):

    def __init__(self, message):
        super(CameraError, self).__init__()
        self.message = message
