from typing import List, TypeVar, Any, Sequence, Union, Iterator, Generic


T = TypeVar('T')


class Vector(Generic[T]):
    _elements: List[T]
    
    def __init__(self, sequence: Union[Iterator[T], Sequence[T]]) -> None:
        self._elements = [el for el in sequence]
        return

    def copy(self) -> 'Vector':
        return Vector(el for el in self)

    def __add__(self, other: Union['Vector', Any]) -> 'Vector':
        other = Vector(other)

        try:
            assert len(self) == len(other)
        except AssertionError:
            error = 'To __add__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise ValueError(error)

        return Vector(x + y for x, y in zip(self, other))
    
    def __sub__(self, other: Union['Vector', Any]) -> 'Vector':
        other = Vector(other)

        try:
            assert len(self) == len(other)
        except AssertionError:
            error = 'To __sub__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise ValueError(error)

        return Vector(x - y for x, y in zip(self, other))
    
    def __mul__(self, scalar: T) -> 'Vector':
        return Vector(x*scalar for x in self)
    
    def __rmul__(self, scalar: T) -> 'Vector':
        return Vector(scalar*x for x in self)

    def dot(self, other: Union['Vector', Any]) -> T:
        other = Vector(other)

        try:
            assert len(self) == len(other)
        except AssertionError:
            error = 'To dot two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise ValueError(error)

        return sum(x*y for x, y in zip(self, other))
    
    def __pos__(self) -> 'Vector':
        return self
    
    def __neg__(self) -> 'Vector':
        v = Vector(-el for el in self)
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

    def __getitem__(self, index: int) -> T:
        return self._elements[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self._elements[index] = value
        return
    
    def __len__(self) -> int:
        return len(self._elements)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._elements)
    
    def __reversed__(self) -> Iterator[T]:
        return reversed(self._elements)

    def __iadd__(self, other: Union['Vector', Any]) -> 'Vector':
        self = self + Vector(other)
        return self

    def __isub__(self, other: Union['Vector', Any]) -> 'Vector':
        self = self - Vector(other)
        return self

    def __imul__(self, scalar: T) -> 'Vector':
        self = scalar * self
        return self

    def __repr__(self) -> str:
        return f'Vector({self._elements})'

