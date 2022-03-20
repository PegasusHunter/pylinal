import random
import math

from typing import Callable
from pylinal.functions.func import Func


def get_monom(deg: int) -> Callable:
    return lambda x: x**deg


class TestFunc:
    
    @staticmethod
    def run_tests():
        tests = [f for f in dir(TestFunc) if f.startswith('test_')]
        for method in tests:
            eval(f'TestFunc.{method}()')

    @staticmethod
    def test_init():
        foo = lambda x: 2*x
        f = Func(foo)
        g = Func(f)
        assert f.function == g.function == foo

    @staticmethod
    def test_monom():
        deg: int = random.randint(0, 20)
        poly = get_monom(deg)
        f = Func(poly)

        interval = range(-20, 20)
        for x in interval:
            scalar = random.random() - 1/2
            assert f(x) == poly(x)
            assert (f + scalar)(x) == poly(x) + scalar

            assert f(scalar*x) == poly(scalar*x)
            assert scalar*f(x) == scalar*poly(x)

    @staticmethod
    def test_evaluate():
        functions: dict = {
            'x*y': lambda x, y: x*y,
            'x + y': lambda x, y: x + y,
            'x/y': lambda x, y: x/y,
            'x**y': lambda x, y: x**y,
            'math.exp(x)': lambda x, y: math.exp(x),
        }

        interval = (-20, 20)
        for _ in range(20):
            k = 2
            key_f, key_g = random.sample(functions.keys(), k)
            
            f, g = functions[key_f], functions[key_g]
            f, g = Func(f), Func(g)
            
            for _ in range(10):
                x: int = random.randint(*interval)
                y: int = random.randint(*interval)

                if 'x**y' in key_f + key_g:
                    y = abs(y)
                if y == 0 and 'x/y' in key_f + key_g:
                    y = random.randint(1, interval[1])
                
                assert f(x, y) == eval(key_f)
                assert g(x, y) == eval(key_g)
                
                h = f + g
                assert h(x, y) == (f + g)(x, y) == eval(key_f) + eval(key_g)
                assert h(x, y) == f(x, y) + g(x, y)
                
                h = f*g
                assert h(x, y) == (f*g)(x, y) == eval(key_f) * eval(key_g)
                assert h(x, y) == f(x, y) * g(x, y)

    @staticmethod
    def test_commutativity():
        f = Func(lambda x: x**2)
        g = Func(lambda x: 3*x)

        tries = 5
        for _ in range(tries):
            x = 10*(random.random() - 1/2)

            assert f(x) + g(x) == g(x) + f(x)
            assert f(x) * g(x) == g(x) * f(x)

            scalar = random.random() - 1/2
            assert (f * scalar)(x) == (scalar * f)(x)
            assert (g * scalar)(x) == (scalar * g)(x)


def main():
    TestFunc.run_tests()
    print('success!')


if __name__ == '__main__':
    main()


