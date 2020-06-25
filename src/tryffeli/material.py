class Material:
    """The material properties of a primitive."""

    class Type:
        """Material type enum."""
        emissive   = 1
        lambertian = 2
        reflective = 3

    def __init__(self, type = Type.lambertian):
        self.type = type
