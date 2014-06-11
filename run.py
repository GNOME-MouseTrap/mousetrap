from mousetrap.vision import Camera, HaarLoader, ImageConverter


class NoseLocatorTest(object):
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


class NoseLocator(object):
    def __init__(self):
        self._face_detector = FeatureDetector(
                'face', scale_factor=1.5, min_neighbors=5)
        self._nose_detector = FeatureDetector(
                'nose', scale_factor=1.3, min_neighbors=5)

    def locate(self, image_grayscale):
        face = self._face_detector.detect(image_grayscale)
        nose = self._nose_detector.detect(face['image'])
        return {
                'x': face['x'] + nose['center']['x'],
                'y': face['y'] + nose['center']['y'],
                }

class FeatureDetector(object):
    def __init__(self, name, scale_factor=1.1, min_neighbors=3):
        '''
        name - name of feature to detect

        scale_factor - how much the image size is reduced at each image scale
                while searching. Default 1.1.

        min_neighbors - how many neighbors each candidate rectangle should have
                to retain it. Default 3.
        '''
        self._name = name
        self._single = None
        self._plural = None
        self._image_grayscale = None
        self._cascade = HaarLoader.from_name(name)
        self._scale_factor = scale_factor
        self._min_neighbors = min_neighbors

    def detect(self, image_grayscale):
        self._image_grayscale = image_grayscale
        self._detect_plural()
        self._exit_if_none_detected()
        self._unpack_first()
        self._extract_image()
        self._calculate_center()
        return self._single

    def _detect_plural(self):
        self._plural = self._cascade.detectMultiScale(
                self._image_grayscale, self._scale_factor, self._min_neighbors)

    def _exit_if_none_detected(self):
        if len(self._plural) == 0:
            raise Exception('No ' + self._name + 's detected.')

    def _unpack_first(self):
        self._single = dict(zip(['x', 'y', 'width', 'height'], self._plural[0]))

    def _calculate_center(self):
        self._single["center"] = {
                "x": (self._single["x"] + self._single["width"]) / 2,
                "y": (self._single["y"] + self._single["height"]) / 2,
                }

    def _extract_image(self):
        single = self._single
        from_y = single['y']
        to_y = single['y'] + single['height']
        from_x = single['x']
        to_x = single['x'] + single['width']
        single["image"] = self._image_grayscale[from_y:to_y, from_x:to_x]


NoseLocatorTest().run()
