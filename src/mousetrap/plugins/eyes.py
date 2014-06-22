import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
import mousetrap.log as log


LOGGER = log.get_logger(__name__)


class EyesPlugin(interface.Plugin):
    def __init__(self):
        self._motion_detector = MotionDetector()
        self._closed_detector = ClosedDetector()

    def run(self, app):
        self._motion_detector.update(app.pointer)
        self._closed_detector.update(app.image)

        if self._motion_detector.is_stationary() and \
                self._closed_detector.is_closed():
            self._closed_detector.reset()
            app.pointer.click()


class MotionDetector(object):
    def __init__(self):
        self._max_samples = 5
        self._history = History(self._max_samples)

    def update(self, pointer):
        self._history.append(pointer.get_position())

    def is_stationary(self):
        last_point = self._history[-1]
        return all([point == last_point for point in self._history])


class ClosedDetector(object):
    def __init__(self):
        self._max_samples = 15
        self._min_fraction_to_be_closed = 0.8
        self._min_misses_to_be_closed = int(
                self._min_fraction_to_be_closed * self._max_samples)
        self._left_locator = LeftEyeLocator()
        self._detection_history = History(self._max_samples)

    def update(self, image):
        self._detection_history.append(self._left_locator.locate(image))

    def is_closed(self):
        misses = self._detection_history.count(False)
        return misses > self._min_misses_to_be_closed

    def reset(self):
        self._detection_history.clear()


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
