import random
import itertools
from typing import Tuple, List

from pylinal import Vector, Matrix


def random_rows(shape: Tuple[int, int], integer: bool = False) -> List:
    dim_0, dim_1 = shape
    prng = lambda: random.random() - 1/2

    if integer:
        prng = lambda: random.randint(-10, 10)

    rows: List[List[float]] = [
        [prng() for _ in range(dim_1)]
        for _ in range(dim_0)
    ]
    return rows


class TestMatrix:

    def test_flatten(self):
        rows = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        m = Matrix(rows)
        
        def chain(rows: List[List]) -> List:
            flatten = [el for row in rows for el in row]
            return flatten

        assert m.flatten() == Vector(el for el in itertools.chain(*rows))
        assert m.flatten() == Vector(rows[0] + rows[1] + rows[2])

        tries = random.randint(5, 10)
        for _ in range(tries):
            shape = (random.randint(1, 10), random.randint(1, 10))
            rows = random_rows(shape, integer=True)
            m = Matrix(rows)
            
            assert m.flatten() == Vector(chain(rows))
            assert m.flatten() == Vector(itertools.chain(*rows))

        return

    def test_init(self):
        rows = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        m = Matrix(rows)
        assert m[0] == Vector(rows[0])
        assert m[1] == Vector(rows[1])
        assert m[2] == Vector(rows[2])

        assert m == Matrix(m)

    def test_transposition(self):
        v = Matrix([
            [2, 4, 6]
        ])
        v_copy = v.copy()
        v.T
        assert v == v_copy == Matrix([[2, 4, 6]])
        assert v.T.T == v
        assert v.T.shape == tuple(reversed(v.shape))
        v_transpose = Matrix([
            [2],
            [4],
            [6]
        ])
        assert v_transpose == v.T

        m = Matrix([
            [2, 3],
            [4, 5]
        ])
        m_copy = m.copy()
        m.T
        assert m == m_copy == Matrix([
            [2, 3],
            [4, 5]
        ])
        assert m.T.shape == tuple(reversed(m.shape))
        assert m.T.T == m

        m_transpose = Matrix([
            [2, 4],
            [3, 5]
        ])
        assert m_transpose == m.T

        n = Matrix([
            [1, 4],
            [8, -2],
            [-3, 5]
        ])
        assert n.shape == (3, 2)
        assert n.T.shape == (2, 3)

        n_transpose = Matrix([
            [1, 8, -3],
            [4, -2, 5]
        ])
        assert n_transpose == n.T

        tries = 5
        for _ in range(tries):
            dim: int = random.randint(1, 5)

            shape = dim, dim

            a = Matrix(random_rows(shape, integer=True))
            b = Matrix(random_rows(shape, integer=True))
            c = Matrix(random_rows(shape, integer=True))

            assert (a + b).T == a.T + b.T
            assert (a + b + c).T == a.T + b.T + c.T

            scalar: float = random.random() - 1/2
            assert (scalar * a).T == scalar * a.T

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

        scalar: int = random.randint(-4, 4)

        assert scalar * ab == (scalar * a) @ b
        assert ab * scalar == a * scalar @ b == a @ b * scalar

        v = Vector([100, 80, 60])
        abv = Vector([1000, 1820, 1180, 2180])
        assert abv == ab.matmul(v)
        assert abv == ab @ v

        assert scalar * abv == (scalar * ab) @ v
        assert abv * scalar == ab @ v * scalar

        tries = 5
        for _ in range(tries):
            dim_0: int = random.randint(1, 5)
            dim_1: int = random.randint(1, 5)
            dim_2: int = random.randint(1, 5)
            dim_3: int = random.randint(1, 5)

            shape_a = dim_0, dim_1
            shape_b = dim_1, dim_2
            shape_c = dim_2, dim_3

            a = Matrix(random_rows(shape_a, integer=True))
            b = Matrix(random_rows(shape_b, integer=True))
            c = Matrix(random_rows(shape_c, integer=True))

            assert (a @ b) @ c == a @ (b @ c)
            assert (a @ b).T == b.T @ a.T
            assert (a @ b @ c).T == c.T @ b.T @ a.T

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

    def test_getitem(self):
        a = Matrix([
            [1, 2, 3],
            [4, 5, 6]
        ])
        assert a[0] == Vector([1, 2, 3]) == a[0, :]
        assert a[1] == Vector([4, 5, 6]) == a[1, :]

        assert (a[0][0], a[0][1], a[0][2]) == (1, 2, 3)
        assert (a[1][0], a[1][1], a[1][2]) == (4, 5, 6)

        
        assert a[0:1] == Matrix([[1, 2, 3]])
        assert a[0:] == a[:, :] == a
        
        assert a[:, 0] == Vector([1, 4])
        assert a[:, 1] == Vector([2, 5])
        assert a[:, 2] == Vector([3, 6])
        
        assert a[:, :1] == Matrix([
            [1],
            [4]
        ])

        assert a[:, 1:2] == Matrix([
            [2],
            [5]
        ])
        
       
        assert a[:, 2:3] == Matrix([
            [3],
            [6]
        ])
        

    def test_setitem(self):
        zero = Matrix([[0, 0], [0, 0]])
        
        a = zero.copy()
        a[0][0] = 1
        a[1][1] = 1
        assert a != zero
        assert zero == Matrix([[0, 0], [0, 0]])
        assert 1 == a[0][0]
        assert 1 == a[1][1]
        assert a == Matrix([[1, 0], [0, 1]])        
        
        e = a.copy()
        assert e == Matrix([[1, 0], [0, 1]])
        a[0] = Vector([0, 0])
        a[1] = Vector([0, 0])
        assert a != e
        assert a == zero

        a = e
        assert a == Matrix([[1, 0], [0, 1]])
        a[0] = [0, 0]
        a[1] = [0, 0]
        assert a == e == zero

        b = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        b[0] = [0, 0, 0]
        assert b == Matrix([
            [0, 0, 0],
            [4, 5, 6],
            [7, 8, 9]
        ])
        assert b[0] == Vector([0, 0, 0])
        assert b[0] != [0, 0, 0]

    def test_copy(self):
        a = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        b = a.copy()
        for row in a:
            row[0] = 0
        assert a != b
        assert a == Matrix([
            [0, 2, 3],
            [0, 5, 6],
            [0, 8, 9]
        ])
        assert b == Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])

        c = b
        for row in b:
            row[0] = 0
        assert b == c
        assert b == Matrix([
            [0, 2, 3],
            [0, 5, 6],
            [0, 8, 9]
        ])

    def test_iter(self):
        a = Matrix([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ])

        for i, row in enumerate(a):
            el: int = 3*i
            assert row == a[i] == Vector((el, el+1, el+2))

        i: int = 0
        for row in a:
            for el in row:
                assert el == i
                i += 1

        for row in a:
            row = Vector([0, 0, 0])
        for row in a:
            assert row != Vector([0, 0, 0])

        assert a[0] == Vector([0, 1, 2])
        assert a[1] == Vector([3, 4, 5])
        assert a[2] == Vector([6, 7, 8])

        for row in a:
            row[0] = -1
        assert a == Matrix([
            [-1, 1, 2],
            [-1, 4, 5],
            [-1, 7, 8]
        ])

    def test_iadd(self):
        dim: int = random.randint(1, 5)
        shape = dim, dim

        a = Matrix(random_rows(shape))
        b = Matrix(random_rows(shape))
        a_copy = a.copy()
        b_copy = b.copy()

        a += b
        assert a == a_copy + b_copy

    def test_isub(self):
        dim: int = random.randint(1, 5)
        shape = dim, dim

        a = Matrix(random_rows(shape))
        b = Matrix(random_rows(shape))
        a_copy = a.copy()
        b_copy = b.copy()

        a -= b
        assert a == a_copy - b_copy

    def test_imul(self):
        dim_0: int = random.randint(1, 5)
        dim_1: int = random.randint(1, 5)
        shape = dim_0, dim_1

        a = Matrix(random_rows(shape))
        a_copy = a.copy()
        scalar: float = random.random() - 1/2

        a *= scalar
        assert a == scalar * a_copy

