"""Numerically stable mathematical building blocks for introductory AI math.

Explanations in the curriculum are Turkish; source code intentionally uses
English names and documentation to mirror professional engineering practice.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from typing import TypeAlias

Number: TypeAlias = int | float
UnaryFunction: TypeAlias = Callable[[float], float]


class MathDomainError(ValueError):
    """Raised when a mathematical function receives an invalid domain value."""


def _as_finite_float(value: Number, *, name: str) -> float:
    """Convert a numeric value to float and reject NaN or infinity."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")

    converted = float(value)
    if not math.isfinite(converted):
        raise ValueError(f"{name} must be finite")
    return converted


def _as_finite_vector(values: Sequence[Number], *, name: str) -> list[float]:
    """Validate a non-empty sequence of finite real numbers."""
    if not values:
        raise ValueError(f"{name} must not be empty")
    return [_as_finite_float(value, name=f"{name}[{index}]") for index, value in enumerate(values)]


def linear(x: Number, *, slope: Number = 1.0, intercept: Number = 0.0) -> float:
    """Evaluate f(x) = slope * x + intercept."""
    x_value = _as_finite_float(x, name="x")
    slope_value = _as_finite_float(slope, name="slope")
    intercept_value = _as_finite_float(intercept, name="intercept")
    return slope_value * x_value + intercept_value


def polynomial(x: Number, coefficients: Sequence[Number]) -> float:
    """Evaluate a polynomial using Horner's method.

    Coefficients are ordered from highest degree to constant term. For example,
    [2, -3, 1] represents 2x^2 - 3x + 1.
    """
    x_value = _as_finite_float(x, name="x")
    coefficient_values = _as_finite_vector(coefficients, name="coefficients")

    result = 0.0
    for coefficient in coefficient_values:
        result = result * x_value + coefficient
    return result


def exponential(x: Number, *, base: Number = math.e) -> float:
    """Evaluate base ** x with a mathematically valid exponential base."""
    x_value = _as_finite_float(x, name="x")
    base_value = _as_finite_float(base, name="base")
    if base_value <= 0.0:
        raise MathDomainError("base must be greater than zero")

    try:
        result = math.pow(base_value, x_value)
    except OverflowError as exc:
        raise OverflowError("exponential result exceeds floating-point range") from exc

    if not math.isfinite(result):
        raise OverflowError("exponential result exceeds floating-point range")
    return result


def logarithm(x: Number, *, base: Number = math.e) -> float:
    """Evaluate log_base(x) after validating the logarithm domain."""
    x_value = _as_finite_float(x, name="x")
    base_value = _as_finite_float(base, name="base")

    if x_value <= 0.0:
        raise MathDomainError("x must be greater than zero for a logarithm")
    if base_value <= 0.0 or math.isclose(base_value, 1.0):
        raise MathDomainError("base must be positive and different from one")

    return math.log(x_value, base_value)


def compose(*functions: UnaryFunction) -> UnaryFunction:
    """Return the composition f(g(...(x))) using right-to-left application."""
    if not functions:
        raise ValueError("at least one function is required")
    if not all(callable(function) for function in functions):
        raise TypeError("all composition items must be callable")

    def composed(x: float) -> float:
        result = _as_finite_float(x, name="x")
        for function in reversed(functions):
            result = _as_finite_float(function(result), name="function result")
        return result

    return composed


def inverse_linear(y: Number, *, slope: Number, intercept: Number = 0.0) -> float:
    """Invert y = slope * x + intercept for a non-zero slope."""
    y_value = _as_finite_float(y, name="y")
    slope_value = _as_finite_float(slope, name="slope")
    intercept_value = _as_finite_float(intercept, name="intercept")
    if math.isclose(slope_value, 0.0):
        raise MathDomainError("a constant linear function has no unique inverse")
    return (y_value - intercept_value) / slope_value


def numerical_derivative(function: UnaryFunction, x: Number, *, step: Number = 1e-5) -> float:
    """Approximate a local derivative with the central-difference formula."""
    if not callable(function):
        raise TypeError("function must be callable")

    x_value = _as_finite_float(x, name="x")
    step_value = _as_finite_float(step, name="step")
    if step_value <= 0.0:
        raise ValueError("step must be greater than zero")

    right = _as_finite_float(function(x_value + step_value), name="right function value")
    left = _as_finite_float(function(x_value - step_value), name="left function value")
    return (right - left) / (2.0 * step_value)


def sigmoid(x: Number) -> float:
    """Compute a numerically stable logistic sigmoid."""
    x_value = _as_finite_float(x, name="x")
    if x_value >= 0.0:
        negative_exp = math.exp(-x_value)
        return 1.0 / (1.0 + negative_exp)

    positive_exp = math.exp(x_value)
    return positive_exp / (1.0 + positive_exp)


def tanh(x: Number) -> float:
    """Compute the hyperbolic tangent activation."""
    return math.tanh(_as_finite_float(x, name="x"))


def relu(x: Number) -> float:
    """Compute the rectified linear unit activation."""
    x_value = _as_finite_float(x, name="x")
    return max(0.0, x_value)


def leaky_relu(x: Number, *, negative_slope: Number = 0.01) -> float:
    """Compute leaky ReLU with a non-negative negative-region slope."""
    x_value = _as_finite_float(x, name="x")
    slope_value = _as_finite_float(negative_slope, name="negative_slope")
    if slope_value < 0.0:
        raise ValueError("negative_slope must not be negative")
    return x_value if x_value >= 0.0 else slope_value * x_value


