class Scene:
    """A collection of data about a renderable scene."""

    def __init__(self):
        self.lights = []
        self.primitives = []
        self.camera = None
