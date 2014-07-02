from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from yaml import safe_load
from os.path import dirname, expanduser, isfile
from os import getcwd
from shutil import copy
from copy import deepcopy
from io import open


class Config(dict):

    def load(self, paths):
        for path in paths:
            self.load_path(path)
        return self

    def load_default(self):
        return self.load_path(dirname(__file__) + '/mousetrap.yaml')

    def load_path(self, path):
        print("# Loading %s" % (path))
        with open(path) as config_file:
            config = safe_load(config_file)
            _rmerge(self, config)
        return self

    def load_dict(self, dictionary):
        _rmerge(self, dictionary)

    def __getitem__(self, key):
        '''
        Allow access to class configuration by passing instance of class as
        the key. For example,

            x = config[self]['x']

        is equivelant to

            x = config['classes'][self.__class__.__module__+'.'+self.__class__.__name__]['x']
        '''
        if isinstance(key, basestring):
            return super(Config, self).__getitem__(key)
        class_ = key.__class__
        return self['classes'][class_.__module__ + '.' + class_.__name__]


def _rmerge(target, source):
    '''
    Recursively update values in target from source.
    Only dicts are updated, all other values are deepcopied.
    '''
    if source is None:
        return
    for key, value in source.items():
        if isinstance(value, dict):
            if key not in target:
                target[key] = {}
            _rmerge(target[key], value)
        else:
            target[key] = deepcopy(value)
