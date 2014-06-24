'''
Where it all begins.
'''


from mousetrap.config import Config
CONFIG = Config()


import logging
import logging.config
logging.config.dictConfig(CONFIG['logging'])
LOGGER = logging.getLogger('mousetrap.main')
import yaml
LOGGER.debug(yaml.dump(dict(CONFIG), default_flow_style=False))


from gi.repository import GObject, Gdk, Gtk
from mousetrap.gui import Gui, Pointer
from mousetrap.vision import Camera


class App(object):
    def __init__(self, config):
        self.config = config
        self.image = None
        self.loop = Loop(config, self)
        self.gui = Gui(config)
        self.camera = Camera(config)
        self.pointer = Pointer(config)
        self.plugins = []
        self._assemble_plugins()

    def _assemble_plugins(self):
        self._load_plugins()
        self._register_plugins_with_loop()

    def _load_plugins(self):
        for class_ in self.config['assembly']:
            self.plugins.append(self._load_plugin(class_))

    def _load_plugin(self, class_):
        try:
            LOGGER.debug('loading %s', class_)
            class_path = class_.split('.')
            module = __import__('.'.join(class_path[:-1]), {}, {}, class_path[-1])
            return getattr(module, class_path[-1])(self.config)
        except ImportError as error:
            LOGGER.error(
                '''Could not import plugin `%s`. Check the config file and
                PYTHONPATH to ensure that Python can find the plugin.'''
                )
            raise

    def _register_plugins_with_loop(self):
        for plugin in self.plugins:
            self.loop.subscribe(plugin)

    def run(self, app=None):
        self.loop.start()
        self.gui.start()


class Observable(object):
    def __init__(self, config):
        self._config = config
        self.__observers = []
        self.__arguments = {}

    def subscribe(self, observer):
        self.__observers.append(observer)

    def _add_argument(self, key, value):
        self.__arguments[key] = value

    def _fire(self, callback_name):
        for observer in self.__observers:
            callback = getattr(observer, callback_name)
            callback(**self.__arguments)


class Loop(Observable):
    MILLISECONDS_PER_SECOND = 1000.0
    CALLBACK_RUN = 'run'

    def __init__(self, config, app):
        super(Loop, self).__init__(config)
        self._set_loops_per_second(app.config['loops_per_second'])
        self._timeout_id = None
        self._add_argument('app', app)

    def _set_loops_per_second(self, loops_per_second):
        self._loops_per_second = loops_per_second
        self._interval = int(round(
            self.MILLISECONDS_PER_SECOND / self._loops_per_second))

    def start(self):
        self.timeout_id = GObject.timeout_add(self._interval, self._run)

    def _run(self):
        CONTINUE = True
        PAUSE = False
        self._fire(self.CALLBACK_RUN)
        return CONTINUE


if __name__ == '__main__':
    App(CONFIG).run()
