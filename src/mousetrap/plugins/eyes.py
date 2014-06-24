import logging
LOGGER = logging.getLogger(__name__)


import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException


class EyesPlugin(interface.Plugin):
    def __init__(self, config):
        self._config = config
        self._motion_detector = MotionDetector(config)
        self._closed_detector = ClosedDetector(config)

    def run(self, app):
        self._motion_detector.update(app.pointer)
        self._closed_detector.update(app.image)

        if self._motion_detector.is_stationary() and \
                self._closed_detector.is_closed():
            self._closed_detector.reset()
            app.pointer.click()


class MotionDetector(object):
    def __init__(self, config):
        self._config = config
        self._max_samples = config[self]['max_samples']
        self._history = History(config, self._max_samples)

    def update(self, pointer):
        self._history.append(pointer.get_position())

    def is_stationary(self):
        last_point = self._history[-1]
        return all([point == last_point for point in self._history])


class ClosedDetector(object):
    def __init__(self, config):
        self._config = config
        self._max_samples = config[self]['max_samples']
        self._min_fraction_to_be_closed = config[self]['min_fraction_to_be_closed']
        self._min_misses_to_be_closed = int(
            self._min_fraction_to_be_closed * self._max_samples)
        self._left_locator = LeftEyeLocator(config)
        self._detection_history = History(config, self._max_samples)

    def update(self, image):
        self._detection_history.append(self._left_locator.locate(image))

    def is_closed(self):
        misses = self._detection_history.count(False)
        return misses > self._min_misses_to_be_closed

    def reset(self):
        self._detection_history.clear()


class LeftEyeLocator(object):

    def __init__(self, config):
        self._config = config
        self._face_detector = FeatureDetector(
            config,
            "face",
            scale_factor=config[self]['face_detector']['scale_factor'],
            min_neighbors=config[self]['face_detector']['min_neighbors'],
        )
        self._open_eye_detector = FeatureDetector(
            config,
            "open_eye",
            scale_factor=config[self]['open_eye_detector']['scale_factor'],
            min_neighbors=config[self]['open_eye_detector']['min_neighbors'],
        )
        self._left_eye_detector = FeatureDetector(
            config,
            "left_eye",
            scale_factor=config[self]['left_eye_detector']['scale_factor'],
            min_neighbors=config[self]['left_eye_detector']['min_neighbors'],
        )

    def locate(self, image):
        face = None

        try:
            face = self._face_detector.detect(image)

            LOGGER.debug(_("Found the face"))
        except FeatureNotFoundException:
            return True

        try:
            left_eye = self._left_eye_detector.detect(face["image"])

            LOGGER.debug(_("Found the left eye at %s"), left_eye)
        except FeatureNotFoundException:
            return True

        try:
            open_eye = self._open_eye_detector.detect(face["image"])

            LOGGER.debug(_("Found an open eye at %s"), open_eye)

            return True
        except FeatureNotFoundException:
            return False


class History(list):
    def __init__(self, config, max_length):
        super(History, self).__init__()
        self._config = config
        self._max_length = max_length

    def append(self, value):
        super(History, self).append(value)
        while len(self) > self._max_length:
            del self[0]

    def clear(self):
        del self[:]
