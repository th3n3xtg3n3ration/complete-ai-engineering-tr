from __future__ import annotations

import logging

import pytest

from src.observable_service import ModelService, PredictionError, ValidationError


def test_predict_returns_dependency_result() -> None:
    service = ModelService(lambda text: ("custom", 0.75), clock=iter([1.0, 1.025]).__next__)

    result = service.predict("valid input", request_id="req-1")

    assert result.label == "custom"
    assert result.score == pytest.approx(0.75)
    assert result.model_version == "sentiment-v1"
    assert result.latency_ms == pytest.approx(25.0)


@pytest.mark.parametrize("invalid_text", ["", "   ", "x" * 11])
def test_predict_rejects_invalid_text(invalid_text: str) -> None:
    service = ModelService(max_input_length=10)

    with pytest.raises(ValidationError):
        service.predict(invalid_text)


def test_predict_rejects_non_string_input() -> None:
    service = ModelService()

    with pytest.raises(ValidationError, match="string"):
        service.predict(42)  # type: ignore[arg-type]


def test_dependency_error_is_wrapped() -> None:
    def failing_predictor(text: str) -> tuple[str, float]:
        raise TimeoutError("provider timeout")

    service = ModelService(failing_predictor)

    with pytest.raises(PredictionError) as error:
        service.predict("valid")

    assert isinstance(error.value.__cause__, TimeoutError)


def test_completion_event_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    service = ModelService(lambda text: ("ok", 1.0), clock=iter([2.0, 2.001]).__next__)

    with caplog.at_level(logging.INFO, logger="model_service"):
        service.predict("valid", request_id="req-42")

    assert "prediction_started" in caplog.messages
    assert "prediction_completed" in caplog.messages
