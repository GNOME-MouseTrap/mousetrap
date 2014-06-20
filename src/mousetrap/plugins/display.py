import mousetrap.plugins.interface as interface
import logging


class DisplayPlugin(interface.Plugin):
    def run(self, app):
        app.gui.show_image('MouseTrap', app.image)
