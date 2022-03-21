import random
from pylinal import Matrix

from pylinal import MatrixFunc


class TestMatrixFunc:

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

