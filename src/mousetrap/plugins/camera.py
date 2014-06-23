import mousetrap.plugins.interface as interface


class CameraPlugin(interface.Plugin):
    def __init__(self, config):
        self._config = config

    def run(self, app):
        app.image = app.camera.read_image()
