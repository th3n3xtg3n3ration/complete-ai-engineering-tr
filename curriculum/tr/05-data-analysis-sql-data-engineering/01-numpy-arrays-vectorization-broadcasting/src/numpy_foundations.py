"""Production-oriented NumPy utilities used in lesson 1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from numpy.typing import ArrayLike, NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class ArraySummary:
    """Compact diagnostics for a numeric array."""

    shape: tuple[int, ...]
    dtype: str
    minimum: float
    maximum: float
    mean: float
    standard_deviation: float
    missing_count: int
    infinite_count: int


def as_float_array(
    values: ArrayLike,
    *,
    ndim: int | None = None,
    copy: bool = False,
) -> FloatArray:
    """Convert input to a finite-capable float64 array and validate dimensionality."""

    array = (
        np.array(values, dtype=np.float64, copy=True)
        if copy
        else np.asarray(values, dtype=np.float64)
    )
    if ndim is not None and array.ndim != ndim:
        raise ValueError(f"expected {ndim} dimensions, got {array.ndim}")
    if array.size == 0:
        raise ValueError("array must not be empty")
    return array


def summarize_array(values: ArrayLike) -> ArraySummary:
    """Return NaN-aware summary statistics without mutating the input."""

    array = as_float_array(values)
    infinite_count = int(np.isinf(array).sum())
    finite_or_nan = np.where(np.isinf(array), np.nan, array)

    if np.isnan(finite_or_nan).all():
        minimum = maximum = mean = standard_deviation = float("nan")
    else:
        minimum = float(np.nanmin(finite_or_nan))
        maximum = float(np.nanmax(finite_or_nan))
        mean = float(np.nanmean(finite_or_nan))
        standard_deviation = float(np.nanstd(finite_or_nan))

    return ArraySummary(
        shape=array.shape,
        dtype=str(array.dtype),
        minimum=minimum,
        maximum=maximum,
        mean=mean,
        standard_deviation=standard_deviation,
        missing_count=int(np.isnan(array).sum()),
        infinite_count=infinite_count,
    )


def standardize(
    values: ArrayLike,
    *,
    axis: int | tuple[int, ...] | None = 0,
    ddof: int = 0,
    zero_scale: Literal["unit", "raise"] = "unit",
) -> FloatArray:
    """Standardize values along an axis using NaN-aware statistics."""

    array = as_float_array(values)
    if ddof < 0:
        raise ValueError("ddof must be non-negative")
    if zero_scale not in {"unit", "raise"}:
        raise ValueError("zero_scale must be 'unit' or 'raise'")

    mean = np.nanmean(array, axis=axis, keepdims=True)
    scale = np.nanstd(array, axis=axis, ddof=ddof, keepdims=True)

    invalid_scale = ~np.isfinite(scale) | (scale == 0.0)
    if zero_scale == "raise" and np.any(invalid_scale):
        raise ValueError("cannot standardize a constant or undefined feature")
    safe_scale = np.where(invalid_scale, 1.0, scale)
    return (array - mean) / safe_scale


def min_max_scale(
    values: ArrayLike,
    *,
    axis: int | tuple[int, ...] | None = 0,
    feature_range: tuple[float, float] = (0.0, 1.0),
) -> FloatArray:
    """Scale values to a requested interval with safe handling of constants."""

    array = as_float_array(values)
    lower, upper = map(float, feature_range)
    if not np.isfinite([lower, upper]).all() or lower >= upper:
        raise ValueError("feature_range must contain finite values with lower < upper")

    minimum = np.nanmin(array, axis=axis, keepdims=True)
    maximum = np.nanmax(array, axis=axis, keepdims=True)
    span = maximum - minimum
    safe_span = np.where((span == 0.0) | ~np.isfinite(span), 1.0, span)
    unit = (array - minimum) / safe_span
    return lower + unit * (upper - lower)


def cosine_similarity_matrix(
    left: ArrayLike,
    right: ArrayLike | None = None,
    *,
    eps: float = 1e-12,
) -> FloatArray:
    """Compute pairwise cosine similarities between row vectors."""

    left_array = as_float_array(left, ndim=2)
    right_array = left_array if right is None else as_float_array(right, ndim=2)

    if left_array.shape[1] != right_array.shape[1]:
        raise ValueError("left and right must have the same feature count")
    if eps <= 0.0 or not np.isfinite(eps):
        raise ValueError("eps must be positive and finite")
    if not np.isfinite(left_array).all() or not np.isfinite(right_array).all():
        raise ValueError("cosine similarity requires finite inputs")

    left_norms = np.linalg.norm(left_array, axis=1, keepdims=True)
    right_norms = np.linalg.norm(right_array, axis=1, keepdims=True)
    left_normalized = left_array / np.maximum(left_norms, eps)
    right_normalized = right_array / np.maximum(right_norms, eps)
    return left_normalized @ right_normalized.T


def pairwise_squared_euclidean(
    left: ArrayLike,
    right: ArrayLike | None = None,
) -> FloatArray:
    """Compute pairwise squared Euclidean distances without a 3-D difference array."""

    left_array = as_float_array(left, ndim=2)
    right_array = left_array if right is None else as_float_array(right, ndim=2)

    if left_array.shape[1] != right_array.shape[1]:
        raise ValueError("left and right must have the same feature count")
    if not np.isfinite(left_array).all() or not np.isfinite(right_array).all():
        raise ValueError("distance calculation requires finite inputs")

    left_sq = np.sum(left_array * left_array, axis=1, keepdims=True)
    right_sq = np.sum(right_array * right_array, axis=1, keepdims=True).T
    distances = left_sq + right_sq - 2.0 * (left_array @ right_array.T)
    return np.maximum(distances, 0.0)


def top_k_cosine_neighbors(
    query: ArrayLike,
    candidates: ArrayLike,
    *,
    k: int,
) -> tuple[NDArray[np.int64], FloatArray]:
    """Return indices and scores of the top-k cosine neighbors."""

    query_array = as_float_array(query)
    if query_array.ndim == 1:
        query_array = query_array.reshape(1, -1)
    if query_array.ndim != 2 or query_array.shape[0] != 1:
        raise ValueError("query must be a single vector")
    candidate_array = as_float_array(candidates, ndim=2)
    if not 1 <= k <= candidate_array.shape[0]:
        raise ValueError("k must be between 1 and the number of candidates")

    scores = cosine_similarity_matrix(query_array, candidate_array)[0]
    partition = np.argpartition(-scores, k - 1)[:k]
    order = partition[np.argsort(-scores[partition], kind="stable")]
    return order.astype(np.int64, copy=False), scores[order]


if __name__ == "__main__":
    matrix = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    print(summarize_array(matrix))
    print(standardize(matrix))
    print(cosine_similarity_matrix(matrix))
