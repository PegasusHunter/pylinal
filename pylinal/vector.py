from typing import (
    List, 
    Any,
    Union, 
    Iterator,
    Iterable,
)
from .typedefs import Scalar, TensorProtocol


class Vector(TensorProtocol[Scalar]):
    _elements: List[Scalar]
    
    def __init__(self, sequence: Iterable = []) -> None:
        self._elements = [el for el in sequence]
        return

    def copy(self) -> 'Vector':
        return Vector(el for el in self)

    def append(self, scalar: Scalar) -> None:
        self._elements.append(scalar)
        return

    def pop(self) -> Scalar:
        return self._elements.pop()

    def __add__(self, other: Union['Vector', Any]) -> 'Vector':
        try:
            assert len(self) == len(other)

        except TypeError: 
            error = f'unsupported operand type(s) for +: {type(self)} '\
                    f'and {type(other)}'
            raise TypeError(error)

        except AssertionError:
            error = 'To __add__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise ValueError(error)

        return Vector(x + y for x, y in zip(self, other))

    def __radd__(self, other: Union['Vector', Any]) -> 'Vector':
        try:
            assert len(self) == len(other)
        except TypeError: 
            error = f'unsupported operand type(s) for +: {type(other)} '\
                    f'and {type(self)}'
            raise TypeError(error)
        except AssertionError:
            error = 'To __add__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(other)} != dim {len(self)}'
            raise ValueError(error)

        return Vector(y + x for x, y in zip(self, other))

    def __sub__(self, other: Union['Vector', Any]) -> 'Vector':
        try:
            assert len(self) == len(other)
        except TypeError:
            error = f'unsupported operand type(s) for -: {type(self)} '\
                    f'and {type(other)}'
            raise TypeError(error)
        except AssertionError:
            error = 'To __sub__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise ValueError(error)

        return Vector(x - y for x, y in zip(self, other))
    
    def __rsub__(self, other: Union['Vector', Any]) -> 'Vector':
        try:
            assert len(self) == len(other)
        except TypeError:
            error = f'unsupported operand type(s) for -: {type(other)} '\
                    f'and {type(self)}'
            raise TypeError(error)
        except AssertionError:
            error = 'To __rsub__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(other)} != dim {len(self)}'
            raise ValueError(error)

        return Vector(y - x for x, y in zip(self, other))

    def __mul__(self, scalar: Scalar) -> 'Vector':
        return Vector(x * scalar for x in self)
    
    def __rmul__(self, scalar: Scalar) -> 'Vector':
        return Vector(scalar * x for x in self)

    def dot(self, other: Union['Vector', Any]) -> Scalar:
        try:
            assert len(self) == len(other)
        except TypeError:
            error = f'unsupported operand type(s) for "dot": {type(other)}'
            raise TypeError(error)
        except AssertionError:
            error = 'To "dot" two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise ValueError(error)

        return sum(x*y for x, y in zip(self, other))  # type: ignore
    
    def __pos__(self) -> 'Vector':
        return self
    
    def __neg__(self) -> 'Vector':
        v: Vector = Vector(-el for el in self)
        return v

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vector):
            return False
        if len(self) != len(other):
            return False
        
        for x, y in zip(self, other):
            if x != y:
                return False
        
        return True

    def __ne__(self, other: Any) -> bool:
        if self == other:
            return False
        return True

    def __getitem__(self, key: Union[int, slice]) -> Union[Scalar, 'Vector']:
        item: Union[Scalar, List] = self._elements[key]

        if isinstance(item, list):
            v: Vector = Vector()
            v._elements = item
            return v

        return item

    def __setitem__(self, index: int, value: Any) -> None:
        self._elements[index] = value
        return
    
    def __len__(self) -> int:
        return len(self._elements)
    
    def __iter__(self) -> Iterator[Scalar]:
        return iter(self._elements)
    
    def __reversed__(self) -> Iterator[Scalar]:
        return reversed(self._elements)

    def __iadd__(self, other: Union['Vector', Any]) -> 'Vector':
        self = self + other
        return self

    def __isub__(self, other: Union['Vector', Any]) -> 'Vector':
        self = self - other
        return self

    def __imul__(self, scalar: Scalar) -> 'Vector':
        self = self * scalar
        return self

    def __repr__(self) -> str:
        return f'Vector({self._elements})'

