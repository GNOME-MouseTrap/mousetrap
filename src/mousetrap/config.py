from yaml import safe_load
from os.path import dirname, expanduser, exists
from os import getcwd
from copy import deepcopy
from mousetrap.i18n import _


class Config(dict):
    SEARCH_PATH = [
        dirname(__file__) + '/' + 'mousetrap.yaml',
        expanduser('~') + '/.mousetrap.yaml',
        getcwd() + '/mousetrap.yaml',
    ]

    def __init__(self):
        for path in self.SEARCH_PATH:
            if exists(path):
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
