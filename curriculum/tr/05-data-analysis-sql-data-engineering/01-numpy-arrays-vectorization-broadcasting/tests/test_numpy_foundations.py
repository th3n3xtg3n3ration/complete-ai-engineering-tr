"""Tests for lesson 1 NumPy utilities."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
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


foundations = _load_module("numpy_foundations")
benchmark = _load_module("vectorization_benchmark")
pipeline_module = _load_module("feature_pipeline")


def test_as_float_array_validates_dimension() -> None:
    with pytest.raises(ValueError, match="expected 2 dimensions"):
        foundations.as_float_array([1, 2, 3], ndim=2)


def test_summary_counts_nan_and_infinity() -> None:
    summary = foundations.summarize_array([1.0, np.nan, np.inf, -np.inf])
    assert summary.missing_count == 1
    assert summary.infinite_count == 2
    assert summary.mean == pytest.approx(1.0)


def test_standardize_columns() -> None:
    values = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    result = foundations.standardize(values, axis=0)
    assert np.mean(result, axis=0) == pytest.approx([0.0, 0.0])
    assert np.std(result, axis=0) == pytest.approx([1.0, 1.0])


def test_standardize_constant_feature_becomes_zero() -> None:
    values = np.array([[2.0, 1.0], [2.0, 3.0], [2.0, 5.0]])
    result = foundations.standardize(values, axis=0)
    assert result[:, 0] == pytest.approx([0.0, 0.0, 0.0])


def test_standardize_can_raise_for_constant_feature() -> None:
    with pytest.raises(ValueError, match="constant"):
        foundations.standardize([1.0, 1.0], axis=0, zero_scale="raise")


def test_min_max_scale_custom_range() -> None:
    values = np.array([0.0, 5.0, 10.0])
    result = foundations.min_max_scale(values, axis=0, feature_range=(-1.0, 1.0))
    assert result == pytest.approx([-1.0, 0.0, 1.0])


def test_cosine_similarity_identity() -> None:
    identity = np.eye(3)
    result = foundations.cosine_similarity_matrix(identity)
    assert result == pytest.approx(identity)


def test_cosine_similarity_rejects_non_finite_input() -> None:
    with pytest.raises(ValueError, match="finite"):
        foundations.cosine_similarity_matrix([[1.0, np.nan]])


def test_pairwise_distance_is_symmetric_with_zero_diagonal() -> None:
    values = np.array([[0.0, 0.0], [3.0, 4.0], [1.0, 1.0]])
    result = foundations.pairwise_squared_euclidean(values)
    assert result == pytest.approx(result.T)
    assert np.diag(result) == pytest.approx([0.0, 0.0, 0.0])
    assert result[0, 1] == pytest.approx(25.0)


def test_top_k_neighbors_are_sorted() -> None:
    candidates = np.array([[1.0, 0.0], [0.8, 0.2], [-1.0, 0.0]])
    indices, scores = foundations.top_k_cosine_neighbors(
        [1.0, 0.0],
        candidates,
        k=2,
    )
    assert indices.tolist() == [0, 1]
    assert scores[0] >= scores[1]


def test_loop_and_vectorized_results_match() -> None:
    values = np.linspace(-2.0, 2.0, 100)
    loop = benchmark.loop_affine_transform(values, scale=2.5, offset=-1.0)
    vectorized = benchmark.vectorized_affine_transform(
        values,
        scale=2.5,
        offset=-1.0,
    )
    assert loop == pytest.approx(vectorized)


def test_benchmark_is_reproducible_in_accuracy() -> None:
    first = benchmark.run_benchmark(size=1_000, repeats=3, seed=7)
    second = benchmark.run_benchmark(size=1_000, repeats=3, seed=7)
    assert first.maximum_absolute_error == second.maximum_absolute_error == 0.0


def test_pipeline_requires_fit() -> None:
    pipeline = pipeline_module.NumericFeaturePipeline()
    with pytest.raises(RuntimeError, match="not been fitted"):
        pipeline.transform([[1.0, 2.0]])


def test_pipeline_imputes_and_standardizes() -> None:
    values = np.array(
        [
            [1.0, 10.0],
            [2.0, np.nan],
            [3.0, 30.0],
            [4.0, 40.0],
        ]
    )
    pipeline = pipeline_module.NumericFeaturePipeline(clip_quantiles=None)
    transformed = pipeline.fit_transform(values)
    assert np.isfinite(transformed).all()
    assert np.mean(transformed, axis=0) == pytest.approx([0.0, 0.0])


def test_pipeline_does_not_refit_during_transform() -> None:
    train = np.array([[0.0], [1.0], [2.0]])
    validation = np.array([[100.0], [101.0]])
    pipeline = pipeline_module.NumericFeaturePipeline(clip_quantiles=None).fit(train)
    original_mean = pipeline.state.means.copy()
    transformed = pipeline.transform(validation)
    assert pipeline.state.means == pytest.approx(original_mean)
    assert np.mean(transformed) > 100.0


def test_pipeline_rejects_feature_count_change() -> None:
    pipeline = pipeline_module.NumericFeaturePipeline().fit([[1.0, 2.0]])
    with pytest.raises(ValueError, match="expected 2 features"):
        pipeline.transform([[1.0, 2.0, 3.0]])


def test_pipeline_rejects_all_missing_feature() -> None:
    values = np.array([[1.0, np.nan], [2.0, np.nan]])
    with pytest.raises(ValueError, match="all values are missing"):
        pipeline_module.NumericFeaturePipeline().fit(values)


def test_pipeline_records_constant_features() -> None:
    values = np.array([[1.0, 5.0], [2.0, 5.0], [3.0, 5.0]])
    pipeline = pipeline_module.NumericFeaturePipeline(clip_quantiles=None).fit(values)
    assert pipeline.state.constant_features == (1,)


def test_pipeline_clipping_limits_outlier() -> None:
    values = np.array([[0.0], [1.0], [2.0], [1000.0]])
    pipeline = pipeline_module.NumericFeaturePipeline(
        clip_quantiles=(0.0, 0.75)
    ).fit(values)
    transformed = pipeline.transform([[10_000.0]])
    expected_upper = (
        pipeline.state.clip_upper[0] - pipeline.state.means[0]
    ) / pipeline.state.scales[0]
    assert transformed[0, 0] == pytest.approx(expected_upper)


def test_inverse_transform_recovers_processed_training_values() -> None:
    values = np.array([[1.0, 10.0], [2.0, 20.0], [3.0, 30.0]])
    pipeline = pipeline_module.NumericFeaturePipeline(clip_quantiles=None)
    transformed = pipeline.fit_transform(values)
    recovered = pipeline.inverse_transform(transformed)
    assert recovered == pytest.approx(values)
