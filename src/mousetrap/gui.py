'''
All things GUI.
'''


import logging
LOGGER = logging.getLogger(__name__)


from gi.repository import Gtk
from gi.repository import Gdk


from Xlib.display import Display as XlibDisplay
from Xlib.ext import xtest
from Xlib import X


from mousetrap.i18n import _


class ImageWindow(object):
    def __init__(self, config, message):
        self._config = config
        self._window = Gtk.Window(title=message)
        self._canvas = Gtk.Image()
        self._window.add(self._canvas)
        self._window.connect("delete-event", Gtk.main_quit)
        self._window.show_all()

    def draw(self, image):
        '''Draw image to this window.
        '''
        image = image.to_pixbuf()
        self._canvas.set_from_pixbuf(image)
        self._canvas.queue_draw()


class Gui(object):
    def __init__(self, config):
        self._config = config
        self._windows = {}

    def show_image(self, window_name, image):
        '''Displays image in window named by window_name.
           May reuse named windows.
           '''
        if window_name not in self._windows:
            self._windows[window_name] = ImageWindow(self._config, window_name)
        self._windows[window_name].draw(image)

    def start(self):
        '''Start handling events.'''
        Gtk.main()

    def get_screen_width(self):
        return Gtk.Window().get_screen().get_width()

    def get_screen_height(self):
        return Gtk.Window().get_screen().get_height()


class Pointer(object):
    BUTTON_LEFT = X.Button1

    def __init__(self, config):
        self._config = config
        gdk_display = Gdk.Display.get_default()
        device_manager = gdk_display.get_device_manager()
        self._pointer = device_manager.get_client_pointer()
        self._screen = gdk_display.get_default_screen()
        self._moved = False

    def set_position(self, position=None):
        '''Move pointer to position (x, y). If position is None,
        no change is made.'''
        self._moved = False
        if position is not None:
            LOGGER.debug(_('Moving pointer to %s'), position)

            self._pointer.warp(self._screen, position[0], position[1])
            self._moved = True
        else:
            LOGGER.debug(_('Not moving the pointer'))

    def is_moving(self):
        '''Returns True if last call to set_position passed a non-None value
        for position.'''
        return self._moved

    def get_position(self):
        X_INDEX = 1
        Y_INDEX = 2
        position = self._pointer.get_position()
        return (position[X_INDEX], position[Y_INDEX])

    def click(self, button=BUTTON_LEFT):
        display = XlibDisplay()
        for event, button in [(X.ButtonPress, button), (X.ButtonRelease, button)]:
            LOGGER.debug('%s %s', event, button)
            xtest.fake_input(display, event, button)
            display.sync()
