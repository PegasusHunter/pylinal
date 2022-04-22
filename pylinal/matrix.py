from typing import (
    List,
    Any,
    Union,
    Iterator,
    Tuple,
    Iterable,
    Sequence,
)

from .vector import Vector
from .typedefs import TensorProtocol, Scalar


def vec(v) -> Vector:
    if isinstance(v, Vector):
        return v
    return Vector(v)


def align_dim(self: 'Matrix', *, other: Any) -> Union['Matrix', List]:
    if hasattr(other, 'shape'):
        assert self.shape == other.shape
        return other
    
    rows: int = self.shape[0]
    assert len(other) == rows
    
    vec_len: int = self.shape[1]

    if hasattr(other[-1], '__len__'):
        assert all(len(row) == vec_len for row in other)
    else:
        other = [other for _ in range(rows)]

    return other


class Matrix(TensorProtocol[Scalar]):
    _rows: List[Vector[Scalar]]
    shape: Tuple[int, int]

    def __init__(self, rows: Iterable, *, _wrap: bool = True) -> None:
        if _wrap:
            self._rows = [Vector(row) for row in rows]
        else:
            self._rows = [row for row in rows]

        vec_len = len(self._rows[0])
        if any(vec_len != len(row) for row in self._rows[1:]):
            raise ValueError('All rows in the matrix must have the same len')

        self.shape = len(self._rows), vec_len
        return

    def __iter__(self) -> Iterator[Vector]:
        rows: Iterator[Vector] = (v for v in self._rows)
        return rows
    
    def __reversed__(self) -> Iterator[Vector]:
        return reversed(self)

    def flatten(self) -> Vector:
        elements: Iterator[Scalar] = (el for row in self._rows for el in row)
        return Vector(elements)

    def copy(self) -> 'Matrix':
        rows: Iterator[Vector] = (v.copy() for v in self)
        return Matrix(rows, _wrap=False)
    
    def __add__(self, other: Union['Matrix', Sequence]) -> 'Matrix':
        other = align_dim(self, other=other)

        rows: Iterator[Vector[Scalar]] = (
            row + vec(other_row)
            for row, other_row in zip(self, other)
        )
        return Matrix(rows, _wrap=False)
    
    def __radd__(self, other: Union['Matrix', Sequence]) -> 'Matrix':
        other = align_dim(self, other=other)

        rows: Iterator[Vector[Scalar]] = (
            vec(other_row) + row
            for row, other_row in zip(self, other)
        )
        return Matrix(rows, _wrap=False)

    def __sub__(self, other: Union['Matrix', Sequence]) -> 'Matrix':
        other = align_dim(self, other=other)

        rows: Iterator[Vector[Scalar]] = (
            row - vec(other_row)
            for row, other_row in zip(self, other)
        )
        return Matrix(rows, _wrap=False)

    def __rsub__(self, other: Union['Matrix', Sequence]) -> 'Matrix':
        other = align_dim(self, other=other)

        rows: Iterator[Vector[Scalar]] = (
            vec(other_row) - row
            for row, other_row in zip(self, other)
        )
        return Matrix(rows, _wrap=False)

    def __mul__(self, scalar: Scalar) -> 'Matrix':
        rows: Iterator[Vector[Scalar]] = (row * scalar for row in self)
        return Matrix(rows, _wrap=False)

    def __rmul__(self, scalar: Scalar) -> 'Matrix':
        rows: Iterator[Vector[Scalar]] = (scalar * row for row in self)
        return Matrix(rows, _wrap=False)

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

            elements: Iterator = (row.dot(other) for row in self)
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
            
            other = other.T
            rows: Iterator[Iterator] = (
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
        return Matrix(rows, _wrap=False)

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

    def __getitem__(
        self, 
        key: Union[int, slice, tuple]
    ) -> Union[Scalar, Vector, 'Matrix']:

        if isinstance(key, int):
            return self._rows[key]

        rows: Iterator
        
        if isinstance(key, slice):
            rows = (v for v in self._rows[key])
            return Matrix(rows, _wrap=False)

        first, second = key

        if isinstance(first, int):
            return self._rows[first][second]

        assert isinstance(first, slice)

        if isinstance(second, int):
            elements: Iterator = (v[second] for v in self._rows[first])
            return Vector(elements)

        assert isinstance(second, slice)

        rows = (v[second] for v in self._rows[first])
        return Matrix(rows, _wrap=False)

    def __setitem__(self, index: int, value: Any) -> None:
        value = vec(value)

        try:
            assert len(value) == self.shape[1]

        except AssertionError:
            error = 'All rows in the matrix must have the same len. '\
                    f'Expected dim {self.shape[1]}, got {len(value)}'
            raise ValueError(error)

        self._rows[index] = value
        return

    def __iadd__(self, other: Union['Matrix', Sequence]) -> 'Matrix':
        self = self + other
        return self

    def __isub__(self, other: Union['Matrix', Sequence]) -> 'Matrix':
        self = self - other
        return self

    def __imul__(self, scalar: Scalar) -> 'Matrix':
        self = self * scalar
        return self

    def __repr__(self) -> str:
        space: str = 4 * ' '
        rows: Iterator[str] = (
            space + str(list(vector))
            for vector in self
        )
        rows_str: str = ',\n'.join(rows)
        return f'Matrix([\n{rows_str}\n])'
