from gi.repository import Gdk


class Mouse:
    def __init__(self):
        self._pointer = None
        self._screen = None

        gdk_display = Gdk.Display.get_default()
        self._screen = gdk_display.get_default_screen()

        device_manager = gdk_display.get_device_manager()
        self._pointer = device_manager.get_client_pointer()

    def get_position(self):
        X_INDEX = 1
        Y_INDEX = 2
        position = self._pointer.get_position()
        return (position[X_INDEX], position[Y_INDEX])

    def set_position(self, x, y):
        self._pointer.warp(self._screen, x, y)

