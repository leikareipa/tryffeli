import abc
from .ray import Ray

class Light(metaclass=abc.ABCMeta):
    def __init__(self, position, intensity, parentScene):
        self.position = position
        self.intensity = intensity
        self.parentScene = parentScene

    def can_see(self, intersection):
        """Returns True if this light can see the given intersection point (given
        as an IntersectionInfo object); False otherwise."""

        lightRay = Ray(position = self.position,
                       direction = (intersection.point - self.position).normalized())

        intersections = lightRay.shoot(self.parentScene)

        if not intersections:
            return False
        else:
            nearest = sorted(intersections, key = lambda intersection: intersection.distance)[0]
            return (nearest.primitive == intersection.primitive)

class PointLight(Light):
    def __init__(self, position, intensity, parentScene):
        super().__init__(position, intensity, parentScene)
