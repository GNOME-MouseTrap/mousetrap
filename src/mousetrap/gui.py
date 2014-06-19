'''
All things GUI.
'''

from gi.repository import Gtk
from gi.repository import Gdk

from Xlib.display import Display as XlibDisplay
from Xlib.ext import xtest
from Xlib import X

import logging
LOGGER = logging.getLogger(__name__)

class ImageWindow(object):
    def __init__(self, message):
        self._window = Gtk.Window(title=message)
        self._canvas = Gtk.Image()
        self._window.add(self._canvas)

        # FIXME: Closing any window kills the application. Need a mechanism
        # that allows windows to be openned and closed, and only kill the
        # application when the last window is closed.
        self._window.connect("delete-event", Gtk.main_quit)

        self._window.show_all()

    def draw(self, image):
        '''Draw image to this window.
        '''
        image = image.to_pixbuf()
        self._canvas.set_from_pixbuf(image)
        self._canvas.queue_draw()


class Gui(object):
    def __init__(self):
        self._windows = {}

    def show_image(self, window_name, image):
        '''Displays image in window named by window_name.
           May reuse named windows.
           '''
        if window_name not in self._windows:
            self._windows[window_name] = ImageWindow(window_name)
        self._windows[window_name].draw(image)

    def start(self):
        '''Start handling events.'''
        Gtk.main()

    def get_screen_width(self):
        return Gtk.Window().get_screen().get_width()

    def get_screen_height(self):
        return Gtk.Window().get_screen().get_height()


class Pointer(object):
    EVENT_MOVE = 'move'
    EVENT_CLICK = 'click'
    EVENT_DOUBLE_CLICK = 'double click'
    EVENT_TRIPLE_CLICK = 'triple click'
    EVENT_PRESS = 'press'
    EVENT_RELEASE = 'release'

    BUTTON_LEFT = X.Button1
    BUTTON_RIGHT = X.Button3
    BUTTON_MIDDLE = X.Button2

    def __init__(self):
        gdk_display = Gdk.Display.get_default()
        device_manager = gdk_display.get_device_manager()
        self._pointer = device_manager.get_client_pointer()
        self._screen = gdk_display.get_default_screen()
        self._moved = False

    def set_position(self, position=None):
        '''Move pointer to position (x, y). If position is None,
        no change is made.'''
        LOGGER.debug('moving to %s', position)
        self._moved = False
        if position is not None:
            self._pointer.warp(self._screen, position[0], position[1])
            self._moved = True

    def is_moving(self):
        '''Returns True if last call to set_position passed a non-None value
        for position.'''
        return self._moved

    def get_position(self):
        x_index = 1
        y_index = 2
        position = self._pointer.get_position()
        return (position[x_index], position[y_index])

    def click(self, button=BUTTON_LEFT):
        display = XlibDisplay()
        for event, button in [(X.ButtonPress, button), (X.ButtonRelease, button)]:
            LOGGER.debug('%s %s', event, button)
            xtest.fake_input(display, event, button)
            display.sync()
