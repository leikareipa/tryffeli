#!/usr/bin/env python3

from PyQt5.QtGui import QImage, QColor

class Color:
    """RGB color. Values are expected in the range [0,1]."""
    
    def __init__(self, red = 0, green = 0, blue = 0):
        self.red = red
        self.green = green
        self.blue = blue

class Vector:
    """A 3-component (XYZ) vector."""

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        pass

    def dot(self, other):
        pass

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

    def __init__(self, materialType):
        self.type = materialType

class GeometricPrimitive:
    """A geometric primitive (e.g. triangle or sphere) capable of being rendered."""
    
    def __init__(self):
        self.material = Material(Material.Type.lambertian)
    
    def intersection_distance(self, ray):
        return 5

class Sphere(GeometricPrimitive):
    pass

print((Vector(1,2,3) / 4).y)
