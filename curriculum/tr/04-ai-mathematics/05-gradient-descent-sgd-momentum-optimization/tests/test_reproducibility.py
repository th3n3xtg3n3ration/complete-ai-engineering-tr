from __future__ import annotations

from pathlib import Path
import sys

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from regression_experiment import make_regression_data


def test_same_seed_produces_identical_regression_data() -> None:
    first = make_regression_data(count=25, seed=123)
    second = make_regression_data(count=25, seed=123)
    different = make_regression_data(count=25, seed=124)

    assert first == second
    assert first != different
