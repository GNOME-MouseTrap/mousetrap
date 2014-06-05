import unittest
import mousetrap.vision as vision

# OpenCV will automatically search for a working camera device if we use the
# index -1.
DEVICE_INDEX = -1
IMAGE_MAX_WIDTH = 400
IMAGE_MAX_HEIGHT = 300

class test_camera(unittest.TestCase):

    def setUp(self):
        self.camera = vision.Camera(DEVICE_INDEX,
                IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT)

    def test_get_image_imageReturned(self):
        image = self.camera.read_image()
        self.assertTrue(
            image is not None,
            msg="Error: Image not captured"
        )


if __name__ == '__main__':
    unittest.main()
