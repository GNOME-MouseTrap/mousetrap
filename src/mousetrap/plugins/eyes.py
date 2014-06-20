import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
import mousetrap.log as log


LOGGER = log.getLogger(__name__)


class EyesPlugin(interface.Plugin):
    def __init__(self):
        self._left_locator = LeftEyeLocator()
        self._history = []
        self._is_closed = False

    def run(self, app):
        try:
            point_image = self._left_locator.locate(app.image)
            self._hit(point_image)
        except FeatureNotFoundException:
            self._miss()

        if self._detect_closed():
            self._history = []
            app.pointer.click()

    def _hit(self, point):
        self._history.append(point)

    def _miss(self):
        self._history.append(None)

    def _detect_closed(self):
        while len(self._history) > 15:
            del self._history[0]

        misses = self._history.count(None)

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

