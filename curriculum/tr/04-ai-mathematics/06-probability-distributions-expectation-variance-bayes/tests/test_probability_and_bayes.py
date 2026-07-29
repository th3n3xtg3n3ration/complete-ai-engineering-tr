"""Tests for lesson 6 probability and Bayesian inference code."""

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


probability = _load_module("probability")
bayes = _load_module("bayes")
simulation = _load_module("simulation_experiment")


def test_conditional_probability() -> None:
    assert probability.conditional_probability(0.2, 0.5) == pytest.approx(0.4)


def test_conditional_probability_rejects_zero_condition() -> None:
    with pytest.raises(ValueError):
        probability.conditional_probability(0.0, 0.0)


def test_union_probability() -> None:
    assert probability.union_probability(0.5, 0.4, 0.2) == pytest.approx(0.7)


def test_binomial_pmf_sums_to_one() -> None:
    total = sum(probability.binomial_pmf(k, 8, 0.3) for k in range(9))
    assert total == pytest.approx(1.0)


def test_poisson_zero_rate() -> None:
    assert probability.poisson_pmf(0, 0.0) == 1.0
    assert probability.poisson_pmf(2, 0.0) == 0.0


def test_normal_pdf_at_mean() -> None:
    assert probability.normal_pdf(0.0) == pytest.approx(1.0 / math.sqrt(2.0 * math.pi))


def test_population_and_sample_variance() -> None:
    values = [1.0, 2.0, 3.0]
    assert probability.variance(values) == pytest.approx(2.0 / 3.0)
    assert probability.variance(values, sample=True) == pytest.approx(1.0)


def test_correlation_for_linear_relationship() -> None:
    assert probability.correlation([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)


def test_expected_value_validates_weights() -> None:
    assert probability.expected_value([0, 1], [0.25, 0.75]) == pytest.approx(0.75)
    with pytest.raises(ValueError):
        probability.expected_value([0, 1], [0.2, 0.2])


def test_entropy_of_fair_binary_distribution() -> None:
    assert probability.entropy([0.5, 0.5]) == pytest.approx(1.0)


def test_binary_bayes_update_includes_base_rate() -> None:
    posterior = bayes.binary_bayes_update(0.01, 0.95, 0.05)
    assert posterior == pytest.approx(0.1610169491)


def test_logsumexp_is_stable_for_large_values() -> None:
    result = bayes.logsumexp([1000.0, 1000.0])
    assert result == pytest.approx(1000.0 + math.log(2.0))


def test_gaussian_naive_bayes_fits_separable_data() -> None:
    model = bayes.GaussianNaiveBayes().fit(
        [[-2.0], [-1.8], [-1.5], [1.5], [1.8], [2.0]],
        [0, 0, 0, 1, 1, 1],
    )
    assert model.predict([[-1.7], [1.7]]) == [0, 1]
    probabilities = model.predict_proba([[0.0]])[0]
    assert sum(probabilities) == pytest.approx(1.0)


def test_gaussian_naive_bayes_requires_fit() -> None:
    with pytest.raises(RuntimeError):
        bayes.GaussianNaiveBayes().predict([[0.0]])


def test_custom_priors_must_sum_to_one() -> None:
    model = bayes.GaussianNaiveBayes(class_priors={0: 0.8, 1: 0.3})
    with pytest.raises(ValueError):
        model.fit([[0.0], [1.0]], [0, 1])


def test_dataset_generation_is_reproducible() -> None:
    first = simulation.make_gaussian_classification_data(samples=50, seed=7)
    second = simulation.make_gaussian_classification_data(samples=50, seed=7)
    assert first == second


def test_train_test_split_has_no_overlap_by_size() -> None:
    features = [[float(index)] for index in range(20)]
    labels = [index % 2 for index in range(20)]
    x_train, x_test, y_train, y_test = simulation.train_test_split(features, labels, test_ratio=0.25, seed=3)
    assert len(x_train) == len(y_train) == 15
    assert len(x_test) == len(y_test) == 5
    assert {row[0] for row in x_train}.isdisjoint({row[0] for row in x_test})


def test_binary_log_loss_rewards_correct_confidence() -> None:
    good = simulation.binary_log_loss([0, 1], [0.1, 0.9])
    bad = simulation.binary_log_loss([0, 1], [0.9, 0.1])
    assert good < bad


def test_calibration_bins_preserve_count() -> None:
    result = simulation.calibration_bins([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9], bins=5)
    assert sum(int(item["count"]) for item in result) == 4


def test_sample_means_are_reproducible() -> None:
    first = simulation.simulate_sample_means(sample_size=5, repetitions=20, seed=9)
    second = simulation.simulate_sample_means(sample_size=5, repetitions=20, seed=9)
    assert first == second


def test_end_to_end_experiment_has_reasonable_metrics() -> None:
    metrics = simulation.run_experiment(seed=42)
    assert 0.7 <= metrics.accuracy <= 1.0
    assert 0.0 < metrics.log_loss < 1.5
    assert sum(sum(row) for row in metrics.confusion_matrix) == 150
