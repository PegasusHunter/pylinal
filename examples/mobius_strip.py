import itertools
from numpy import linspace
from pylinal import VectorFunc
from math import cos, sin, pi

# u in [0, 2pi); v in [-1, 1]
x = lambda u, v: (1 + v/2 * cos(u/2)) * cos(u)
y = lambda u, v: (1 + v/2 * cos(u/2)) * sin(u)
z = lambda u, v: v/2 * sin(u/2)

mobius_strip = VectorFunc([x, y, z])

us = linspace(0, 2*pi, 40, endpoint=False)
vs = linspace(-1, 1, 40)
cartesian = itertools.product(us, vs)

points = [mobius_strip(u, v) for (u, v) in cartesian]

