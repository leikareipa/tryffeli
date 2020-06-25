import math
import abc

class GeometricPrimitive(metaclass=abc.ABCMeta):
    """A geometric primitive (e.g. triangle or sphere) capable of being rendered."""
    
    @abc.abstractmethod
    def intersection_distance(self, ray):
        """Ray-primitive intersection.
        
        Returns math.inf if the ray misses this primitive; a positive value if the
        ray hits the primitive's front face; and a negative value if the ray hits
        the primitive's back face. The value's magnitude gives the distance from
        the ray's origin to the intersection point along the ray's direction.
        """
        
        pass

class Sphere(GeometricPrimitive):
    def __init__(self, position, radius, material):
        self.radius = radius
        self.position = position
        self.material = material

    def intersection_distance(self, ray):
        """Ray-sphere intersection.

        A positive value means the ray hit the sphere from outside of the sphere;
        a negative value that the ray hit the sphere from inside the sphere.
        
        Adapted with superficial changes from an implementation by Jacco Bikker
        (https://web.archive.org/web/20080509075746/http://www.devmaster.net/articles/raytracing_series/part2.php).
        """

        v = (self.position - ray.position)
        b = -v.dot(ray.direction)
        det = ((b ** 2) - v.dot(v) + (self.radius ** 2))

        if det > 0:
            i1 = 0
            i2 = 0

            det = math.sqrt(det)
            i1 = (b - det)
            i2 = (b + det)

            if i2 > 0:
                if i1 < 0:
                    return -i2
                else:
                    return i1

        return math.inf
