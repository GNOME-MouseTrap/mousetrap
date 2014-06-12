import unittest
from mousetrap.gui import ScreenPointer


class test_pointer(unittest.TestCase):

    def setUp(self):
        self.pointer = ScreenPointer()

    def test_get_position(self):
        pointer_x, pointer_y = self.pointer.get_position()
        try:
            pointer_x += 1
            pointer_y += 1
        except TypeError:
            self.assertTrue(False, msg='pointer_x or pointer_y is not a number')

    def test_set_position(self):
        self.pointer.set_position((3, 4))
        pointer_x, pointer_y = self.pointer.get_position()
        self.assertEquals(3, pointer_x)
        self.assertEquals(4, pointer_y)


if __name__ == '__main__':
    unittest.main()
