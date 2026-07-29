"""Tests for lesson 6 reusable model helpers."""

from __future__ import annotations

import numpy as np
import pytest

from src.models import (
    build_kmeans_pipeline,
    evaluate_partition,
    fit_dbscan,
    fit_isolation_forest,
    threshold_by_review_capacity,
)


def make_clusters() -> np.ndarray:
    rng = np.random.default_rng(42)
    left = rng.normal(loc=-3, scale=0.3, size=(50, 2))
    right = rng.normal(loc=3, scale=0.3, size=(50, 2))
    return np.vstack([left, right])


def test_kmeans_pipeline_is_reproducible() -> None:
    values = make_clusters()
    first = build_kmeans_pipeline(2, random_state=7).fit_predict(values)
    second = build_kmeans_pipeline(2, random_state=7).fit_predict(values)
    np.testing.assert_array_equal(first, second)


def test_kmeans_pipeline_rejects_invalid_cluster_count() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        build_kmeans_pipeline(1)


def test_partition_metrics_are_valid() -> None:
    values = make_clusters()
    labels = build_kmeans_pipeline(2).fit_predict(values)
    metrics = evaluate_partition(values, labels)
    assert metrics.n_clusters == 2
    assert 0.0 < metrics.silhouette <= 1.0
    assert metrics.davies_bouldin >= 0.0


def test_partition_ignores_noise() -> None:
    values = make_clusters()
    labels = np.array([0] * 50 + [1] * 49 + [-1])
    metrics = evaluate_partition(values, labels)
    assert metrics.n_clusters == 2


def test_dbscan_returns_one_label_per_row() -> None:
    values = make_clusters()
    labels, transformed = fit_dbscan(values, eps=0.5, min_samples=4)
    assert labels.shape == (values.shape[0],)
    assert transformed.shape == values.shape


def test_isolation_scores_use_lower_as_more_anomalous() -> None:
    normal = make_clusters()
    values = np.vstack([normal, np.array([[50.0, 50.0]])])
    _, scores = fit_isolation_forest(values, contamination=0.01)
    assert scores[-1] < np.median(scores[:-1])


def test_capacity_threshold_selects_lower_tail() -> None:
    scores = np.arange(100, dtype=float)
    threshold = threshold_by_review_capacity(scores, 0.10)
    selected = scores <= threshold
    assert 9 <= selected.sum() <= 11


@pytest.mark.parametrize(
    "bad_values",
    [
        np.array([1.0, 2.0]),
        np.array([[1.0, np.nan], [2.0, 3.0]]),
        np.array([[1.0, np.inf], [2.0, 3.0]]),
    ],
)
def test_invalid_inputs_are_rejected(bad_values: np.ndarray) -> None:
    with pytest.raises(ValueError):
        fit_isolation_forest(bad_values)
