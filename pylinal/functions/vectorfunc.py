from typing import (
    Union,
    Optional,
    Iterator,
    Iterable,
)

from ..vector import Vector
from ..matrix import Matrix
from .func import Func

from ..typedefs import Scalar

Grad = Union['VectorFunc', Matrix]


class VectorFunc:
    grad: Optional[Grad]
    vec: Vector[Func]

    def __init__(
        self,
        sequence: Iterable,
        *,
        grad: Optional[Grad] = None,
        _wrap: bool = True,
    ) -> None:
        if _wrap:
            seq = (Func(f) for f in sequence)
            self.vec = Vector(seq)
        else:
            self.vec = sequence  # type: ignore
        self.grad = grad
        return

    def __call__(self, *args, **kwargs) -> Vector:
        result: Vector = Vector(f(*args, **kwargs) for f in self)
        return result
    
    def dot(self, other: 'VectorFunc') -> 'Func':
        return self.vec.dot(other.vec)  # type: ignore
    
    def __add__(self, other: 'VectorFunc') -> 'VectorFunc':  # type: ignore[override]
        vec: Vector = self.vec + other.vec
        
        grad = None
        if self.grad and other.grad:
            grad = self.grad + other.grad  # type: ignore

        return VectorFunc(vec, grad=grad, _wrap=False)

    def __radd__(self, other: 'VectorFunc') -> 'VectorFunc':  # type: ignore[override]
        vec: Vector = other.vec + self.vec
        
        grad = None
        if self.grad and other.grad:
            grad = other.grad + self.grad  # type: ignore
        
        return VectorFunc(vec, grad=grad, _wrap=False)

    def __sub__(self, other: 'VectorFunc') -> 'VectorFunc':
        vec = self.vec - other.vec
        
        grad = None
        if self.grad and other.grad:
            grad = self.grad - other.grad  # type: ignore
        
        return VectorFunc(vec, grad=grad, _wrap=False)

    def __rsub__(self, other: 'VectorFunc') -> 'VectorFunc':
        vec: Vector = other.vec - self.vec
        
        grad = None
        if self.grad and other.grad:
            grad = other.grad - self.grad  # type: ignore
        
        return VectorFunc(vec, grad=grad, _wrap=False)

    def __mul__(self, scalar: Func) -> 'VectorFunc':
        vec: Vector = self.vec * scalar         
        grad = self.grad * scalar if self.grad else None

        return VectorFunc(vec, grad=grad, _wrap=False)

    def __rmul__(self, scalar: Scalar) -> 'VectorFunc':
        vec: Vector = scalar * self.vec
        grad = scalar * self.grad if self.grad else None
        
        return VectorFunc(vec, grad=grad, _wrap=False)
    
    def __pos__(self) -> 'VectorFunc':
        return self

    def __neg__(self) -> 'VectorFunc':
        vec: Vector = -self.vec
        grad = -self.grad if self.grad else None
        
        return VectorFunc(vec, grad=grad, _wrap=False)

    def __getitem__(self, key: Union[int, slice]) -> Union[Func, Vector]:
        return self.vec[key]

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

    def __imul__(self, scalar: Scalar) -> 'VectorFunc':
        self = scalar * self
        return self

    def __len__(self) -> int:
        return len(self.vec)
 
    def __repr__(self) -> str:
        seq = [f for f in self]

        string: str
        if isinstance(self.grad, VectorFunc):
            string = f'{seq}, grad=VectorFunc(...)'
        elif isinstance(self.grad, Matrix):
            string = f'{seq}, grad=Matrix(...)'
        else:
            string = f'{seq}, grad={type(self.grad)}'

        return f'VectorFunc({string})'

