import random
import itertools
from typing import List, Tuple

from pylinal import Matrix, MatrixFunc, VectorFunc


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


class TestMatrixFunc:

    def test_flatten(self):
        rows = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        m = MatrixFunc(rows)
        
        def chain(rows: List[List]) -> List:
            flatten = [el for row in rows for el in row]
            return flatten

        assert m.flatten()() == VectorFunc(el for el in itertools.chain(*rows))()
        assert m.flatten()() == VectorFunc(rows[0] + rows[1] + rows[2])()

        tries = random.randint(5, 10)
        for _ in range(tries):
            shape = (random.randint(1, 10), random.randint(1, 10))
            rows = random_rows(shape, integer=True)
            
            m = MatrixFunc(rows)
            
            assert m.flatten()() == VectorFunc(chain(rows))()
            assert m.flatten()() == VectorFunc(itertools.chain(*rows))()

        return

    @staticmethod
    def run_tests():
        tests = [f for f in dir(TestMatrixFunc) if f.startswith('test_')]
        for method in tests:
            eval(f'TestMatrixFunc.{method}()')

    @staticmethod
    def test_example():
        rand = lambda: random.randint(-10, 10)

        shape = (1+abs(rand()), 1+abs(rand()))
        rows = [
            [rand() for _ in range(shape[1])]
            for _ in range(shape[0])
        ]
        matrix = Matrix(rows)

        f = MatrixFunc(rows)
        assert f() == matrix

        scalar = rand()
        assert scalar * f() == (scalar * f)() == scalar * matrix
        assert f() * scalar == (f * scalar)() == matrix * scalar

        assert f() + matrix == (f + matrix)() == 2*matrix
        assert matrix + f() == (matrix + f)() == 2*matrix

        assert f().T == f.T() == matrix.T


def main():
    TestMatrixFunc.run_tests()
    print('success!')


if __name__ == '__main__':
    main()

