from typing import Protocol, TypeVar, Generic


class Ring(Protocol):

    def __radd__(self, other):
        ...

    def __add__(self, other):
        ...

    def __rsub__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __rmul__(self, other):
        ...

    def __mul__(self, other):
        ...

    def __neg__(self):
        ...


Scalar = TypeVar('Scalar', bound=Ring)


class TensorProtocol(Generic[Scalar]):

    def __add__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __mul__(self, other):
        ...

    def __rmul__(self, other):
        ...

