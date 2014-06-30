import unittest
from mousetrap.vision import Camera
from mousetrap.main import Config


class test_camera(unittest.TestCase):

    def setUp(self):
        self.camera = Camera(Config().load_default())

    def test_get_image_imageReturned(self):
        image = self.camera.read_image()
        self.assertTrue(
            image is not None,
            msg="Error: Image not captured"
        )


if __name__ == '__main__':
    unittest.main()
