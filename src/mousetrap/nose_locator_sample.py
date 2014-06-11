from mousetrap.vision import Camera, ImageConverter, NoseLocator


class NoseLocatorSample(object):
    def __init__(self):
        self._camera = None
        self._nose_locator = NoseLocator()
        self._initialize_camera()

    def _initialize_camera(self):
        search_for_device = -1
        self._camera = Camera(
                device_index=search_for_device,
                width=400, height=300)

    def run(self):
        image = self._read_grayscale_image()
        nose = self._nose_locator.locate(image)
        print nose

    def _read_grayscale_image(self):
        image = self._camera.read_image()
        return ImageConverter.rgb_to_grayscale(image)


if __name__ == '__main__':
    NoseLocatorSample().run()
