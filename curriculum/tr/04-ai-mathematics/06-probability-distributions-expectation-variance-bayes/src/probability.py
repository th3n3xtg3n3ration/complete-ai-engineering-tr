"""Pure-Python probability and descriptive-statistics utilities.

The module intentionally avoids third-party dependencies so learners can inspect
all calculations. Public functions validate inputs and prefer numerically stable
formulations where practical.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
import math


def _as_finite_floats(values: Iterable[float], *, name: str) -> list[float]:
    result = [float(value) for value in values]
    if not result:
        raise ValueError(f"{name} must not be empty")
    if not all(math.isfinite(value) for value in result):
        raise ValueError(f"{name} must contain only finite values")
    return result


def validate_probability(value: float, *, name: str = "probability") -> float:
    probability = float(value)
    if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return probability


def conditional_probability(joint_probability: float, condition_probability: float) -> float:
    joint = validate_probability(joint_probability, name="joint_probability")
    condition = validate_probability(condition_probability, name="condition_probability")
    if condition == 0.0:
        raise ValueError("condition_probability must be greater than zero")
    if joint > condition:
        raise ValueError("joint_probability cannot exceed condition_probability")
    return joint / condition


def union_probability(probability_a: float, probability_b: float, intersection: float) -> float:
    a = validate_probability(probability_a, name="probability_a")
    b = validate_probability(probability_b, name="probability_b")
    overlap = validate_probability(intersection, name="intersection")
    if overlap > min(a, b):
        raise ValueError("intersection cannot exceed either event probability")
    result = a + b - overlap
    if result > 1.0 + 1e-12:
        raise ValueError("inconsistent probabilities produce a union above one")
    return min(result, 1.0)


def bernoulli_pmf(outcome: int, probability: float) -> float:
    p = validate_probability(probability)
    if outcome not in (0, 1):
        raise ValueError("outcome must be 0 or 1")
    return p if outcome == 1 else 1.0 - p


def binomial_pmf(successes: int, trials: int, probability: float) -> float:
    if not isinstance(trials, int) or trials < 0:
        raise ValueError("trials must be a non-negative integer")
    if not isinstance(successes, int) or not 0 <= successes <= trials:
        raise ValueError("successes must be an integer between 0 and trials")
    p = validate_probability(probability)
    return math.comb(trials, successes) * (p**successes) * ((1.0 - p) ** (trials - successes))


def poisson_pmf(events: int, rate: float) -> float:
    if not isinstance(events, int) or events < 0:
        raise ValueError("events must be a non-negative integer")
    lam = float(rate)
    if not math.isfinite(lam) or lam < 0.0:
        raise ValueError("rate must be non-negative and finite")
    if lam == 0.0:
        return 1.0 if events == 0 else 0.0
    log_probability = -lam + events * math.log(lam) - math.lgamma(events + 1.0)
    return math.exp(log_probability)


def normal_pdf(value: float, mean: float = 0.0, standard_deviation: float = 1.0) -> float:
    x = float(value)
    mu = float(mean)
    sigma = float(standard_deviation)
    if not all(math.isfinite(item) for item in (x, mu, sigma)):
        raise ValueError("arguments must be finite")
    if sigma <= 0.0:
        raise ValueError("standard_deviation must be positive")
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2.0 * math.pi))


def mean(values: Iterable[float]) -> float:
    data = _as_finite_floats(values, name="values")
    return math.fsum(data) / len(data)


def variance(values: Iterable[float], *, sample: bool = False) -> float:
    data = _as_finite_floats(values, name="values")
    if sample and len(data) < 2:
        raise ValueError("sample variance requires at least two values")
    center = math.fsum(data) / len(data)
    squared_deviations = math.fsum((value - center) ** 2 for value in data)
    denominator = len(data) - 1 if sample else len(data)
    return squared_deviations / denominator


def standard_deviation(values: Iterable[float], *, sample: bool = False) -> float:
    return math.sqrt(variance(values, sample=sample))


def covariance(x_values: Iterable[float], y_values: Iterable[float], *, sample: bool = False) -> float:
    x = _as_finite_floats(x_values, name="x_values")
    y = _as_finite_floats(y_values, name="y_values")
    if len(x) != len(y):
        raise ValueError("x_values and y_values must have equal length")
    if sample and len(x) < 2:
        raise ValueError("sample covariance requires at least two pairs")
    x_mean = math.fsum(x) / len(x)
    y_mean = math.fsum(y) / len(y)
    denominator = len(x) - 1 if sample else len(x)
    return math.fsum((a - x_mean) * (b - y_mean) for a, b in zip(x, y, strict=True)) / denominator


def correlation(x_values: Iterable[float], y_values: Iterable[float]) -> float:
    x = _as_finite_floats(x_values, name="x_values")
    y = _as_finite_floats(y_values, name="y_values")
    if len(x) != len(y):
        raise ValueError("x_values and y_values must have equal length")
    x_std = standard_deviation(x)
    y_std = standard_deviation(y)
    if x_std == 0.0 or y_std == 0.0:
        raise ValueError("correlation is undefined for a constant variable")
    return covariance(x, y) / (x_std * y_std)


def expected_value(outcomes: Sequence[float], probabilities: Sequence[float]) -> float:
    if len(outcomes) != len(probabilities) or not outcomes:
        raise ValueError("outcomes and probabilities must be non-empty and equal length")
    values = _as_finite_floats(outcomes, name="outcomes")
    weights = [validate_probability(value, name="probability") for value in probabilities]
    if not math.isclose(math.fsum(weights), 1.0, rel_tol=1e-9, abs_tol=1e-12):
        raise ValueError("probabilities must sum to one")
    return math.fsum(value * weight for value, weight in zip(values, weights, strict=True))


def running_mean(values: Iterable[float]) -> list[float]:
    data = _as_finite_floats(values, name="values")
    result: list[float] = []
    total = 0.0
    for index, value in enumerate(data, start=1):
        total += value
        result.append(total / index)
    return result


def entropy(probabilities: Iterable[float], *, base: float = 2.0) -> float:
    weights = [validate_probability(value) for value in probabilities]
    if not weights:
        raise ValueError("probabilities must not be empty")
    if not math.isclose(math.fsum(weights), 1.0, rel_tol=1e-9, abs_tol=1e-12):
        raise ValueError("probabilities must sum to one")
    if not math.isfinite(base) or base <= 0.0 or base == 1.0:
        raise ValueError("base must be positive and different from one")
    return -math.fsum(value * (math.log(value) / math.log(base)) for value in weights if value > 0.0)


if __name__ == "__main__":
    observations = [0, 1, 1, 0, 1, 1, 1, 0]
    print(f"mean={mean(observations):.4f}")
    print(f"variance={variance(observations):.4f}")
    print(f"binomial_pmf={binomial_pmf(3, 5, 0.5):.4f}")
    print(f"entropy={entropy([0.25, 0.75]):.4f} bits")
