import itertools
import random

from numpy import linspace
from pylinal import VectorFunc
from math import cos, sin, pi

   
R = 8
r = 1

# u in [0, 2pi]; v in [-pi, pi]
x = lambda u, v: (R + r*cos(v)) * cos(u)
y = lambda u, v: (R + r*cos(v)) * sin(u)
z = lambda u, v: r*sin(v)

torus = VectorFunc([x, y, z])

us = linspace(0, 2*pi, 40)
vs = linspace(-pi, pi, 40)
cartesian = itertools.product(us, vs)

points = [torus(u, v) for (u, v) in cartesian]
