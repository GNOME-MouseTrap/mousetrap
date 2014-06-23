import mousetrap.plugins.interface as interface
import logging


class DisplayPlugin(interface.Plugin):
    def __init__(self, config):
        self._config = config

    def run(self, app):
        app.gui.show_image('MouseTrap', app.image)
