from yaml import safe_load
from os.path import dirname
from copy import deepcopy


class Config(dict):
    DEFAULT_CONFIG_PATH = dirname(__file__) + '/' + 'config_default.yaml'

    def __init__(self):
        with open(self.DEFAULT_CONFIG_PATH) as config_file:
            defaults = safe_load(config_file)
            _rmerge(self, defaults)

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
