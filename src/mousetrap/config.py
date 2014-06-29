from yaml import safe_load
from os.path import dirname, expanduser, isfile
from os import getcwd
from shutil import copy
from copy import deepcopy
from collections import OrderedDict


class Config(dict):
    SEARCH_PATH = OrderedDict([
        ('default', dirname(__file__) + '/mousetrap.yaml'),
        ('user', expanduser('~/.mousetrap.yaml')),
        ('user_specified_file', None),
        ])

    @classmethod
    def get_config_path(cls, key):
        return cls.SEARCH_PATH[key]

    def __init__(self, user_specified_file=None):
        self.SEARCH_PATH['user_specified_file']=user_specified_file
        self._load()

    def _load(self):
        for name, path in self.SEARCH_PATH.items():
            if path is not None and isfile(path):
                print "# Loading %s" % (path)
                with open(path) as config_file:
                    config = safe_load(config_file)
                    if config is not None:
                        _rmerge(self, config)
                    else:
                        print "# Warning: config is empty."

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
    for key, value in source.items():
        if isinstance(value, dict):
            if key not in target:
                target[key] = {}
            _rmerge(target[key], value)
        else:
            target[key] = deepcopy(value)
