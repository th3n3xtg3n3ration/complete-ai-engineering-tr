"""Reusable clustering, anomaly-detection and PCA helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.typing import ArrayLike, NDArray
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class ClusterMetrics:
    """Internal clustering metrics for a fitted partition."""

    silhouette: float
    davies_bouldin: float
    n_clusters: int


def _as_2d_float_array(values: ArrayLike) -> NDArray[np.float64]:
    array = np.asarray(values, dtype=float)
    if array.ndim != 2:
        raise ValueError("Input must be a two-dimensional array.")
    if array.shape[0] < 2 or array.shape[1] < 1:
        raise ValueError("Input must contain at least two rows and one feature.")
    if not np.isfinite(array).all():
        raise ValueError("Input contains NaN or infinite values.")
    return array


def build_kmeans_pipeline(
    n_clusters: int,
    *,
    random_state: int = 42,
    n_init: int = 20,
    pca_components: int | float | None = None,
) -> Pipeline:
    """Create a scaling-safe K-Means pipeline with optional PCA."""
    if n_clusters < 2:
        raise ValueError("n_clusters must be at least 2.")
    if n_init < 1:
        raise ValueError("n_init must be positive.")

    steps: list[tuple[str, object]] = [("scale", StandardScaler())]
    if pca_components is not None:
        steps.append(("pca", PCA(n_components=pca_components, svd_solver="full")))
    steps.append(
        (
            "cluster",
            KMeans(
                n_clusters=n_clusters,
                n_init=n_init,
                random_state=random_state,
            ),
        )
    )
    return Pipeline(steps)


def evaluate_partition(values: ArrayLike, labels: Iterable[int]) -> ClusterMetrics:
    """Calculate internal metrics after excluding DBSCAN noise labels."""
    array = _as_2d_float_array(values)
    label_array = np.asarray(list(labels))
    if label_array.shape != (array.shape[0],):
        raise ValueError("labels must contain one value per row.")

    keep = label_array != -1
    filtered_values = array[keep]
    filtered_labels = label_array[keep]
    unique = np.unique(filtered_labels)

    if unique.size < 2 or filtered_values.shape[0] <= unique.size:
        raise ValueError("At least two non-noise clusters with enough samples are required.")

    return ClusterMetrics(
        silhouette=float(silhouette_score(filtered_values, filtered_labels)),
        davies_bouldin=float(davies_bouldin_score(filtered_values, filtered_labels)),
        n_clusters=int(unique.size),
    )


def fit_dbscan(
    values: ArrayLike,
    *,
    eps: float,
    min_samples: int = 5,
    scale: bool = True,
) -> tuple[NDArray[np.int_], NDArray[np.float64]]:
    """Fit DBSCAN and return labels plus the representation used by the model."""
    array = _as_2d_float_array(values)
    if eps <= 0:
        raise ValueError("eps must be positive.")
    if min_samples < 2:
        raise ValueError("min_samples must be at least 2.")

    transformed = StandardScaler().fit_transform(array) if scale else array
    labels = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(transformed)
    return labels, np.asarray(transformed, dtype=float)


def fit_isolation_forest(
    values: ArrayLike,
    *,
    contamination: float | str = "auto",
    random_state: int = 42,
) -> tuple[IsolationForest, NDArray[np.float64]]:
    """Fit Isolation Forest and return scores where lower means more anomalous."""
    array = _as_2d_float_array(values)
    model = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=random_state,
    )
    model.fit(array)
    scores = model.score_samples(array)
    return model, np.asarray(scores, dtype=float)


def threshold_by_review_capacity(scores: ArrayLike, review_fraction: float) -> float:
    """Choose a lower-tail anomaly threshold for a fixed review capacity."""
    array = np.asarray(scores, dtype=float)
    if array.ndim != 1 or array.size == 0:
        raise ValueError("scores must be a non-empty one-dimensional array.")
    if not np.isfinite(array).all():
        raise ValueError("scores contain NaN or infinite values.")
    if not 0 < review_fraction < 1:
        raise ValueError("review_fraction must be between 0 and 1.")
    return float(np.quantile(array, review_fraction))
