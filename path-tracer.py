#!/usr/bin/env python3

import math

class Color:
    """A 3-component (RGB) color. Values are expected in the range [0,1]."""
    
    def __init__(self, red = 0, green = 0, blue = 0):
        self.red = red
        self.green = green
        self.blue = blue

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
