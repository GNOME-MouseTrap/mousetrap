import mousetrap.parts.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
from mousetrap.gui import Gui


class Part(interface.Part):
    def __init__(self):
        self._nose_locator = NoseLocator()
        self._gui = Gui()
        self._location = None
        self._image = None

    def update_image(self, image):
        self._image = image
        try:
            point_image = self._nose_locator.locate(image)
            point_screen = self._convert_image_to_screen_point(*point_image)
            self._location = point_screen
        except FeatureNotFoundException:
            self._location = None

    def _convert_image_to_screen_point(self, image_x, image_y):
        image_width = self._image.get_width()
        image_height = self._image.get_height()
        percent_x = 1.0 * image_x / image_width
        percent_y = 1.0 * image_y / image_height
        screen_x = percent_x * self._gui.get_screen_width()
        screen_y = percent_y * self._gui.get_screen_height()
        half_width = self._gui.get_screen_width() / 2
        screen_x = (-1 * (screen_x - half_width)) + half_width
        return (screen_x, screen_y)

    def get_new_position(self):
        return self._location


class NoseLocator(object):
    def __init__(self):
        self._face_detector = FeatureDetector(
                'face', scale_factor=1.5, min_neighbors=5)
        self._nose_detector = FeatureDetector(
                'nose', scale_factor=1.1, min_neighbors=5)

    def locate(self, image):
        face = self._face_detector.detect(image)
        nose = self._nose_detector.detect(face['image'])
        return (
                face['x'] + nose['center']['x'],
                face['y'] + nose['center']['y'],
                )
