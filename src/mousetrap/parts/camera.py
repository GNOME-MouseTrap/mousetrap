import mousetrap.parts.interface as interface


class Part(interface.Part):
    def run(self, app):
        app.image = app.camera.read_image()
