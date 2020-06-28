#!/usr/bin/env python3

import os

from src.tryffeli.primitive import Sphere
from src.tryffeli.camera import SimpleCamera
from src.tryffeli.vector import Vector
from src.tryffeli.film import RenderSurface
from src.tryffeli.material import Material
from src.tryffeli.color import Color
from src.tryffeli.scene import Scene

camera = SimpleCamera(position = Vector(0, 0, 0),
                      direction = Vector(0, 0, -1),
                      film = RenderSurface(640, 360, backgroundColor = Color(0, 0, 0)))

scene = Scene()

scene.primitives = [
    Sphere(radius = 30,
           position = Vector(0, 0, 200),
           material = Material(type = Material.Type.lambertian)),
    Sphere(radius = 10,
           position = Vector(50, 0, 200),
           material = Material(type = Material.Type.lambertian))
]

camera.shoot(scene)

print("Exporting as a PNG...")
camera.film.as_qimage().save("./misc/tryffeli.png")

os.system("display ./misc/tryffeli.png")
