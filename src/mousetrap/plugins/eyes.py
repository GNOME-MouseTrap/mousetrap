import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
import mousetrap.log as log


LOGGER = log.get_logger(__name__)


class EyesPlugin(interface.Plugin):
    def __init__(self):
        self._left_locator = LeftEyeLocator()
        self._eye_detection_history = History(max_length=15)
        self._pointer_history = History(max_length=5)
        self._is_closed = False

    def run(self, app):
        self._eye_detection_history.append(self._left_locator.locate(app.image))

        if self._stationary(app) and self._detect_closed():
            self._eye_detection_history.clear()
            app.pointer.click()

    def _stationary(self, app):
        self._pointer_history.append(app.pointer.get_position())

        last_point = app.pointer.get_position()

        for point in self._pointer_history:
            if point != last_point:
                return False

        return True

    def _detect_closed(self):
        misses = self._eye_detection_history.count(False)

        return misses > 12


class LeftEyeLocator(object):

    def __init__(self):
        self._face_detector = FeatureDetector(
            "face",
            scale_factor=1.5,
            min_neighbors=5,
        )
        self._eye_detector = FeatureDetector(
            "open_eye",
            scale_factor=1.1,
            min_neighbors=3,
        )

    def locate(self, image):
        try:
            face = self._face_detector.detect(image)
            eye = self._eye_detector.detect(face["image"])
            LOGGER.debug(eye)
            return True
        except FeatureNotFoundException:
            return False


class History(list):
    def __init__(self, max_length):
        super(History, self).__init__()
        self._max_length = max_length

    def append(self, value):
        super(History, self).append(value)
        while len(self) > self._max_length:
            del self[0]

    def clear(self):
        del self[:]


