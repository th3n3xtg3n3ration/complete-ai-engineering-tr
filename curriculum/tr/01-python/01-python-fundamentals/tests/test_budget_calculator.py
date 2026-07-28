from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).parents[1] / "src" / "budget_calculator.py"
SPEC = importlib.util.spec_from_file_location("budget_calculator", MODULE_PATH)
assert SPEC and SPEC.loader
budget_calculator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(budget_calculator)


def test_parse_accepts_decimal_comma() -> None:
    assert budget_calculator.parse_non_negative_number("12,5", "Değer") == 12.5


def test_parse_rejects_negative_value() -> None:
    with pytest.raises(ValueError, match="negatif"):
        budget_calculator.parse_non_negative_number("-1", "Gelir")


def test_parse_rejects_non_numeric_value() -> None:
    with pytest.raises(ValueError, match="geçerli bir sayı"):
        budget_calculator.parse_non_negative_number("abc", "Gelir")


def test_calculate_balance() -> None:
    assert budget_calculator.calculate_balance(30_000, 22_500) == 7_500


def test_calculate_savings_rate() -> None:
    assert budget_calculator.calculate_savings_rate(20_000, 15_000) == 25.0


def test_zero_income_has_zero_rate() -> None:
    assert budget_calculator.calculate_savings_rate(0, 100) == 0.0


@pytest.mark.parametrize(("balance", "expected"), [(1, "fazla"), (-1, "açık"), (0, "dengeli")])
def test_classify_budget(balance: float, expected: str) -> None:
    assert budget_calculator.classify_budget(balance) == expected


def test_build_summary_contains_key_metrics() -> None:
    summary = budget_calculator.build_summary(10_000, 7_500)
    assert "Bakiye: 2,500.00 TL" in summary
    assert "Tasarruf oranı: %25.0" in summary
    assert "Durum: fazla" in summary
