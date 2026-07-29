from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from embedding_experiment import DOCUMENTS, QUERY, rank_embeddings  # noqa: E402
from linear_algebra import (  # noqa: E402
    add_bias,
    cosine_similarity,
    dot,
    euclidean_distance,
    flatten_tensor,
    infinity_norm,
    l1_norm,
    l2_norm,
    matrix_add,
    matrix_multiply,
    matrix_vector_multiply,
    mean_vector,
    normalize,
    outer_product,
    reshape,
    scalar_multiply,
    tensor_shape,
    transpose,
    vector_add,
    vector_subtract,
)


def test_vector_arithmetic() -> None:
    assert vector_add([1, 2, 3], [4, 5, 6]) == [5.0, 7.0, 9.0]
    assert vector_subtract([5, 7], [2, 3]) == [3.0, 4.0]
    assert scalar_multiply(2, [1, -3]) == [2.0, -6.0]


def test_vector_size_mismatch_is_rejected() -> None:
    with pytest.raises(ValueError, match="same length"):
        vector_add([1, 2], [1])

    with pytest.raises(ValueError, match="same length"):
        dot([1, 2], [1])


def test_dot_and_outer_product() -> None:
    assert dot([1, 2, 3], [4, 5, 6]) == pytest.approx(32.0)
    assert outer_product([1, 2], [3, 4]) == [[3.0, 4.0], [6.0, 8.0]]


def test_norms() -> None:
    vector = [-3, 4]
    assert l1_norm(vector) == pytest.approx(7.0)
    assert l2_norm(vector) == pytest.approx(5.0)
    assert infinity_norm(vector) == pytest.approx(4.0)


def test_normalize_produces_unit_vector() -> None:
    result = normalize([3, 4])
    assert result == pytest.approx([0.6, 0.8])
    assert l2_norm(result) == pytest.approx(1.0)


def test_zero_vector_operations_are_rejected() -> None:
    with pytest.raises(ValueError, match="zero"):
        normalize([0, 0, 0])

    with pytest.raises(ValueError, match="zero"):
        cosine_similarity([1, 0], [0, 0])


def test_distance_and_similarity() -> None:
    assert euclidean_distance([0, 0], [3, 4]) == pytest.approx(5.0)
    assert cosine_similarity([1, 0], [1, 0]) == pytest.approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)
    assert cosine_similarity([1, 0], [-1, 0]) == pytest.approx(-1.0)


def test_transpose_and_matrix_addition() -> None:
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [
        [1.0, 4.0],
        [2.0, 5.0],
        [3.0, 6.0],
    ]
    assert matrix_add([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [
        [6.0, 8.0],
        [10.0, 12.0],
    ]


def test_matrix_multiplication() -> None:
    assert matrix_multiply([[1, 2], [3, 4]], [[2, 0], [1, 2]]) == [
        [4.0, 4.0],
        [10.0, 8.0],
    ]
    assert matrix_vector_multiply([[1, 2], [3, 4]], [5, 6]) == [17.0, 39.0]


def test_invalid_matrix_shapes_are_rejected() -> None:
    with pytest.raises(ValueError, match="rectangular"):
        transpose([[1, 2], [3]])

    with pytest.raises(ValueError, match="left columns"):
        matrix_multiply([[1, 2, 3]], [[1, 2], [3, 4]])


def test_bias_and_mean_vector() -> None:
    assert add_bias([[1, 2], [3, 4]], [0.5, -0.5]) == [
        [1.5, 1.5],
        [3.5, 3.5],
    ]
    assert mean_vector([[1, 2], [3, 4], [5, 6]]) == pytest.approx([3.0, 4.0])


def test_tensor_shape_and_flatten() -> None:
    tensor = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
    assert tensor_shape(tensor) == (2, 2, 2)
    assert flatten_tensor(tensor) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]


def test_ragged_tensor_is_rejected() -> None:
    with pytest.raises(ValueError, match="rectangular"):
        tensor_shape([[1, 2], [3]])


def test_reshape_round_trip() -> None:
    values = [1, 2, 3, 4, 5, 6]
    reshaped = reshape(values, (2, 3))
    assert reshaped == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    assert flatten_tensor(reshaped) == [float(value) for value in values]


def test_reshape_rejects_wrong_element_count() -> None:
    with pytest.raises(ValueError, match="element count"):
        reshape([1, 2, 3], (2, 2))


def test_non_finite_values_are_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        l2_norm([1.0, math.inf])


def test_embedding_rankings_have_expected_ordering() -> None:
    cosine_results = rank_embeddings(
        QUERY,
        DOCUMENTS,
        metric="cosine",
        normalized=False,
    )
    euclidean_results = rank_embeddings(
        QUERY,
        DOCUMENTS,
        metric="euclidean",
        normalized=True,
    )

    assert [result.rank for result in cosine_results] == [1, 2, 3, 4, 5]
    assert cosine_results[0].score >= cosine_results[-1].score
    assert euclidean_results[0].score <= euclidean_results[-1].score
    assert cosine_results[0].document_id == "doc-003"
