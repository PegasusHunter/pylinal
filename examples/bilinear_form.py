from typing import Callable
from pylinal import Vector, Matrix

K = float
BilinearForm = Callable[[Vector[K], Vector[K]], K]


def main():
    b = Matrix([
        [1, 0],
        [0, 1]
    ])

    dot: BilinearForm = bilinear_form(b)
    
    v = Vector([1, -2])
    w = Vector([-3, 5])
    u = Vector([7, -2])

    assert dot(v, w) == v.dot(w)

    assert dot(5*v, w) == dot(v, 5*w) == 5*dot(v, w)
    assert dot(v + u, w) == dot(v, w) + dot(u, w)
    assert dot(v, u + w) == dot(v, u) + dot(v, w)

    return


def bilinear_form(b: Matrix) -> BilinearForm:
    
    def closure(v: Vector, w: Vector) -> K:
        scalar: K = v.dot(b @ w)
        return scalar

    return closure


if __name__ == '__main__':
    main()

