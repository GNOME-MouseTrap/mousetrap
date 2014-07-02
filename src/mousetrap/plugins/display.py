from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mousetrap.i18n import _
import mousetrap.plugins.interface as interface
import logging


class DisplayPlugin(interface.Plugin):
    def __init__(self, config):
        self._config = config
        self._window_title = config[self]['window_title']

    def run(self, app):
        app.gui.show_image(self._window_title, app.image)
