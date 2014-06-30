import unittest
from mousetrap.config import _rmerge


class test__rmerge(unittest.TestCase):

    def setUp(self):
        self.a = {
            'red': 1,
            'white': ['washington', [2, 3], {'lincoln': 4}],
            'blue': {'alpha': 5, 'list': [6, 7], 'dict': {'charlie' : 8}},
            }

        self.b = {
            'new': 9,
            'white': ['replacement'],
            'blue': {'new': 10, 'dict': {'charlie': 11, 'new': 12, 'newdict': {'some':'dict'}}},
            }
        self.ab = {
            'new': 9,
            'red': 1,
            'white': ['replacement'],
            'blue': {'new': 10, 'alpha': 5, 'list': [6, 7], 'dict': {'charlie' : 11, 'new': 12, 'newdict': {'some':'dict'}}},
            }

    def test__rmerge(self):
        _rmerge(self.a, self.b)
        self.assertEqual(self.ab, self.a)
