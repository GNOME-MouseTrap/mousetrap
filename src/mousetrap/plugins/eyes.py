import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
import mousetrap.log as log


LOGGER = log.get_logger(__name__)


class EyesPlugin(interface.Plugin):
    def __init__(self):
        self._max_pointer_samples = 5
        self._max_eye_samples = 15
        self._min_fraction_to_be_closed = 0.8

        self._min_misses_to_be_closed = int(
                self._min_fraction_to_be_closed * self._max_eye_samples)

        self._eye_detection_history = History(self._max_eye_samples)
        self._pointer_history = History(self._max_pointer_samples)

        self._left_locator = LeftEyeLocator()

    def run(self, app):
        self._update_eye_detection_history(app.image)
        self._update_pointer_history(app.pointer)

        if self._stationary(app) and self._detect_closed():
            self._eye_detection_history.clear()
            app.pointer.click()

    def _update_eye_detection_history(self, image):
        self._eye_detection_history.append(self._left_locator.locate(image))

    def _update_pointer_history(self, pointer):
        self._pointer_history.append(pointer.get_position())

    def _stationary(self, app):
        last_point = self._pointer_history[-1]

        for point in self._pointer_history:
            if point != last_point:
                return False

        return True

    def _detect_closed(self):
        misses = self._eye_detection_history.count(False)

        return misses > self._min_misses_to_be_closed


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


