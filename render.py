#!/usr/bin/env python3

import math
import os

from src.tryffeli.primitive import Sphere
from src.tryffeli.camera import SimpleCamera
from src.tryffeli.vector import Vector
from src.tryffeli.film import RenderSurface
from src.tryffeli.material import Material
from src.tryffeli.color import Color

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

camera.film.as_qimage().save("./misc/tryffeli.png")
os.system("display ./misc/tryffeli.png")
