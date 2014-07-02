from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from mousetrap.i18n import _
import mousetrap.plugins.interface as interface


class CameraPlugin(interface.Plugin):
    def __init__(self, config):
        self._config = config

    def run(self, app):
        app.image = app.camera.read_image()
