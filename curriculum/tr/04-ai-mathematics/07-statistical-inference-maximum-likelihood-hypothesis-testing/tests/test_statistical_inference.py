"""Tests for lesson 7 statistical inference implementations."""

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


inference = _load_module("statistical_inference")
likelihood = _load_module("maximum_likelihood")
testing = _load_module("hypothesis_testing")


def test_mean_and_variance() -> None:
    values = [1.0, 2.0, 3.0, 4.0]
    assert inference.mean(values) == pytest.approx(2.5)
    assert inference.population_variance(values) == pytest.approx(1.25)
    assert inference.sample_variance(values) == pytest.approx(5.0 / 3.0)


def test_standard_error_decreases_when_sample_is_repeated() -> None:
    small = [1.0, 2.0, 3.0, 4.0]
    large = small * 4
    assert inference.standard_error(large) < inference.standard_error(small)


def test_quantile_interpolates() -> None:
    assert inference.quantile([0.0, 10.0], 0.25) == pytest.approx(2.5)
    assert inference.quantile([0.0, 10.0], 0.75) == pytest.approx(7.5)


def test_bootstrap_is_reproducible() -> None:
    first = inference.bootstrap_statistics([1, 2, 3, 4], resamples=50, seed=42)
    second = inference.bootstrap_statistics([1, 2, 3, 4], resamples=50, seed=42)
    assert first == second


def test_bootstrap_interval_contains_sample_mean() -> None:
    values = [2.0, 3.0, 4.0, 5.0, 6.0]
    lower, upper = inference.bootstrap_percentile_interval(
        values,
        resamples=2_000,
        seed=7,
    )
    assert lower <= inference.mean(values) <= upper


def test_sampling_distribution_has_expected_center() -> None:
    estimates = inference.sampling_distribution_means(
        population_mean=10.0,
        population_std=2.0,
        sample_size=20,
        repetitions=2_000,
        seed=3,
    )
    assert inference.mean(estimates) == pytest.approx(10.0, abs=0.08)


def test_bernoulli_mle_is_sample_mean() -> None:
    observations = [1, 0, 1, 1, 0]
    assert likelihood.bernoulli_mle(observations) == pytest.approx(0.6)


def test_bernoulli_log_likelihood_prefers_mle() -> None:
    observations = [1, 0, 1, 1, 0]
    mle_score = likelihood.bernoulli_log_likelihood(observations, 0.6)
    other_score = likelihood.bernoulli_log_likelihood(observations, 0.2)
    assert mle_score > other_score


def test_bernoulli_boundary_log_likelihood() -> None:
    assert likelihood.bernoulli_log_likelihood([0, 0], 0.0) == 0.0
    assert likelihood.bernoulli_log_likelihood([1, 0], 0.0) == -math.inf


def test_beta_bernoulli_map() -> None:
    estimate = likelihood.beta_bernoulli_map(8, 2, alpha=2.0, beta=2.0)
    assert estimate == pytest.approx(0.75)


def test_gaussian_mle() -> None:
    estimate = likelihood.gaussian_mle([1.0, 2.0, 3.0])
    assert estimate.mean == pytest.approx(2.0)
    assert estimate.variance_mle == pytest.approx(2.0 / 3.0)


def test_normal_cdf_symmetry() -> None:
    assert testing.normal_cdf(0.0) == pytest.approx(0.5)
    assert testing.normal_cdf(-1.0) == pytest.approx(1.0 - testing.normal_cdf(1.0))


def test_one_sample_mean_test_detects_large_difference() -> None:
    result = testing.one_sample_mean_test(
        [9.8, 10.0, 10.1, 9.9, 10.2, 10.1],
        null_mean=0.0,
    )
    assert result.reject_null
    assert result.p_value < 0.05


def test_two_sample_mean_test_reports_treatment_minus_control() -> None:
    result = testing.two_sample_mean_test(
        [1.0, 2.0, 3.0, 4.0],
        [2.0, 3.0, 4.0, 5.0],
    )
    assert result.estimate == pytest.approx(1.0)
    assert result.standard_error > 0.0


def test_conversion_rate_test() -> None:
    result = testing.conversion_rate_test(
        control_successes=100,
        control_total=1_000,
        treatment_successes=130,
        treatment_total=1_000,
    )
    assert result.control_rate == pytest.approx(0.1)
    assert result.treatment_rate == pytest.approx(0.13)
    assert result.absolute_lift == pytest.approx(0.03)
    assert result.relative_lift == pytest.approx(0.3)


def test_permutation_test_is_reproducible() -> None:
    first = testing.permutation_test_mean_difference(
        [1, 2, 3],
        [4, 5, 6],
        permutations=500,
        seed=11,
    )
    second = testing.permutation_test_mean_difference(
        [1, 2, 3],
        [4, 5, 6],
        permutations=500,
        seed=11,
    )
    assert first == second
    assert 0.0 < first[1] <= 1.0


def test_multiple_testing_adjustments() -> None:
    p_values = [0.001, 0.01, 0.04, 0.2]
    bonferroni = testing.bonferroni_adjust(p_values)
    bh = testing.benjamini_hochberg_adjust(p_values)
    assert bonferroni == pytest.approx([0.004, 0.04, 0.16, 0.8])
    assert all(original <= adjusted <= 1.0 for original, adjusted in zip(p_values, bh))


def test_invalid_inputs_raise() -> None:
    with pytest.raises(ValueError):
        inference.mean([])
    with pytest.raises(ValueError):
        likelihood.bernoulli_mle([0, 2])
    with pytest.raises(ValueError):
        testing.conversion_rate_test(
            control_successes=11,
            control_total=10,
            treatment_successes=1,
            treatment_total=10,
        )
