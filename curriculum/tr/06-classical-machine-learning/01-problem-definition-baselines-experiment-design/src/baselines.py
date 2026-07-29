"""Transparent regression and classification baseline models and metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)

RegressionStrategy = Literal["mean", "median"]
ClassificationStrategy = Literal["majority", "prior"]


@dataclass(frozen=True)
class RegressionMetricReport:
    """Core regression metrics for one prediction vector."""

    mae: float
    rmse: float
    r2: float


@dataclass(frozen=True)
class ClassificationMetricReport:
    """Core binary-classification metrics for one prediction vector."""

    accuracy: float
    balanced_accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float | None
    log_loss: float | None


class RegressionBaseline:
    """Predict a training-set mean or median."""

    def __init__(self, strategy: RegressionStrategy = "mean") -> None:
        if strategy not in {"mean", "median"}:
            raise ValueError(f"unsupported regression strategy: {strategy}")
        self.strategy = strategy
        self.constant_: float | None = None

    def fit(self, y: np.ndarray | list[float]) -> "RegressionBaseline":
        values = np.asarray(y, dtype=float)
        finite = values[np.isfinite(values)]
        if finite.size == 0:
            raise ValueError("y must contain at least one finite value")
        if self.strategy == "mean":
            self.constant_ = float(np.mean(finite))
        else:
            self.constant_ = float(np.median(finite))
        return self

    def predict(self, row_count: int) -> np.ndarray:
        if self.constant_ is None:
            raise RuntimeError("fit must be called before predict")
        if row_count < 0:
            raise ValueError("row_count must be non-negative")
        return np.full(row_count, self.constant_, dtype=float)


class ClassificationBaseline:
    """Predict the majority class or training class priors."""

    def __init__(self, strategy: ClassificationStrategy = "majority") -> None:
        if strategy not in {"majority", "prior"}:
            raise ValueError(f"unsupported classification strategy: {strategy}")
        self.strategy = strategy
        self.classes_: np.ndarray | None = None
        self.class_probabilities_: np.ndarray | None = None
        self.majority_class_: object | None = None

    def fit(self, y: np.ndarray | list[object]) -> "ClassificationBaseline":
        values = np.asarray(y)
        if values.size == 0:
            raise ValueError("y must not be empty")
        if any(value is None for value in values):
            raise ValueError("y must not contain None")
        classes, counts = np.unique(values, return_counts=True)
        probabilities = counts.astype(float) / counts.sum()
        self.classes_ = classes
        self.class_probabilities_ = probabilities
        self.majority_class_ = classes[int(np.argmax(counts))]
        return self

    def predict(self, row_count: int) -> np.ndarray:
        if self.classes_ is None or self.majority_class_ is None:
            raise RuntimeError("fit must be called before predict")
        if row_count < 0:
            raise ValueError("row_count must be non-negative")
        if self.strategy == "majority":
            return np.full(
                row_count,
                self.majority_class_,
                dtype=self.classes_.dtype,
            )
        indices = np.argmax(self.class_probabilities_)
        return np.full(
            row_count,
            self.classes_[indices],
            dtype=self.classes_.dtype,
        )

    def predict_proba(self, row_count: int) -> np.ndarray:
        if self.class_probabilities_ is None:
            raise RuntimeError("fit must be called before predict_proba")
        if row_count < 0:
            raise ValueError("row_count must be non-negative")
        probabilities = self.class_probabilities_
        if self.strategy == "majority":
            probabilities = np.zeros_like(probabilities)
            probabilities[int(np.argmax(self.class_probabilities_))] = 1.0
        return np.tile(probabilities, (row_count, 1))


def regression_metrics(
    y_true: np.ndarray | list[float],
    y_pred: np.ndarray | list[float],
) -> RegressionMetricReport:
    """Calculate MAE, RMSE, and R² after validating aligned finite inputs."""

    truth = np.asarray(y_true, dtype=float)
    prediction = np.asarray(y_pred, dtype=float)
    if truth.shape != prediction.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if truth.size == 0:
        raise ValueError("metric inputs must not be empty")
    if not np.isfinite(truth).all() or not np.isfinite(prediction).all():
        raise ValueError("metric inputs must be finite")
    return RegressionMetricReport(
        mae=float(mean_absolute_error(truth, prediction)),
        rmse=float(np.sqrt(mean_squared_error(truth, prediction))),
        r2=float(r2_score(truth, prediction)),
    )


def binary_classification_metrics(
    y_true: np.ndarray | list[object],
    y_pred: np.ndarray | list[object],
    *,
    positive_label: object,
    positive_probabilities: np.ndarray | list[float] | None = None,
) -> ClassificationMetricReport:
    """Calculate threshold and probability metrics for binary classification."""

    truth = np.asarray(y_true)
    prediction = np.asarray(y_pred)
    if truth.shape != prediction.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if truth.size == 0:
        raise ValueError("metric inputs must not be empty")
    labels = np.unique(truth)
    if labels.size != 2:
        raise ValueError("binary metrics require exactly two observed classes")
    if positive_label not in labels:
        raise ValueError("positive_label is absent from y_true")

    probability_auc: float | None = None
    probability_log_loss: float | None = None
    if positive_probabilities is not None:
        probabilities = np.asarray(positive_probabilities, dtype=float)
        if probabilities.shape != truth.shape:
            raise ValueError("positive_probabilities must match y_true shape")
        if not np.isfinite(probabilities).all():
            raise ValueError("probabilities must be finite")
        if ((probabilities < 0.0) | (probabilities > 1.0)).any():
            raise ValueError("probabilities must be between 0 and 1")
        binary_truth = (truth == positive_label).astype(int)
        probability_auc = float(roc_auc_score(binary_truth, probabilities))
        probability_log_loss = float(log_loss(binary_truth, probabilities))

    return ClassificationMetricReport(
        accuracy=float(accuracy_score(truth, prediction)),
        balanced_accuracy=float(balanced_accuracy_score(truth, prediction)),
        precision=float(
            precision_score(
                truth,
                prediction,
                pos_label=positive_label,
                zero_division=0,
            )
        ),
        recall=float(
            recall_score(
                truth,
                prediction,
                pos_label=positive_label,
                zero_division=0,
            )
        ),
        f1=float(
            f1_score(
                truth,
                prediction,
                pos_label=positive_label,
                zero_division=0,
            )
        ),
        roc_auc=probability_auc,
        log_loss=probability_log_loss,
    )
