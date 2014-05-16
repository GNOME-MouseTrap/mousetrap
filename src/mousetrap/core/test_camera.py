__author__ = 'foss2serve'

import unittest
from .camera import Camera, CameraError


class test_camera(unittest.TestCase):

    def setUp(self):
        self.camera = Camera()

    def test_get_image_withStart_imageReturned(self):
        self.camera.start_camera();
        image = self.camera.get_image()
        self.assertTrue(
            image is not None,
            msg="Error: Image not captured"
        )

    def test_get_image_withoutStart_expectError(self):
        with self.assertRaises(CameraError):
            self.camera.get_image()


if __name__ == '__main__':
    unittest.main()
