#!/usr/bin/env python3

import abc
import math
import random
import os
from PyQt5.QtGui import QImage, QColor

random.seed(1)

class Matrix:
    """A 4-component (XYZW) matrix."""

    def __init__(self):
        self.data = []

    def __getitem__(self, idx):
        return self.data[idx]

    def __mul__(self, other):
        result = Matrix.identity()

        for i in range(0, 4):
            for j in range(0, 4):
                result.data[i + (j * 4)] = ((self.data[i + (0 * 4)] * other.data[0 + (j * 4)]) +
                                            (self.data[i + (1 * 4)] * other.data[1 + (j * 4)]) +
                                            (self.data[i + (2 * 4)] * other.data[2 + (j * 4)]) +
                                            (self.data[i + (3 * 4)] * other.data[3 + (j * 4)]))

        return result

    @staticmethod
    def identity():
        m = Matrix()

        m.data = [1, 0, 0, 0,
                  0, 1, 0, 0,
                  0, 0, 1, 0,
                  0, 0, 0, 1]

        return m

    @staticmethod
    def scaling(x = 0, y = 0, z = 0):
        m = Matrix()
        
        m.data = [x, 0, 0, 0,
                  0, y, 0, 0,
                  0, 0, z, 0,
                  0, 0, 0, 1]

        return m

    @staticmethod
    def translation(x = 0, y = 0, z = 0):
        m = Matrix()

        m.data = [1, 0, 0, 0,
                  0, 1, 0, 0,
                  0, 0, 1, 0,
                  x, y, z, 1]

        return m

    @staticmethod
    def rotation(x = 0, y = 0, z = 0):
        mx = Matrix()
        my = Matrix()
        mz = Matrix()

        mx.data = [1,           0,            0,            0,
                   0,           math.cos(x),  -math.sin(x), 0,
                   0,           math.sin(x),  math.cos(x),  0,
                   0,           0,            0,            1]

        my.data = [math.cos(y), 0,            -math.sin(y), 0,
                   0,           1,            0,            0,
                   math.sin(y), 0,            math.cos(y),  0,
                   0,           0,            0,            1]

        mz.data = [math.cos(z), -math.sin(z), 0,            0,
                   math.sin(z), math.cos(z),  0,            0,
                   0,           0,            1,            0,
                   0,           0,            0,            1]

        return ((my * mz) * mx)

    @staticmethod
    def perspective(fov = 0, aspectRatio = 0, zNear = 0, zFar = 0):
        fovHalf = math.tan(fov / 2)
        zRange = (zNear - zFar)

        m = Matrix()

        m.data = [(1 / (fovHalf * aspectRatio)), 0,             0,                             0,
                  0,                             (1 / fovHalf), 0,                             0,
                  0,                             0,             ((-zNear - zFar) / zRange),    1,
                  0,                             0,             (2 * zFar * (zNear / zRange)), 0]

        return m

    @staticmethod
    def screenspace(screenWidth = 0, screenHeight = 0):
        m = Matrix()

        m.data = [(screenWidth / 2),        0,                           0, 0,
                  0,                        -(screenHeight / 2),         0, 0,
                  0,                         0,                          1, 0,
                  ((screenWidth / 2) - 0.5), ((screenHeight / 2) - 0.5), 0, 1]

        return m

class Vector:
    """A 3-component (XYZ) vector."""

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x - other.x),
                          (self.y - other.y),
                          (self.z - other.z))
        else: # Assumed int or float.
            return Vector((self.x - other),
                          (self.y - other),
                          (self.z - other))

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x * other.x),
                          (self.y * other.y),
                          (self.z * other.z))
        else: # Assumed int or float.
            return Vector((self.x * other),
                          (self.y * other),
                          (self.z * other))

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x / other.x),
                          (self.y / other.y),
                          (self.z / other.z))
        else: # Assumed int or float.
            return Vector((self.x / other),
                          (self.y / other),
                          (self.z / other))

    def rotate(self, matrix):
        """Rotate this vector with the given 4-by-4 rotation matrix."""

        _x = ((matrix[0] * self.x) + (matrix[4] * self.y) + (matrix[ 8] * self.z));
        _y = ((matrix[1] * self.x) + (matrix[5] * self.y) + (matrix[ 9] * self.z));
        _z = ((matrix[2] * self.x) + (matrix[6] * self.y) + (matrix[10] * self.z));

        self.x = _x
        self.y = _y
        self.z = _z

    def normalize(self):
        sn = math.sqrt((self.x * self.x) +
                       (self.y * self.y) +
                       (self.z * self.z))

        if not sn: return

        self.x /= sn
        self.y /= sn
        self.z /= sn

    def dot(self, other):
        return ((self.x * other.x) +
                (self.y * other.y) +
                (self.z * other.z))

    def cross(self, other):
        return Vector(((self.y * other.z) - (self.z * other.y)),
                      ((self.z * other.x) - (self.x * other.z)),
                      ((self.x * other.y) - (self.y * other.x)))

