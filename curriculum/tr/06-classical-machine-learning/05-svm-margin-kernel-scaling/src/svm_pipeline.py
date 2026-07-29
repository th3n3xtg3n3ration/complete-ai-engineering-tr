"""Leakage-safe preprocessing and model-selection utilities for SVM."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC


def build_preprocessor(
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
) -> ColumnTransformer:
    """Build a mixed-type preprocessor that is safe to fit inside CV folds."""
    if not numeric_features and not categorical_features:
        raise ValueError("at least one feature must be provided")
    overlap = set(numeric_features).intersection(categorical_features)
    if overlap:
        raise ValueError(f"features cannot be both numeric and categorical: {overlap}")

    transformers: list[tuple[str, Pipeline, list[str]]] = []
    if numeric_features:
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("numeric", numeric_pipeline, list(numeric_features)))
    if categorical_features:
        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )
        transformers.append(
            ("categorical", categorical_pipeline, list(categorical_features))
        )
    return ColumnTransformer(transformers=transformers, remainder="drop")


def build_svm_pipeline(
    numeric_features: Sequence[str],
    categorical_features: Sequence[str],
    *,
    c: float = 1.0,
    kernel: str = "rbf",
    gamma: str | float = "scale",
    degree: int = 3,
    coef0: float = 0.0,
    class_weight: str | dict[int, float] | None = None,
    probability: bool = False,
    random_state: int = 42,
) -> Pipeline:
    """Build preprocessing and SVC as one leakage-safe pipeline."""
    if c <= 0:
        raise ValueError("c must be positive")
    if degree < 1:
        raise ValueError("degree must be at least 1")
    if isinstance(gamma, (int, float)) and gamma <= 0:
        raise ValueError("numeric gamma must be positive")
    model = SVC(
        C=c,
        kernel=kernel,
        gamma=gamma,
        degree=degree,
        coef0=coef0,
        class_weight=class_weight,
        probability=probability,
        random_state=random_state,
        cache_size=512.0,
    )
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(numeric_features, categorical_features)),
            ("model", model),
        ]
    )


def default_svm_parameter_grid() -> list[dict[str, object]]:
    """Return a compact but meaningful joint kernel search space."""
    return [
        {
            "model__kernel": ["linear"],
            "model__C": [0.01, 0.1, 1.0, 10.0, 100.0],
        },
        {
            "model__kernel": ["rbf"],
            "model__C": [0.01, 0.1, 1.0, 10.0, 100.0],
            "model__gamma": [0.001, 0.01, 0.1, 1.0, "scale"],
        },
        {
            "model__kernel": ["poly"],
            "model__C": [0.1, 1.0, 10.0],
            "model__gamma": ["scale", 0.01, 0.1],
            "model__degree": [2, 3],
            "model__coef0": [0.0, 1.0],
        },
    ]


def build_svm_grid_search(
    pipeline: Pipeline,
    *,
    cv: int | StratifiedKFold = 5,
    scoring: str = "average_precision",
    n_jobs: int | None = None,
    parameter_grid: list[dict[str, object]] | None = None,
) -> GridSearchCV:
    """Build a refitting grid search over kernel-specific parameters."""
    if isinstance(cv, int) and cv < 2:
        raise ValueError("cv must be at least 2")
    grid = default_svm_parameter_grid() if parameter_grid is None else parameter_grid
    if not grid:
        raise ValueError("parameter_grid must not be empty")
    return GridSearchCV(
        estimator=pipeline,
        param_grid=grid,
        scoring=scoring,
        cv=cv,
        n_jobs=n_jobs,
        refit=True,
        return_train_score=True,
    )


def run_nested_cv(
    search: GridSearchCV,
    x,
    y,
    *,
    outer_splits: int = 5,
    scoring: Sequence[str] = ("roc_auc", "average_precision", "balanced_accuracy"),
    random_state: int = 42,
    n_jobs: int | None = None,
) -> dict[str, np.ndarray]:
    """Evaluate a hyperparameter search with an outer stratified CV loop."""
    if outer_splits < 2:
        raise ValueError("outer_splits must be at least 2")
    outer_cv = StratifiedKFold(
        n_splits=outer_splits,
        shuffle=True,
        random_state=random_state,
    )
    result = cross_validate(
        search,
        x,
        y,
        cv=outer_cv,
        scoring=list(scoring),
        n_jobs=n_jobs,
        return_train_score=False,
        return_estimator=False,
        error_score="raise",
    )
    return {key: np.asarray(value) for key, value in result.items()}
