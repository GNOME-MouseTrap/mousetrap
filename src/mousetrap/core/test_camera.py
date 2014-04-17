__author__ = 'foss2serve'

import unittest
import camera


class test_camera(unittest.TestCase):

    def test_get_image_correctInput(self):

        #Setup
        cam = camera.Camera()

        #Capture Image
        img = cam.get_image()

        self.assertTrue(
            img is not None,
            msg="Error: Image not captured"
        )

    def test_start_camera_correctInput(self):

        #Setup
        cam = camera.Camera()

        self.assertTrue(
            cam.capture.isOpened(),
            msg="Error: Camera feed not initialized"
        )

if __name__ == '__main__':
    unittest.main()