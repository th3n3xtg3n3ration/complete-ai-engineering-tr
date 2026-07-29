"""Stable classification loss functions implemented without third-party packages."""

from __future__ import annotations

import math
from collections.abc import Sequence


def _validate_binary_target(target: float) -> float:
    value = float(target)
    if value not in (0.0, 1.0):
        raise ValueError("binary target must be 0 or 1")
    return value


def binary_cross_entropy_from_logits(target: float, logit: float) -> float:
    """Compute numerically stable binary cross-entropy from a raw logit."""

    target_value = _validate_binary_target(target)
    logit_value = float(logit)
    if not math.isfinite(logit_value):
        raise ValueError("logit must be finite")
    return max(logit_value, 0.0) - logit_value * target_value + math.log1p(
        math.exp(-abs(logit_value))
    )


def sigmoid(logit: float) -> float:
    value = float(logit)
    if not math.isfinite(value):
        raise ValueError("logit must be finite")
    if value >= 0.0:
        exponential = math.exp(-value)
        return 1.0 / (1.0 + exponential)
    exponential = math.exp(value)
    return exponential / (1.0 + exponential)


def log_sum_exp(values: Sequence[float]) -> float:
    numbers = tuple(float(value) for value in values)
    if not numbers:
        raise ValueError("values must not be empty")
    if any(not math.isfinite(value) for value in numbers):
        raise ValueError("values must be finite")
    maximum = max(numbers)
    return maximum + math.log(sum(math.exp(value - maximum) for value in numbers))


def log_softmax(logits: Sequence[float]) -> tuple[float, ...]:
    numbers = tuple(float(value) for value in logits)
    normalizer = log_sum_exp(numbers)
    return tuple(value - normalizer for value in numbers)


def categorical_cross_entropy_from_logits(
    target_index: int,
    logits: Sequence[float],
) -> float:
    """Return negative log-likelihood for one multiclass example."""

    log_probabilities = log_softmax(logits)
    if not 0 <= target_index < len(log_probabilities):
        raise ValueError("target_index is outside the class range")
    return -log_probabilities[target_index]


def label_smoothed_cross_entropy(
    target_index: int,
    logits: Sequence[float],
    *,
    smoothing: float = 0.1,
) -> float:
    """Compute cross-entropy against a uniformly smoothed target distribution."""

    if not math.isfinite(smoothing) or not 0.0 <= smoothing < 1.0:
        raise ValueError("smoothing must be finite and within [0, 1)")
    log_probabilities = log_softmax(logits)
    class_count = len(log_probabilities)
    if not 0 <= target_index < class_count:
        raise ValueError("target_index is outside the class range")

    off_value = smoothing / class_count
    on_value = 1.0 - smoothing + off_value
    return -sum(
        (on_value if index == target_index else off_value) * log_probability
        for index, log_probability in enumerate(log_probabilities)
    )


def focal_loss_binary_from_logits(
    target: float,
    logit: float,
    *,
    gamma: float = 2.0,
    alpha: float = 0.25,
) -> float:
    """Compute binary focal loss from a raw logit."""

    target_value = _validate_binary_target(target)
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError("gamma must be finite and non-negative")
    if not math.isfinite(alpha) or not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha must be finite and within [0, 1]")

    probability = sigmoid(logit)
    probability_of_target = probability if target_value == 1.0 else 1.0 - probability
    alpha_of_target = alpha if target_value == 1.0 else 1.0 - alpha
    base_loss = binary_cross_entropy_from_logits(target_value, logit)
    return alpha_of_target * (1.0 - probability_of_target) ** gamma * base_loss


def brier_score(target_index: int, probabilities: Sequence[float]) -> float:
    """Compute multiclass Brier score for one example."""

    values = tuple(float(value) for value in probabilities)
    if not values:
        raise ValueError("probabilities must not be empty")
    if any(not math.isfinite(value) or value < 0.0 or value > 1.0 for value in values):
        raise ValueError("probabilities must be finite and within [0, 1]")
    if not math.isclose(sum(values), 1.0, abs_tol=1e-9, rel_tol=0.0):
        raise ValueError("probabilities must sum to 1")
    if not 0 <= target_index < len(values):
        raise ValueError("target_index is outside the class range")
    return sum(
        (probability - (1.0 if index == target_index else 0.0)) ** 2
        for index, probability in enumerate(values)
    )


def weighted_mean(losses: Sequence[float], weights: Sequence[float] | None = None) -> float:
    """Aggregate finite losses with optional non-negative weights."""

    loss_values = tuple(float(value) for value in losses)
    if not loss_values:
        raise ValueError("losses must not be empty")
    if any(not math.isfinite(value) for value in loss_values):
        raise ValueError("losses must be finite")
    if weights is None:
        return sum(loss_values) / len(loss_values)

    weight_values = tuple(float(value) for value in weights)
    if len(weight_values) != len(loss_values):
        raise ValueError("weights must match losses")
    if any(not math.isfinite(value) or value < 0.0 for value in weight_values):
        raise ValueError("weights must be finite and non-negative")
    total_weight = sum(weight_values)
    if total_weight <= 0.0:
        raise ValueError("at least one weight must be positive")
    return sum(loss * weight for loss, weight in zip(loss_values, weight_values, strict=True)) / total_weight


if __name__ == "__main__":
    example_logits = (2.0, 0.5, -1.0)
    print("categorical CE:", categorical_cross_entropy_from_logits(0, example_logits))
    print("smoothed CE:", label_smoothed_cross_entropy(0, example_logits, smoothing=0.1))
    print("binary BCE:", binary_cross_entropy_from_logits(1.0, 3.0))
    print("binary focal:", focal_loss_binary_from_logits(1.0, 3.0))
