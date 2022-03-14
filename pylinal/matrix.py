from typing import List, TypeVar, Any, Sequence, Union, Iterator, Generic, Tuple
from .vector import Vector


T = TypeVar('T')


class Matrix(Generic[T]):
    _rows: List[Vector[T]]
    shape: Tuple[int, int]

    def __init__(self, rows: Union[Iterator, Sequence]) -> None:
        self._rows = [Vector(row) for row in rows]

        vec_len = len(self._rows[0])
        if any((vec_len != len(row) for row in self._rows[1:])):
            raise ValueError('All rows in the matrix must have the same len')

        self.shape = len(self._rows), vec_len
        return

    def __iter__(self) -> Iterator[Vector]:
        rows: Iterator[Vector] = (v for v in self._rows)
        return rows

    def copy(self) -> 'Matrix':
        rows: Iterator[Vector] = (v for v in self)
        return Matrix(rows)

    def __add__(self, other: 'Matrix') -> 'Matrix':
        assert self.shape == other.shape

        rows: Iterator[Vector[T]] = (
            row + other_row
            for row, other_row in zip(self, other)
        )
        return Matrix(rows)

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        assert self.shape == other.shape

        rows: Iterator[Vector[T]] = (
            row - other_row
            for row, other_row in zip(self, other)
        )
        return Matrix(rows)

    def __mul__(self, scalar: T) -> 'Matrix':
        rows: Iterator[Vector[T]] = (row * scalar for row in self)
        return Matrix(rows)

    def __rmul__(self, scalar: T) -> 'Matrix':
        rows: Iterator[Vector[T]] = (scalar * row for row in self)
        return Matrix(rows)

    def matmul(self, other: Union['Matrix', Vector]) -> Union['Matrix', Vector]:
        """Linear transformation"""

        if isinstance(other, Vector):
            try:
                assert self.shape[1] == len(other)
            except AssertionError:
                error = 'To matmul matrix and vector, the second dim of ' \
                        'matrix must be equal to the dim of vector, but ' \
                        f'dim {self.shape[1]} != dim {len(other)}'
                raise ValueError(error)

            elements: Iterator[T] = (row.dot(other) for row in self)
            return Vector(elements)

        elif isinstance(other, Matrix):
            try:
                assert self.shape[1] == other.shape[0]
            except AssertionError:
                dim_0 = self.shape[1]
                dim_1 = other.shape[0]
                error = 'To matmul two matrices, the dimensions must be ' \
                        'aligned: (m, n) and (n, k), but matrices have ' \
                        f'{self.shape} and {other.shape}, {dim_0} != {dim_1}'
                raise ValueError(error)

            other: Matrix = other.T
            rows: Iterator[Iterator[T]] = (
                (row.dot(col) for col in other)
                for row in self
            )
            return Matrix(rows)
        raise TypeError

    def __matmul__(self, other: Union['Matrix', Vector]) -> Union['Matrix', Vector]:
        """Linear transformation"""

        return self.matmul(other)

    @property
    def T(self) -> 'Matrix':
        """Transpose of a matrix """
        cols: Iterator = zip(*self._rows)
        return Matrix(cols)

    def __pos__(self) -> 'Matrix':
        return self

    def __neg__(self) -> 'Matrix':
        rows: Iterator[Vector] = (-row for row in self)
        return Matrix(rows)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Matrix):
            return False
        if self.shape != other.shape:
            return False
        for row, other_row in zip(self, other):
            if row != other_row:
                return False
        return True

    def __ne__(self, other: Any) -> bool:
        if self == other:
            return False
        return True

    def __getitem__(self, index: int) -> Vector:
        return self._rows[index]

    def __setitem__(self, index: int, value: Any) -> None:
        value = Vector(value)

        try:
            assert len(value) == self.shape[1]
        except AssertionError:
            error = 'All rows in the matrix must have the same len. '\
                    f'Expected dim {self.shape[1]}, got {len(value)}'
            raise ValueError(error)

        self._rows[index] = value
        return

    def __iadd__(self, other: Union['Matrix', Any]) -> 'Matrix':
        self = self + Matrix(other)
        return self

    def __isub__(self, other: Union['Matrix', Any]) -> 'Matrix':
        self = self - Matrix(other)
        return self

    def __imul__(self, scalar: T) -> 'Matrix':
        self = scalar * self
        return self

    def __repr__(self) -> str:
        space: str = 4 * ' '
        rows: Iterator[str] = (
            space + str(list(vector))
            for vector in self
        )
        rows: str = ',\n'.join(rows)
        return f'Matrix([\n{rows}\n])'

