from __future__ import annotations

import importlib.util
import json
import sys
from http import HTTPStatus
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

LESSON_DIR = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = LESSON_DIR / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


system_inspector = load_module("lesson_system_inspector", "src/system_inspector.py")
http_api = load_module("lesson_http_api", "src/http_api.py")


def test_run_command_captures_success() -> None:
    result = system_inspector.run_command(
        [sys.executable, "-c", "print('ready')"],
        timeout_seconds=2,
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "ready"
    assert result.stderr == ""


def test_run_command_returns_nonzero_exit_code() -> None:
    result = system_inspector.run_command(
        [sys.executable, "-c", "raise SystemExit(7)"],
        timeout_seconds=2,
    )

    assert result.returncode == 7


def test_run_command_rejects_invalid_arguments() -> None:
    with pytest.raises(ValueError, match="non-empty strings"):
        system_inspector.run_command([])


def test_run_command_timeout_is_domain_error() -> None:
    with pytest.raises(system_inspector.CommandTimeoutError):
        system_inspector.run_command(
            [sys.executable, "-c", "import time; time.sleep(0.2)"],
            timeout_seconds=0.01,
        )


def test_parallel_map_preserves_input_order() -> None:
    assert system_inspector.parallel_map(
        lambda value: value * value,
        [3, 1, 2],
        max_workers=2,
    ) == [9, 1, 4]


def test_thread_safe_counter() -> None:
    counter = system_inspector.ThreadSafeCounter()

    system_inspector.parallel_map(
        lambda _: counter.increment(),
        range(100),
        max_workers=8,
    )

    assert counter.value == 100


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"features": []},
        {"features": [True]},
        {"features": ["0.2"]},
        {"features": [float("inf")]},
    ],
)
def test_validate_features_rejects_invalid_values(payload) -> None:
    with pytest.raises(http_api.ApiProblem) as exc_info:
        http_api.validate_features(payload)

    assert exc_info.value.status == HTTPStatus.UNPROCESSABLE_ENTITY


def test_validate_features_normalizes_numbers() -> None:
    assert http_api.validate_features({"features": [1, 0.25]}) == [1.0, 0.25]


def test_predict_is_deterministic() -> None:
    result = http_api.predict([0.25, 0.75], "model-v2")

    assert result == {
        "label": 1,
        "score": 0.5,
        "model_version": "model-v2",
    }


def test_error_document_has_stable_contract() -> None:
    problem = http_api.ApiProblem(
        HTTPStatus.BAD_REQUEST,
        "INVALID_JSON",
        "invalid JSON",
    )

    assert http_api.error_document(problem, "request-1") == {
        "error": {
            "code": "INVALID_JSON",
            "message": "invalid JSON",
            "request_id": "request-1",
        }
    }


@pytest.fixture
def running_server():
    server = http_api.InferenceHTTPServer(
        ("127.0.0.1", 0),
        model_version="test-v1",
        max_concurrency=2,
    )
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_health_endpoint(running_server: str) -> None:
    with urlopen(f"{running_server}/health", timeout=2) as response:
        document = json.loads(response.read())

    assert response.status == HTTPStatus.OK
    assert document == {"status": "ok", "model_version": "test-v1"}
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.headers["X-Request-ID"]


def test_prediction_endpoint(running_server: str) -> None:
    request = Request(
        f"{running_server}/v1/predictions",
        data=json.dumps({"features": [0.2, 0.8]}).encode(),
        headers={
            "Content-Type": "application/json",
            "X-Request-ID": "test-request",
        },
        method="POST",
    )

    with urlopen(request, timeout=2) as response:
        document = json.loads(response.read())

    assert response.status == HTTPStatus.OK
    assert response.headers["X-Request-ID"] == "test-request"
    assert document["request_id"] == "test-request"
    assert document["prediction"]["label"] == 1
    assert document["prediction"]["score"] == 0.5


def test_prediction_endpoint_rejects_wrong_media_type(
    running_server: str,
) -> None:
    request = Request(
        f"{running_server}/v1/predictions",
        data=b"hello",
        headers={"Content-Type": "text/plain"},
        method="POST",
    )

    with pytest.raises(HTTPError) as exc_info:
        urlopen(request, timeout=2)

    assert exc_info.value.code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    document = json.loads(exc_info.value.read())
    assert document["error"]["code"] == "UNSUPPORTED_MEDIA_TYPE"
