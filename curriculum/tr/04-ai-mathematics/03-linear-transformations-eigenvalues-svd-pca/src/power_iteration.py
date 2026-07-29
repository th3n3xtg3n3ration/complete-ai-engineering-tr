"""Power iteration and eigenvalue helpers."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]


@dataclass(frozen=True)
class Eigenpair:
    value: float
    vector: Vector
    iterations: int
    converged: bool


def _validate_square_matrix(matrix: Sequence[Sequence[float]]) -> Matrix:
    if not matrix or not matrix[0]:
        raise ValueError("matrix must not be empty")
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square")
    return [[float(value) for value in row] for row in matrix]


def _dot(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have equal length")
    return sum(a * b for a, b in zip(left, right, strict=True))


def _norm(vector: Sequence[float]) -> float:
    return math.sqrt(_dot(vector, vector))


def _normalize(vector: Sequence[float]) -> Vector:
    norm = _norm(vector)
    if math.isclose(norm, 0.0, abs_tol=1e-15):
        raise ValueError("zero vector cannot be normalized")
    return [value / norm for value in vector]


def _matvec(matrix: Matrix, vector: Sequence[float]) -> Vector:
    if len(matrix[0]) != len(vector):
        raise ValueError("matrix and vector shapes are incompatible")
    return [_dot(row, vector) for row in matrix]


def rayleigh_quotient(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> float:
    values = _validate_square_matrix(matrix)
    if len(vector) != len(values):
        raise ValueError("matrix and vector shapes are incompatible")
    numerator = _dot(vector, _matvec(values, vector))
    denominator = _dot(vector, vector)
    if math.isclose(denominator, 0.0, abs_tol=1e-15):
        raise ValueError("zero vector has no Rayleigh quotient")
    return numerator / denominator


def power_iteration(
    matrix: Sequence[Sequence[float]],
    *,
    initial_vector: Sequence[float] | None = None,
    max_iterations: int = 1_000,
    tolerance: float = 1e-10,
) -> Eigenpair:
    values = _validate_square_matrix(matrix)
    if max_iterations < 1:
        raise ValueError("max_iterations must be positive")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    vector = [1.0] * len(values) if initial_vector is None else [float(v) for v in initial_vector]
    if len(vector) != len(values):
        raise ValueError("initial vector length must match matrix size")
    vector = _normalize(vector)

    previous_value: float | None = None
    for iteration in range(1, max_iterations + 1):
        multiplied = _matvec(values, vector)
        next_vector = _normalize(multiplied)

        # Eigenvectors are sign-ambiguous. Compare both orientations.
        direct_distance = _norm([a - b for a, b in zip(next_vector, vector, strict=True)])
        flipped_distance = _norm([a + b for a, b in zip(next_vector, vector, strict=True)])
        eigenvalue = rayleigh_quotient(values, next_vector)

        value_converged = previous_value is not None and math.isclose(
            eigenvalue,
            previous_value,
            rel_tol=tolerance,
            abs_tol=tolerance,
        )
        vector_converged = min(direct_distance, flipped_distance) <= tolerance
        vector = next_vector

        if value_converged and vector_converged:
            return Eigenpair(eigenvalue, vector, iteration, True)
        previous_value = eigenvalue

    return Eigenpair(rayleigh_quotient(values, vector), vector, max_iterations, False)


def deflate_symmetric(matrix: Sequence[Sequence[float]], eigenpair: Eigenpair) -> Matrix:
    values = _validate_square_matrix(matrix)
    if len(eigenpair.vector) != len(values):
        raise ValueError("eigenvector length must match matrix size")
    unit = _normalize(eigenpair.vector)
    return [
        [
            values[row][column] - eigenpair.value * unit[row] * unit[column]
            for column in range(len(values))
        ]
        for row in range(len(values))
    ]


if __name__ == "__main__":
    sample = [[4.0, 1.0], [1.0, 3.0]]
    result = power_iteration(sample)
    print(result)
