import random
from typing import Tuple, List

from pylinal import Vector, Matrix


def random_elements(dim: int) -> List:
    rows: List[float] = [random.random() for _ in range(dim)]
    return rows


class TestVector:
    def test_equality(self):
        tries = random.randint(2, 5)
        for _ in range(tries):
            dim = random.randint(2, 10)
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
        assert a == Vector([1, 2, 3])
        assert -a == Vector([-1, -2, -3])
        assert -a == -1 * a == a * -1

        b = Vector([-2, 0, 4])
        assert b == Vector([-2, 0, 4])
        assert -b == Vector([2, 0, -4])
        assert -b == -1 * b == b * -1

        c = Vector([-1, 2, 7])
        assert a + b == c
        assert a + b == b + a
        assert 10*c == (b + a)*10 == Vector([-10, 20, 70])

        a_sub_b = Vector([3, 2, -1])
        assert a_sub_b == a - b

        a_sub_b_mul_3 = Vector([-9, -6, 3])
        assert a_sub_b_mul_3 == -3 * a_sub_b
        assert a_sub_b_mul_3 == -3*(a - b) == -3*a + 3*b

    def test_dot(self):
        a = Vector([1, 3, -5])
        b = Vector([4, -2, -1])
        assert a.dot(b) == b.dot(a) == 3


def random_rows(shape: Tuple[int, int]) -> List:
    dim_0, dim_1 = shape
    rows: List[List[float]] = [
        [random.random() for _ in range(dim_1)]
        for _ in range(dim_0)
    ]
    return rows


class TestMatrix:
    def test_equality(self):
        tries = random.randint(2, 5)
        for _ in range(tries):
            shape = (random.randint(2, 10), random.randint(2, 10))
            rows = random_rows(shape)
            a = Matrix(rows)

            assert a.shape == shape
            assert a == a
            assert -a == -a

            assert a == Matrix(rows)
            assert -a == -Matrix(rows)

            scalar = random.random() - 1/2
            assert scalar * a == scalar * Matrix(rows)
            assert a * scalar == Matrix(rows) * scalar

    def test_matmul(self):
        a_rows = [
            [1, 0, 1],
            [2, 1, 1],
            [0, 1, 1],
            [1, 1, 2]
        ]
        a = Matrix(a_rows)
        assert a.shape == (4, 3)

        b_rows = [
            [1, 2, 1],
            [2, 3, 1],
            [4, 2, 2]
        ]
        b = Matrix(b_rows)

        ab = Matrix([
            [5, 4, 3],
            [8, 9, 5],
            [6, 5, 3],
            [11, 9, 6]
        ])
        assert ab == a.matmul(b)
        assert ab == a @ b
        assert ab.T == (a @ b).T == b.T @ a.T

        v = Vector([100, 80, 60])
        abv = Vector([1000, 1820, 1180, 2180])
        assert abv == ab.matmul(v)
        assert abv == ab @ v

    def test_commutativity(self):
        a_rows = [
            [0, 1],
            [0, 0]
        ]
        b_rows = [
            [0, 0],
            [1, 0]
        ]
        a = Matrix(a_rows)
        b = Matrix(b_rows)
        assert a + b == b + a

        ab = Matrix([[1, 0], [0, 0]])
        assert ab == a @ b and ab == a.matmul(b)

        ba = Matrix([[0, 0], [0, 1]])
        assert ba == b @ a and ba == b.matmul(a)
        assert ab != ba

    def test_sub(self):
        a = Matrix([
            [2, 3],
            [4, 5]
        ])
        b = Matrix([
            [6, 2],
            [7, 9]
        ])

        a_sub_b = Matrix([
            [-4, 1],
            [-3, -4]
        ])

        b_sub_a = Matrix([
            [4, -1],
            [3, 4]
        ])

        assert a_sub_b == -1*b_sub_a
        assert b_sub_a == -1*a_sub_b

        assert a - b == a_sub_b
        assert b - a == b_sub_a

