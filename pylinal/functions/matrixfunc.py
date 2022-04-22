from typing import (
    Tuple,
    Union,
    Iterator,
    Iterable,
    Any,
    Sequence,
)

from ..matrix import Matrix, Vector
from .func import Func
from .vectorfunc import VectorFunc


class MatrixFunc(Matrix):
    matrix: Matrix[Func]

    def __init__(self, rows: Iterable, *, _wrap: bool = True) -> None:
        if _wrap:
            rows = ((Func(f) for f in row) for row in rows)
            self.matrix = Matrix(rows)
        else:
            self.matrix = rows  # type: ignore
        return

    def __call__(self, *args, **kwargs) -> Matrix:
        result: Matrix = Matrix(
            (f(*args, **kwargs) for f in row)
            for row in self
        )
        return result

    def flatten(self) -> VectorFunc:  # type: ignore[override]
        v: Vector[Func] = Vector(el for row in self for el in row)
        return VectorFunc(v, _wrap=False)

    def copy(self) -> 'MatrixFunc':
        return MatrixFunc(self.matrix.copy(), _wrap=False)        

    @property
    def shape(self) -> Tuple[int, int]:  # type: ignore[override]
        return self.matrix.shape

    @property
    def T(self) -> 'MatrixFunc':
        return MatrixFunc(self.matrix.T, _wrap=False)

    def __add__(self, other: Union['MatrixFunc', Matrix, Sequence]) -> 'MatrixFunc':
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        
        matrix: Matrix = self.matrix + other_matrix
        return MatrixFunc(matrix, _wrap=False)

    def __radd__(self, other: Union['MatrixFunc', Matrix, Sequence]) -> 'MatrixFunc':
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        
        matrix: Matrix = other_matrix + self.matrix
        return MatrixFunc(matrix, _wrap=False)

    def __sub__(self, other: Union['MatrixFunc', Matrix]) -> 'MatrixFunc':  # type: ignore[override]
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        
        matrix: Matrix = self.matrix - other_matrix
        return MatrixFunc(matrix, _wrap=False)

    def __rsub__(self, other: Union['MatrixFunc', Matrix]) -> 'MatrixFunc':  # type: ignore[override]
        other_matrix = other
        if isinstance(other, MatrixFunc):
            other_matrix = other.matrix
        
        matrix: Matrix = other_matrix - self.matrix
        return MatrixFunc(matrix, _wrap=False)

    def __mul__(self, scalar: Func) -> 'MatrixFunc':
        matrix: Matrix = self.matrix * scalar
        return MatrixFunc(matrix, _wrap=False)

    def __rmul__(self, scalar: Func) -> 'MatrixFunc':
        matrix: Matrix[Func] = self.matrix.__rmul__(scalar)
        return MatrixFunc(matrix, _wrap=False)

    def __matmul__(  # type: ignore[override]
        self,
        other: Union['MatrixFunc', Matrix, Vector]
    ) -> Union['MatrixFunc', VectorFunc]:
        
        result: Union[Matrix, Vector]

        if isinstance(other, MatrixFunc):
            result = self.matrix @ other.matrix
            return MatrixFunc(result, _wrap=False)
        
        else:
            result = self.matrix @ other
            if isinstance(result, Vector):
                return VectorFunc(result, _wrap=False)
            else:
                return MatrixFunc(result, _wrap=False)

    def __pos__(self) -> 'MatrixFunc':
        return self

    def __neg__(self) -> 'MatrixFunc':
        matrix: Matrix[Func] = -self.matrix
        return MatrixFunc(matrix, _wrap=False)

    def __iadd__(self, other: Union[Matrix, 'MatrixFunc', Sequence]) -> 'MatrixFunc':  # type: ignore[override]
        self = self + other
        return self

    def __isub__(self, other: Union[Matrix, 'MatrixFunc']) -> 'MatrixFunc':  # type: ignore[override]
        self = self - other
        return self

    def __imul__(self, scalar: Func) -> 'MatrixFunc':  # type: ignore[override]
        self = self.__mul__(scalar)
        return self

    def __iter__(self) -> Iterator[VectorFunc]:  # type: ignore[override]
        rows: Iterator[VectorFunc] = (
            VectorFunc(v, _wrap=False)
            for v in self.matrix
        )
        return rows

    def __getitem__(  # type: ignore[override]
        self,
        key: Union[int, slice, tuple]
    ) -> Union[Func, VectorFunc, 'MatrixFunc']:
        
        item: Union[Func, Vector, Matrix] = self.matrix[key]

        if isinstance(item, Matrix):
            return MatrixFunc(item, _wrap=False)

        if isinstance(item, Vector):
            return VectorFunc(item, _wrap=False)

        return item
        
    def __repr__(self) -> str:
        space: str = 4 * ' '
        rows: Iterator[str] = (
            space + str(list(vector))
            for vector in self
        )
        rows_str: str = ',\n'.join(rows)
        return f'MatrixFunc([\n{rows_str}\n])'
    
    def __setitem__(self, index: Any, value: Any):
        error = '"MatrixFunc" object has no attribute "__setitem__"'
        raise AttributeError(error)
