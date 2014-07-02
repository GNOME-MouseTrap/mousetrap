from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import unittest
from mousetrap.gui import Pointer
from mousetrap.main import Config


class test_pointer(unittest.TestCase):

    def setUp(self):
        self.pointer = Pointer(Config().load_default())

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
