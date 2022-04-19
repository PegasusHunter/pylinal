import itertools
from numpy import linspace
from pylinal import VectorFunc
from math import cos, sin, pi

   
R = 8  # distance from the center of the tube to the center of the torus
r = 1  # radius of the tube

# theta, phi in [0, 2*pi)
x = lambda theta, phi: (R + r*cos(theta)) * cos(phi)
y = lambda theta, phi: (R + r*cos(theta)) * sin(phi)
z = lambda theta, phi: r*sin(theta)

torus = VectorFunc([x, y, z])

arg = linspace(0, 2*pi, 40, endpoint=False)
cartesian = itertools.product(arg, arg)

points = [torus(theta, phi) for (theta, phi) in cartesian]

