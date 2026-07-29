"""Reproducible experiment configuration, uncertainty, and baseline runners."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd

from baselines import (
    ClassificationBaseline,
    RegressionBaseline,
    binary_classification_metrics,
    regression_metrics,
)
from problem_definition import ProblemDefinition, SplitStrategy

MetricDirection = Literal["maximize", "minimize"]


@dataclass(frozen=True)
class ExperimentConfig:
    """Reproducibility and decision settings for one experiment."""

    name: str
    split_strategy: SplitStrategy = "random"
    test_size: float = 0.2
    random_state: int = 42
    primary_metric: str = "mae"
    metric_direction: MetricDirection = "minimize"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if self.split_strategy not in {"random", "temporal", "entity"}:
            raise ValueError(f"unsupported split strategy: {self.split_strategy}")
        if not 0.0 < self.test_size < 1.0:
            raise ValueError("test_size must be between 0 and 1")
        if self.metric_direction not in {"maximize", "minimize"}:
            raise ValueError(f"unsupported metric_direction: {self.metric_direction}")
        if not self.primary_metric.strip():
            raise ValueError("primary_metric must not be empty")


@dataclass(frozen=True)
class ExperimentResult:
    """Serializable baseline result and dataset diagnostics."""

    experiment_name: str
    problem_name: str
    task_type: str
    split_strategy: str
    train_rows: int
    evaluation_rows: int
    baseline_name: str
    metrics: dict[str, float | None]
    random_state: int


def bootstrap_confidence_interval(
    values: np.ndarray | list[float],
    *,
    statistic: Callable[[np.ndarray], float] = np.mean,
    confidence: float = 0.95,
    resamples: int = 2_000,
    random_state: int = 42,
) -> tuple[float, float]:
    """Return a percentile bootstrap confidence interval for a 1-D sample."""

    sample = np.asarray(values, dtype=float)
    if sample.ndim != 1 or sample.size == 0:
        raise ValueError("values must be a non-empty 1-D array")
    if not np.isfinite(sample).all():
        raise ValueError("values must be finite")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if resamples <= 0:
        raise ValueError("resamples must be positive")

    rng = np.random.default_rng(random_state)
    statistics = np.empty(resamples, dtype=float)
    for index in range(resamples):
        resample = rng.choice(sample, size=sample.size, replace=True)
        statistics[index] = float(statistic(resample))
    alpha = 1.0 - confidence
    return (
        float(np.quantile(statistics, alpha / 2.0)),
        float(np.quantile(statistics, 1.0 - alpha / 2.0)),
    )


def paired_bootstrap_difference(
    y_true: np.ndarray | list[float],
    prediction_a: np.ndarray | list[float],
    prediction_b: np.ndarray | list[float],
    *,
    metric: Callable[[np.ndarray, np.ndarray], float],
    confidence: float = 0.95,
    resamples: int = 2_000,
    random_state: int = 42,
) -> tuple[float, float, float]:
    """Estimate metric(A)-metric(B) and its paired bootstrap interval."""

    truth = np.asarray(y_true)
    first = np.asarray(prediction_a)
    second = np.asarray(prediction_b)
    if truth.shape != first.shape or truth.shape != second.shape:
        raise ValueError("all arrays must have the same shape")
    if truth.ndim != 1 or truth.size == 0:
        raise ValueError("arrays must be non-empty and one-dimensional")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if resamples <= 0:
        raise ValueError("resamples must be positive")

    observed = float(metric(truth, first) - metric(truth, second))
    rng = np.random.default_rng(random_state)
    differences = np.empty(resamples, dtype=float)
    indices = np.arange(truth.size)
    for index in range(resamples):
        sampled = rng.choice(indices, size=indices.size, replace=True)
        differences[index] = float(
            metric(truth[sampled], first[sampled])
            - metric(truth[sampled], second[sampled])
        )
    alpha = 1.0 - confidence
    return (
        observed,
        float(np.quantile(differences, alpha / 2.0)),
        float(np.quantile(differences, 1.0 - alpha / 2.0)),
    )


def run_baseline_experiment(
    frame: pd.DataFrame,
    definition: ProblemDefinition,
    config: ExperimentConfig,
) -> ExperimentResult:
    """Split the dataset, fit a transparent baseline, and calculate metrics."""

    split = definition.split(
        frame,
        strategy=config.split_strategy,
        test_size=config.test_size,
        random_state=config.random_state,
    )
    train_target = split.train[definition.target_column]
    evaluation_target = split.evaluation[definition.target_column]

    if definition.task_type == "regression":
        baseline = RegressionBaseline("mean").fit(train_target.to_numpy())
        predictions = baseline.predict(len(split.evaluation))
        report = regression_metrics(evaluation_target.to_numpy(), predictions)
        metrics: dict[str, float | None] = {
            "mae": report.mae,
            "rmse": report.rmse,
            "r2": report.r2,
        }
        baseline_name = "mean"
    elif definition.task_type == "binary_classification":
        baseline = ClassificationBaseline("prior").fit(train_target.to_numpy())
        predictions = baseline.predict(len(split.evaluation))
        probabilities = baseline.predict_proba(len(split.evaluation))
        class_index = list(baseline.classes_).index(definition.positive_label)
        report = binary_classification_metrics(
            evaluation_target.to_numpy(),
            predictions,
            positive_label=definition.positive_label,
            positive_probabilities=probabilities[:, class_index],
        )
        metrics = {
            "accuracy": report.accuracy,
            "balanced_accuracy": report.balanced_accuracy,
            "precision": report.precision,
            "recall": report.recall,
            "f1": report.f1,
            "roc_auc": report.roc_auc,
            "log_loss": report.log_loss,
        }
        baseline_name = "class_prior"
    else:
        baseline = ClassificationBaseline("majority").fit(train_target.to_numpy())
        predictions = baseline.predict(len(split.evaluation))
        accuracy = float(np.mean(predictions == evaluation_target.to_numpy()))
        metrics = {"accuracy": accuracy}
        baseline_name = "majority"

    if config.primary_metric not in metrics:
        raise ValueError(
            f"primary_metric is unavailable for task: {config.primary_metric}"
        )
    return ExperimentResult(
        experiment_name=config.name,
        problem_name=definition.name,
        task_type=definition.task_type,
        split_strategy=config.split_strategy,
        train_rows=len(split.train),
        evaluation_rows=len(split.evaluation),
        baseline_name=baseline_name,
        metrics=metrics,
        random_state=config.random_state,
    )


def save_experiment_result(
    result: ExperimentResult,
    path: str | Path,
) -> Path:
    """Write a stable JSON experiment record."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(asdict(result), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return output


def load_experiment_result(path: str | Path) -> ExperimentResult:
    """Load a previously written experiment record."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return ExperimentResult(**data)


if __name__ == "__main__":
    demo = pd.DataFrame(
        {
            "customer_id": [f"c{index}" for index in range(20)],
            "age": np.arange(20) + 20,
            "monthly_spend": np.linspace(50, 250, 20),
            "churned": [0] * 14 + [1] * 6,
        }
    )
    problem = ProblemDefinition(
        name="customer-churn",
        task_type="binary_classification",
        target_column="churned",
        feature_columns=("age", "monthly_spend"),
        id_columns=("customer_id",),
        positive_label=1,
    )
    configuration = ExperimentConfig(
        name="churn-prior-baseline",
        primary_metric="balanced_accuracy",
        metric_direction="maximize",
    )
    print(run_baseline_experiment(demo, problem, configuration))
