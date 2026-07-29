"""Small PCA implementation for educational use, without third-party packages."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class PCAResult:
    mean: Vector
    components: Matrix
    eigenvalues: Vector
    explained_variance_ratio: Vector


def _validate_data(data: Sequence[Sequence[float]]) -> Matrix:
    if len(data) < 2:
        raise ValueError("data must contain at least two rows")
    if not data[0]:
        raise ValueError("data must contain at least one feature")
    width = len(data[0])
    if any(len(row) != width for row in data):
        raise ValueError("data must be rectangular")
    return [[float(value) for value in row] for row in data]


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


def feature_means(data: Sequence[Sequence[float]]) -> Vector:
    values = _validate_data(data)
    return [sum(row[column] for row in values) / len(values) for column in range(len(values[0]))]


def center_data(data: Sequence[Sequence[float]], mean: Sequence[float] | None = None) -> tuple[Matrix, Vector]:
    values = _validate_data(data)
    means = feature_means(values) if mean is None else [float(value) for value in mean]
    if len(means) != len(values[0]):
        raise ValueError("mean length must match feature count")
    return [[value - means[index] for index, value in enumerate(row)] for row in values], means


def covariance_matrix(data: Sequence[Sequence[float]]) -> Matrix:
    centered, _ = center_data(data)
    sample_count = len(centered)
    feature_count = len(centered[0])
    return [
        [
            sum(row[i] * row[j] for row in centered) / (sample_count - 1)
            for j in range(feature_count)
        ]
        for i in range(feature_count)
    ]


def _matvec(matrix: Matrix, vector: Sequence[float]) -> Vector:
    if len(matrix[0]) != len(vector):
        raise ValueError("matrix and vector shapes are incompatible")
    return [_dot(row, vector) for row in matrix]


def _rayleigh(matrix: Matrix, vector: Sequence[float]) -> float:
    denominator = _dot(vector, vector)
    if math.isclose(denominator, 0.0, abs_tol=1e-15):
        raise ValueError("zero vector is invalid")
    return _dot(vector, _matvec(matrix, vector)) / denominator


def _dominant_eigenpair(
    matrix: Matrix,
    *,
    max_iterations: int = 2_000,
    tolerance: float = 1e-10,
) -> tuple[float, Vector]:
    vector = _normalize([1.0 + index / 10.0 for index in range(len(matrix))])
    previous_value: float | None = None

    for _ in range(max_iterations):
        multiplied = _matvec(matrix, vector)
        norm = _norm(multiplied)
        if math.isclose(norm, 0.0, abs_tol=1e-14):
            return 0.0, vector
        next_vector = [value / norm for value in multiplied]
        value = _rayleigh(matrix, next_vector)
        if previous_value is not None and math.isclose(value, previous_value, rel_tol=tolerance, abs_tol=tolerance):
            vector = next_vector
            break
        vector = next_vector
        previous_value = value

    return max(_rayleigh(matrix, vector), 0.0), vector


def _deflate(matrix: Matrix, eigenvalue: float, eigenvector: Sequence[float]) -> Matrix:
    unit = _normalize(eigenvector)
    return [
        [matrix[i][j] - eigenvalue * unit[i] * unit[j] for j in range(len(matrix))]
        for i in range(len(matrix))
    ]


def fit_pca(data: Sequence[Sequence[float]], n_components: int) -> PCAResult:
    values = _validate_data(data)
    feature_count = len(values[0])
    if not 1 <= n_components <= feature_count:
        raise ValueError("n_components must be between 1 and the feature count")

    centered, mean = center_data(values)
    covariance = covariance_matrix(values)
    working = [row[:] for row in covariance]

    eigenvalues: Vector = []
    components: Matrix = []
    for _ in range(n_components):
        eigenvalue, eigenvector = _dominant_eigenpair(working)
        eigenvalues.append(eigenvalue)
        components.append(eigenvector)
        working = _deflate(working, eigenvalue, eigenvector)

    total_variance = sum(covariance[i][i] for i in range(feature_count))
    ratios = [value / total_variance if total_variance > 0 else 0.0 for value in eigenvalues]
    return PCAResult(mean, components, eigenvalues, ratios)


def transform(data: Sequence[Sequence[float]], model: PCAResult) -> Matrix:
    centered, _ = center_data(data, model.mean)
    return [[_dot(row, component) for component in model.components] for row in centered]


def inverse_transform(projected: Sequence[Sequence[float]], model: PCAResult) -> Matrix:
    if not projected:
        raise ValueError("projected data must not be empty")
    if any(len(row) != len(model.components) for row in projected):
        raise ValueError("projected width must match component count")

    reconstructed: Matrix = []
    for row in projected:
        restored = model.mean[:]
        for score, component in zip(row, model.components, strict=True):
            restored = [value + float(score) * loading for value, loading in zip(restored, component, strict=True)]
        reconstructed.append(restored)
    return reconstructed


def reconstruction_error(original: Sequence[Sequence[float]], reconstructed: Sequence[Sequence[float]]) -> float:
    original_values = _validate_data(original)
    reconstructed_values = _validate_data(reconstructed)
    if len(original_values) != len(reconstructed_values) or len(original_values[0]) != len(reconstructed_values[0]):
        raise ValueError("datasets must have identical shapes")
    squared_errors = [
        (actual - estimate) ** 2
        for actual_row, estimate_row in zip(original_values, reconstructed_values, strict=True)
        for actual, estimate in zip(actual_row, estimate_row, strict=True)
    ]
    return sum(squared_errors) / len(squared_errors)


if __name__ == "__main__":
    sample = [
        [2.5, 2.4], [0.5, 0.7], [2.2, 2.9], [1.9, 2.2], [3.1, 3.0],
        [2.3, 2.7], [2.0, 1.6], [1.0, 1.1], [1.5, 1.6], [1.1, 0.9],
    ]
    model = fit_pca(sample, 1)
    reduced = transform(sample, model)
    restored = inverse_transform(reduced, model)
    print("explained variance:", model.explained_variance_ratio)
    print("reconstruction error:", reconstruction_error(sample, restored))
