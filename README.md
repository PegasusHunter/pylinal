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

