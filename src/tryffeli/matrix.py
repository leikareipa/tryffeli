import math

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
