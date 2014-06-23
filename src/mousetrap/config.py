class Config(dict):
    def __init__(self):
        self['loops_per_second'] = 10

        # The plugins to load in the order they will load and run.
        self['assembly'] =  [
            'mousetrap.plugins.camera.CameraPlugin',
            'mousetrap.plugins.display.DisplayPlugin',
            'mousetrap.plugins.nose_joystick.NoseJoystickPlugin',
            'mousetrap.plugins.eyes.EyesPlugin',
            ]

        self['haar_files'] = {
            "face": "haars/haarcascade_frontalface_default.xml",
            "nose": "haars/haarcascade_mcs_nose.xml",
            "left_eye": "haars/haarcascade_mcs_lefteye.xml",
            "open_eye": "haars/haarcascade_eye.xml",
            }

        # See `logging` and `logging.config`
        self['logging'] = {
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
            }

        self['plugins'] = {
            }


    def for_plugin(self, plugin_object):
        class_ = plugin_object.__class__
        return self[class_.__module__ + '.' + class_.__name__]
