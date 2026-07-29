"""Leakage-safe SVM pipeline helpers."""

from __future__ import annotations
from typing import Sequence
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC

def build_preprocessor(numeric_features: Sequence[str], categorical_features: Sequence[str]) -> ColumnTransformer:
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))])
    return ColumnTransformer([("numeric", numeric, list(numeric_features)), ("categorical", categorical, list(categorical_features))], remainder="drop")

def build_svm_pipeline(numeric_features: Sequence[str], categorical_features: Sequence[str], *, c: float = 1.0, kernel: str = "rbf", gamma: str | float = "scale", class_weight=None, probability: bool = False, random_state: int = 42) -> Pipeline:
    if c <= 0:
        raise ValueError("c must be positive")
    return Pipeline([("preprocessor", build_preprocessor(numeric_features, categorical_features)), ("model", SVC(C=c, kernel=kernel, gamma=gamma, class_weight=class_weight, probability=probability, random_state=random_state))])

def build_svm_grid_search(pipeline: Pipeline, *, cv: int = 3, scoring: str = "average_precision", n_jobs: int | None = None) -> GridSearchCV:
    if cv < 2:
        raise ValueError("cv must be at least 2")
    grid = [{"model__kernel": ["linear"], "model__C": [0.1, 1.0, 10.0]}, {"model__kernel": ["rbf"], "model__C": [0.1, 1.0, 10.0], "model__gamma": ["scale", 0.1, 1.0]}]
    return GridSearchCV(pipeline, grid, scoring=scoring, cv=cv, n_jobs=n_jobs, refit=True)
