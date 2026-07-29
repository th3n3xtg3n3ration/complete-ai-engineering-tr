from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import pytest

BASE = Path(__file__).resolve().parents[1] / "src"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, BASE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lt = load_module("linear_transformations", "linear_transformations.py")
pi = load_module("power_iteration", "power_iteration.py")
pca = load_module("pca_from_scratch", "pca_from_scratch.py")


def test_rotation_preserves_norm() -> None:
    vector = [3.0, 4.0]
    rotated = lt.matrix_vector_multiply(lt.rotation_matrix(math.pi / 3), vector)
    assert lt.l2_norm(rotated) == pytest.approx(5.0)


def test_projection_residual_is_orthogonal() -> None:
    projected = lt.projection([3.0, 4.0], [1.0, 1.0])
    residual = lt.residual([3.0, 4.0], projected)
    assert lt.dot(projected, residual) == pytest.approx(0.0, abs=1e-10)


def test_projection_matrix_matches_projection() -> None:
    direction = [1.0, 2.0]
    vector = [4.0, -1.0]
    expected = lt.projection(vector, direction)
    actual = lt.matrix_vector_multiply(lt.projection_matrix(direction), vector)
    assert actual == pytest.approx(expected)


def test_zero_direction_rejected() -> None:
    with pytest.raises(ValueError):
        lt.projection([1.0, 2.0], [0.0, 0.0])


def test_matrix_vector_shape_validation() -> None:
    with pytest.raises(ValueError):
        lt.matrix_vector_multiply([[1.0, 2.0]], [1.0])


def test_power_iteration_finds_dominant_eigenvalue() -> None:
    result = pi.power_iteration([[4.0, 1.0], [1.0, 3.0]])
    assert result.converged
    assert result.value == pytest.approx((7.0 + math.sqrt(5.0)) / 2.0, rel=1e-7)


def test_power_iteration_vector_satisfies_equation() -> None:
    matrix = [[4.0, 1.0], [1.0, 3.0]]
    result = pi.power_iteration(matrix)
    multiplied = [sum(a * b for a, b in zip(row, result.vector, strict=True)) for row in matrix]
    scaled = [result.value * value for value in result.vector]
    assert multiplied == pytest.approx(scaled, rel=1e-7, abs=1e-7)


def test_power_iteration_rejects_non_square_matrix() -> None:
    with pytest.raises(ValueError):
        pi.power_iteration([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


def test_covariance_matrix_is_symmetric() -> None:
    covariance = pca.covariance_matrix([[1.0, 2.0], [2.0, 3.0], [4.0, 8.0]])
    assert covariance[0][1] == pytest.approx(covariance[1][0])


def test_pca_reduces_dimension() -> None:
    data = [[1.0, 1.1], [2.0, 2.1], [3.0, 2.9], [4.0, 4.2]]
    model = pca.fit_pca(data, 1)
    reduced = pca.transform(data, model)
    assert len(reduced) == len(data)
    assert all(len(row) == 1 for row in reduced)


def test_pca_explained_variance_is_bounded() -> None:
    data = [[1.0, 1.0], [2.0, 2.0], [3.0, 3.1], [4.0, 4.0]]
    model = pca.fit_pca(data, 1)
    assert 0.0 <= model.explained_variance_ratio[0] <= 1.0
    assert model.explained_variance_ratio[0] > 0.99


def test_full_component_reconstruction_is_near_exact() -> None:
    data = [[1.0, 2.0], [2.0, 1.0], [3.0, 4.0], [4.0, 3.0]]
    model = pca.fit_pca(data, 2)
    reconstructed = pca.inverse_transform(pca.transform(data, model), model)
    assert pca.reconstruction_error(data, reconstructed) < 1e-10


def test_invalid_component_count_rejected() -> None:
    with pytest.raises(ValueError):
        pca.fit_pca([[1.0, 2.0], [2.0, 3.0]], 3)


def test_ragged_data_rejected() -> None:
    with pytest.raises(ValueError):
        pca.fit_pca([[1.0, 2.0], [3.0]], 1)
