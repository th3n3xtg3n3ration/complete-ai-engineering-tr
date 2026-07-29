"""Tests for lesson 8 information theory, losses, and capstone code."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import sys

import pytest


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SRC / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


information = _load_module("information_theory")
losses = _load_module("classification_losses")
capstone = _load_module("math_capstone")


def test_entropy_of_certain_distribution_is_zero() -> None:
    assert information.entropy((1.0, 0.0, 0.0), base=2.0) == pytest.approx(0.0)


def test_uniform_four_class_entropy_is_two_bits() -> None:
    assert information.entropy((0.25, 0.25, 0.25, 0.25), base=2.0) == pytest.approx(2.0)


def test_binary_entropy_is_maximum_at_half() -> None:
    middle = information.binary_entropy(0.5, base=2.0)
    edge = information.binary_entropy(0.1, base=2.0)
    assert middle == pytest.approx(1.0)
    assert middle > edge


def test_cross_entropy_decomposition() -> None:
    target = (0.7, 0.2, 0.1)
    prediction = (0.5, 0.3, 0.2)
    assert information.cross_entropy(target, prediction) == pytest.approx(
        information.entropy(target) + information.kl_divergence(target, prediction)
    )


def test_kl_is_zero_for_identical_distributions() -> None:
    distribution = (0.2, 0.3, 0.5)
    assert information.kl_divergence(distribution, distribution) == pytest.approx(0.0)


def test_kl_is_directional() -> None:
    first = (0.9, 0.1)
    second = (0.5, 0.5)
    assert information.kl_divergence(first, second) != pytest.approx(
        information.kl_divergence(second, first)
    )


def test_support_mismatch_returns_infinity() -> None:
    assert math.isinf(information.kl_divergence((1.0, 0.0), (0.0, 1.0)))
    assert math.isinf(information.cross_entropy((1.0, 0.0), (0.0, 1.0)))


def test_jensen_shannon_is_symmetric() -> None:
    first = (0.8, 0.2)
    second = (0.3, 0.7)
    assert information.jensen_shannon_divergence(first, second) == pytest.approx(
        information.jensen_shannon_divergence(second, first)
    )


def test_softmax_is_stable_for_large_logits() -> None:
    probabilities = information.softmax((1000.0, 1001.0, 999.0))
    assert all(math.isfinite(value) for value in probabilities)
    assert sum(probabilities) == pytest.approx(1.0)
    assert probabilities[1] == max(probabilities)


def test_mutual_information_is_zero_for_independent_table() -> None:
    joint = ((0.25, 0.25), (0.25, 0.25))
    assert information.mutual_information(joint, base=2.0) == pytest.approx(0.0)


def test_mutual_information_is_one_bit_for_perfect_binary_match() -> None:
    joint = ((0.5, 0.0), (0.0, 0.5))
    assert information.mutual_information(joint, base=2.0) == pytest.approx(1.0)


def test_binary_cross_entropy_from_extreme_logits_is_finite() -> None:
    assert math.isfinite(losses.binary_cross_entropy_from_logits(1.0, 1000.0))
    assert math.isfinite(losses.binary_cross_entropy_from_logits(0.0, -1000.0))


def test_correct_class_logit_reduces_categorical_loss() -> None:
    good = losses.categorical_cross_entropy_from_logits(0, (5.0, 0.0, -1.0))
    bad = losses.categorical_cross_entropy_from_logits(0, (-1.0, 5.0, 0.0))
    assert good < bad


def test_label_smoothing_is_finite_and_non_negative() -> None:
    value = losses.label_smoothed_cross_entropy(1, (0.5, 2.0, -1.0), smoothing=0.1)
    assert math.isfinite(value)
    assert value >= 0.0


def test_focal_loss_downweights_easy_example() -> None:
    easy = losses.focal_loss_binary_from_logits(1.0, 5.0)
    hard = losses.focal_loss_binary_from_logits(1.0, -1.0)
    assert easy < hard


def test_brier_score_is_zero_for_perfect_prediction() -> None:
    assert losses.brier_score(1, (0.0, 1.0, 0.0)) == pytest.approx(0.0)


def test_weighted_mean() -> None:
    assert losses.weighted_mean((1.0, 3.0), (1.0, 3.0)) == pytest.approx(2.5)


def test_capstone_training_is_reproducible() -> None:
    features, labels = capstone.make_three_class_dataset(samples_per_class=12, seed=5)
    first = capstone.SoftmaxRegression(learning_rate=0.15, epochs=60, seed=9)
    second = capstone.SoftmaxRegression(learning_rate=0.15, epochs=60, seed=9)
    first_history = first.fit(features, labels)
    second_history = second.fit(features, labels)
    assert first_history.losses == second_history.losses
    assert first.weights == second.weights


def test_capstone_loss_decreases_and_accuracy_is_high() -> None:
    features, labels = capstone.make_three_class_dataset(samples_per_class=25, seed=12)
    model = capstone.SoftmaxRegression(
        learning_rate=0.15,
        epochs=150,
        l2=0.001,
        label_smoothing=0.02,
        seed=3,
    )
    history = model.fit(features, labels)
    predictions = model.predict(features)
    assert history.losses[-1] < history.losses[0]
    assert capstone.accuracy(labels, predictions) > 0.95


def test_confusion_matrix_preserves_sample_count() -> None:
    labels = (0, 0, 1, 1, 2)
    predictions = (0, 1, 1, 1, 2)
    matrix = capstone.confusion_matrix(labels, predictions)
    assert sum(sum(row) for row in matrix) == len(labels)


def test_expected_calibration_error_is_bounded() -> None:
    labels = (0, 1, 1, 0)
    probabilities = ((0.9, 0.1), (0.2, 0.8), (0.4, 0.6), (0.7, 0.3))
    value = capstone.expected_calibration_error(labels, probabilities, bins=4)
    assert 0.0 <= value <= 1.0


def test_invalid_distribution_is_rejected() -> None:
    with pytest.raises(ValueError):
        information.entropy((0.2, 0.2))
