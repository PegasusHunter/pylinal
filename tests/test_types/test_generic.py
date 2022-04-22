from typing import Union
from pylinal import Vector


class T:
    def __init__(self, x):
        self.x = x

    def __mul__(self, other: Union['T', Vector]) -> Union['T', Vector]:
        return other.__rmul__(self)

    def __rmul__(self, other: 'T') -> 'T':
        return T(self.x.__rmul__(other.x))

    def __eq__(self, other: 'T') -> bool:
        return self.x == other.x


def test_mul():
    v = Vector([T(1), T(1)])
    assert T(2) * v == v * T(2)
