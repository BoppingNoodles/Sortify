import json
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app, fastapi_app
from backend.app.routers.classify import get_model_service
from backend.app.routers.history import get_history_service
from backend.app.services.history_service import HistoryService
from backend.scripts import verify_release

PREDICTION = {
    "item_name": "Plastic",
    "category": "plastic",
    "confidence": 0.92,
    "disposal_tip": "Empty and rinse.",
    "location": "oakland",
}


@pytest.fixture
def sample_image(tmp_path):
    path = tmp_path / "sample.png"
    Image.new("RGB", (10, 10), "blue").save(path)
    return path


def test_success_records_first_and_warm_requests_without_history_writes(sample_image):
    paths = []

    def transport(request):
        paths.append((request.method, request.url.path))
        if request.url.path == "/health":
            return httpx.Response(200, json={"status": "ok"})
        assert request.url.params["location"] == "oakland"
        assert b'filename="sample.png"' in request.read()
        return httpx.Response(200, json=PREDICTION)

    with httpx.Client(
        transport=httpx.MockTransport(transport), base_url="https://api.example"
    ) as client:
        report = verify_release.run_release(client, sample_image, "oakland", 20)
    assert paths == [("GET", "/health")] + [("POST", "/api/classify")] * 21
    assert report["ok"] is True
    assert report["first_classification"]["prediction"]["category"] == "plastic"
    assert len(report["warm_requests"]) == 20
    assert report["warm_summary"]["success_count"] == 20
    assert report["warm_target_met"] is True


@pytest.mark.parametrize(
    "failure", ["timeout", "503", "invalid-json", "invalid-schema", "fallback"]
)
def test_classification_failures_are_reported_without_retry(sample_image, failure):
    classify_calls = 0

    def transport(request):
        nonlocal classify_calls
        if request.url.path == "/health":
            return httpx.Response(200, json={"status": "ok"})
        classify_calls += 1
        if classify_calls == 1:
            return httpx.Response(200, json=PREDICTION)
        if failure == "timeout":
            raise httpx.ReadTimeout("timeout", request=request)
        if failure == "503":
            return httpx.Response(503)
        if failure == "invalid-json":
            return httpx.Response(200, text="<html>Busy</html>")
        if failure == "invalid-schema":
            return httpx.Response(200, json={**PREDICTION, "confidence": "0.92"})
        return httpx.Response(
            200, json={**PREDICTION, "item_name": "Almond Milk Carton (Scaffold)"}
        )

    with httpx.Client(
        transport=httpx.MockTransport(transport), base_url="https://api.example"
    ) as client:
        report = verify_release.run_release(client, sample_image, "oakland", 20)
    assert classify_calls == 21
    assert report["ok"] is False
    assert report["warm_summary"]["failure_count"] == 20
    assert report["warm_summary"]["p95_ms"] is None
    for sample in report["warm_requests"]:
        assert sample["status"] == {"timeout": None, "503": 503}.get(failure, 200)
        assert sample["error"]


def test_nearest_rank_and_loopback_policy():
    samples = [{"ok": True, "elapsed_ms": value} for value in range(1, 21)]
    samples.append({"ok": False, "elapsed_ms": 999})
    result = verify_release.summarize_warm(samples)
    assert (result["p50_ms"], result["p95_ms"], result["p99_ms"]) == (10, 19, 20)
    assert (
        verify_release.validate_url("https://staging.example/")
        == "https://staging.example"
    )
    assert verify_release.validate_url("http://[::1]:8000") == "http://[::1]:8000"
    with pytest.raises(ValueError, match="HTTPS"):
        verify_release.validate_url("http://staging.example")
    with pytest.raises(ValueError, match="without credentials"):
        verify_release.validate_url("https://user:pass@staging.example")


def test_explicit_staging_check_exercises_real_history_routes(
    sample_image, monkeypatch
):
    class ControlledModel:
        def predict(self, _image):
            return {"category": "plastic", "item_name": "Plastic", "confidence": 0.92}

    monkeypatch.setitem(
        fastapi_app.dependency_overrides, get_model_service, ControlledModel
    )
    history = HistoryService()
    monkeypatch.setitem(
        fastapi_app.dependency_overrides, get_history_service, lambda: history
    )
    with TestClient(app) as client:
        report = verify_release.run_release(
            client, sample_image, "oakland", 20, staging_history=True
        )
    staging = report["staging_history"]
    assert staging["ok"] is True
    assert [sample["status"] for sample in staging["samples"]] == [201, 201, 200, 200]
    stored = history.get_user_history(staging["user_id"])["scans"]
    assert len(stored) == 1
    assert stored[0]["scan_id"] == staging["scan_id"]


def test_observation_preserves_recorded_health(tmp_path, monkeypatch):
    elapsed = 0

    def advance(seconds):
        nonlocal elapsed
        elapsed += seconds

    monkeypatch.setattr(verify_release.time, "sleep", advance)
    monkeypatch.setattr(verify_release.time, "monotonic", lambda: elapsed)
    responses = iter((httpx.Response(200, json={"status": "ok"}), httpx.Response(503)))
    output: Path = tmp_path / "release.json"
    with httpx.Client(
        transport=httpx.MockTransport(lambda _request: next(responses)),
        base_url="https://api.example",
    ) as client:
        verify_release.observe_health(client, {"ok": True}, output, 5)
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["ok"] is False
    assert report["uptime"]["complete"] is True
    assert report["uptime"]["elapsed_seconds"] == 300
    assert report["uptime"]["failure_count"] == 1


def test_observation_marks_gaps_after_suspension(tmp_path, monkeypatch):
    elapsed = 0

    def suspend(seconds):
        nonlocal elapsed
        if seconds:
            elapsed += seconds + 300

    monkeypatch.setattr(verify_release.time, "sleep", suspend)
    monkeypatch.setattr(verify_release.time, "monotonic", lambda: elapsed)
    output = tmp_path / "release.json"
    with httpx.Client(
        transport=httpx.MockTransport(
            lambda _request: httpx.Response(200, json={"status": "ok"})
        ),
        base_url="https://api.example",
    ) as client:
        verify_release.observe_health(client, {"ok": True}, output, 10)
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["ok"] is False
    assert report["uptime"]["complete"] is False
    assert report["uptime"]["missed_intervals"] == 1
    assert len(report["uptime"]["samples"]) == 2
