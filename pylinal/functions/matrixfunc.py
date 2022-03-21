from typing import (
    TypeVar,
    Tuple,
    Union,
    Iterator,
    Sequence,
)

from ..matrix import Matrix, Vector
from .func import Func
from .vectorfunc import VectorFunc


T = TypeVar('T')


class MatrixFunc(Matrix):
    matrix: Matrix[Func]

    def __init__(
        self,
        rows: Union[Iterator, Sequence, Matrix],
        *,
        __wrap: bool = True,
    ) -> None:
        if __wrap:
            rows = ((Func(f) for f in row) for row in rows)
            self.matrix = Matrix(rows)
        else:
            self.matrix = rows
        return

    def __call__(self, *args, **kwargs) -> Matrix:
        result = Matrix(
            (f(*args, **kwargs) for f in row)
            for row in self
        )
        return result

    @property
    def shape(self) -> Tuple[int, int]:
        return self.matrix.shape

    @property
    def T(self) -> 'MatrixFunc':
        return MatrixFunc(self.matrix.T, _MatrixFunc__wrap=False)

    def __add__(self, other: Union['MatrixFunc', Matrix]) -> 'MatrixFunc':
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        matrix: Matrix = self.matrix + other_matrix
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __radd__(self, other: Union['MatrixFunc', Matrix]) -> 'MatrixFunc':
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        matrix: Matrix = other_matrix + self.matrix
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __sub__(self, other: Union['MatrixFunc', Matrix]) -> 'MatrixFunc':
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        matrix: Matrix = self.matrix - other_matrix
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __rsub__(self, other: Union['MatrixFunc', Matrix]) -> 'MatrixFunc':
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        matrix: Matrix = other_matrix - self.matrix
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __mul__(self, scalar: T) -> 'MatrixFunc':
        matrix: Matrix = self.matrix * scalar
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __rmul__(self, scalar: T) -> 'MatrixFunc':
        matrix: Matrix = scalar * self.matrix
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __matmul__(
        self,
        other: Union['MatrixFunc', Matrix, Vector]
    ) -> Union['MatrixFunc', VectorFunc]:

        if isinstance(other, MatrixFunc):
            result: Matrix = self.matrix @ other.matrix
            return MatrixFunc(result, _MatrixFunc__wrap=False)
        else:
            result: Union[Vector, Matrix] = self.matrix @ other
            if isinstance(result, Vector):
                return VectorFunc(result, _VectorFunc__wrap=False)
            else:
                return MatrixFunc(result, _MatrixFunc__wrap=False)

    def __pos__(self) -> 'MatrixFunc':
        return self

    def __neg__(self) -> 'MatrixFunc':
        matrix: Matrix[Func] = -self.matrix
        return MatrixFunc(matrix, _MatrixFunc__wrap=False)

    def __iadd__(self, other: 'MatrixFunc') -> 'MatrixFunc':
        self = self + other
        return self

    def __isub__(self, other: 'MatrixFunc') -> 'MatrixFunc':
        self = self - other
        return self

    def __imul__(self, scalar: T) -> 'MatrixFunc':
        self = scalar * self
        return self

    def __iter__(self) -> Iterator[VectorFunc]:
        rows: Iterator[VectorFunc] = (
            VectorFunc(v, _VectorFunc__wrap=False)
            for v in self.matrix
        )
        return rows

    def __reversed__(self) -> Iterator[VectorFunc]:
        return reversed(iter(self))

    def __getitem__(self, index: int) -> VectorFunc:
        return VectorFunc(self.matrix[index], _VectorFunc__wrap=False)

    def __repr__(self) -> str:
        space: str = 4 * ' '
        rows: Iterator[str] = (
            space + str(list(vector))
            for vector in self
        )
        rows: str = ',\n'.join(rows)
        return f'MatrixFunc([\n{rows}\n])'

