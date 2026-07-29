"""Tests for logistic regression, thresholding, and calibration."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

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


models = _load_module("logistic_models")
metrics = _load_module("classification_metrics")
pipelines = _load_module("calibration_pipeline")


@pytest.fixture
def binary_data() -> tuple[np.ndarray, np.ndarray]:
    features, target = make_classification(
        n_samples=400,
        n_features=5,
        n_informative=4,
        n_redundant=0,
        class_sep=1.4,
        random_state=42,
    )
    return features, target


@pytest.fixture
def mixed_frame() -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(7)
    size = 240
    age = rng.normal(40, 10, size)
    spend = rng.normal(100, 25, size)
    region = rng.choice(["north", "south", "west"], size=size)
    logits = -4.0 + 0.06 * age + 0.025 * spend + (region == "south") * 0.8
    probability = 1.0 / (1.0 + np.exp(-logits))
    target = rng.binomial(1, probability)
    frame = pd.DataFrame({"age": age, "spend": spend, "region": region})
    frame.loc[0, "age"] = np.nan
    frame.loc[1, "region"] = None
    return frame, target


def test_sigmoid_zero_is_half() -> None:
    assert models.sigmoid([0.0]).item() == pytest.approx(0.5)


def test_sigmoid_is_stable_for_extreme_values() -> None:
    result = models.sigmoid([-1_000.0, 1_000.0])
    assert result[0] == pytest.approx(0.0)
    assert result[1] == pytest.approx(1.0)


def test_sigmoid_is_monotonic() -> None:
    result = models.sigmoid([-2.0, -1.0, 0.0, 1.0, 2.0])
    assert np.all(np.diff(result) > 0)


def test_binary_log_loss_matches_known_value() -> None:
    loss = models.binary_log_loss([0, 1], [0.25, 0.75])
    assert loss == pytest.approx(-np.log(0.75))


def test_binary_log_loss_clips_extreme_probabilities() -> None:
    loss = models.binary_log_loss([0, 1], [1.0, 0.0])
    assert np.isfinite(loss)
    assert loss > 20.0


def test_binary_log_loss_rejects_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="equal shape"):
        models.binary_log_loss([0, 1], [0.5])


def test_binary_log_loss_supports_sample_weights() -> None:
    loss = models.binary_log_loss([0, 1], [0.1, 0.6], sample_weight=[1.0, 3.0])
    expected = np.average([-np.log(0.9), -np.log(0.6)], weights=[1.0, 3.0])
    assert loss == pytest.approx(expected)


def test_model_validates_hyperparameters() -> None:
    with pytest.raises(ValueError, match="learning_rate"):
        models.LogisticRegressionGD(learning_rate=0)
    with pytest.raises(ValueError, match="max_iter"):
        models.LogisticRegressionGD(max_iter=0)
    with pytest.raises(ValueError, match="l2_strength"):
        models.LogisticRegressionGD(l2_strength=-1)


def test_model_requires_two_classes() -> None:
    model = models.LogisticRegressionGD()
    with pytest.raises(ValueError, match="both binary classes"):
        model.fit([[0.0], [1.0]], [0, 0])


def test_model_fits_separable_data() -> None:
    features = np.array([[-2.0], [-1.0], [1.0], [2.0]])
    target = np.array([0, 0, 1, 1])
    model = models.LogisticRegressionGD(learning_rate=0.2, max_iter=4_000).fit(
        features,
        target,
    )
    assert np.array_equal(model.predict(features), target)
    assert model.coef_[0] > 0


def test_model_loss_decreases() -> None:
    features = np.array([[-2.0], [-1.0], [1.0], [2.0]])
    target = np.array([0, 0, 1, 1])
    model = models.LogisticRegressionGD(max_iter=100).fit(features, target)
    assert model.loss_history_[-1] < model.loss_history_[0]


def test_model_predict_requires_fit() -> None:
    with pytest.raises(RuntimeError, match="fit"):
        models.LogisticRegressionGD().predict([[0.0]])


def test_model_predict_proba_rows_sum_to_one(binary_data) -> None:
    features, target = binary_data
    model = models.LogisticRegressionGD(max_iter=500).fit(features, target)
    probabilities = model.predict_proba(features[:10])
    assert probabilities.shape == (10, 2)
    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_model_threshold_changes_positive_rate(binary_data) -> None:
    features, target = binary_data
    model = models.LogisticRegressionGD(max_iter=500).fit(features, target)
    low = model.predict(features, threshold=0.2).sum()
    high = model.predict(features, threshold=0.8).sum()
    assert low >= high


def test_model_rejects_invalid_threshold(binary_data) -> None:
    features, target = binary_data
    model = models.LogisticRegressionGD(max_iter=50).fit(features, target)
    with pytest.raises(ValueError, match="threshold"):
        model.predict(features, threshold=1.1)


def test_l2_regularization_reduces_coefficient_norm(binary_data) -> None:
    features, target = binary_data
    plain = models.LogisticRegressionGD(max_iter=1_000).fit(features, target)
    regularized = models.LogisticRegressionGD(
        max_iter=1_000,
        l2_strength=1.0,
    ).fit(features, target)
    assert np.linalg.norm(regularized.coef_) < np.linalg.norm(plain.coef_)


def test_balanced_class_weights_fit(binary_data) -> None:
    features, target = binary_data
    model = models.LogisticRegressionGD(
        max_iter=300,
        class_weight="balanced",
    ).fit(features, target)
    assert model.n_iter_ > 0


def test_confusion_counts_are_correct() -> None:
    counts = metrics.confusion_counts([0, 0, 1, 1], [0.1, 0.8, 0.4, 0.9])
    assert counts.true_negative == 1
    assert counts.false_positive == 1
    assert counts.false_negative == 1
    assert counts.true_positive == 1
    assert counts.total == 4


def test_expected_cost_uses_error_costs() -> None:
    counts = metrics.ConfusionCounts(7, 1, 2, 10)
    cost = metrics.expected_cost(
        counts,
        false_positive_cost=2.0,
        false_negative_cost=5.0,
        normalize=False,
    )
    assert cost == pytest.approx(12.0)


def test_classification_metrics_include_probability_metrics() -> None:
    report = metrics.classification_metrics([0, 0, 1, 1], [0.1, 0.3, 0.7, 0.9])
    assert report["accuracy"] == pytest.approx(1.0)
    assert report["roc_auc"] == pytest.approx(1.0)
    assert 0.0 <= report["brier_score"] <= 1.0


def test_threshold_table_has_requested_thresholds() -> None:
    table = metrics.threshold_table(
        [0, 0, 1, 1],
        [0.1, 0.4, 0.6, 0.9],
        thresholds=[0.25, 0.5, 0.75],
    )
    assert table["threshold"].tolist() == [0.25, 0.5, 0.75]
    assert "expected_cost" in table


def test_select_threshold_maximizes_f1() -> None:
    table = metrics.threshold_table(
        [0, 0, 1, 1],
        [0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3, 0.5, 0.7],
    )
    threshold = metrics.select_threshold(table, metric="f1")
    assert threshold == pytest.approx(0.5)


def test_select_threshold_minimizes_expected_cost() -> None:
    table = metrics.threshold_table(
        [0, 0, 1, 1],
        [0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3, 0.5, 0.7],
        false_negative_cost=10.0,
    )
    threshold = metrics.select_threshold(table, metric="expected_cost")
    assert threshold == pytest.approx(0.5)


def test_select_threshold_applies_recall_constraint() -> None:
    table = metrics.threshold_table(
        [0, 0, 1, 1],
        [0.1, 0.4, 0.6, 0.9],
        thresholds=[0.3, 0.5, 0.7],
    )
    threshold = metrics.select_threshold(
        table,
        metric="balanced_accuracy",
        minimum_recall=1.0,
    )
    assert threshold in {0.3, 0.5}


def test_select_threshold_fails_when_constraints_are_impossible() -> None:
    table = metrics.threshold_table([0, 1], [0.7, 0.6], thresholds=[0.5])
    with pytest.raises(ValueError, match="no threshold"):
        metrics.select_threshold(table, metric="f1", minimum_precision=1.0)


def test_calibration_table_preserves_count() -> None:
    table = metrics.calibration_table(
        [0, 0, 1, 1],
        [0.1, 0.2, 0.8, 0.9],
        n_bins=4,
    )
    assert table["count"].sum() == 4
    assert set(table.columns) >= {"mean_probability", "event_rate", "absolute_gap"}


def test_calibration_table_rejects_small_bin_count() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        metrics.calibration_table([0, 1], [0.2, 0.8], n_bins=1)


def test_expected_calibration_error_is_zero_for_perfect_bins() -> None:
    table = pd.DataFrame({"count": [5, 5], "absolute_gap": [0.0, 0.0]})
    assert metrics.expected_calibration_error(table) == pytest.approx(0.0)


def test_pipeline_rejects_overlapping_feature_lists() -> None:
    with pytest.raises(ValueError, match="disjoint"):
        pipelines.build_classifier_pipeline(
            numeric_features=["age"],
            categorical_features=["age"],
        )


def test_pipeline_handles_missing_and_unknown_categories(mixed_frame) -> None:
    frame, target = mixed_frame
    model = pipelines.build_classifier_pipeline(
        numeric_features=["age", "spend"],
        categorical_features=["region"],
    )
    model.fit(frame, target)
    new_rows = pd.DataFrame(
        {"age": [35.0], "spend": [120.0], "region": ["new-region"]}
    )
    probability = pipelines.positive_probabilities(model, new_rows)
    assert probability.shape == (1,)
    assert 0.0 <= probability[0] <= 1.0


def test_l1_pipeline_fits(mixed_frame) -> None:
    frame, target = mixed_frame
    model = pipelines.build_classifier_pipeline(
        numeric_features=["age", "spend"],
        categorical_features=["region"],
        penalty="l1",
    )
    model.fit(frame, target)
    assert pipelines.positive_probabilities(model, frame[:5]).shape == (5,)


def test_positive_probabilities_rejects_non_binary_estimator() -> None:
    class BadEstimator:
        def predict_proba(self, features):
            return np.ones((len(features), 3)) / 3

    with pytest.raises(ValueError, match="two-class"):
        pipelines.positive_probabilities(BadEstimator(), pd.DataFrame({"x": [1]}))


def test_sigmoid_calibration_fits(mixed_frame) -> None:
    frame, target = mixed_frame
    train_x, test_x, train_y, _ = train_test_split(
        frame,
        target,
        test_size=0.25,
        stratify=target,
        random_state=42,
    )
    base = pipelines.build_classifier_pipeline(
        numeric_features=["age", "spend"],
        categorical_features=["region"],
    )
    calibrated = pipelines.calibrate_classifier(base, train_x, train_y, cv=3)
    probabilities = pipelines.positive_probabilities(calibrated, test_x)
    assert probabilities.shape[0] == test_x.shape[0]


def test_isotonic_calibration_fits(mixed_frame) -> None:
    frame, target = mixed_frame
    base = pipelines.build_classifier_pipeline(
        numeric_features=["age", "spend"],
        categorical_features=["region"],
    )
    calibrated = pipelines.calibrate_classifier(
        base,
        frame,
        target,
        method="isotonic",
        cv=3,
    )
    assert pipelines.positive_probabilities(calibrated, frame[:3]).shape == (3,)


def test_calibration_rejects_invalid_method(mixed_frame) -> None:
    frame, target = mixed_frame
    base = pipelines.build_classifier_pipeline(
        numeric_features=["age"],
        categorical_features=["region"],
    )
    with pytest.raises(ValueError, match="method"):
        pipelines.calibrate_classifier(base, frame, target, method="bad")


def test_evaluate_classifier_returns_complete_summary(mixed_frame) -> None:
    frame, target = mixed_frame
    model = pipelines.build_classifier_pipeline(
        numeric_features=["age", "spend"],
        categorical_features=["region"],
        class_weight="balanced",
    )
    model.fit(frame, target)
    result = pipelines.evaluate_classifier(model, frame, target, n_bins=6)
    assert "roc_auc" in result.metrics
    assert result.threshold_rows == 101
    assert 1 <= result.calibration_bins <= 6
    assert result.expected_calibration_error >= 0.0
