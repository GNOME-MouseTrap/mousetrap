from gi.repository import GObject

import mousetrap.vision as vision
import mousetrap.gui as gui


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

    def run(self):
        self.timeout_id = GObject.timeout_add(INTERVAL, self.on_timeout, None)
        gui.start()

    def on_timeout(self, user_data):
        self.image = self.camera.read_image()
        try:
            location = self.locator.locate(self.image)
            print location
        except Exception as exception:
            print exception.args
        gui.show_image('diff', self.image)
        return True


if __name__ == '__main__':
    Main().run()
