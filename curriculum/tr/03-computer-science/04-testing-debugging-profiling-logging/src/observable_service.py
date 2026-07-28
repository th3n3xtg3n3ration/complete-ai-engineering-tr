from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

LOGGER = logging.getLogger("model_service")


class ValidationError(ValueError):
    """Raised when an inference request is invalid."""


class PredictionError(RuntimeError):
    """Raised when the prediction dependency fails."""


@dataclass(frozen=True)
class PredictionResult:
    label: str
    score: float
    model_version: str
    latency_ms: float


Predictor = Callable[[str], tuple[str, float]]
Clock = Callable[[], float]


def default_predictor(text: str) -> tuple[str, float]:
    normalized = text.casefold()
    positive_words = {"good", "great", "excellent", "love"}
    score = sum(word in normalized for word in positive_words) / len(positive_words)
    return ("positive" if score > 0 else "neutral", score)


class ModelService:
    def __init__(
        self,
        predictor: Predictor = default_predictor,
        *,
        model_version: str = "sentiment-v1",
        max_input_length: int = 1_000,
        clock: Clock = time.perf_counter,
    ) -> None:
        if max_input_length <= 0:
            raise ValueError("max_input_length must be positive")
        self._predictor = predictor
        self._model_version = model_version
        self._max_input_length = max_input_length
        self._clock = clock

    def predict(self, text: str, *, request_id: str = "unknown") -> PredictionResult:
        self._validate(text)
        started_at = self._clock()
        LOGGER.info(
            "prediction_started",
            extra={
                "request_id": request_id,
                "model_version": self._model_version,
                "input_length": len(text),
            },
        )

        try:
            label, score = self._predictor(text)
        except Exception as exc:
            LOGGER.exception(
                "prediction_failed",
                extra={"request_id": request_id, "model_version": self._model_version},
            )
            raise PredictionError("prediction dependency failed") from exc

        latency_ms = (self._clock() - started_at) * 1_000
        result = PredictionResult(
            label=label,
            score=float(score),
            model_version=self._model_version,
            latency_ms=latency_ms,
        )
        LOGGER.info(
            "prediction_completed",
            extra={
                "request_id": request_id,
                "model_version": self._model_version,
                "latency_ms": latency_ms,
                "label": label,
            },
        )
        return result

    def _validate(self, text: Any) -> None:
        if not isinstance(text, str):
            raise ValidationError("text must be a string")
        if not text.strip():
            raise ValidationError("text must not be empty")
        if len(text) > self._max_input_length:
            raise ValidationError("text exceeds maximum length")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


if __name__ == "__main__":
    configure_logging()
    service = ModelService()
    print(service.predict("I love this course", request_id="demo-1"))
