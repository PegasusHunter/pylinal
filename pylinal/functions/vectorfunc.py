from typing import TypeVar, Union, Optional, Iterator, Sequence

from ..vector import Vector
from ..matrix import Matrix

from .func import Func


def has_grad(*args) -> bool:
    if all(f.grad is not None for f in args):
        return True
    return False


T = TypeVar('T')


class VectorFunc:
    grad: Optional[Union['VectorFunc', Matrix]]
    vec: Vector[Func]

    def __init__(
        self,
        sequence: Union[Iterator, Sequence, Vector],
        *,
        grad: Optional[Union['VectorFunc', Matrix]] = None,
        __wrap: bool = True,
    ) -> None:
        if __wrap:
            seq = (Func(f) for f in sequence)
            self.vec = Vector(seq)
        else:
            self.vec = sequence
        self.grad = grad
        return

    def __call__(self, *args, **kwargs) -> Vector:
        result = Vector(f(*args, **kwargs) for f in self)
        return result
    
    def dot(self, other: 'VectorFunc') -> 'Func':
        return self.vec.dot(other.vec)
    
    def __add__(self, other: 'VectorFunc') -> 'VectorFunc':
        vec: Vector = self.vec + other.vec
        grad = None
        if has_grad(self, other):
            grad = self.grad + other.grad
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)

    def __radd__(self, other: 'VectorFunc') -> 'VectorFunc':
        vec: Vector = other.vec + self.vec
        grad = None
        if has_grad(self, other):
            grad = other.grad + self.grad
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)

    def __sub__(self, other: 'VectorFunc') -> 'VectorFunc':
        vec = self.vec - other.vec
        grad = None
        if has_grad(self, grad):
            grad = self.grad - other.grad
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)

    def __rsub__(self, other: 'VectorFunc') -> 'VectorFunc':
        vec: Vector = other.vec - self.vec
        grad = None
        if has_grad(self, other):
            grad = other.grad - self.grad
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)

    def __mul__(self, scalar: T) -> 'VectorFunc':
        vec: Vector = self.vec * scalar
        grad = None
        if has_grad(self):
            grad = self.grad * scalar
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)

    def __rmul__(self, scalar: T) -> 'VectorFunc':
        vec: Vector = scalar * self.vec
        grad = None
        if has_grad(self):
            grad = scalar * self.grad
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)
    
    def __pos__(self) -> 'VectorFunc':
        self

    def __neg__(self) -> 'VectorFunc':
        vec: Vector = -self.vec
        grad = None
        if has_grad(self):
            grad = -self.grad
        return VectorFunc(vec, grad=grad, _VectorFunc__wrap=False)

    def __getitem__(self, index: int) -> Func:
        return self.vec[index]

    def __iter__(self) -> Iterator[Func]:
        return iter(self.vec)

    def __reversed__(self) -> Iterator[Func]:
        return reversed(self.vec)

    def __iadd__(self, other: 'VectorFunc') -> 'VectorFunc':
        self = self + other
        return self

    def __isub__(self, other: 'VectorFunc') -> 'VectorFunc':
        self = self - other
        return self

    def __imul__(self, scalar: T) -> 'VectorFunc':
        self = scalar * self
        return self

    def __len__(self) -> int:
        return len(self.vec)
 
    def __repr__(self) -> str:
        seq = [f for f in self]

        if isinstance(self.grad, VectorFunc):
            string: str = f'{seq}, grad=VectorFunc(...)'
        elif isinstance(self.grad, Matrix):
            string: str = f'{seq}, grad=Matrix(...)'
        else:
            string: str = f'{seq}, grad={type(self.grad)}'

        return f'VectorFunc({string})'

