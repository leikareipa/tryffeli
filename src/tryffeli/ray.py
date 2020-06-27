class Ray:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

class RayIntersectionInfo:
    """Metadata about an intersection between a ray and a primitive."""

    def __init__(self, ray, primitive):
        self.ray = ray
        self.primitive = primitive
        
        # Distance from the ray's origin to the intersection point on the primitive.
        self.distance = None

        # Location in world XYZ coordinates of where this intersection occurs.
        self.position = None

        # The primitive's normal at the interscection point.
        self.normal = None

        # Texture UV coordinates of the primitive on the intersection point.
        self.u = None
        self.v = None
