import math

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

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector((self.x + other.x),
                          (self.y + other.y),
                          (self.z + other.z))
        else: # Assumed int or float.
            return Vector((self.x + other),
                          (self.y + other),
                          (self.z + other))

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
