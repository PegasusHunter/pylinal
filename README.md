# PyLinal

Generic Linear Algebra in Python.

## Install

From PyPi
```sh
pip install pylinal
```

From git
```sh
pip install git+https://github.com/cospectrum/pylinal.git
```

## Usage


### Vector

```python
from pylinal import Vector


v = Vector([2, 3.1, 1])
w = Vector(2*i for i in range(3))

u = 2*(w - 5*v)  # Vector

dot = v.dot(w)

```


### Matrix

```python
from pylinal import Matrix, Vector


a = Matrix([
    [1, 3.1, 2],
    [2.4, 2, 5],
])

b = Matrix(range(3) for i in range(2)) # Matrix with shape (2, 3)
c = a - b

ab = a.matmul(b.T) # or a @ b.T
type(ab) == Matrix

v = Vector([2, 1.2, 3])
av = a.matmul(v)  # or a @ v
type(av) == Vector

```


### Functions

#### MatrixFunc

MatrixFunc is a callable Matrix where each element is a function.
It wraps each element in a primitive called "Func".
The sum and multiplication by a scalar will be a MatrixFunc again.

```python
from math import sin, cos, pi
from pylinal import MatrixFunc, Vector


# 3D rotation
rotation = MatrixFunc([
    (cos, lambda x: -sin(x), 0),
    (sin, cos, 0),
    (0, 0, 1)
])

rotate_45 = rotation(pi/4)

v = Vector([1, 1, 1])
u = rotate_45 @ v

```


#### VectorFunc

VectorFunc is similar to a vector-valued function (of several variables).
It wraps each element in a Func.
The sum and multiplication by a scalar will be VectorFunc again.

```python
from math import sin, cos
from pylinal import VectorFunc


parabola = VectorFunc([lambda t: t, lambda t: t**2])
circle = VectorFunc([cos, sin])

curve = parabola + circle

assert curve(1) == (parabola + circle)(1)

```

VectorFunc also has a grad attribute.
Operations will change grad (if grad is not None).

```python
from math import sin, cos
from pylinal import VectorFunc


# t != 0
df = VectorFunc([1, lambda t: -cos(1/t) + 2*t*sin(1/t)])
f = VectorFunc([lambda t: t, lambda t: t**2 * sin(1/t)], grad=df)

g = 3*f

assert g(1) == 3*f(1)
assert g.grad(1) == 3*f.grad(1)

```


