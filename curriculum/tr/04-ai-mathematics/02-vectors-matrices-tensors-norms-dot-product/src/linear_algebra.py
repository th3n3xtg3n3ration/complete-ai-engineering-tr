"""Small, dependency-free linear algebra utilities for learning purposes."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypeAlias

Number: TypeAlias = int | float
Vector: TypeAlias = Sequence[Number]
Matrix: TypeAlias = Sequence[Sequence[Number]]
TensorData: TypeAlias = Number | Sequence["TensorData"]


def _as_finite_float(value: Number, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must contain only real numbers")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must contain only finite numbers")
    return result


def _validated_vector(vector: Vector, *, name: str = "vector", allow_empty: bool = False) -> list[float]:
    values = [_as_finite_float(value, name=name) for value in vector]
    if not allow_empty and not values:
        raise ValueError(f"{name} must not be empty")
    return values


def _validated_matrix(matrix: Matrix, *, name: str = "matrix") -> list[list[float]]:
    rows = [_validated_vector(row, name=f"{name} row") for row in matrix]
    if not rows:
        raise ValueError(f"{name} must not be empty")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError(f"{name} must be rectangular")
    return rows


def vector_add(left: Vector, right: Vector) -> list[float]:
    """Return element-wise vector addition."""
    a = _validated_vector(left, name="left")
    b = _validated_vector(right, name="right")
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    return [x + y for x, y in zip(a, b, strict=True)]


def vector_subtract(left: Vector, right: Vector) -> list[float]:
    """Return element-wise vector subtraction."""
    a = _validated_vector(left, name="left")
    b = _validated_vector(right, name="right")
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    return [x - y for x, y in zip(a, b, strict=True)]


def scalar_multiply(scalar: Number, vector: Vector) -> list[float]:
    """Multiply every vector component by a scalar."""
    factor = _as_finite_float(scalar, name="scalar")
    values = _validated_vector(vector)
    return [factor * value for value in values]


def dot(left: Vector, right: Vector) -> float:
    """Return the dot product of two equally sized vectors."""
    a = _validated_vector(left, name="left")
    b = _validated_vector(right, name="right")
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    return math.fsum(x * y for x, y in zip(a, b, strict=True))


def outer_product(left: Vector, right: Vector) -> list[list[float]]:
    """Return the outer product of two vectors."""
    a = _validated_vector(left, name="left")
    b = _validated_vector(right, name="right")
    return [[x * y for y in b] for x in a]


def l1_norm(vector: Vector) -> float:
    values = _validated_vector(vector)
    return math.fsum(abs(value) for value in values)


def l2_norm(vector: Vector) -> float:
    values = _validated_vector(vector)
    return math.sqrt(math.fsum(value * value for value in values))


def infinity_norm(vector: Vector) -> float:
    values = _validated_vector(vector)
    return max(abs(value) for value in values)


def normalize(vector: Vector, *, epsilon: float = 1e-12) -> list[float]:
    """Return an L2-normalized vector and reject near-zero magnitude."""
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    values = _validated_vector(vector)
    magnitude = l2_norm(values)
    if magnitude <= epsilon:
        raise ValueError("cannot normalize a zero or near-zero vector")
    return [value / magnitude for value in values]


def euclidean_distance(left: Vector, right: Vector) -> float:
    return l2_norm(vector_subtract(left, right))


def cosine_similarity(left: Vector, right: Vector, *, epsilon: float = 1e-12) -> float:
    """Return cosine similarity in the interval [-1, 1]."""
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    a = _validated_vector(left, name="left")
    b = _validated_vector(right, name="right")
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    denominator = l2_norm(a) * l2_norm(b)
    if denominator <= epsilon:
        raise ValueError("cosine similarity is undefined for zero vectors")
    value = dot(a, b) / denominator
    return max(-1.0, min(1.0, value))


def transpose(matrix: Matrix) -> list[list[float]]:
    rows = _validated_matrix(matrix)
    return [list(column) for column in zip(*rows, strict=True)]


def matrix_add(left: Matrix, right: Matrix) -> list[list[float]]:
    a = _validated_matrix(left, name="left")
    b = _validated_matrix(right, name="right")
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("matrices must have the same shape")
    return [
        [x + y for x, y in zip(row_a, row_b, strict=True)]
        for row_a, row_b in zip(a, b, strict=True)
    ]


def matrix_vector_multiply(matrix: Matrix, vector: Vector) -> list[float]:
    rows = _validated_matrix(matrix)
    values = _validated_vector(vector)
    if len(rows[0]) != len(values):
        raise ValueError("matrix column count must equal vector length")
    return [dot(row, values) for row in rows]


def matrix_multiply(left: Matrix, right: Matrix) -> list[list[float]]:
    a = _validated_matrix(left, name="left")
    b = _validated_matrix(right, name="right")
    if len(a[0]) != len(b):
        raise ValueError("left columns must equal right rows")
    columns = transpose(b)
    return [[dot(row, column) for column in columns] for row in a]


def add_bias(matrix: Matrix, bias: Vector) -> list[list[float]]:
    """Add one feature-sized bias vector to each matrix row."""
    rows = _validated_matrix(matrix)
    values = _validated_vector(bias, name="bias")
    if len(rows[0]) != len(values):
        raise ValueError("bias length must equal matrix column count")
    return [vector_add(row, values) for row in rows]


def mean_vector(vectors: Matrix) -> list[float]:
    rows = _validated_matrix(vectors, name="vectors")
    count = len(rows)
    return [math.fsum(column) / count for column in zip(*rows, strict=True)]


def tensor_shape(data: TensorData) -> tuple[int, ...]:
    """Infer a rectangular nested sequence shape and reject ragged data."""
    if isinstance(data, (list, tuple)):
        if not data:
            return (0,)
        child_shapes = [tensor_shape(item) for item in data]
        first = child_shapes[0]
        if any(shape != first for shape in child_shapes[1:]):
            raise ValueError("tensor data must be rectangular")
        return (len(data),) + first
    _as_finite_float(data, name="tensor")
    return ()


def flatten_tensor(data: TensorData) -> list[float]:
    """Flatten rectangular tensor data in row-major order."""
    tensor_shape(data)
    if isinstance(data, (list, tuple)):
        flattened: list[float] = []
        for item in data:
            flattened.extend(flatten_tensor(item))
        return flattened
    return [_as_finite_float(data, name="tensor")]


def reshape(values: Vector, shape: Sequence[int]) -> TensorData:
    """Reshape a flat vector into a rectangular nested list."""
    flat = _validated_vector(values, name="values", allow_empty=True)
    dimensions = list(shape)
    if not dimensions:
        if len(flat) != 1:
            raise ValueError("scalar shape requires exactly one value")
        return flat[0]
    if any(isinstance(size, bool) or not isinstance(size, int) or size < 0 for size in dimensions):
        raise ValueError("shape dimensions must be non-negative integers")
    required = math.prod(dimensions)
    if required != len(flat):
        raise ValueError("shape element count must match the number of values")

    iterator = iter(flat)

    def build(axis: int) -> TensorData:
        size = dimensions[axis]
        if axis == len(dimensions) - 1:
            return [next(iterator) for _ in range(size)]
        return [build(axis + 1) for _ in range(size)]

    return build(0)


def _demo() -> None:
    vector_a = [1.0, 2.0, 3.0]
    vector_b = [4.0, 5.0, 6.0]
    matrix_a = [[1.0, 2.0], [3.0, 4.0]]
    matrix_b = [[2.0, 0.0], [1.0, 2.0]]

    print("dot:", dot(vector_a, vector_b))
    print("cosine similarity:", round(cosine_similarity(vector_a, vector_b), 6))
    print("normalized:", [round(value, 6) for value in normalize(vector_a)])
    print("matrix multiplication:", matrix_multiply(matrix_a, matrix_b))
    print("tensor shape:", tensor_shape([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))


if __name__ == "__main__":
    _demo()
