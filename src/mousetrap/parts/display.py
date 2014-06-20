import mousetrap.parts.interface as interface
import logging


class DisplayPart(interface.Part):
    def run(self, app):
        app.gui.show_image('MouseTrap', app.image)
