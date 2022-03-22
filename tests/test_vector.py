import random
from typing import List

from pylinal import Vector


def random_elements(dim: int) -> List:
    elements: List[float] = [random.random() - 1/2 for _ in range(dim)]
    return elements


class TestVector:

    def test_init(self):
        sequence = [1, 2, 3]
        v = Vector(sequence)
        assert v[0] == 1
        assert v[1] == 2
        assert v[2] == 3

        assert v == Vector(v)

    def test_equality(self):
        tries = random.randint(2, 4)
        for _ in range(tries):
            dim = random.randint(1, 5)
            elements = random_elements(dim)
            a = Vector(elements)

            assert a == a
            assert -a == -a

            assert a == Vector(elements)
            assert -a == -Vector(elements)
            
            assert len(a) == len(Vector(elements))
            assert len(a) == dim

            scalar = random.random() - 1/2
            assert scalar * a == scalar * a
            assert scalar * a == scalar * Vector(elements)

    def test_examples(self):
        a = Vector([1, 2, 3])
        assert len(a) == 3
        assert len(-a) == 3
        assert len(-1 * a) == len(a * -1) == 3

        assert a == Vector([1, 2, 3])
        assert -a == Vector([-1, -2, -3])
        assert -a == -1 * a == a * -1

        b = Vector([-2, 0, 4])
        assert len(b) == 3
        assert len(-b) == 3
        assert len(-1 * b) == len(b * -1) == 3

        assert b == Vector([-2, 0, 4])
        assert -b == Vector([2, 0, -4])
        assert -b == -1 * b == b * -1

        assert 3 == len(a + b)
        assert 3 == len(b + a)
        assert 3 == len(-(a + b)) == len(-1*(a + b))

        c = Vector([-1, 2, 7])
        assert a + b == c
        assert a + b == b + a
        assert 10*c == (b + a)*10 == Vector([-10, 20, 70])

        a_sub_b = Vector([3, 2, -1])
        assert a_sub_b == a - b

        a_sub_b_mul_3 = Vector([-9, -6, 3])
        assert a_sub_b_mul_3 == -3 * a_sub_b
        assert a_sub_b_mul_3 == -3 * (a - b) == -3 * a + 3 * b

    def test_dot(self):
        a = Vector([1, 3, -5])
        b = Vector([4, -2, -1])
        assert a.dot(b) == b.dot(a) == 3

    def test_getitem(self):
        dim: int = random.randint(2, 5)
        elements: List[float] = random_elements(dim)

        a = Vector(elements)
        for i, el in enumerate(elements):
            assert el == a[i]

        key: int = random.randint(0, dim)
        assert a[:key] == Vector(elements[:key])

    def test_setitem(self):
        dim: int = random.randint(1, 5)
        elements: List[float] = random_elements(dim)

        a: Vector[int] = Vector(range(dim))
        for i, el in enumerate(elements):
            a[i] = el
            assert el == a[i]
        assert a == Vector(elements)

    def test_iadd(self):
        dim: int = random.randint(1, 5)
        elements: List[float] = random_elements(dim)

        a = Vector(range(dim))
        a += Vector(elements)
        assert Vector(range(dim)) + Vector(elements) == a

    def test_isub(self):
        dim: int = random.randint(1, 5)
        elements: List[float] = random_elements(dim)

        a = Vector(range(dim))
        a -= Vector(elements)
        assert Vector(range(dim)) - Vector(elements) == a

    def test_copy(self):
        a = Vector([1, 2, 3])
        b = a.copy()
        for i in range(len(b)):
            b[i] = 0
        assert b == Vector([0, 0, 0])
        assert a != b
        assert a == Vector([1, 2, 3])

        c = a
        assert a == c == Vector([1, 2, 3])
        for i in range(len(c)):
            c[i] = 0
        assert a == Vector([0, 0, 0])

    def test_iter(self):
        a = Vector([1, 2, 3])
        assert list(a) == [1, 2, 3]
        elements = tuple(el for el in a)
        assert elements == (1, 2, 3)

        for el in a:
            el = 0
        assert (a[0], a[1], a[2]) != (0, 0, 0)
        assert a == Vector([1, 2, 3])

    def test_imul(self):
        dim: int = random.randint(1, 5)

        a = Vector(random_elements(dim))
        a_copy = a.copy()
        scalar: float = random.random() - 1 / 2

        a *= scalar
        assert a == scalar * a_copy

