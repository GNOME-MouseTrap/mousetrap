from gi.repository import Gdk


class Pointer(object):

    def __init__(self):
        gdk_display = Gdk.Display.get_default()
        device_manager = gdk_display.get_device_manager()
        self._pointer = device_manager.get_client_pointer()
        self._screen = gdk_display.get_default_screen()

    def get_position(self):
        x_index = 1
        y_index = 2
        position = self._pointer.get_position()
        return (position[x_index], position[y_index])

    def set_position(self, point):
        self._pointer.warp(self._screen, point[0], point[1])
