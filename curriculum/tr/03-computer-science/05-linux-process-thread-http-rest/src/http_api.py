"""A dependency-free, testable HTTP inference service for the lesson."""

from __future__ import annotations

import json
import logging
import math
import os
import uuid
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import BoundedSemaphore
from typing import Any, cast
from urllib.parse import urlsplit

MAX_BODY_BYTES = 1_048_576
MAX_FEATURES = 1_024
LOGGER = logging.getLogger("inference_api")


@dataclass(frozen=True, slots=True)
class ApiProblem(Exception):
    status: HTTPStatus
    code: str
    message: str


@dataclass(slots=True)
class InferenceState:
    model_version: str
    concurrency: BoundedSemaphore


def validate_features(payload: Any) -> list[float]:
    """Validate and normalize a prediction request payload."""

    if not isinstance(payload, dict):
        raise ApiProblem(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "INVALID_PAYLOAD",
            "request body must be a JSON object",
        )

    raw_features = payload.get("features")
    if not isinstance(raw_features, list) or not raw_features:
        raise ApiProblem(
            HTTPStatus.UNPROCESSABLE_ENTITY,
            "INVALID_FEATURES",
            "features must be a non-empty numeric list",
        )
    if len(raw_features) > MAX_FEATURES:
        raise ApiProblem(
            HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            "TOO_MANY_FEATURES",
            f"features cannot contain more than {MAX_FEATURES} values",
        )

    features: list[float] = []
    for value in raw_features:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ApiProblem(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "INVALID_FEATURES",
                "every feature must be a finite number",
            )
        normalized = float(value)
        if not math.isfinite(normalized):
            raise ApiProblem(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                "INVALID_FEATURES",
                "every feature must be a finite number",
            )
        features.append(normalized)
    return features


def predict(features: list[float], model_version: str) -> dict[str, Any]:
    """Return a deterministic placeholder prediction.

    This function intentionally represents service mechanics, not model quality.
    """

    if not features:
        raise ValueError("features cannot be empty")
    score = sum(features) / len(features)
    return {
        "label": int(score >= 0.5),
        "score": round(score, 6),
        "model_version": model_version,
    }


def error_document(problem: ApiProblem, request_id: str) -> dict[str, Any]:
    return {
        "error": {
            "code": problem.code,
            "message": problem.message,
            "request_id": request_id,
        }
    }


def success_document(
    prediction: dict[str, Any], request_id: str
) -> dict[str, Any]:
    return {"prediction": prediction, "request_id": request_id}


class PredictionHandler(BaseHTTPRequestHandler):
    """HTTP adapter around pure validation and prediction functions."""

    server_version = "LessonInferenceAPI/1.0"

    def _state(self) -> InferenceState:
        return cast(InferenceState, getattr(self.server, "state"))

    def _request_id(self) -> str:
        candidate = self.headers.get("X-Request-ID", "").strip()
        if candidate and len(candidate) <= 128 and candidate.isprintable():
            return candidate
        return str(uuid.uuid4())

    def _send_json(
        self,
        status: HTTPStatus,
        document: dict[str, Any],
        request_id: str,
    ) -> None:
        body = json.dumps(document, separators=(",", ":")).encode("utf-8")
        self.send_response(status.value)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> Any:
        media_type = self.headers.get("Content-Type", "").split(";", 1)[0].lower()
        if media_type != "application/json":
            raise ApiProblem(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "UNSUPPORTED_MEDIA_TYPE",
                "Content-Type must be application/json",
            )

        raw_length = self.headers.get("Content-Length")
        try:
            content_length = int(raw_length or "0")
        except ValueError as exc:
            raise ApiProblem(
                HTTPStatus.BAD_REQUEST,
                "INVALID_CONTENT_LENGTH",
                "Content-Length must be an integer",
            ) from exc

        if content_length <= 0:
            raise ApiProblem(
                HTTPStatus.BAD_REQUEST,
                "EMPTY_BODY",
                "request body cannot be empty",
            )
        if content_length > MAX_BODY_BYTES:
            raise ApiProblem(
                HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                "BODY_TOO_LARGE",
                f"request body cannot exceed {MAX_BODY_BYTES} bytes",
            )

        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ApiProblem(
                HTTPStatus.BAD_REQUEST,
                "INVALID_JSON",
                "request body must contain valid UTF-8 JSON",
            ) from exc

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        request_id = self._request_id()
        path = urlsplit(self.path).path
        if path == "/health":
            self._send_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "model_version": self._state().model_version,
                },
                request_id,
            )
            return

        problem = ApiProblem(
            HTTPStatus.NOT_FOUND,
            "NOT_FOUND",
            "resource not found",
        )
        self._send_json(problem.status, error_document(problem, request_id), request_id)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        request_id = self._request_id()
        path = urlsplit(self.path).path
        if path != "/v1/predictions":
            problem = ApiProblem(
                HTTPStatus.NOT_FOUND,
                "NOT_FOUND",
                "resource not found",
            )
            self._send_json(
                problem.status,
                error_document(problem, request_id),
                request_id,
            )
            return

        state = self._state()
        acquired = state.concurrency.acquire(timeout=0.05)
        if not acquired:
            problem = ApiProblem(
                HTTPStatus.SERVICE_UNAVAILABLE,
                "SERVICE_BUSY",
                "prediction capacity is temporarily exhausted",
            )
            self._send_json(
                problem.status,
                error_document(problem, request_id),
                request_id,
            )
            return

        try:
            payload = self._read_json()
            features = validate_features(payload)
            result = predict(features, state.model_version)
            self._send_json(
                HTTPStatus.OK,
                success_document(result, request_id),
                request_id,
            )
        except ApiProblem as problem:
            self._send_json(
                problem.status,
                error_document(problem, request_id),
                request_id,
            )
        except Exception:
            LOGGER.exception("unhandled prediction error", extra={"request_id": request_id})
            problem = ApiProblem(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "INTERNAL_ERROR",
                "an unexpected server error occurred",
            )
            self._send_json(
                problem.status,
                error_document(problem, request_id),
                request_id,
            )
        finally:
            state.concurrency.release()

    def log_message(self, format: str, *args: Any) -> None:
        LOGGER.info(
            "http_request",
            extra={
                "client_ip": self.client_address[0],
                "request_line": self.requestline,
                "message": format % args,
            },
        )


class InferenceHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(
        self,
        server_address: tuple[str, int],
        model_version: str,
        max_concurrency: int,
    ) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1")
        super().__init__(server_address, PredictionHandler)
        self.state = InferenceState(
            model_version=model_version,
            concurrency=BoundedSemaphore(max_concurrency),
        )


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8080"))
    model_version = os.getenv("MODEL_VERSION", "demo-v1")
    max_concurrency = int(os.getenv("MAX_CONCURRENCY", "8"))

    server = InferenceHTTPServer(
        (host, port),
        model_version=model_version,
        max_concurrency=max_concurrency,
    )
    LOGGER.info(
        "server_started host=%s port=%s model_version=%s max_concurrency=%s",
        host,
        port,
        model_version,
        max_concurrency,
    )
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        LOGGER.info("shutdown_requested")
    finally:
        server.server_close()
        LOGGER.info("server_stopped")


if __name__ == "__main__":
    main()
