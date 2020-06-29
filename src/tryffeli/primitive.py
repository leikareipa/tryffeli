import math
import abc
from .ray import RayIntersectionInfo
from .vector import Vector

class GeometricPrimitive(metaclass=abc.ABCMeta):
    """A geometric primitive (e.g. triangle or sphere) capable of being rendered."""
    
    @abc.abstractmethod
    def intersection_with(self, ray):
        """Ray-primitive intersection.
        
        Returns either None if the ray misses this primitive, or a RayIntersectionInfo
        instance if the ray intersects this primitive.
        
        The 'distance' property of the RayIntersectionInfo instance will be positive
        if the ray hits the primitive's front face and negative if the back face.
        """
        
        pass

class Sphere(GeometricPrimitive):
    def __init__(self, position, radius, material):
        self.radius = radius
        self.position = position
        self.material = material

    def intersection_with(self, ray):
        """Ray-sphere intersection.

        A positive value means the ray hit the sphere from outside of the sphere;
        a negative value that the ray hit the sphere from inside the sphere.
        
        Adapted with superficial changes from an implementation by Jacco Bikker
        (https://web.archive.org/web/20080509075746/http://www.devmaster.net/articles/raytracing_series/part2.php).
        """

        intersection = RayIntersectionInfo(ray, self)

        v = (ray.position - self.position)
        b = -v.dot(ray.direction)
        det = ((b * b) - v.dot(v) + (self.radius ** 2))

        if det <= 0:
            return None
        else:
            det = math.sqrt(det)
            i1 = (b - det)
            i2 = (b + det)

            if i2 > 0:
                if i1 < 0:
                    intersection.distance = -i2
                else:
                    intersection.distance = i1

                intersection.point = (ray.position + (ray.direction * intersection.distance))
                intersection.normal = (intersection.point - self.position).normalized()
            else:
                return None

        return intersection
