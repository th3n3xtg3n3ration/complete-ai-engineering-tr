"""Linear transformation utilities implemented with the Python standard library."""

from __future__ import annotations

import math
from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]


def _validate_vector(vector: Sequence[float], *, name: str = "vector") -> Vector:
    if not vector:
        raise ValueError(f"{name} must not be empty")
    return [float(value) for value in vector]


def _validate_matrix(matrix: Sequence[Sequence[float]], *, name: str = "matrix") -> Matrix:
    if not matrix or not matrix[0]:
        raise ValueError(f"{name} must not be empty")
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError(f"{name} must be rectangular")
    return [[float(value) for value in row] for row in matrix]


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    left_values = _validate_vector(left, name="left")
    right_values = _validate_vector(right, name="right")
    if len(left_values) != len(right_values):
        raise ValueError("vectors must have equal length")
    return sum(a * b for a, b in zip(left_values, right_values, strict=True))


def l2_norm(vector: Sequence[float]) -> float:
    values = _validate_vector(vector)
    return math.sqrt(sum(value * value for value in values))


def normalize(vector: Sequence[float]) -> Vector:
    values = _validate_vector(vector)
    norm = l2_norm(values)
    if math.isclose(norm, 0.0, abs_tol=1e-15):
        raise ValueError("zero vector cannot be normalized")
    return [value / norm for value in values]


def matrix_vector_multiply(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> Vector:
    matrix_values = _validate_matrix(matrix)
    vector_values = _validate_vector(vector)
    if len(matrix_values[0]) != len(vector_values):
        raise ValueError("matrix columns must match vector length")
    return [dot(row, vector_values) for row in matrix_values]


def transpose(matrix: Sequence[Sequence[float]]) -> Matrix:
    values = _validate_matrix(matrix)
    return [list(column) for column in zip(*values, strict=True)]


def matrix_multiply(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]]) -> Matrix:
    left_values = _validate_matrix(left, name="left")
    right_values = _validate_matrix(right, name="right")
    if len(left_values[0]) != len(right_values):
        raise ValueError("left columns must match right rows")
    right_t = transpose(right_values)
    return [[dot(row, column) for column in right_t] for row in left_values]


def scaling_matrix(scale_x: float, scale_y: float) -> Matrix:
    return [[float(scale_x), 0.0], [0.0, float(scale_y)]]


def rotation_matrix(angle_radians: float) -> Matrix:
    cosine = math.cos(angle_radians)
    sine = math.sin(angle_radians)
    return [[cosine, -sine], [sine, cosine]]


def shear_matrix(factor: float) -> Matrix:
    return [[1.0, float(factor)], [0.0, 1.0]]


def projection(vector: Sequence[float], direction: Sequence[float]) -> Vector:
    values = _validate_vector(vector)
    unit = normalize(direction)
    if len(values) != len(unit):
        raise ValueError("vector and direction must have equal length")
    coefficient = dot(values, unit)
    return [coefficient * value for value in unit]


def projection_matrix(direction: Sequence[float]) -> Matrix:
    unit = normalize(direction)
    return [[left * right for right in unit] for left in unit]


def residual(vector: Sequence[float], projected: Sequence[float]) -> Vector:
    values = _validate_vector(vector)
    projected_values = _validate_vector(projected, name="projected")
    if len(values) != len(projected_values):
        raise ValueError("vectors must have equal length")
    return [value - estimate for value, estimate in zip(values, projected_values, strict=True)]


def is_linear_transformation(
    matrix: Sequence[Sequence[float]],
    first: Sequence[float],
    second: Sequence[float],
    scalar: float,
    *,
    tolerance: float = 1e-9,
) -> bool:
    first_values = _validate_vector(first, name="first")
    second_values = _validate_vector(second, name="second")
    if len(first_values) != len(second_values):
        raise ValueError("vectors must have equal length")

    summed = [a + b for a, b in zip(first_values, second_values, strict=True)]
    transformed_sum = matrix_vector_multiply(matrix, summed)
    separate_sum = [
        a + b
        for a, b in zip(
            matrix_vector_multiply(matrix, first_values),
            matrix_vector_multiply(matrix, second_values),
            strict=True,
        )
    ]

    scaled = [scalar * value for value in first_values]
    transformed_scaled = matrix_vector_multiply(matrix, scaled)
    scaled_transformation = [scalar * value for value in matrix_vector_multiply(matrix, first_values)]

    return all(
        math.isclose(left, right, abs_tol=tolerance, rel_tol=tolerance)
        for left, right in zip(transformed_sum, separate_sum, strict=True)
    ) and all(
        math.isclose(left, right, abs_tol=tolerance, rel_tol=tolerance)
        for left, right in zip(transformed_scaled, scaled_transformation, strict=True)
    )


if __name__ == "__main__":
    point = [2.0, 1.0]
    print("scaled:", matrix_vector_multiply(scaling_matrix(2.0, 0.5), point))
    print("rotated:", matrix_vector_multiply(rotation_matrix(math.pi / 2), point))
    print("projected:", projection([3.0, 4.0], [1.0, 1.0]))
