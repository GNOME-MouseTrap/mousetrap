class Config(dict):
    defaults = {
        'loops_per_second': 10,

        'camera': {
            'device_index': -1,     # -1 to search for device
            'width': 400,
            'height': 300,
            },

        # The plugins to load in the order they will load and run.
        'assembly':  [
            'mousetrap.plugins.camera.CameraPlugin',
            'mousetrap.plugins.display.DisplayPlugin',
            'mousetrap.plugins.nose_joystick.NoseJoystickPlugin',
            'mousetrap.plugins.eyes.EyesPlugin',
            ],

        'haar_files': {
            "face": "haars/haarcascade_frontalface_default.xml",
            "nose": "haars/haarcascade_mcs_nose.xml",
            "left_eye": "haars/haarcascade_mcs_lefteye.xml",
            "open_eye": "haars/haarcascade_eye.xml",
            },

        # See `logging` and `logging.config`
        'logging': {
            'version': 1,
            'root': {
                'level': 'DEBUG',
                'formatters': ['default'],
                'handlers': ['console']
                },
            'formatters': {
                'default': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    }
                },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter' : 'default',
                    'stream' : 'ext://sys.stdout'
                    }
                }
            },

        'classes': {
            'mousetrap.plugins.display.DisplayPlugin': {
                'window_title': 'MouseTrap',
                },

            'mousetrap.plugins.eyes.MotionDetector': {
                'max_samples': 5,
                },

            'mousetrap.plugins.eyes.ClosedDetector': {
                'max_samples': 15,
                'min_fraction_to_be_closed': 0.8,
                },

            'mousetrap.plugins.eyes.LeftEyeLocator': {
                'face_detector': {
                    'scale_factor': 1.5,
                    'min_neighbors': 5,
                    },

                'open_eye_detector': {
                    'scale_factor': 1.1,
                    'min_neighbors': 3,
                    },

                'left_eye_detector': {
                    'scale_factor': 1.5,
                    'min_neighbors': 10,
                    },
                },

            'mousetrap.plugins.nose_joystick.NoseJoystickPlugin': {
                'threshold': 5,
                },

            'mousetrap.plugins.nose.NoseLocator': {
                'face_detector': {
                    'scale_factor': 1.5,
                    'min_neighbors': 5
                    },

                'nose_detector': {
                    'scale_factor': 1.1,
                    'min_neighbors': 5
                    },
                },
            },
        }

    def __init__(self):
        _rmerge(self, self.defaults)

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
    import copy
    for key, value in source.items():
        if isinstance(value, dict):
            if key not in target:
                target[key] = {}
            _rmerge(target[key], value)
        else:
            target[key] = copy.deepcopy(value)
