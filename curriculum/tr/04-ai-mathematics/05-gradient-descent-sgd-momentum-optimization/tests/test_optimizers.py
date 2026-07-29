from __future__ import annotations

import math
from pathlib import Path
import sys

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from optimization_diagnostics import EarlyStopping, diagnose_training
from optimizers import (
    Adam,
    RMSProp,
    SGD,
    clip_by_global_norm,
    cosine_decay,
    exponential_decay,
    l2_norm,
    step_decay,
)
from regression_experiment import (
    make_regression_data,
    mean_squared_error,
    mse_gradient,
    train,
)


def test_l2_norm_and_global_norm_clipping() -> None:
    assert l2_norm([3.0, 4.0]) == pytest.approx(5.0)
    clipped = clip_by_global_norm([3.0, 4.0], max_norm=2.0)
    assert clipped == pytest.approx([1.2, 1.6])
    assert l2_norm(clipped) == pytest.approx(2.0)


def test_clipping_preserves_small_gradient() -> None:
    gradient = [0.1, -0.2]
    assert clip_by_global_norm(gradient, max_norm=1.0) == gradient


def test_sgd_performs_expected_update() -> None:
    optimizer = SGD(learning_rate=0.1)
    assert optimizer.step([1.0, -2.0], [2.0, -4.0]) == pytest.approx([0.8, -1.6])


def test_momentum_accumulates_velocity() -> None:
    optimizer = SGD(learning_rate=0.1, momentum=0.9)
    parameters = optimizer.step([1.0], [1.0])
    assert parameters == pytest.approx([0.9])
    parameters = optimizer.step(parameters, [1.0])
    assert parameters == pytest.approx([0.71])
    assert optimizer.velocity == pytest.approx([1.9])


def test_nesterov_requires_momentum() -> None:
    with pytest.raises(ValueError, match="nesterov"):
        SGD(learning_rate=0.1, nesterov=True)


def test_adam_first_step_is_bias_corrected() -> None:
    optimizer = Adam(learning_rate=0.1)
    updated = optimizer.step([1.0], [2.0])
    assert updated == pytest.approx([0.9], abs=1e-8)
    assert optimizer.timestep == 1


def test_rmsprop_reduces_quadratic_loss() -> None:
    optimizer = RMSProp(learning_rate=0.05)
    parameters = [4.0, -3.0]
    initial_loss = parameters[0] ** 2 + parameters[1] ** 2
    for _ in range(200):
        gradients = [2.0 * parameters[0], 2.0 * parameters[1]]
        parameters = optimizer.step(parameters, gradients)
    final_loss = parameters[0] ** 2 + parameters[1] ** 2
    assert final_loss < initial_loss * 1e-3


def test_learning_rate_schedules() -> None:
    assert step_decay(1.0, 0, drop=0.5, every=10) == pytest.approx(1.0)
    assert step_decay(1.0, 10, drop=0.5, every=10) == pytest.approx(0.5)
    assert exponential_decay(1.0, 2, decay=0.5) == pytest.approx(0.25)
    assert cosine_decay(1.0, 0, 100, minimum_rate=0.1) == pytest.approx(1.0)
    assert cosine_decay(1.0, 100, 100, minimum_rate=0.1) == pytest.approx(0.1)


def test_mse_gradient_matches_central_difference() -> None:
    examples = [(-1.0, -3.0), (0.5, 0.25), (2.0, 5.0)]
    parameters = [1.2, -0.4]
    analytical = mse_gradient(parameters, examples)
    epsilon = 1e-6
    numerical: list[float] = []
    for index in range(2):
        plus = parameters.copy()
        minus = parameters.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        numerical.append(
            (mean_squared_error(plus, examples) - mean_squared_error(minus, examples))
            / (2.0 * epsilon)
        )
    assert analytical == pytest.approx(numerical, rel=1e-5, abs=1e-6)


def test_training_recovers_linear_relationship() -> None:
    examples = make_regression_data(count=300, noise_std=0.1, seed=12)
    result = train(
        examples,
        SGD(learning_rate=0.03, momentum=0.8),
        epochs=120,
        batch_size=30,
        seed=4,
    )
    slope, intercept = result.parameters
    assert slope == pytest.approx(3.5, abs=0.08)
    assert intercept == pytest.approx(-1.25, abs=0.08)
    assert result.history[-1].loss < result.history[0].loss
    assert math.isfinite(result.history[-1].gradient_norm)


def test_early_stopping_tracks_best_epoch() -> None:
    stopper = EarlyStopping(patience=2, minimum_delta=0.01)
    assert stopper.update(1.0, 1) is False
    assert stopper.update(0.8, 2) is False
    assert stopper.update(0.795, 3) is False
    assert stopper.update(0.794, 4) is True
    assert stopper.best_epoch == 2


def test_diagnostics_detect_non_finite_loss() -> None:
    report = diagnose_training([1.0, 0.8, float("nan")], plateau_window=2)
    assert report.status == "diverged"


def test_diagnostics_accept_healthy_history() -> None:
    report = diagnose_training(
        [10.0, 7.0, 4.0, 2.0, 1.0],
        gradient_norms=[5.0, 4.0, 3.0, 2.0, 1.0],
        update_norms=[0.5, 0.4, 0.3, 0.2, 0.1],
        plateau_window=3,
    )
    assert report.status == "healthy"


def test_invalid_shapes_raise_clear_errors() -> None:
    with pytest.raises(ValueError, match="same length"):
        SGD().step([1.0, 2.0], [1.0])
    with pytest.raises(ValueError, match="positive"):
        clip_by_global_norm([1.0], max_norm=0.0)
