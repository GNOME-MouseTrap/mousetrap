import mousetrap.plugins.interface as interface


class CameraPlugin(interface.Plugin):
    def run(self, app):
        app.image = app.camera.read_image()
