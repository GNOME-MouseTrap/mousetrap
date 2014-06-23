import mousetrap.plugins.interface as interface
import logging


class DisplayPlugin(interface.Plugin):
    def __init__(self, config):
        self._config = config
        self._window_title = config.for_plugin(self)['window_title']

    def run(self, app):
        app.gui.show_image(self._window_title, app.image)