def softplus(x: Number) -> float:
    """Compute log(1 + exp(x)) without overflow or avoidable precision loss."""
    x_value = _as_finite_float(x, name="x")
    return max(x_value, 0.0) + math.log1p(math.exp(-abs(x_value)))


def softmax(logits: Sequence[Number]) -> list[float]:
    """Convert logits into a numerically stable probability distribution."""
    values = _as_finite_vector(logits, name="logits")
    maximum = max(values)
    exponentials = [math.exp(value - maximum) for value in values]
    normalizer = math.fsum(exponentials)
    return [value / normalizer for value in exponentials]


def mean_squared_error(targets: Sequence[Number], predictions: Sequence[Number]) -> float:
    """Return the mean squared error for equally sized non-empty vectors."""
    target_values = _as_finite_vector(targets, name="targets")
    prediction_values = _as_finite_vector(predictions, name="predictions")
    if len(target_values) != len(prediction_values):
        raise ValueError("targets and predictions must have equal length")

    squared_errors = [
        (target - prediction) ** 2
        for target, prediction in zip(target_values, prediction_values, strict=True)
    ]
    return math.fsum(squared_errors) / len(squared_errors)


def _clip_probability(probability: Number, *, epsilon: Number) -> float:
    probability_value = _as_finite_float(probability, name="probability")
    epsilon_value = _as_finite_float(epsilon, name="epsilon")
    if not 0.0 < epsilon_value < 0.5:
        raise ValueError("epsilon must be between zero and 0.5")
    if not 0.0 <= probability_value <= 1.0:
        raise MathDomainError("probabilities must be between zero and one")
    return min(max(probability_value, epsilon_value), 1.0 - epsilon_value)


def binary_cross_entropy(
    targets: Sequence[Number],
    probabilities: Sequence[Number],
    *,
    epsilon: Number = 1e-12,
) -> float:
    """Compute mean binary cross-entropy with safe probability clipping."""
    target_values = _as_finite_vector(targets, name="targets")
    probability_values = _as_finite_vector(probabilities, name="probabilities")
    if len(target_values) != len(probability_values):
        raise ValueError("targets and probabilities must have equal length")

    losses: list[float] = []
    for target, probability in zip(target_values, probability_values, strict=True):
        if target not in (0.0, 1.0):
            raise MathDomainError("binary targets must be zero or one")
        clipped = _clip_probability(probability, epsilon=epsilon)
        loss = -(target * math.log(clipped) + (1.0 - target) * math.log1p(-clipped))
        losses.append(loss)

    return math.fsum(losses) / len(losses)


def categorical_cross_entropy(
    target_distribution: Sequence[Number],
    probabilities: Sequence[Number],
    *,
    epsilon: Number = 1e-12,
) -> float:
    """Compute cross-entropy between target and predicted distributions."""
    targets = _as_finite_vector(target_distribution, name="target_distribution")
    predictions = _as_finite_vector(probabilities, name="probabilities")
    if len(targets) != len(predictions):
        raise ValueError("target_distribution and probabilities must have equal length")
    if any(target < 0.0 or target > 1.0 for target in targets):
        raise MathDomainError("target values must be between zero and one")
    if not math.isclose(math.fsum(targets), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise MathDomainError("target distribution must sum to one")
    if not math.isclose(math.fsum(predictions), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise MathDomainError("probability distribution must sum to one")

    losses = [
        -target * math.log(_clip_probability(probability, epsilon=epsilon))
        for target, probability in zip(targets, predictions, strict=True)
        if target > 0.0
    ]
    return math.fsum(losses)


def sample_function(
    function: UnaryFunction,
    *,
    start: Number,
    stop: Number,
    step: Number,
) -> list[tuple[float, float]]:
    """Sample an inclusive numeric interval without cumulative-loop drift."""
    if not callable(function):
        raise TypeError("function must be callable")

    start_value = _as_finite_float(start, name="start")
    stop_value = _as_finite_float(stop, name="stop")
    step_value = _as_finite_float(step, name="step")
    if step_value <= 0.0:
        raise ValueError("step must be greater than zero")
    if stop_value < start_value:
        raise ValueError("stop must be greater than or equal to start")

    count = int(math.floor((stop_value - start_value) / step_value + 1e-12))
    points: list[tuple[float, float]] = []
    for index in range(count + 1):
        x_value = start_value + index * step_value
        y_value = _as_finite_float(function(x_value), name="sampled function value")
        points.append((x_value, y_value))

    if not math.isclose(points[-1][0], stop_value, rel_tol=0.0, abs_tol=1e-12):
        points.append((stop_value, _as_finite_float(function(stop_value), name="sampled function value")))
    return points


def main() -> None:
    """Run a compact demonstration when this module is executed directly."""
    logits = [1_000.0, 1_001.0, 999.0]
    probabilities = softmax(logits)
    print("stable_softmax:", [round(value, 6) for value in probabilities])
    print("sigmoid(-1000):", sigmoid(-1_000.0))
    print("sigmoid(1000):", sigmoid(1_000.0))
    print("relu slope at x=2:", round(numerical_derivative(relu, 2.0), 6))
    print("mse:", mean_squared_error([1.0, 0.0], [0.8, 0.1]))
    print("binary_cross_entropy:", binary_cross_entropy([1, 0], [0.8, 0.1]))


if __name__ == "__main__":
    main()
