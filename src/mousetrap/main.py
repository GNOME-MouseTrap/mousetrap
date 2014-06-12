from gi.repository import GObject
from gi.repository import Gtk

from mousetrap.vision import Camera, NoseLocator
from mousetrap.gui import Pointer, Gui


FPS = 5
INTERVAL = int(round(1000.0 / FPS))


class Main(object):
    def __init__(self):
        self.image = None
        self.timeout_id = None
        self.camera = Camera()
        self.camera.set_dimensions(300, 200)
        self.locator = NoseLocator()
        self.pointer = Pointer()
        self.screen = Gtk.Window().get_screen()
        self.gui = Gui()

    def run(self):
        self.timeout_id = GObject.timeout_add(INTERVAL, self.on_timeout, None)
        self.gui.start()

    def on_timeout(self, user_data):
        self.image = self.camera.read_image()
        try:
            location = self.locator.locate(self.image)
            print 'Nose location in image: ' + str(location)

            # Map coordinates from image to screen.
            image_width = self.image.get_width()
            image_height = self.image.get_height()
            x_percent = 1.0 * location['x'] / image_width
            y_percent = 1.0 * location['y'] / image_height
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
        self.gui.show_image('diff', self.image)
        return True


if __name__ == '__main__':
    Main().run()
