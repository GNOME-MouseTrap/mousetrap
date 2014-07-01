import unittest
from mousetrap.config import _rmerge, Config


class test__rmerge(unittest.TestCase):

    def setUp(self):
        self.a = {
            'red': 1,
            'white': ['washington', [2, 3], {'lincoln': 4}],
            'blue': {
                'alpha': 5,
                'list': [6, 7],
                'dict': {
                    'charlie' : 8}}}

        self.b = {
            'new': 9,
            'white': ['replacement'],
            'blue': {
                'new': 10,
                'dict': {
                    'charlie': 11,
                    'new': 12,
                    'newdict': {
                        'some':'dict'}}}}
        self.ab = {
            'new': 9,
            'red': 1,
            'white': ['replacement'],
            'blue': {
                'new': 10,
                'alpha': 5,
                'list': [6, 7],
                'dict': {
                    'charlie' : 11,
                    'new': 12,
                    'newdict': {
                        'some':'dict'}}}}

    def test__rmerge(self):
        _rmerge(self.a, self.b)
        self.assertEqual(self.ab, self.a)

    def test__rmerge_None(self):
        from copy import deepcopy
        original = deepcopy(self.a)
        _rmerge(self.a, None)
        self.assertEqual(original, self.a)


class test_Config(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.files = Files()

    def tearDown(self):
        self.files.delete()

    def test_load_default(self):
        self.config.load_default()
        self.assertIsInstance(self.config['assembly'], list)

    def test_load(self):
        self.files.write('f1',\
"""
x: 1
y: 2
""")
        self.files.write('f2',\
"""
x: 3
z: 4
""")
        self.config.load([self.files.path('f1'), self.files.path('f2')])
        self.assertEquals({'x': 3, 'y': 2, 'z': 4}, self.config)

    def test_classes_config(self):
        self.config.load_dict({
            'classes': {
                self.__class__.__module__ + '.' + self.__class__.__name__: {
                    'x': 4}}})
        self.assertEquals(4, self.config[self]['x'])


class Files(object):
    def __init__(self, directory=None):
        if directory is None:
            directory = __file__ + '.data'
        from os.path import exists
        from os import mkdir
        if not exists(directory):
            mkdir(directory)
        self.directory = directory

    def write(self, file_name, data):
        with open(self.path(file_name), 'w') as data_file:
            data_file.write(data)

    def read(self, file_name, data):
        with open(self.path(file_name), 'r') as data_file:
            return data_file.read()

    def path(self, file_name):
        return self.directory + '/' + file_name

    def delete(self):
        from shutil import rmtree
        rmtree(self.directory)