class Ray:
    def __init__(self, position = Vector(), direction = Vector()):
        self.position = position
        self.direction = direction

class Material:
    """The material properties of a primitive."""

    class Type:
        """Material type enum."""
        emissive   = 1
        lambertian = 2
        reflective = 3

    def __init__(self, type = Type.lambertian):
        self.type = type

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
    def __init__(self, position = Vector(), radius = 1, material = Material()):
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

        v = (sphere.position - ray.position)
        b = -v.dot(ray.direction)
        det = ((b ** 2) - v.dot(v) + (sphere.radius ** 2))

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

class Color:
    """A 3-component (RGB) color. Values are expected in the range [0,1]."""
    
    def __init__(self, red = 1, green = 0, blue = 1):
        self.red = red
        self.green = green
        self.blue = blue

class RenderSurface:
    """A pixel buffer for rendering into."""

    def __init__(self, width = 640, height = 480, clearColor = Color()):
        self.width = width
        self.height = height
        self.pixels = ([clearColor] * width * height)

    def put_pixel(self, x = 0, y = 0, color = Color()):
        self.pixels[x + y * self.width] = color

    def pixel_at(self, x = 0, y = 0):
        return self.pixels[x + y * self.width]

    def as_qimage(self):
        """Returns the surface's pixels as a Qt QImage."""

        image = QImage(self.width, self.height, QImage.Format_RGB32)

        for y in range(0, self.height):
            for x in range(0, self.width):
                color = self.pixel_at(x, y)
                image.setPixelColor(x, y, QColor((color.red * 255),
                                                 (color.green * 255),
                                                 (color.blue * 255)))

        return image

class Camera(metaclass=abc.ABCMeta):
    """Base camera class."""

    def __init__(self, position = Vector(), direction = Vector(), film = RenderSurface()):
        self.position = position
        self.direction = direction
        self.film = film
        self.antialiasing = False
        self.fov = 20

    @abc.abstractmethod
    def ray_for_pixel(self, x, y):
        """Creates and returns a ray shot from the camera's position toward a
        direction corresponding to the film's XY pixel coordinates."""
        pass

class AntialiasingCamera(Camera):
    """A camera that renders an antialiased image."""

    def __init__(self, position = Vector(), direction = Vector(), film = RenderSurface()):
        super().__init__(position, direction, film)

    def ray_for_pixel(self, x, y):
        aspectRatio = (self.film.width / self.film.height);

        # Aim the ray toward the given pixel, and perturb its direction slightly
        # to create an antialiasing effect. This algo was adapted from one posted
        # by friedlinguini on the now-deceased ompf.org form.
        r1 = random.random()
        r2 = random.random()
        rad = (0.49 * math.sqrt(-math.log(1 - r1)))
        angle = (2 * math.pi * r2)
        rayDirection = Vector(((2 * ((x + 0.5 + rad * math.cos(angle)) / self.film.width) - 1) * math.tan(self.fov * math.pi / 180) * aspectRatio),
                               (1 - 2 * ((y + 0.5 + rad * math.sin(angle)) / self.film.height)) * math.tan(self.fov * math.pi / 180),
                               -1)

        rayDirection.normalize()
        return Ray(position = self.position, direction = rayDirection)

class SimpleCamera(Camera):
    """A basic camera."""

    def __init__(self, position = Vector(), direction = Vector(), film = RenderSurface()):
        super().__init__(position, direction, film)

    def ray_for_pixel(self, x, y):
        aspectRatio = (self.film.width / self.film.height);

        # Aim the ray toward the given pixel.
        a = math.tan(self.fov * math.pi / 180);
        rayDirection = Vector(((2 * ((x + 0.5) / self.film.width) - 1) * a * aspectRatio),
                                ((1 - (2 * ((y + 0.5) / self.film.height))) * a),
                                -1)

        rayDirection.normalize()
        return Ray(position = self.position, direction = rayDirection)




sphere = Sphere(radius = 50,
                position = Vector(0, 0, 200),
                material = Material(type = Material.Type.lambertian))

camera = SimpleCamera(position = Vector(0, 0, 0),
                      direction = Vector(0, 0, 1),
                      film = RenderSurface(640, 480, clearColor = Color(0, 0, 0)))

# Cast a ray into each pixel on the film.
for y in range(0, camera.film.height):
    for x in range(0, camera.film.width):
        ray = camera.ray_for_pixel(x, y)
        if sphere.intersection_distance(ray) != math.inf:
            camera.film.put_pixel(x, y, Color(1, 1, 1))

camera.film.as_qimage().save("test.png")
os.system("display test.png")
