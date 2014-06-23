import mousetrap.plugins.interface as interface
from mousetrap.vision import FeatureDetector, FeatureNotFoundException
from mousetrap.plugins.nose import NoseLocator


class NoseJoystickPlugin(interface.Plugin):

    def __init__(self, config):
        self._config = config
        self._threshold = config[self]['threshold']
        self._nose_locator = NoseLocator(config)
        self._initial_image_location = (0, 0)
        self._last_delta = (0, 0)

    def run(self, app):
        self._app = app
        location = None
        try:
            point_image = self._nose_locator.locate(app.image)
            point_screen = self._convert_image_to_screen_point(*point_image)
            location = point_screen
        except FeatureNotFoundException:
            location = app.pointer.get_position()
            location = self._apply_delta_to_point(location, self._last_delta)
        app.pointer.set_position(location)

    def _apply_delta_to_point(self, point, delta):
        delta_x, delta_y = delta
        point_x, point_y = point

        if delta_x == 0 and delta_y == 0:
            return None

        point_x += delta_x
        point_y += delta_y

        return (point_x, point_y)

    def _convert_image_to_screen_point(self, image_x, image_y):
        initial_x, initial_y = self._initial_image_location

        if initial_x == 0 and initial_y == 0:
            self._initial_image_location = (image_x, image_y)

            return self._initial_image_location

        delta_x = initial_x - image_x
        delta_y = image_y - initial_y

        if abs(delta_x) < self._threshold:
            delta_x = 0

        if abs(delta_y) < self._threshold:
            delta_y = 0

        delta = (delta_x, delta_y)

        self._last_delta = delta

        location = self._app.pointer.get_position()

        return self._apply_delta_to_point(location, delta)
