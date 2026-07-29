from __future__ import annotations

import math
import pathlib
import sys

import pytest

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from autodiff import Value
from calculus import central_difference, directional_derivative, gradient, hessian, jacobian
from gradient_check import run_check


def test_central_difference_quadratic() -> None:
    assert central_difference(lambda x: x * x, 3.0) == pytest.approx(6.0, rel=1e-6)


def test_invalid_step() -> None:
    with pytest.raises(ValueError):
        central_difference(lambda x: x, 1.0, 0.0)


def test_gradient() -> None:
    result = gradient(lambda v: v[0] ** 2 + 3.0 * v[1] ** 2, [2.0, -1.0])
    assert result == pytest.approx([4.0, -6.0], rel=1e-5)


def test_directional_derivative() -> None:
    value = directional_derivative(lambda v: v[0] ** 2 + v[1] ** 2, [1.0, 0.0], [1.0, 0.0])
    assert value == pytest.approx(2.0, rel=1e-5)


def test_zero_direction_rejected() -> None:
    with pytest.raises(ValueError):
        directional_derivative(lambda v: sum(v), [1.0, 2.0], [0.0, 0.0])


def test_jacobian() -> None:
    result = jacobian(lambda v: [v[0] * v[1], v[0] ** 2 + v[1]], [2.0, 3.0])
    assert result[0] == pytest.approx([3.0, 2.0], rel=1e-5)
    assert result[1] == pytest.approx([4.0, 1.0], rel=1e-5)


def test_hessian() -> None:
    result = hessian(lambda v: v[0] ** 2 + 3.0 * v[1] ** 2, [2.0, -1.0])
    assert result[0] == pytest.approx([2.0, 0.0], abs=1e-5)
    assert result[1] == pytest.approx([0.0, 6.0], abs=1e-5)


def test_autodiff_product_and_sum() -> None:
    x = Value(2.0)
    y = Value(3.0)
    output = x * y + x
    output.backward()
    assert x.grad == pytest.approx(4.0)
    assert y.grad == pytest.approx(2.0)


def test_autodiff_shared_node_accumulates() -> None:
    x = Value(3.0)
    output = x * x + x
    output.backward()
    assert x.grad == pytest.approx(7.0)


def test_autodiff_tanh() -> None:
    x = Value(0.5)
    output = x.tanh()
    output.backward()
    expected = 1.0 - math.tanh(0.5) ** 2
    assert x.grad == pytest.approx(expected)


def test_autodiff_relu() -> None:
    negative = Value(-2.0)
    negative.relu().backward()
    assert negative.grad == 0.0


def test_autodiff_log_domain() -> None:
    with pytest.raises(ValueError):
        Value(0.0).log()


def test_gradient_check_passes() -> None:
    results = run_check()
    assert results
    assert all(result.passed for result in results)
