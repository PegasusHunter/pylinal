from typing import Protocol, Union, TypeVar


T = TypeVar('T', bound=Union[int, float, complex])


class TensorProtocol(Protocol[T]):

    def __add__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __mult__(self, other):
        ...

    def __rmult__(self, other):
        ...


