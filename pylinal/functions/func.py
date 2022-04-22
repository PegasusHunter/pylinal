from typing import (
    Any,
    Callable, 
    Union,
)

from ..typedefs import Scalar, Ring

F = Union['Func', Callable[[Any], Scalar]]


def unwrap(f: Any) -> Callable:
    if isinstance(f, Func):
        return f.function
    if callable(f):
        return f
    const = lambda *args, **kwargs: f
    return const


class Func(Ring):
    function: Callable[[Any], Scalar]

    def __init__(self, function: Union[F, Scalar]) -> None:
        self.function = unwrap(function)  # type: ignore
        return

    def __call__(self, *args, **kwargs) -> Scalar:
        return self.function(*args, **kwargs)

    def __add__(self, other: Union[F, Scalar]) -> 'Func':
        f = self.function
        g = unwrap(other)
         
        def add(*args, **kwargs) -> Scalar:
            return f(*args, **kwargs) + g(*args, **kwargs)
        return Func(add)

    def __sub__(self, other: Union[F, Scalar]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def sub(*args, **kwargs) -> Scalar:
            return f(*args, **kwargs) - g(*args, **kwargs)
        return Func(sub)        

    def __mul__(self, other: Union[F, Scalar]) -> 'Func':
        f = self.function
        g = unwrap(other)
        
        def mul(*args, **kwargs) -> Scalar:
            return f(*args, **kwargs) * g(*args, **kwargs)
        return Func(mul)

    def __radd__(self, other: Union[F, Scalar]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def radd(*args, **kwargs) -> Scalar:
            return g(*args, **kwargs) + f(*args, **kwargs)
        return Func(radd)

    def __rsub__(self, other: Union[F, Scalar]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def rsub(*args, **kwargs) -> Scalar:
            return g(*args, **kwargs) - f(*args, **kwargs)
        return Func(rsub)

    def __rmul__(self, other: Union[F, Scalar]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def rmul(*args, **kwargs) -> Scalar:
            return g(*args, **kwargs) * f(*args, **kwargs)
        return Func(rmul)

    def __repr__(self) -> str:
        return f'Func({self.function})'

