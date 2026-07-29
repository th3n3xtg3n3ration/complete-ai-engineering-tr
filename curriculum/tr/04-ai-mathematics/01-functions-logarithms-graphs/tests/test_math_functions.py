from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

LESSON_DIRECTORY = Path(__file__).resolve().parents[1]
SRC_DIRECTORY = LESSON_DIRECTORY / "src"
sys.path.insert(0, str(SRC_DIRECTORY))

import function_experiment as experiment  # noqa: E402
import math_functions as mf  # noqa: E402


def test_linear_and_inverse_linear_round_trip() -> None:
    output = mf.linear(4.0, slope=2.5, intercept=-3.0)
    assert output == pytest.approx(7.0)
    assert mf.inverse_linear(output, slope=2.5, intercept=-3.0) == pytest.approx(4.0)


def test_polynomial_uses_highest_degree_first() -> None:
    assert mf.polynomial(3.0, [2.0, -3.0, 1.0]) == pytest.approx(10.0)


def test_logarithm_and_exponential_are_inverse_operations() -> None:
    value = 5.5
    assert mf.logarithm(mf.exponential(value, base=2.0), base=2.0) == pytest.approx(value)


@pytest.mark.parametrize(
    ("x", "expected"),
    [(-1_000.0, 0.0), (0.0, 0.5), (1_000.0, 1.0)],
)
def test_sigmoid_is_stable_for_extreme_values(x: float, expected: float) -> None:
    assert mf.sigmoid(x) == pytest.approx(expected)


def test_softplus_is_stable_for_extreme_values() -> None:
    assert mf.softplus(1_000.0) == pytest.approx(1_000.0)
    assert mf.softplus(-1_000.0) == pytest.approx(0.0, abs=1e-12)


def test_softmax_is_stable_and_normalized() -> None:
    probabilities = mf.softmax([1_000.0, 1_001.0, 999.0])
    assert math.fsum(probabilities) == pytest.approx(1.0)
    assert probabilities[1] == max(probabilities)
    assert all(0.0 < probability < 1.0 for probability in probabilities)


def test_softmax_is_shift_invariant() -> None:
    first = mf.softmax([1.0, 2.0, 3.0])
    second = mf.softmax([101.0, 102.0, 103.0])
    assert second == pytest.approx(first)


def test_compose_applies_functions_right_to_left() -> None:
    double = lambda value: 2.0 * value
    add_three = lambda value: value + 3.0
    function = mf.compose(double, add_three)
    assert function(4.0) == pytest.approx(14.0)


def test_numerical_derivative_matches_quadratic_slope() -> None:
    square = lambda value: value**2
    assert mf.numerical_derivative(square, 3.0) == pytest.approx(6.0, rel=1e-5)


def test_mean_squared_error() -> None:
    assert mf.mean_squared_error([1.0, 0.0], [0.8, 0.1]) == pytest.approx(0.025)


def test_binary_cross_entropy_rewards_better_predictions() -> None:
    good = mf.binary_cross_entropy([1.0, 0.0], [0.9, 0.1])
    bad = mf.binary_cross_entropy([1.0, 0.0], [0.1, 0.9])
    assert good < bad


def test_binary_cross_entropy_clips_zero_and_one() -> None:
    loss = mf.binary_cross_entropy([1.0, 0.0], [1.0, 0.0])
    assert math.isfinite(loss)
    assert loss >= 0.0


def test_categorical_cross_entropy_matches_correct_class_log_loss() -> None:
    probabilities = [0.1, 0.7, 0.2]
    loss = mf.categorical_cross_entropy([0.0, 1.0, 0.0], probabilities)
    assert loss == pytest.approx(-math.log(0.7))


def test_sample_function_includes_stop_value() -> None:
    points = mf.sample_function(mf.relu, start=-1.0, stop=1.0, step=0.3)
    assert points[0][0] == pytest.approx(-1.0)
    assert points[-1][0] == pytest.approx(1.0)


def test_experiment_builds_expected_zero_row() -> None:
    rows = experiment.build_rows(-1.0, 1.0, 0.5)
    zero_row = next(row for row in rows if row["x"] == pytest.approx(0.0))
    assert zero_row["sigmoid"] == pytest.approx(0.5)
    assert zero_row["relu"] == pytest.approx(0.0)
    assert zero_row["softplus"] == pytest.approx(math.log(2.0))


def test_experiment_writes_csv(tmp_path: Path) -> None:
    output = tmp_path / "curves.csv"
    rows = experiment.build_rows(-1.0, 1.0, 1.0)
    experiment.write_csv(rows, output)
    content = output.read_text(encoding="utf-8")
    assert "sigmoid_slope" in content
    assert len(content.splitlines()) == 4


@pytest.mark.parametrize(
    ("call", "exception_type"),
    [
        (lambda: mf.logarithm(0.0), mf.MathDomainError),
        (lambda: mf.logarithm(2.0, base=1.0), mf.MathDomainError),
        (lambda: mf.inverse_linear(1.0, slope=0.0), mf.MathDomainError),
        (lambda: mf.softmax([]), ValueError),
        (lambda: mf.mean_squared_error([1.0], [1.0, 2.0]), ValueError),
        (lambda: mf.binary_cross_entropy([2.0], [0.5]), mf.MathDomainError),
        (lambda: mf.categorical_cross_entropy([1.0, 0.0], [0.8, 0.3]), mf.MathDomainError),
    ],
)
def test_invalid_inputs_fail_explicitly(call, exception_type: type[Exception]) -> None:
    with pytest.raises(exception_type):
        call()
