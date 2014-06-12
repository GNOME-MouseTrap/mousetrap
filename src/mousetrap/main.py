'''
Where it all begins.
'''

from datetime import datetime
from gi.repository import GObject
from mousetrap.vision import Camera
from mousetrap.gui import MousePointer, Gui
from mousetrap.pointers.nose import Pointer


FPS = 10
INTERVAL = int(round(1000.0 / FPS))


class Main(object):
    def __init__(self):
        self.timeout_id = None
        self.camera = Camera()
        self.camera.set_dimensions(300, 200)
        self.gui = Gui()
        self.pointer = MousePointer()
        self.nose = Pointer()

    def run(self):
        self.timeout_id = GObject.timeout_add(INTERVAL, self.on_timeout, None)
        self.gui.start()

    def on_timeout(self, user_data):
        image = self.camera.read_image()
        self.gui.show_image('Raw', image)
        self.nose.update_image(image)
        position = self.nose.get_new_position()
        self.pointer.set_position(position)
        if position is None:
            print str(datetime.now()) + ': No change.'
        return True


if __name__ == '__main__':
    Main().run()
