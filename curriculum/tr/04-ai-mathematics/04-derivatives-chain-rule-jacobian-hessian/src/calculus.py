"""Numerical differentiation utilities implemented with the standard library."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from math import isfinite, sqrt

ScalarFunction = Callable[[float], float]
VectorFunction = Callable[[Sequence[float]], float]
VectorValuedFunction = Callable[[Sequence[float]], Sequence[float]]


def _validate_step(step: float) -> None:
    if not isfinite(step) or step <= 0.0:
        raise ValueError("step must be a positive finite number")


def central_difference(function: ScalarFunction, x: float, step: float = 1e-5) -> float:
    """Approximate a scalar derivative with the central-difference formula."""
    _validate_step(step)
    result = (function(x + step) - function(x - step)) / (2.0 * step)
    if not isfinite(result):
        raise ValueError("derivative result is not finite")
    return result


def gradient(function: VectorFunction, point: Sequence[float], step: float = 1e-5) -> list[float]:
    """Approximate the gradient of a scalar-valued multivariate function."""
    _validate_step(step)
    if not point:
        raise ValueError("point must not be empty")
    base = [float(value) for value in point]
    result: list[float] = []
    for index in range(len(base)):
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step
        result.append((function(plus) - function(minus)) / (2.0 * step))
    return result


def directional_derivative(
    function: VectorFunction,
    point: Sequence[float],
    direction: Sequence[float],
    step: float = 1e-5,
) -> float:
    """Approximate a directional derivative using a normalized direction."""
    if len(point) != len(direction) or not point:
        raise ValueError("point and direction must have the same non-zero dimension")
    norm = sqrt(sum(float(value) ** 2 for value in direction))
    if norm == 0.0:
        raise ValueError("direction must not be the zero vector")
    unit = [float(value) / norm for value in direction]
    grad = gradient(function, point, step)
    return sum(g * u for g, u in zip(grad, unit, strict=True))


def jacobian(
    function: VectorValuedFunction,
    point: Sequence[float],
    step: float = 1e-5,
) -> list[list[float]]:
    """Approximate the Jacobian matrix of a vector-valued function."""
    _validate_step(step)
    if not point:
        raise ValueError("point must not be empty")
    base_output = list(function(point))
    if not base_output:
        raise ValueError("function output must not be empty")
    matrix = [[0.0 for _ in point] for _ in base_output]
    for column in range(len(point)):
        plus = list(map(float, point))
        minus = list(map(float, point))
        plus[column] += step
        minus[column] -= step
        out_plus = list(function(plus))
        out_minus = list(function(minus))
        if len(out_plus) != len(base_output) or len(out_minus) != len(base_output):
            raise ValueError("function output dimension changed")
        for row in range(len(base_output)):
            matrix[row][column] = (out_plus[row] - out_minus[row]) / (2.0 * step)
    return matrix


def hessian(function: VectorFunction, point: Sequence[float], step: float = 1e-4) -> list[list[float]]:
    """Approximate a Hessian matrix with second-order central differences."""
    _validate_step(step)
    if not point:
        raise ValueError("point must not be empty")
    base = list(map(float, point))
    size = len(base)
    result = [[0.0 for _ in range(size)] for _ in range(size)]
    center = function(base)
    for i in range(size):
        plus = base.copy()
        minus = base.copy()
        plus[i] += step
        minus[i] -= step
        result[i][i] = (function(plus) - 2.0 * center + function(minus)) / (step**2)
        for j in range(i + 1, size):
            pp, pm, mp, mm = (base.copy() for _ in range(4))
            pp[i] += step; pp[j] += step
            pm[i] += step; pm[j] -= step
            mp[i] -= step; mp[j] += step
            mm[i] -= step; mm[j] -= step
            value = (function(pp) - function(pm) - function(mp) + function(mm)) / (4.0 * step**2)
            result[i][j] = value
            result[j][i] = value
    return result


if __name__ == "__main__":
    quadratic = lambda values: values[0] ** 2 + 3.0 * values[1] ** 2
    print("gradient:", gradient(quadratic, [2.0, -1.0]))
    print("hessian:", hessian(quadratic, [2.0, -1.0]))
