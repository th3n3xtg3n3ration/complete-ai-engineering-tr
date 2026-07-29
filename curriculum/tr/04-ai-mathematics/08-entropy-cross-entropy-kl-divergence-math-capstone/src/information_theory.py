"""Numerically stable information-theory utilities implemented with Python only."""

from __future__ import annotations

import math
from collections.abc import Sequence


ProbabilityVector = Sequence[float]


def _validate_base(base: float) -> None:
    if not math.isfinite(base) or base <= 0.0 or math.isclose(base, 1.0):
        raise ValueError("base must be positive, finite, and different from 1")


def validate_distribution(
    probabilities: ProbabilityVector,
    *,
    tolerance: float = 1e-9,
) -> tuple[float, ...]:
    """Return a validated probability vector without silently normalizing it."""

    values = tuple(float(value) for value in probabilities)
    if not values:
        raise ValueError("probability vector must not be empty")
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be positive and finite")
    if any(not math.isfinite(value) or value < 0.0 for value in values):
        raise ValueError("probabilities must be finite and non-negative")
    if not math.isclose(sum(values), 1.0, abs_tol=tolerance, rel_tol=0.0):
        raise ValueError("probabilities must sum to 1")
    return values


def normalize_non_negative(weights: ProbabilityVector) -> tuple[float, ...]:
    """Normalize non-negative finite weights into a probability distribution."""

    values = tuple(float(value) for value in weights)
    if not values:
        raise ValueError("weights must not be empty")
    if any(not math.isfinite(value) or value < 0.0 for value in values):
        raise ValueError("weights must be finite and non-negative")
    total = sum(values)
    if total <= 0.0:
        raise ValueError("at least one weight must be positive")
    return tuple(value / total for value in values)


def surprisal(probability: float, *, base: float = math.e) -> float:
    """Compute self-information for an event."""

    _validate_base(base)
    probability = float(probability)
    if not math.isfinite(probability) or probability < 0.0 or probability > 1.0:
        raise ValueError("probability must be finite and within [0, 1]")
    if probability == 0.0:
        return math.inf
    return -math.log(probability, base)


def entropy(probabilities: ProbabilityVector, *, base: float = math.e) -> float:
    """Compute Shannon entropy using the convention 0 * log(0) = 0."""

    _validate_base(base)
    values = validate_distribution(probabilities)
    return -sum(value * math.log(value, base) for value in values if value > 0.0)


def binary_entropy(probability: float, *, base: float = math.e) -> float:
    probability = float(probability)
    if not math.isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be finite and within [0, 1]")
    return entropy((probability, 1.0 - probability), base=base)


def cross_entropy(
    target: ProbabilityVector,
    prediction: ProbabilityVector,
    *,
    base: float = math.e,
) -> float:
    """Compute H(target, prediction), returning infinity for support mismatch."""

    _validate_base(base)
    target_values = validate_distribution(target)
    prediction_values = validate_distribution(prediction)
    if len(target_values) != len(prediction_values):
        raise ValueError("target and prediction must have equal length")

    total = 0.0
    for expected, predicted in zip(target_values, prediction_values, strict=True):
        if expected == 0.0:
            continue
        if predicted == 0.0:
            return math.inf
        total -= expected * math.log(predicted, base)
    return total


def kl_divergence(
    target: ProbabilityVector,
    approximation: ProbabilityVector,
    *,
    base: float = math.e,
) -> float:
    """Compute KL(target || approximation)."""

    _validate_base(base)
    target_values = validate_distribution(target)
    approximation_values = validate_distribution(approximation)
    if len(target_values) != len(approximation_values):
        raise ValueError("distributions must have equal length")

    total = 0.0
    for expected, approximate in zip(target_values, approximation_values, strict=True):
        if expected == 0.0:
            continue
        if approximate == 0.0:
            return math.inf
        total += expected * math.log(expected / approximate, base)
    return total


def jensen_shannon_divergence(
    first: ProbabilityVector,
    second: ProbabilityVector,
    *,
    base: float = 2.0,
) -> float:
    """Compute the symmetric Jensen-Shannon divergence."""

    first_values = validate_distribution(first)
    second_values = validate_distribution(second)
    if len(first_values) != len(second_values):
        raise ValueError("distributions must have equal length")
    mixture = tuple((left + right) / 2.0 for left, right in zip(first_values, second_values, strict=True))
    return 0.5 * kl_divergence(first_values, mixture, base=base) + 0.5 * kl_divergence(
        second_values,
        mixture,
        base=base,
    )


def log_sum_exp(values: Sequence[float]) -> float:
    """Compute log(sum(exp(values))) without avoidable overflow."""

    numbers = tuple(float(value) for value in values)
    if not numbers:
        raise ValueError("values must not be empty")
    if any(math.isnan(value) for value in numbers):
        raise ValueError("values must not contain NaN")
    maximum = max(numbers)
    if maximum == math.inf:
        return math.inf
    if maximum == -math.inf:
        return -math.inf
    return maximum + math.log(sum(math.exp(value - maximum) for value in numbers))


def log_softmax(logits: Sequence[float]) -> tuple[float, ...]:
    numbers = tuple(float(value) for value in logits)
    if not numbers:
        raise ValueError("logits must not be empty")
    if any(not math.isfinite(value) for value in numbers):
        raise ValueError("logits must be finite")
    normalizer = log_sum_exp(numbers)
    return tuple(value - normalizer for value in numbers)


def softmax(logits: Sequence[float]) -> tuple[float, ...]:
    return tuple(math.exp(value) for value in log_softmax(logits))


def perplexity(mean_negative_log_likelihood: float) -> float:
    value = float(mean_negative_log_likelihood)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError("mean negative log-likelihood must be finite and non-negative")
    return math.exp(value)


def mutual_information(joint: Sequence[Sequence[float]], *, base: float = math.e) -> float:
    """Compute mutual information from a finite joint probability table."""

    _validate_base(base)
    rows = tuple(tuple(float(value) for value in row) for row in joint)
    if not rows or not rows[0]:
        raise ValueError("joint table must not be empty")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("joint table must be rectangular")
    flattened = tuple(value for row in rows for value in row)
    validate_distribution(flattened)

    row_marginals = tuple(sum(row) for row in rows)
    column_marginals = tuple(sum(rows[row][column] for row in range(len(rows))) for column in range(width))

    total = 0.0
    for row_index, row in enumerate(rows):
        for column_index, probability in enumerate(row):
            if probability == 0.0:
                continue
            independent_probability = row_marginals[row_index] * column_marginals[column_index]
            total += probability * math.log(probability / independent_probability, base)
    return total


if __name__ == "__main__":
    target_distribution = (0.7, 0.2, 0.1)
    model_distribution = (0.6, 0.25, 0.15)
    print("entropy:", entropy(target_distribution))
    print("cross-entropy:", cross_entropy(target_distribution, model_distribution))
    print("KL:", kl_divergence(target_distribution, model_distribution))
    print("JS:", jensen_shannon_divergence(target_distribution, model_distribution))
    print("softmax:", softmax((1000.0, 1001.0, 999.0)))
