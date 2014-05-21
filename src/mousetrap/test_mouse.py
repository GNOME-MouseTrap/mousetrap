# pylint: skip-file

import unittest
from mousetrap.mouse import Mouse


class test_mouse(unittest.TestCase):

    def setUp(self):
        self.mouse = Mouse()

    def test_get_position(self):
        # pylint: disable=unused-variable
        x, y = self.mouse.get_position()
        try:
            x += 1
            y += 1
        except TypeError:
            self.assertTrue(False, msg='x or y is not a number')

    def test_set_position(self):
        self.mouse.set_position((3, 4))
        x, y = self.mouse.get_position()
        self.assertEquals(3, x)
        self.assertEquals(4, y)


if __name__ == '__main__':
    unittest.main()
