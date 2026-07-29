"""Pure-Python utilities for estimation, uncertainty, and bootstrap analysis."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
import math
import random
from typing import TypeAlias


Statistic: TypeAlias = Callable[[Sequence[float]], float]


def _finite_values(values: Iterable[float], *, minimum_size: int = 1) -> list[float]:
    result = [float(value) for value in values]
    if len(result) < minimum_size:
        raise ValueError(f"at least {minimum_size} observations are required")
    if not all(math.isfinite(value) for value in result):
        raise ValueError("all observations must be finite")
    return result


def mean(values: Iterable[float]) -> float:
    """Return the arithmetic mean using an accurate floating-point sum."""

    data = _finite_values(values)
    return math.fsum(data) / len(data)


def population_variance(values: Iterable[float]) -> float:
    """Return variance with denominator ``n``."""

    data = _finite_values(values)
    center = mean(data)
    return math.fsum((value - center) ** 2 for value in data) / len(data)


def sample_variance(values: Iterable[float]) -> float:
    """Return Bessel-corrected variance with denominator ``n - 1``."""

    data = _finite_values(values, minimum_size=2)
    center = mean(data)
    return math.fsum((value - center) ** 2 for value in data) / (len(data) - 1)


def sample_standard_deviation(values: Iterable[float]) -> float:
    return math.sqrt(sample_variance(values))


def standard_error(values: Iterable[float]) -> float:
    """Estimate the standard error of the sample mean."""

    data = _finite_values(values, minimum_size=2)
    return sample_standard_deviation(data) / math.sqrt(len(data))


def quantile(values: Iterable[float], probability: float) -> float:
    """Return a linearly interpolated empirical quantile."""

    data = sorted(_finite_values(values))
    if not 0.0 <= probability <= 1.0 or not math.isfinite(probability):
        raise ValueError("probability must be finite and between 0 and 1")
    if len(data) == 1:
        return data[0]

    position = probability * (len(data) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return data[lower]
    weight = position - lower
    return data[lower] * (1.0 - weight) + data[upper] * weight


def normal_confidence_interval(
    values: Iterable[float],
    *,
    confidence: float = 0.95,
    critical_value: float | None = None,
) -> tuple[float, float]:
    """Return a symmetric normal-approximation interval for the mean.

    The default critical value is 1.959963984540054 for a 95% interval.
    Other confidence levels require an explicit critical value so the function
    does not silently pretend to provide a general inverse-normal routine.
    """

    data = _finite_values(values, minimum_size=2)
    if not 0.0 < confidence < 1.0 or not math.isfinite(confidence):
        raise ValueError("confidence must be finite and between 0 and 1")
    if critical_value is None:
        if not math.isclose(confidence, 0.95, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("critical_value is required when confidence is not 0.95")
        critical_value = 1.959963984540054
    if critical_value <= 0.0 or not math.isfinite(critical_value):
        raise ValueError("critical_value must be positive and finite")

    center = mean(data)
    margin = critical_value * standard_error(data)
    return center - margin, center + margin


def bootstrap_statistics(
    values: Iterable[float],
    statistic: Statistic = mean,
    *,
    resamples: int = 2_000,
    seed: int | None = None,
) -> list[float]:
    """Generate a bootstrap sampling distribution for ``statistic``."""

    data = _finite_values(values)
    if resamples <= 0:
        raise ValueError("resamples must be positive")

    rng = random.Random(seed)
    size = len(data)
    estimates: list[float] = []
    for _ in range(resamples):
        sample = [data[rng.randrange(size)] for _ in range(size)]
        estimate = float(statistic(sample))
        if not math.isfinite(estimate):
            raise ValueError("statistic must return a finite value")
        estimates.append(estimate)
    return estimates


def bootstrap_standard_error(
    values: Iterable[float],
    statistic: Statistic = mean,
    *,
    resamples: int = 2_000,
    seed: int | None = None,
) -> float:
    estimates = bootstrap_statistics(
        values,
        statistic,
        resamples=resamples,
        seed=seed,
    )
    return sample_standard_deviation(estimates)


def bootstrap_percentile_interval(
    values: Iterable[float],
    statistic: Statistic = mean,
    *,
    confidence: float = 0.95,
    resamples: int = 2_000,
    seed: int | None = None,
) -> tuple[float, float]:
    """Return a percentile bootstrap confidence interval."""

    if not 0.0 < confidence < 1.0 or not math.isfinite(confidence):
        raise ValueError("confidence must be finite and between 0 and 1")
    estimates = bootstrap_statistics(
        values,
        statistic,
        resamples=resamples,
        seed=seed,
    )
    tail = (1.0 - confidence) / 2.0
    return quantile(estimates, tail), quantile(estimates, 1.0 - tail)


def sampling_distribution_means(
    *,
    population_mean: float,
    population_std: float,
    sample_size: int,
    repetitions: int,
    seed: int | None = None,
) -> list[float]:
    """Simulate sample means from a Gaussian population."""

    if not math.isfinite(population_mean):
        raise ValueError("population_mean must be finite")
    if population_std <= 0.0 or not math.isfinite(population_std):
        raise ValueError("population_std must be positive and finite")
    if sample_size <= 0 or repetitions <= 0:
        raise ValueError("sample_size and repetitions must be positive")

    rng = random.Random(seed)
    means: list[float] = []
    for _ in range(repetitions):
        observations = [
            rng.gauss(population_mean, population_std)
            for _ in range(sample_size)
        ]
        means.append(mean(observations))
    return means


if __name__ == "__main__":
    sample = [91, 87, 95, 101, 89, 110, 93, 96, 88, 105, 99, 92]
    print(f"mean={mean(sample):.3f}")
    print(f"standard_error={standard_error(sample):.3f}")
    print(f"normal_ci={normal_confidence_interval(sample)}")
    print(
        "bootstrap_ci=",
        bootstrap_percentile_interval(sample, resamples=5_000, seed=42),
    )
