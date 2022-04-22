from pylinal import Vector


def test():
    v = Vector([1j, 1+1j])
    iv = Vector([-1, 1j - 1])
    assert 1j*v == iv == v*1j
