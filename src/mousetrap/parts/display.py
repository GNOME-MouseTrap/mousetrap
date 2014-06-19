import mousetrap.parts.interface as interface
import logging


class Part(interface.Part):
    def run(self, app):
        app.gui.show_image('MouseTrap', app.image)
