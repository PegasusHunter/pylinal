import itertools
from numpy import linspace
from pylinal import VectorFunc
from math import cos, sin, pi


center = (0, 0, 0)
x0, y0, z0 = center
r = 1  # radius

# theta in [0, pi]; phi in [0, 2*pi]
x = lambda theta, phi: x0 + r * sin(theta) * cos(phi)
y = lambda theta, phi: y0 + r * sin(theta) * sin(phi)
z = lambda theta, phi: z0 + r * cos(theta)

sphere = VectorFunc([x, y, z])

theta = linspace(0, pi)
phi = linspace(0, 2*pi)
cartesian = itertools.product(theta, phi)

points = [sphere(theta, phi) for (theta, phi) in cartesian]
