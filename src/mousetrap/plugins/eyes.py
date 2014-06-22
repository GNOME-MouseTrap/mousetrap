import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
import mousetrap.log as log


LOGGER = log.get_logger(__name__)


class EyesPlugin(interface.Plugin):
    def __init__(self):
        self._left_locator = LeftEyeLocator()
        self._eye_detection_history = []
        self._pointer_history = []
        self._is_closed = False

    def run(self, app):
        try:
            point_image = self._left_locator.locate(app.image)
            self._hit(point_image)
        except FeatureNotFoundException:
            self._miss()

        if self._stationary(app) and self._detect_closed():
            self._eye_detection_history = []
            app.pointer.click()

    def _hit(self, point):
        self._eye_detection_history.append(point)

    def _miss(self):
        self._eye_detection_history.append(None)

    def _stationary(self, app):
        self._pointer_history.append(app.pointer.get_position())

        last_point = app.pointer.get_position()

        while len(self._pointer_history) > 5:
            del self._pointer_history[0]

        for point in self._pointer_history:
            if point != last_point:
                return False

        return True

    def _detect_closed(self):
        while len(self._eye_detection_history) > 15:
            del self._eye_detection_history[0]

        misses = self._eye_detection_history.count(None)

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
        face = self._face_detector.detect(image)
        eye = self._eye_detector.detect(face["image"])

        LOGGER.debug(eye)

        return (0, 0)
