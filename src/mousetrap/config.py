from yaml import safe_load
from os.path import dirname, expanduser, isfile
from os import getcwd
from shutil import copy
from copy import deepcopy


class Config(dict):
    SEARCH_PATH = {
        'default': dirname(__file__) + '/mousetrap.yaml',
        'user': expanduser('~/.mousetrap.yaml'),
        'local_hidden': getcwd() + '/.mousetrap.yaml',
        'local': getcwd() + '/mousetrap.yaml',
    }

    def __init__(self):
        self._install()
        self._load()

    def _install(self):
        if not isfile(self.SEARCH_PATH['user']):
            print("Copying %s to %s" % (self.SEARCH_PATH['default'], self.SEARCH_PATH['user']))
            copy(self.SEARCH_PATH['default'], self.SEARCH_PATH['user'])

    def _load(self):
        for name, path in self.SEARCH_PATH.items():
            if isfile(path):
                print("loading %s" % (path))
                with open(path) as config_file:
                    config = safe_load(config_file)
                    _rmerge(self, config)

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
