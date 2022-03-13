from typing import List, TypeVar, Any, Sequence, Union, Iterator, Generic, Tuple
from .vector import Vector


T = TypeVar('T')


class Matrix(Generic[T]):
    rows: List[Vector[T]]
    shape: Tuple[int, int]

    def __init__(self, rows: Union[Iterator, Sequence]) -> None:
        self.rows = [Vector(row) for row in rows]

        vec_len = len(self.rows[0])
        if any((vec_len != len(row) for row in self.rows[1:])):
            raise ValueError('All rows in the matrix must have the same len')

        self.shape = len(self.rows), vec_len

    def __add__(self, other: 'Matrix') -> 'Matrix':
        assert self.shape == other.shape
        
        rows: Iterator[Vector[T]] = (
            row + other_row
            for row, other_row in zip(self.rows, other.rows)
        )
        return Matrix(rows)
    
    def __sub__(self, other: 'Matrix') -> 'Matrix':
        assert self.shape == other.shape

        rows: Iterator[Vector[T]] = (
            row - other_row
            for row, other_row in zip(self.rows, other.rows)
        )
        return Matrix(rows)

    def __mul__(self, scalar: T) -> 'Matrix':
        rows: Iterator[Vector[T]] = (row * scalar for row in self.rows)
        return Matrix(rows)
    
    def __rmul__(self, scalar: T) -> 'Matrix':
        rows: Iterator[Vector[T]] = (scalar * row for row in self.rows)
        return Matrix(rows)

    def matmul(self, other: Union['Matrix', Vector]) -> Union['Matrix', Vector]:
        """Linear transformation"""

        if isinstance(other, Vector):
            try:
                assert self.shape[1] == len(other)
            except AssertionError:
                error = 'To matmul matrix and vector, the second dim of '\
                        'matrix must be equal to the dim of vector, but '\
                        f'dim {self.shape[1]} != dim {len(other)}'
                raise ValueError(error)

            elements: Iterator[T] = (row.dot(other) for row in self.rows)
            return Vector(elements)
        
        elif isinstance(other, Matrix):
            try:
                assert self.shape[1] == other.shape[0]
            except AssertionError:
                dim_0 = self.shape[1]
                dim_1 = other.shape[0]
                error = 'To matmul two matrices, the dimensions must be '\
                        'aligned: (m, n) and (n, k), but matrices have '\
                        f'{self.shape} and {other.shape}, {dim_0} != {dim_1}'
                raise ValueError(error)

            other: Matrix = other.T
            rows: Iterator[Iterator[T]] = (
                (row.dot(col) for col in other)
                for row in self.rows
            )
            return Matrix(rows)
        raise TypeError

    def __matmul__(self, other: Union['Matrix', Vector]) -> Union['Matrix', Vector]:
        """Linear transformation"""

        return self.matmul(other)

    @property
    def T(self) -> 'Matrix':
        """Transpose of a matrix """
        cols: Iterator[Vector] = zip(*self.rows)
        return Matrix(cols)
    
    def __pos__(self) -> 'Matrix':
        return self
    
    def __neg__(self) -> 'Matrix':
        rows: Iterator[Vector] = (-row for row in self.rows)
        return Matrix(rows)
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Matrix):
            return False
        if self.shape != other.shape:
            return False
        for row, other_row in zip(self.rows, other.rows):
            if row != other_row:
                return False
        return True
 
    def __ne__(self, other: Any) -> bool:
        if self == other:
            return False
        return True

    def __getitem__(self, index: int) -> Vector:
        return self.rows[index]

    def __str__(self) -> str:
        space: str = 4*' '
        rows: Iterator[str] = (space + str(row.elements) for row in self.rows)
        rows: str = ',\n'.join(rows)
        return f'Matrix(\n{rows}\n)'

    def __repr__(self) -> str:
        space: str = 4*' '
        rows: str = ',\n'.join(space + repr(row) for row in self.rows)
        return f'Matrix(\n{rows}\n)'


