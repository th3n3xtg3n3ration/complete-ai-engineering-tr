"""Leakage-safe scikit-learn pipelines and regression model comparison."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler

from regression_diagnostics import regression_metrics


@dataclass(frozen=True)
class ModelEvaluation:
    """Evaluation record for one fitted regression pipeline."""

    model_name: str
    mae: float
    rmse: float
    r2: float
    adjusted_r2: float | None


def build_preprocessor(
    numeric_columns: Sequence[str],
    categorical_columns: Sequence[str],
) -> ColumnTransformer:
    """Build a leakage-safe numeric and categorical preprocessor."""

    numeric = list(numeric_columns)
    categorical = list(categorical_columns)
    if not numeric and not categorical:
        raise ValueError("at least one feature column is required")
    if set(numeric) & set(categorical):
        raise ValueError("numeric and categorical columns must not overlap")

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric),
            ("categorical", categorical_pipeline, categorical),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def build_regression_pipeline(
    numeric_columns: Sequence[str],
    categorical_columns: Sequence[str],
    *,
    model_name: str = "ridge",
    alpha: float = 1.0,
    l1_ratio: float = 0.5,
    polynomial_degree: int = 1,
    random_state: int = 42,
) -> Pipeline:
    """Create a preprocessing and regression pipeline."""

    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    if not 0 <= l1_ratio <= 1:
        raise ValueError("l1_ratio must be between zero and one")
    if polynomial_degree <= 0:
        raise ValueError("polynomial_degree must be positive")

    preprocessor = build_preprocessor(numeric_columns, categorical_columns)
    if model_name == "linear":
        estimator = LinearRegression()
    elif model_name == "ridge":
        estimator = Ridge(alpha=alpha)
    elif model_name == "lasso":
        estimator = Lasso(alpha=alpha, max_iter=20_000, random_state=random_state)
    elif model_name == "elastic_net":
        estimator = ElasticNet(
            alpha=alpha,
            l1_ratio=l1_ratio,
            max_iter=20_000,
            random_state=random_state,
        )
    else:
        raise ValueError(f"unsupported model_name: {model_name}")

    steps: list[tuple[str, object]] = [("preprocessor", preprocessor)]
    if polynomial_degree > 1:
        steps.append(
            (
                "polynomial",
                PolynomialFeatures(
                    degree=polynomial_degree,
                    include_bias=False,
                ),
            )
        )
    steps.append(("model", estimator))
    return Pipeline(steps=steps)


def evaluate_pipeline(
    pipeline: Pipeline,
    X_train: pd.DataFrame,
    y_train: object,
    X_evaluation: pd.DataFrame,
    y_evaluation: object,
    *,
    model_name: str,
) -> ModelEvaluation:
    """Fit a pipeline and return evaluation metrics."""

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_evaluation)
    feature_count = len(pipeline[:-1].get_feature_names_out())
    metrics = regression_metrics(
        y_evaluation,
        predictions,
        feature_count=feature_count,
    )
    return ModelEvaluation(
        model_name=model_name,
        mae=metrics.mae,
        rmse=metrics.rmse,
        r2=metrics.r2,
        adjusted_r2=metrics.adjusted_r2,
    )


def compare_models(
    models: Mapping[str, Pipeline],
    X_train: pd.DataFrame,
    y_train: object,
    X_evaluation: pd.DataFrame,
    y_evaluation: object,
) -> pd.DataFrame:
    """Fit configured models and return a comparison table."""

    if not models:
        raise ValueError("models must not be empty")
    evaluations = [
        evaluate_pipeline(
            pipeline,
            X_train,
            y_train,
            X_evaluation,
            y_evaluation,
            model_name=name,
        )
        for name, pipeline in models.items()
    ]
    return pd.DataFrame(
        [evaluation.__dict__ for evaluation in evaluations]
    ).sort_values(["rmse", "mae", "model_name"]).reset_index(drop=True)


def cross_validation_report(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: object,
    *,
    folds: int = 5,
    random_state: int = 42,
) -> dict[str, float]:
    """Return mean and standard deviation of CV MAE, RMSE, and R²."""

    if folds < 2:
        raise ValueError("folds must be at least two")
    splitter = KFold(n_splits=folds, shuffle=True, random_state=random_state)
    scores = cross_validate(
        pipeline,
        X,
        y,
        cv=splitter,
        scoring={
            "mae": "neg_mean_absolute_error",
            "rmse": "neg_root_mean_squared_error",
            "r2": "r2",
        },
        n_jobs=None,
    )
    return {
        "mae_mean": float(-np.mean(scores["test_mae"])),
        "mae_std": float(np.std(-scores["test_mae"], ddof=0)),
        "rmse_mean": float(-np.mean(scores["test_rmse"])),
        "rmse_std": float(np.std(-scores["test_rmse"], ddof=0)),
        "r2_mean": float(np.mean(scores["test_r2"])),
        "r2_std": float(np.std(scores["test_r2"], ddof=0)),
    }


if __name__ == "__main__":
    print("Import this module to build leakage-safe regression pipelines.")
