"""Leakage-safe classification pipelines and probability calibration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike, NDArray
from sklearn.base import BaseEstimator, clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from classification_metrics import (
    calibration_table,
    classification_metrics,
    expected_calibration_error,
    threshold_table,
)

CalibrationMethod = Literal["sigmoid", "isotonic"]


@dataclass(frozen=True)
class ClassifierEvaluation:
    """Serializable classifier evaluation result."""

    metrics: dict[str, float]
    expected_calibration_error: float
    threshold_rows: int
    calibration_bins: int


def build_classifier_pipeline(
    *,
    numeric_features: list[str],
    categorical_features: list[str],
    c: float = 1.0,
    penalty: Literal["l1", "l2"] = "l2",
    class_weight: Literal["balanced"] | dict[int, float] | None = None,
    max_iter: int = 2_000,
) -> Pipeline:
    """Build a preprocessing and logistic-regression pipeline."""

    if not numeric_features and not categorical_features:
        raise ValueError("at least one feature is required")
    if set(numeric_features).intersection(categorical_features):
        raise ValueError("numeric and categorical features must be disjoint")
    if c <= 0:
        raise ValueError("c must be positive")
    if penalty not in {"l1", "l2"}:
        raise ValueError("penalty must be l1 or l2")
    transformers: list[tuple[str, Pipeline, list[str]]] = []
    if numeric_features:
        numeric_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("numeric", numeric_pipeline, numeric_features))
    if categorical_features:
        categorical_pipeline = Pipeline(
            [
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "encoder",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                ),
            ]
        )
        transformers.append(("categorical", categorical_pipeline, categorical_features))
    preprocessor = ColumnTransformer(transformers=transformers)
    solver = "liblinear" if penalty == "l1" else "lbfgs"
    model = LogisticRegression(
        C=c,
        penalty=penalty,
        class_weight=class_weight,
        max_iter=max_iter,
        solver=solver,
        random_state=42,
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def calibrate_classifier(
    estimator: BaseEstimator,
    features: pd.DataFrame,
    target: ArrayLike,
    *,
    method: CalibrationMethod = "sigmoid",
    cv: int = 5,
) -> CalibratedClassifierCV:
    """Clone and calibrate an estimator using cross-validation."""

    if method not in {"sigmoid", "isotonic"}:
        raise ValueError("method must be sigmoid or isotonic")
    if cv < 2:
        raise ValueError("cv must be at least 2")
    labels = np.asarray(target, dtype=int).reshape(-1)
    if features.shape[0] != labels.size:
        raise ValueError("features and target must have equal row counts")
    calibrated = CalibratedClassifierCV(
        estimator=clone(estimator),
        method=method,
        cv=cv,
    )
    calibrated.fit(features, labels)
    return calibrated


def positive_probabilities(
    estimator: BaseEstimator,
    features: pd.DataFrame,
) -> NDArray[np.float64]:
    """Return validated positive-class probabilities."""

    probabilities = np.asarray(estimator.predict_proba(features), dtype=float)
    if probabilities.ndim != 2 or probabilities.shape[1] != 2:
        raise ValueError("estimator must return two-class probabilities")
    positive = probabilities[:, 1]
    if not np.isfinite(positive).all() or np.any((positive < 0) | (positive > 1)):
        raise ValueError("estimator returned invalid probabilities")
    return positive


def evaluate_classifier(
    estimator: BaseEstimator,
    features: pd.DataFrame,
    target: ArrayLike,
    *,
    threshold: float = 0.5,
    n_bins: int = 10,
) -> ClassifierEvaluation:
    """Evaluate discrimination, decision threshold, and calibration."""

    labels = np.asarray(target, dtype=int).reshape(-1)
    probabilities = positive_probabilities(estimator, features)
    metrics = classification_metrics(labels, probabilities, threshold=threshold)
    reliability = calibration_table(labels, probabilities, n_bins=n_bins)
    thresholds = threshold_table(labels, probabilities)
    return ClassifierEvaluation(
        metrics=metrics,
        expected_calibration_error=expected_calibration_error(reliability),
        threshold_rows=len(thresholds),
        calibration_bins=len(reliability),
    )
