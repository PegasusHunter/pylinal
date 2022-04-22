from pylinal import Vector


def test():
    v: Vector[str] = Vector(['a', 'b', 'c'])
    double = Vector(['aa', 'bb', 'cc'])
    assert 2*v == double == v*2
    assert v + v == double
