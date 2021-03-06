class Color:
    """A 3-component (RGB) color. Values are expected in the range [0,1]."""
    
    def __init__(self, red = 1, green = 0, blue = 1):
        self.red = red
        self.green = green
        self.blue = blue

    def __iadd__(self, other):
        self.red += other.red
        self.green += other.green
        self.blue += other.blue

        return self

    def __add__(self, other):
        self += other
