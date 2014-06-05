import unittest
import mousetrap.pointer as pointer


class test_pointer(unittest.TestCase):

    def setUp(self):
        self.pointer = pointer.Pointer()

    def test_get_position(self):
        x, y = self.pointer.get_position()
        try:
            x += 1
            y += 1
        except TypeError:
            self.assertTrue(False, msg='x or y is not a number')

    def test_set_position(self):
        self.pointer.set_position((3, 4))
        x, y = self.pointer.get_position()
        self.assertEquals(3, x)
        self.assertEquals(4, y)


if __name__ == '__main__':
    unittest.main()
