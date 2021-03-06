import abc
import random
import math
from .vector import Vector
from .color import Color
from .ray import Ray

random.seed(1)

class Camera(metaclass=abc.ABCMeta):
    """Base camera class."""

    def __init__(self, position, direction, film):
        self.position = position
        self.direction = direction
        self.film = film
        self.antialiasing = False
        self.fov = 15

    @abc.abstractmethod
    def ray_for_pixel(self, x, y):
        """Creates and returns a ray shot from the camera's position toward a
        direction corresponding to the film's XY pixel coordinates."""
        pass

    def shoot(self, scene):
        """Exposes the camera's film to the scene. In other words, renders the
        scene from the camera's point of view."""

        for y in range(0, self.film.height):

            for x in range(0, self.film.width):

                ray = self.ray_for_pixel(x, y)
                intersections = ray.shoot(scene)

                if intersections:

                    intersections.sort(key = lambda intersection: intersection.distance)
                    nearest = intersections[0]

                    totalIncidentLight = 0

                    for light in scene.lights:
                        if not light.can_see(nearest):
                            continue

                        lightDirection = (light.position - nearest.point).normalized()
                        lightDistance = nearest.point.distance_to(light.position)

                        shade = max(0, min(1, nearest.normal.dot(lightDirection)))
                        falloff = max(0, min(1, (1 - (lightDistance / 400))))
                        incidentLight = (light.intensity * shade * falloff)

                        totalIncidentLight = max(0, min(1, (totalIncidentLight + incidentLight)))

                    self.film.put_pixel(x, y, Color(totalIncidentLight, totalIncidentLight, totalIncidentLight))

            if ((y % 10) == 0):
                print("Exposing film: %d%%" % (y / self.film.height * 100), end = "\r")

        # Clear the previous line in the terminal.
        print("%s", (" " * 50), end = "\r")

class AntialiasingCamera(Camera):
    """A camera that renders an antialiased image."""

    def __init__(self, position, direction, film):
        super().__init__(position, direction, film)

    def ray_for_pixel(self, x, y):
        aspectRatio = (self.film.width / self.film.height)

        # Aim the ray toward the given pixel, and perturb its direction slightly
        # to create an antialiasing effect. This algo was adapted from one posted
        # by friedlinguini on the now-deceased ompf.org form.
        r1 = random.random()
        r2 = random.random()
        rad = (0.49 * math.sqrt(-math.log(1 - r1)))
        angle = (2 * math.pi * r2)
        rayDirection = Vector(((2 * ((x + 0.5 + rad * math.cos(angle)) / self.film.width) - 1) * math.tan(self.fov * math.pi / 180) * aspectRatio),
                              (1 - 2 * ((y + 0.5 + rad * math.sin(angle)) / self.film.height)) * math.tan(self.fov * math.pi / 180),
                              1)

        rayDirection.normalize()

        ### TODO: Transform the ray direction by the camera's viewing direction. 

        return Ray(position = self.position, direction = rayDirection)

class SimpleCamera(Camera):
    """A basic camera."""

    def __init__(self, position, direction, film):
        super().__init__(position, direction, film)

    def ray_for_pixel(self, x, y):
        aspectRatio = (self.film.width / self.film.height)

        # Aim the ray toward the given pixel.
        a = math.tan(self.fov * math.pi / 180)
        rayDirection = Vector(((2 * ((x + 0.5) / self.film.width) - 1) * a * aspectRatio),
                               ((1 - (2 * ((y + 0.5) / self.film.height))) * a),
                               1)

        rayDirection.normalize()

        ### TODO: Transform the ray direction by the camera's viewing direction.

        return Ray(position = self.position, direction = rayDirection)
