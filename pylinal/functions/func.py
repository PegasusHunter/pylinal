from typing import (
    TypeVar,
    Any,
    Callable, 
    Union,
)

T = TypeVar('T')
F = Union['Func', Callable[[Any], T]]


def unwrap(f: Any) -> Callable:
    if isinstance(f, Func):
        return f.function
    if callable(f):
        return f
    const = lambda *args, **kwargs: f
    return const


class Func:
    function: Callable[[Any], T]

    def __init__(self, function: Union[F, T]):
        self.function = unwrap(function)

    def __call__(self, *args, **kwargs) -> T:
        return self.function(*args, **kwargs)

    def __add__(self, other: Union[F, T]) -> 'Func':
        f = self.function
        g = unwrap(other)
         
        def add(*args, **kwargs) -> T:
            return f(*args, **kwargs) + g(*args, **kwargs)
        return Func(add)

    def __sub__(self, other: Union[F, T]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def sub(*args, **kwargs) -> T:
            return f(*args, **kwargs) - g(*args, **kwargs)
        return Func(sub)        

    def __mul__(self, other: Union[F, T]) -> 'Func':
        f = self.function
        g = unwrap(other)
        
        def mul(*args, **kwargs) -> T:
            return f(*args, **kwargs) * g(*args, **kwargs)
        return Func(mul)

    def __radd__(self, other: Union[F, T]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def radd(*args, **kwargs) -> T:
            return g(*args, **kwargs) + f(*args, **kwargs)
        return Func(radd)

    def __rsub__(self, other: Union[F, T]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def rsub(*args, **kwargs) -> T:
            return g(*args, **kwargs) - f(*args, **kwargs)
        return Func(rsub)

    def __rmul__(self, other: Union[F, T]) -> 'Func':
        f = self.function
        g = unwrap(other)

        def rmul(*args, **kwargs) -> T:
            return g(*args, **kwargs) * f(*args, **kwargs)
        return Func(rmul)

    def __repr__(self) -> str:
        return f'Func({self.function})'

