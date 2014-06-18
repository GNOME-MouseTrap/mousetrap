'''
Where it all begins.
'''

# NOTE: import this first to set up logging properly.
import mousetrap.initialize_logging

import logging
from gi.repository import GObject, Gdk, Gtk
from mousetrap.vision import Camera
from mousetrap.gui import ScreenPointer, Gui
from mousetrap.pointers.nose_joystick import Pointer
from mousetrap.pointers.eyes import Pointer as Eyes


LOGGER = logging.getLogger('mousetrap.main')


class Main(object):

    FPS = 10
    INTERVAL = int(round(1000.0 / FPS))

    def __init__(self):
        self.timeout_id = None
        self.camera = Camera()
        self.camera.set_dimensions(320, 240)
        self.gui = Gui()
        self.pointer = ScreenPointer()
        self.nose = Pointer()
        self.eyes = Eyes()

    def run(self):
        self.timeout_id = GObject.timeout_add(self.INTERVAL, self.on_timeout, None)
        self.gui.start()

    def on_timeout(self, user_data):

        image = self.camera.read_image()
        self.gui.show_image('Raw', image)
        self.nose.update_image(image)
        for event in self.nose.get_pointer_events():
            self.pointer.trigger_event(event)

        if self.pointer.is_moving():
            return True

        self.eyes.update_image(image)
        events = self.eyes.get_pointer_events()
        for event in events:
            self.pointer.trigger_event(event)

        return True


if __name__ == '__main__':
    Main().run()
