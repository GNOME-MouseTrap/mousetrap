import mousetrap.pointers.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException


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

    def get_keys(self):
        if self._detect_closed():
            if not self._is_closed:
                self._is_closed = True

                return LeftClick()

            self._is_closed = True
        else:
            self._is_closed = False

        return None


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

        print eye

        return (0, 0)


class LeftClick(object):

    def get_actions(self):
        from Xlib import X

        press = Button(event=X.ButtonPress)

        release = Button(event=X.ButtonRelease)

        return [press, release]


class Button(object):

    def __init__(self, event, button=1):
        self.event = event
        self.button = button
