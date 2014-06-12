from mousetrap.vision import Camera
from mousetrap.pointers.nose import NoseLocator


class NoseLocatorSample(object):
    def __init__(self):
        self._camera = Camera()
        self._nose_locator = NoseLocator()

    def run(self):
        image = self._camera.read_image()
        nose = self._nose_locator.locate(image)
        print nose


if __name__ == '__main__':
    NoseLocatorSample().run()
