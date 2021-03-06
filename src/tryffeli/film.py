from PyQt5.QtGui import QImage, QColor
from .color import Color

class RenderSurface:
    """A pixel buffer for rendering into."""

    def __init__(self, width, height, backgroundColor):
        self.width = width
        self.height = height
        self.pixels = [Color(backgroundColor.red,
                             backgroundColor.green,
                             backgroundColor.blue) for x in range(width * height)]

    def put_pixel(self, x, y, color):
        self.pixels[x + y * self.width] += color

    def pixel_at(self, x, y):
        return self.pixels[x + y * self.width]

    def as_qimage(self):
        """Returns the surface's pixels as a Qt QImage."""

        image = QImage(self.width, self.height, QImage.Format_RGB32)

        for y in range(0, self.height):
            for x in range(0, self.width):
                color = self.pixel_at(x, y)
                image.setPixelColor(x, y, QColor(max(0, min(255, (color.red   * 255))),
                                                 max(0, min(255, (color.green * 255))),
                                                 max(0, min(255, (color.blue  * 255)))))

        return image
