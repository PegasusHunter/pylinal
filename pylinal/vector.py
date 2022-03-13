from typing import List, TypeVar, Any, Sequence, Union, Iterator, Generic


T = TypeVar('T')


class Vector(Generic[T]):
    elements: List[T]
    
    def __init__(self, sequence: Union[Iterator[T], Sequence[T]]) -> None:
        self.elements = [el for el in sequence]

    def __add__(self, other: 'Vector') -> 'Vector':
        try:
            assert len(self) == len(other)
        except AssertionError:
            error = 'To __add__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise AssertionError(error)

        return Vector(x + y for x, y in zip(self, other))
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        try:
            assert len(self) == len(other)
        except AssertionError:
            error = 'To __sub__ two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise AssertionError(error)

        return Vector(x - y for x, y in zip(self, other))
    
    def __mul__(self, scalar: T) -> 'Vector':
        return Vector(x*scalar for x in self)
    
    def __rmul__(self, scalar: T) -> 'Vector':
        return Vector(scalar*x for x in self)
    
    def dot(self, other: Union['Vector', Sequence[T]]) -> T:
        try:
            assert len(self) == len(other)
        except AssertionError:
            error = 'To dot two vectors, the dimensions must be the same,'\
                    f' but dim {len(self)} != dim {len(other)}'
            raise AssertionError(error)

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
        return self.elements[index]
    
    def __len__(self) -> int:
        return len(self.elements)
    
    def __iter__(self) -> Iterator[T]:
        return iter(self.elements)
    
    def __reversed__(self) -> Iterator[T]:
        return reversed(self.elements)
    
    def __repr__(self) -> str:
        return f'Vector({self.elements})'


