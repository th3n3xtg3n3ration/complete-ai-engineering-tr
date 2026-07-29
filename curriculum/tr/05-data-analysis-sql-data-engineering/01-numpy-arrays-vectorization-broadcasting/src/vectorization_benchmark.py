"""Reproducible loop-versus-vectorization benchmark."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from time import perf_counter

import numpy as np
from numpy.typing import NDArray


FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class BenchmarkReport:
    size: int
    repeats: int
    loop_seconds_median: float
    vectorized_seconds_median: float
    speedup: float
    maximum_absolute_error: float


def loop_affine_transform(
    values: FloatArray,
    *,
    scale: float,
    offset: float,
) -> FloatArray:
    """Apply y = scale * x + offset using a Python loop."""

    output = np.empty_like(values, dtype=np.float64)
    for index, value in enumerate(values):
        output[index] = scale * float(value) + offset
    return output


def vectorized_affine_transform(
    values: FloatArray,
    *,
    scale: float,
    offset: float,
) -> FloatArray:
    """Apply y = scale * x + offset using NumPy vectorization."""

    return scale * values + offset


def _measure(function, *args, repeats: int, **kwargs) -> list[float]:
    durations: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        function(*args, **kwargs)
        durations.append(perf_counter() - start)
    return durations


def run_benchmark(
    *,
    size: int = 250_000,
    repeats: int = 5,
    seed: int = 42,
) -> BenchmarkReport:
    """Benchmark equivalent loop and vectorized affine transforms."""

    if size <= 0:
        raise ValueError("size must be positive")
    if repeats < 3:
        raise ValueError("repeats must be at least 3")

    rng = np.random.default_rng(seed)
    values = rng.normal(size=size).astype(np.float64)

    expected = loop_affine_transform(values, scale=1.75, offset=-0.4)
    actual = vectorized_affine_transform(values, scale=1.75, offset=-0.4)
    maximum_absolute_error = float(np.max(np.abs(expected - actual)))

    # Warm-up excludes one-time dispatch and cache effects from the report.
    vectorized_affine_transform(values, scale=1.75, offset=-0.4)

    loop_times = _measure(
        loop_affine_transform,
        values,
        scale=1.75,
        offset=-0.4,
        repeats=repeats,
    )
    vectorized_times = _measure(
        vectorized_affine_transform,
        values,
        scale=1.75,
        offset=-0.4,
        repeats=repeats,
    )

    loop_median = median(loop_times)
    vectorized_median = median(vectorized_times)
    speedup = loop_median / max(vectorized_median, 1e-15)

    return BenchmarkReport(
        size=size,
        repeats=repeats,
        loop_seconds_median=loop_median,
        vectorized_seconds_median=vectorized_median,
        speedup=speedup,
        maximum_absolute_error=maximum_absolute_error,
    )


if __name__ == "__main__":
    print(run_benchmark())
