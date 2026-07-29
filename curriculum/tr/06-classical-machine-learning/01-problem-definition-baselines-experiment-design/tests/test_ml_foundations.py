"""Tests for classical ML problem framing, baselines, and experiment design."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import mean_absolute_error

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


problem = _load_module("problem_definition")
baselines = _load_module("baselines")
experiments = _load_module("experiment_design")


@pytest.fixture
def classification_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [f"c{index}" for index in range(20)],
            "event_at": pd.date_range(
                "2026-01-01",
                periods=20,
                freq="D",
                tz="UTC",
            ),
            "age": np.arange(20) + 20,
            "spend": np.linspace(10.0, 200.0, 20),
            "churned": [0, 1] * 10,
        }
    )


@pytest.fixture
def classification_problem():
    return problem.ProblemDefinition(
        name="customer-churn",
        task_type="binary_classification",
        target_column="churned",
        feature_columns=("age", "spend"),
        id_columns=("customer_id",),
        timestamp_column="event_at",
        positive_label=1,
    )


def test_problem_definition_requires_name() -> None:
    with pytest.raises(ValueError, match="name"):
        problem.ProblemDefinition(
            name="",
            task_type="regression",
            target_column="target",
            feature_columns=("feature",),
        )


def test_problem_definition_rejects_target_as_feature() -> None:
    with pytest.raises(ValueError, match="target_column"):
        problem.ProblemDefinition(
            name="bad",
            task_type="regression",
            target_column="target",
            feature_columns=("feature", "target"),
        )


def test_binary_problem_requires_positive_label() -> None:
    with pytest.raises(ValueError, match="positive_label"):
        problem.ProblemDefinition(
            name="binary",
            task_type="binary_classification",
            target_column="target",
            feature_columns=("feature",),
        )


def test_validate_frame_reports_schema_and_classes(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    report = classification_problem.validate_frame(classification_frame)
    assert report.rows == 20
    assert report.feature_count == 2
    assert report.target_missing_count == 0
    assert report.duplicate_entity_rows == 0
    assert report.target_classes == (0, 1)


def test_validate_frame_reports_missing_columns(classification_problem) -> None:
    with pytest.raises(ValueError, match="missing required columns"):
        classification_problem.validate_frame(pd.DataFrame({"age": [20]}))


def test_validate_frame_rejects_invalid_timestamp(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    frame = classification_frame.copy()
    frame["event_at"] = frame["event_at"].astype("object")
    frame.loc[0, "event_at"] = "bad"
    with pytest.raises(ValueError, match="invalid"):
        classification_problem.validate_frame(frame)


def test_validate_binary_requires_two_classes(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    frame = classification_frame.assign(churned=0)
    with pytest.raises(ValueError, match="exactly two"):
        classification_problem.validate_frame(frame)


def test_model_frame_selects_declared_columns(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    model_frame = classification_problem.model_frame(classification_frame)
    assert model_frame.columns.tolist() == ["age", "spend", "churned"]


def test_random_split_is_reproducible_and_stratified(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    first = classification_problem.split(
        classification_frame,
        strategy="random",
        test_size=0.25,
        random_state=7,
    )
    second = classification_problem.split(
        classification_frame,
        strategy="random",
        test_size=0.25,
        random_state=7,
    )
    assert first.evaluation.index.tolist() == second.evaluation.index.tolist()
    counts = first.evaluation["churned"].value_counts().to_dict()
    assert set(counts) == {0, 1}
    assert abs(counts[0] - counts[1]) == 1


def test_temporal_split_keeps_future_in_evaluation(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    split = classification_problem.split(
        classification_frame.sample(frac=1.0, random_state=3),
        strategy="temporal",
        test_size=0.2,
    )
    assert split.train["event_at"].max() < split.evaluation["event_at"].min()
    assert len(split.evaluation) == 4


def test_entity_split_has_no_overlap() -> None:
    frame = pd.DataFrame(
        {
            "customer_id": ["c1", "c1", "c2", "c2", "c3", "c3"],
            "x": range(6),
            "target": [0, 1, 0, 1, 0, 1],
        }
    )
    definition = problem.ProblemDefinition(
        name="repeat-events",
        task_type="binary_classification",
        target_column="target",
        feature_columns=("x",),
        id_columns=("customer_id",),
        positive_label=1,
    )
    split = definition.split(frame, strategy="entity", test_size=0.34, random_state=5)
    problem.assert_no_entity_overlap(split, ("customer_id",))


def test_overlap_check_detects_shared_entity() -> None:
    split = problem.DataSplit(
        train=pd.DataFrame({"id": ["a", "b"]}),
        evaluation=pd.DataFrame({"id": ["b", "c"]}),
        strategy="entity",
    )
    with pytest.raises(ValueError, match="overlap"):
        problem.assert_no_entity_overlap(split, ("id",))


def test_regression_mean_baseline() -> None:
    baseline = baselines.RegressionBaseline("mean").fit([1.0, 2.0, 6.0])
    assert baseline.predict(2).tolist() == pytest.approx([3.0, 3.0])


def test_regression_median_baseline_ignores_non_finite() -> None:
    baseline = baselines.RegressionBaseline("median").fit([1.0, np.nan, 9.0])
    assert baseline.predict(1).item() == pytest.approx(5.0)


def test_regression_baseline_requires_fit() -> None:
    with pytest.raises(RuntimeError, match="fit"):
        baselines.RegressionBaseline().predict(1)


def test_classification_majority_baseline() -> None:
    baseline = baselines.ClassificationBaseline("majority").fit(
        ["yes", "no", "yes"]
    )
    assert baseline.predict(3).tolist() == ["yes", "yes", "yes"]
    assert baseline.predict_proba(2).shape == (2, 2)
    assert baseline.predict_proba(2).sum(axis=1).tolist() == pytest.approx([1.0, 1.0])


def test_classification_prior_probabilities() -> None:
    baseline = baselines.ClassificationBaseline("prior").fit([0, 0, 0, 1])
    probabilities = baseline.predict_proba(2)
    assert probabilities[0].tolist() == pytest.approx([0.75, 0.25])


def test_regression_metrics_known_values() -> None:
    report = baselines.regression_metrics([1.0, 2.0], [1.0, 4.0])
    assert report.mae == pytest.approx(1.0)
    assert report.rmse == pytest.approx(np.sqrt(2.0))
    assert report.r2 == pytest.approx(-7.0)


def test_regression_metrics_reject_shape_mismatch() -> None:
    with pytest.raises(ValueError, match="same shape"):
        baselines.regression_metrics([1.0], [1.0, 2.0])


def test_binary_metrics_with_probabilities() -> None:
    report = baselines.binary_classification_metrics(
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        positive_label=1,
        positive_probabilities=[0.1, 0.6, 0.8, 0.9],
    )
    assert report.accuracy == pytest.approx(0.75)
    assert report.recall == pytest.approx(1.0)
    assert report.roc_auc == pytest.approx(1.0)
    assert report.log_loss is not None


def test_binary_metrics_validate_probability_range() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        baselines.binary_classification_metrics(
            [0, 1],
            [0, 1],
            positive_label=1,
            positive_probabilities=[0.1, 1.2],
        )


def test_experiment_config_validates_test_size() -> None:
    with pytest.raises(ValueError, match="test_size"):
        experiments.ExperimentConfig(name="bad", test_size=1.0)


def test_bootstrap_interval_is_reproducible() -> None:
    first = experiments.bootstrap_confidence_interval(
        [1.0, 2.0, 3.0, 4.0],
        resamples=200,
        random_state=9,
    )
    second = experiments.bootstrap_confidence_interval(
        [1.0, 2.0, 3.0, 4.0],
        resamples=200,
        random_state=9,
    )
    assert first == second
    assert first[0] <= 2.5 <= first[1]


def test_paired_bootstrap_difference_detects_better_prediction() -> None:
    truth = np.array([0.0, 1.0, 2.0, 3.0])
    prediction_a = truth.copy()
    prediction_b = np.zeros_like(truth)
    observed, lower, upper = experiments.paired_bootstrap_difference(
        truth,
        prediction_a,
        prediction_b,
        metric=mean_absolute_error,
        resamples=300,
        random_state=4,
    )
    assert observed < 0.0
    assert lower <= observed <= upper


def test_run_regression_baseline_experiment() -> None:
    frame = pd.DataFrame(
        {
            "row_id": [f"r{index}" for index in range(20)],
            "feature": np.arange(20),
            "target": np.linspace(10.0, 30.0, 20),
        }
    )
    definition = problem.ProblemDefinition(
        name="value-regression",
        task_type="regression",
        target_column="target",
        feature_columns=("feature",),
        id_columns=("row_id",),
    )
    configuration = experiments.ExperimentConfig(
        name="mean-baseline",
        primary_metric="mae",
    )
    result = experiments.run_baseline_experiment(
        frame,
        definition,
        configuration,
    )
    assert result.baseline_name == "mean"
    assert result.train_rows == 16
    assert result.evaluation_rows == 4
    assert set(result.metrics) == {"mae", "rmse", "r2"}


def test_run_binary_baseline_experiment(
    classification_frame: pd.DataFrame,
    classification_problem,
) -> None:
    configuration = experiments.ExperimentConfig(
        name="prior-baseline",
        test_size=0.3,
        primary_metric="balanced_accuracy",
        metric_direction="maximize",
    )
    result = experiments.run_baseline_experiment(
        classification_frame,
        classification_problem,
        configuration,
    )
    assert result.baseline_name == "class_prior"
    assert result.metrics["balanced_accuracy"] == pytest.approx(0.5)
    assert result.metrics["roc_auc"] == pytest.approx(0.5)


def test_experiment_result_json_round_trip(tmp_path: Path) -> None:
    result = experiments.ExperimentResult(
        experiment_name="baseline",
        problem_name="problem",
        task_type="regression",
        split_strategy="random",
        train_rows=8,
        evaluation_rows=2,
        baseline_name="mean",
        metrics={"mae": 1.25},
        random_state=42,
    )
    path = experiments.save_experiment_result(result, tmp_path / "result.json")
    assert experiments.load_experiment_result(path) == result
