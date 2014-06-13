import mousetrap.pointers.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
from mousetrap.gui import Gui, ScreenPointer

from mousetrap.pointers.nose import NoseLocator


class Pointer(interface.Pointer):
    THRESHOLD = 5

    def __init__(self):
        self._nose_locator = NoseLocator()
        self._image = None

        pointer = ScreenPointer()

        self._last_pointer_location = pointer.get_position()
        self._initial_image_location = (0, 0)

        self._location = self._last_pointer_location

    def update_image(self, image):
        self._image = image

        try:
            point_image = self._nose_locator.locate(image)
            point_screen = self._convert_image_to_screen_point(*point_image)
            self._location = point_screen
        except FeatureNotFoundException:
            self._location = None

    def _convert_image_to_screen_point(self, image_x, image_y):
        initial_x, initial_y = self._initial_image_location

        if initial_x == 0 and initial_y == 0:
            self._initial_image_location = (image_x, image_y)

            return self._initial_image_location

        delta_x = initial_x - image_x
        delta_y = image_y - initial_y

        if abs(delta_x) < self.THRESHOLD:
            delta_x = 0

        if abs(delta_y) < self.THRESHOLD:
            delta_y = 0

        if delta_x == 0 and delta_y == 0:
            return None

        pointer_x, pointer_y = self._last_pointer_location

        pointer_x += delta_x
        pointer_y += delta_y

        return (pointer_x, pointer_y)

    def get_new_position(self):
        if self._location:
            self._last_pointer_location = self._location

        return self._location
