class Ray:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def shoot(self, scene):
        """Casts the ray into the given scene. Returns an unordered list of the
        ray-primitive intersections that occur."""

        # An IntersectionInfo object for each ray-primitive intersection that
        # occurs in the scene.
        intersections = []

        for primitive in scene.primitives:
            intersection = primitive.intersection_with(self)

            if intersection != None:
                intersections.append(intersection)

        return intersections

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
