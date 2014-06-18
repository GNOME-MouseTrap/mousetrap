import mousetrap.pointers.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
from mousetrap.gui import ScreenPointer
import logging


LOGGER = logging.getLogger(__name__)


class Pointer(interface.Pointer):
    def __init__(self):

        self._left_locator = LeftEyeLocator()

        self._history = []

        self._is_closed = False

    def update_image(self, image):
        try:
            point_image = self._left_locator.locate(image)

            self._hit(point_image)
        except FeatureNotFoundException:
            self._miss()

    def _hit(self, point):
        self._history.append(point)

    def _miss(self):
        self._history.append(None)

    def _detect_closed(self):
        while len(self._history) > 15:
            del self._history[0]

        misses = self._history.count(None)

        return misses > 12

    def get_new_position(self):
        return None

    def get_pointer_events(self):
        if self._detect_closed():
            self._is_closed = True
            if not self._is_closed:
                return [ScreenPointerEvent(
                            ScreenPointer.EVENT_CLICK,
                            ScreenPointer.BUTTON_LEFT)]
        else:
            self._is_closed = False
        return []


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

