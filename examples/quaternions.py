from pylinal import Vector


def main():
    a = 4
    v = Vector([2, 3, 4])
    av: Vector = a*v

    q = Quaternion(a, 0, 0, 0)
    p = Quaternion(0, *v)

    assert -p == p.conjugate()

    qp: Quaternion = q * p
    assert qp == Quaternion(0, *av)
    print(f'q*p = {qp}')
    
    return


class Quaternion:
    scalar: float   # scalar part
    vector: Vector[float]  # 3d vector

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        self.scalar = a
        self.vector = Vector([b, c, d])

    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        scalar: float = self.scalar + other.scalar
        vector: Vector = self.vector + other.vector
        return Quaternion(scalar, *vector)

    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        a: float = self.scalar
        b: float = other.scalar
        u: Vector = self.vector
        v: Vector = other.vector

        scalar: float = a*b - u.dot(v)
        vector: Vector = a*v + b*u + cross(u, v)
        return Quaternion(scalar, *vector)

    def conjugate(self) -> 'Quaternion':
        b, c, d = self.vector
        return Quaternion(self.scalar, -b, -c, -d)

    def __abs__(self) -> float:
        a = self.scalar
        b, c, d = self.vector
        return (a**2 + b**2 + c**2 + d**2)**0.5

    def __neg__(self) -> 'Quaternion': 
        b, c, d = self.vector
        return Quaternion(-self.scalar, -b, -c, -d)

    def __eq__(self, other: 'Quaternion') -> bool:
        return self.scalar == other.scalar and self.vector == other.vector

    def __repr__(self) -> str:
        v = self.vector
        return f'Quaternion({self.scalar}, {v[0]}, {v[1]}, {v[2]})'


def cross(a: Vector, b: Vector) -> Vector:
    assert len(a) == len(b) == 3

    first = a[1]*b[2] - a[2]*b[1]
    second = -(a[0]*b[2] - a[2]*b[0])
    third = a[0]*b[1] - a[1]*b[0]

    return Vector([first, second, third])


if __name__ == '__main__':
    main()

