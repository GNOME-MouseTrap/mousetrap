from gi.repository import GObject
from gi.repository import Gtk

import mousetrap.vision as vision
import mousetrap.gui as gui
import mousetrap.pointer as pointer


SEARCH_FOR_CAMERA = -1
DEVICE_INDEX = SEARCH_FOR_CAMERA
IMAGE_MAX_WIDTH = 400
IMAGE_MAX_HEIGHT = 300
FPS = 5
INTERVAL = int(round(1000.0 / FPS))


class Main(object):
    def __init__(self):
        self.image = None
        self.timeout_id = None
        self.camera = vision.Camera(DEVICE_INDEX,
                IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT)
        self.locator = vision.NoseLocator()
        self.pointer = pointer.Pointer()
        self.screen = Gtk.Window().get_screen()

    def run(self):
        self.timeout_id = GObject.timeout_add(INTERVAL, self.on_timeout, None)
        gui.start()

    def on_timeout(self, user_data):
        self.image = self.camera.read_image()
        try:
            location = self.locator.locate(self.image)
            print 'Nose location in image: ' + str(location)

            # Map coordinates from image to screen.
            x_percent = 1.0 * location['x'] / IMAGE_MAX_WIDTH
            y_percent = 1.0 * location['y'] / IMAGE_MAX_HEIGHT
            screen = Gtk.Window().get_screen()
            x_screen = x_percent * screen.get_width()
            y_screen = y_percent * screen.get_width()
            half_width = screen.get_width() / 2
            x_screen = (-1 * (x_screen - half_width)) + half_width
            print 'Pointer location in screen:' + \
                str({'x':x_screen, 'y':y_screen})

            # move the pointer
            self.pointer.set_position((x_screen, y_screen))
        except Exception as exception:
            print exception.args[0]
        gui.show_image('diff', self.image)
        return True


if __name__ == '__main__':
    Main().run()
