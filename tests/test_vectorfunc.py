import math
import random

from typing import List, Callable

from pylinal import (
    VectorFunc,
    MatrixFunc,
    Vector,
    Matrix,
)


def get_random_poly(deg, integer=True) -> List[Callable]:
    if integer:
        random_scalar = lambda: random.randint(0, 10) - 5
    else:
        random_scalar = lambda: random.random() - 1/2

    scalars = (random_scalar() for _ in range(deg+1))
    poly: List[Callable] = [
        lambda x: scalar * x**n
        for scalar, n in zip(scalars, range(deg+1))
    ]
    return poly


class TestVectorFunc:

    @staticmethod
    def run_tests():
        tests = [f for f in dir(TestVectorFunc) if f.startswith('test_')]
        for method in tests:
            eval(f'TestFunc.{method}()')

    @staticmethod
    def test_poly():
        deg: int = random.randint(0, 30)
        poly = get_random_poly(deg)
        f = VectorFunc(poly)

        tries = 10
        for _ in range(tries):
            x = random.random() - 1/2
            poly_x = [p(x) for p in poly]
            f_x: Vector = f(x)

            assert f_x == Vector(poly_x)
            assert list(f_x) == poly_x

    @staticmethod
    def test_example_1():
        df = VectorFunc([1, lambda x: 2*x])
        f = VectorFunc([lambda x: x, lambda x: x**2], grad=df)

        for x in range(-9, 9):

            f_x = f(x)
            assert type(f_x) == Vector
            assert tuple(f_x) == (x, x**2)
            
            grad = f.grad(x)
            assert type(grad) == Vector
            assert grad == df(x)
            assert tuple(grad) == (1, 2*x)
                
    @staticmethod
    def test_example_2():
        f_1 = lambda x, y: x**2 * y
        f_2 = lambda x, y: 5*x + math.sin(y)
        f = VectorFunc([f_1, f_2])
        
        df_1 = VectorFunc([lambda x, y: 2*x*y, lambda x, y: x**2])
        df_2 = VectorFunc([5, lambda x, y: math.cos(y)])
        
        df = MatrixFunc([
            df_1,
            df_2    
        ])

        f.grad = df
        
        interval = range(-9, 9), range(-9, 9)
        for x in zip(*interval):
            f_x = f(*x)
            assert type(f_x) == Vector
            assert tuple(f_x) == (f_1(*x), f_2(*x))

            df_x = f.grad(*x)
            assert type(df_x) == Matrix
            assert df_x == df(*x)
            
            assert df_x[0] == df_1(*x)
            assert df_x[1] == df_2(*x)


def main():
    TestVectorFunc.test_poly()
    print('success!')


if __name__ == '__main__':
    main()
