"""Mathematical utilities for SVM kernels, margins, and hinge loss."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatMatrix = NDArray[np.float64]


def _as_2d_float(array: ArrayLike, *, name: str) -> FloatMatrix:
    result = np.atleast_2d(np.asarray(array, dtype=float))
    if result.ndim != 2:
        raise ValueError(f"{name} must be convertible to a 2D array")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    return result


def _validate_pair(x: ArrayLike, z: ArrayLike) -> tuple[FloatMatrix, FloatMatrix]:
    x_arr = _as_2d_float(x, name="x")
    z_arr = _as_2d_float(z, name="z")
    if x_arr.shape[1] != z_arr.shape[1]:
        raise ValueError("x and z must have the same number of features")
    return x_arr, z_arr


def linear_kernel(x: ArrayLike, z: ArrayLike) -> FloatMatrix:
    """Return the pairwise linear Gram matrix ``x @ z.T``."""
    x_arr, z_arr = _validate_pair(x, z)
    return x_arr @ z_arr.T


def polynomial_kernel(
    x: ArrayLike,
    z: ArrayLike,
    *,
    degree: int = 3,
    gamma: float = 1.0,
    coef0: float = 1.0,
) -> FloatMatrix:
    """Return ``(gamma * <x, z> + coef0) ** degree`` pairwise."""
    if degree < 1:
        raise ValueError("degree must be at least 1")
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    if not np.isfinite(coef0):
        raise ValueError("coef0 must be finite")
    return (gamma * linear_kernel(x, z) + coef0) ** degree


def rbf_kernel(
    x: ArrayLike,
    z: ArrayLike,
    *,
    gamma: float = 1.0,
) -> FloatMatrix:
    """Return the pairwise radial basis function kernel matrix."""
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    x_arr, z_arr = _validate_pair(x, z)
    squared_distances = (
        np.sum(x_arr**2, axis=1)[:, None]
        + np.sum(z_arr**2, axis=1)[None, :]
        - 2.0 * x_arr @ z_arr.T
    )
    return np.exp(-gamma * np.maximum(squared_distances, 0.0))


def sigmoid_kernel(
    x: ArrayLike,
    z: ArrayLike,
    *,
    gamma: float = 1.0,
    coef0: float = 0.0,
) -> FloatMatrix:
    """Return the pairwise hyperbolic-tangent kernel matrix."""
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    if not np.isfinite(coef0):
        raise ValueError("coef0 must be finite")
    return np.tanh(gamma * linear_kernel(x, z) + coef0)


def gram_matrix(
    x: ArrayLike,
    kernel: Callable[..., FloatMatrix],
    **kernel_kwargs: float | int,
) -> FloatMatrix:
    """Return a symmetric Gram matrix for ``x`` using ``kernel``."""
    x_arr = _as_2d_float(x, name="x")
    matrix = np.asarray(kernel(x_arr, x_arr, **kernel_kwargs), dtype=float)
    expected_shape = (x_arr.shape[0], x_arr.shape[0])
    if matrix.shape != expected_shape:
        raise ValueError(f"kernel returned {matrix.shape}, expected {expected_shape}")
    return matrix


def is_positive_semidefinite(
    matrix: ArrayLike,
    *,
    tolerance: float = 1e-10,
) -> bool:
    """Check whether a symmetric matrix is positive semidefinite."""
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    matrix_arr = _as_2d_float(matrix, name="matrix")
    if matrix_arr.shape[0] != matrix_arr.shape[1]:
        raise ValueError("matrix must be square")
    if not np.allclose(matrix_arr, matrix_arr.T, atol=tolerance, rtol=0.0):
        return False
    eigenvalues = np.linalg.eigvalsh(matrix_arr)
    return bool(np.min(eigenvalues) >= -tolerance)


def hinge_losses(y_true: ArrayLike, decision_scores: ArrayLike) -> FloatMatrix:
    """Return per-example binary hinge losses as a one-dimensional array."""
    labels = np.asarray(y_true, dtype=float).reshape(-1)
    scores = np.asarray(decision_scores, dtype=float).reshape(-1)
    if labels.shape != scores.shape:
        raise ValueError("y_true and decision_scores must have equal length")
    if not np.all(np.isin(labels, (-1.0, 1.0))):
        raise ValueError("y_true must contain only -1 and +1")
    if not np.all(np.isfinite(scores)):
        raise ValueError("decision_scores must contain only finite values")
    return np.maximum(0.0, 1.0 - labels * scores)


def hinge_loss(y_true: ArrayLike, decision_scores: ArrayLike) -> float:
    """Return mean binary hinge loss."""
    return float(np.mean(hinge_losses(y_true, decision_scores)))


def svm_primal_objective(
    weights: ArrayLike,
    y_true: ArrayLike,
    decision_scores: ArrayLike,
    *,
    c: float = 1.0,
    reduction: str = "sum",
) -> float:
    """Return ``0.5 * ||w||² + C * hinge penalty``.

    ``reduction='sum'`` matches the common soft-margin primal objective.
    ``reduction='mean'`` is convenient for dataset-size-independent comparisons.
    """
    if c <= 0:
        raise ValueError("c must be positive")
    if reduction not in {"sum", "mean"}:
        raise ValueError("reduction must be 'sum' or 'mean'")
    weight_arr = np.asarray(weights, dtype=float).reshape(-1)
    if not np.all(np.isfinite(weight_arr)):
        raise ValueError("weights must contain only finite values")
    losses = hinge_losses(y_true, decision_scores)
    penalty = float(np.sum(losses) if reduction == "sum" else np.mean(losses))
    return float(0.5 * np.dot(weight_arr, weight_arr) + c * penalty)


def margin_width(weights: ArrayLike) -> float:
    """Return canonical full margin width ``2 / ||w||``."""
    weight_arr = np.asarray(weights, dtype=float).reshape(-1)
    norm = float(np.linalg.norm(weight_arr))
    if norm == 0.0:
        raise ValueError("weights must not be all zeros")
    if not np.isfinite(norm):
        raise ValueError("weights must contain only finite values")
    return 2.0 / norm


def functional_margin(
    x: ArrayLike,
    y_true: ArrayLike,
    weights: ArrayLike,
    bias: float,
) -> NDArray[np.float64]:
    """Return per-example functional margins ``y * (Xw + b)``."""
    x_arr = _as_2d_float(x, name="x")
    labels = np.asarray(y_true, dtype=float).reshape(-1)
    weight_arr = np.asarray(weights, dtype=float).reshape(-1)
    if x_arr.shape[0] != labels.shape[0]:
        raise ValueError("x and y_true must have equal sample counts")
    if x_arr.shape[1] != weight_arr.shape[0]:
        raise ValueError("weights must match x feature count")
    if not np.all(np.isin(labels, (-1.0, 1.0))):
        raise ValueError("y_true must contain only -1 and +1")
    return labels * (x_arr @ weight_arr + float(bias))


def geometric_margin(
    x: ArrayLike,
    y_true: ArrayLike,
    weights: ArrayLike,
    bias: float,
) -> NDArray[np.float64]:
    """Return per-example signed geometric margins."""
    weight_arr = np.asarray(weights, dtype=float).reshape(-1)
    norm = float(np.linalg.norm(weight_arr))
    if norm == 0.0:
        raise ValueError("weights must not be all zeros")
    return functional_margin(x, y_true, weight_arr, bias) / norm


@dataclass(frozen=True)
class MarginGroups:
    """Indices grouped by their position relative to the canonical margin."""

    outside: NDArray[np.int64]
    on_margin: NDArray[np.int64]
    inside: NDArray[np.int64]
    misclassified: NDArray[np.int64]


def classify_margin_positions(
    y_true: ArrayLike,
    decision_scores: ArrayLike,
    *,
    tolerance: float = 1e-8,
) -> MarginGroups:
    """Group examples by the value of ``y * f(x)``."""
    labels = np.asarray(y_true, dtype=float).reshape(-1)
    scores = np.asarray(decision_scores, dtype=float).reshape(-1)
    if labels.shape != scores.shape:
        raise ValueError("y_true and decision_scores must have equal length")
    if not np.all(np.isin(labels, (-1.0, 1.0))):
        raise ValueError("y_true must contain only -1 and +1")
    signed = labels * scores
    outside = np.flatnonzero(signed > 1.0 + tolerance)
    on_margin = np.flatnonzero(np.isclose(signed, 1.0, atol=tolerance, rtol=0.0))
    inside = np.flatnonzero((signed > 0.0) & (signed < 1.0 - tolerance))
    misclassified = np.flatnonzero(signed <= 0.0)
    return MarginGroups(outside, on_margin, inside, misclassified)
