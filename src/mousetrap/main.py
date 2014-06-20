'''
Where it all begins.
'''

import mousetrap.log as log
from gi.repository import GObject, Gdk, Gtk
from mousetrap.gui import Gui, Pointer
from mousetrap.vision import Camera


LOGGER = log.getLogger('mousetrap.main')


#TODO: Should be a configuration file.
DEFAULT_PARTS = [
        ('camera', 'mousetrap.parts.camera'),
        ('display', 'mousetrap.parts.display'),
        ('nose_joystick', 'mousetrap.parts.nose_joystick'),
        ('eye_click', 'mousetrap.parts.eyes'),
        ]
DEFAULT_LOOPS_PER_SECOND = 10


class Main(object):
    def __init__(self):
        self._app = App()

    def run(self):
        self._app.run()


class App(object):
    def __init__(self):
        self.image = None
        self.loop = Loop(self)
        self.gui = Gui()
        self.camera = Camera()
        self.pointer = Pointer()
        self.parts = []
        self._assemble_parts()

    def _assemble_parts(self):
        self._load_parts(DEFAULT_PARTS)
        self._register_parts_with_loop()

    def _load_parts(self, part_descriptors):
        for name, module in part_descriptors:
            self.parts.append(self._load_part(module))

    @staticmethod
    def _load_part(module):
        LOGGER.debug('loading %s', module)
        module = __import__(module, globals(), locals(), ['Part'])
        part = module.Part()
        return part

    def _register_parts_with_loop(self):
        for part in self.parts:
            self.loop.subscribe(part)

    def run(self, app=None):
        self.loop.start()
        self.gui.start()


class Observable(object):
    def __init__(self):
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

    def __init__(self, app):
        super(Loop, self).__init__()
        self.set_loops_per_second(DEFAULT_LOOPS_PER_SECOND)
        self._timeout_id = None
        self._add_argument('app', app)

    def set_loops_per_second(self, loops_per_second):
        self._loops_per_second = loops_per_second
        self._interval = int(round(
            self.MILLISECONDS_PER_SECOND / self._loops_per_second))

    def start(self):
        self.timeout_id = GObject.timeout_add(self._interval, self.run)

    def run(self):
        CONTINUE = True
        PAUSE = False
        self._fire(self.CALLBACK_RUN)
        return CONTINUE


if __name__ == '__main__':
    Main().run()
