"""Compare autodiff gradients with finite-difference estimates."""

from __future__ import annotations

from dataclasses import dataclass

from autodiff import Value


@dataclass(frozen=True)
class CheckResult:
    parameter: str
    analytical: float
    numerical: float
    relative_error: float
    passed: bool


def scalar_loss(x: float, w: float, bias: float, target: float) -> float:
    prediction = x * w + bias
    return (prediction - target) ** 2


def numerical_derivative(
    x: float,
    w: float,
    bias: float,
    target: float,
    parameter: str,
    step: float = 1e-6,
) -> float:
    if step <= 0.0:
        raise ValueError("step must be positive")
    values = {"x": x, "w": w, "bias": bias}
    if parameter not in values:
        raise ValueError(f"unknown parameter: {parameter}")
    plus = values.copy()
    minus = values.copy()
    plus[parameter] += step
    minus[parameter] -= step
    return (
        scalar_loss(plus["x"], plus["w"], plus["bias"], target)
        - scalar_loss(minus["x"], minus["w"], minus["bias"], target)
    ) / (2.0 * step)


def run_check(tolerance: float = 1e-6) -> list[CheckResult]:
    x = Value(1.5, "x")
    w = Value(-0.75, "w")
    bias = Value(0.25, "bias")
    target = 0.8
    loss = (x * w + bias - target).pow(2.0)
    loss.backward()

    results: list[CheckResult] = []
    for name, node in (("x", x), ("w", w), ("bias", bias)):
        numerical = numerical_derivative(x.data, w.data, bias.data, target, name)
        scale = max(1.0, abs(node.grad), abs(numerical))
        error = abs(node.grad - numerical) / scale
        results.append(CheckResult(name, node.grad, numerical, error, error <= tolerance))
    return results


if __name__ == "__main__":
    for result in run_check():
        print(result)
