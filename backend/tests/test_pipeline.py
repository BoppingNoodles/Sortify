"""Exercise the API pipeline with controlled inference and fake Firestore."""

from datetime import UTC, datetime
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app, fastapi_app
from backend.app.routers.classify import get_model_service
from backend.app.routers.history import get_history_service
from backend.app.schemas import ClassifyResponse, HistoryPage, SavedGuestScan
from backend.app.services import streak_calculator
from backend.app.services.history_service import HistoryService
from backend.tests.fake_firestore import BoomDB, FakeDB

GUEST = "7cd51b0a-153d-4183-8eac-3cbde188c1f9"
OTHER_GUEST = "ad9737de-96af-4ee6-ad58-38122f4f561e"
FIRST_SCAN = "a08949ce-7606-49fa-b8f0-fa6d23207398"
SECOND_SCAN = "bc0bfd26-6ccc-40aa-af56-dc11c80b9d78"
THIRD_SCAN = "ca0bfd26-6ccc-40aa-af56-dc11c80b9d78"


class FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 11, 16, 21, tzinfo=UTC).astimezone(tz)


class ControlledInference:
    def predict(self, image_bytes):
        with Image.open(BytesIO(image_bytes)) as image:
            pixel = image.convert("RGB").getpixel((0, 0))
        category = "plastic" if pixel == (255, 0, 0) else "paper"
        return {"category": category, "item_name": category.title(), "confidence": 0.9}


@pytest.fixture
def pipeline(monkeypatch):
    with monkeypatch.context() as overrides:
        overrides.setitem(
            fastapi_app.dependency_overrides, get_model_service, ControlledInference
        )
        history = HistoryService(FakeDB())
        overrides.setitem(
            fastapi_app.dependency_overrides, get_history_service, lambda: history
        )
        overrides.setattr(streak_calculator, "datetime", FrozenDatetime)
        with TestClient(app) as client:
            yield client, history


def classify(client, color):
    image = BytesIO()
    Image.new("RGB", (16, 16), color).save(image, format="PNG")
    response = client.post(
        "/api/classify",
        params={"location": "oakland"},
        files={"file": ("sample.png", image.getvalue(), "image/png")},
    )
    assert response.status_code == 200, response.text
    result = ClassifyResponse.model_validate(response.json())
    assert result.location == "oakland"
    assert result.disposal_tip
    return result


def record_from(result, scan_id, timestamp):
    return {
        **result.model_dump(
            include={
                "category",
                "item_name",
                "confidence",
                "location",
                "bin_color",
                "bin",
            }
        ),
        "user_id": GUEST,
        "scan_id": scan_id,
        "timestamp": timestamp,
    }


def test_classify_then_save_retry_page_and_aggregate(pipeline):
    client, _ = pipeline
    first = classify(client, "red")
    second = classify(client, "blue")
    assert (first.category, second.category) == ("plastic", "paper")

    history_params = {"user_id": GUEST, "limit": 1}
    response = client.get("/api/history", params=history_params)
    assert response.status_code == 200
    assert response.json() == {"scans": [], "limit": 1, "next_cursor": None}

    first_record = record_from(first, FIRST_SCAN, "2026-11-15T21:00:00Z")
    newer_timestamp = "2026-11-16T20:00:00Z"
    second_record = record_from(second, SECOND_SCAN, newer_timestamp)
    third_record = record_from(second, THIRD_SCAN, newer_timestamp)
    for record in (
        first_record,
        {**first_record, "item_name": "Bottle"},
        second_record,
        third_record,
    ):
        response = client.post("/api/history", json=record)
        assert response.status_code == 201, response.text
        saved = SavedGuestScan.model_validate(response.json())
        assert str(saved.scan_id) == record["scan_id"]
        assert saved.scan.model_dump(mode="json") == record

    response = client.get("/api/history", params=history_params)
    assert response.status_code == 200
    page = HistoryPage.model_validate(response.json())
    # The higher scan ID sorts first among scans with the same timestamp.
    assert [str(scan.scan_id) for scan in page.scans] == [THIRD_SCAN]
    assert page.next_cursor

    response = client.get(
        "/api/history", params={**history_params, "cursor": page.next_cursor}
    )
    assert response.status_code == 200
    middle_page = HistoryPage.model_validate(response.json())
    assert [str(scan.scan_id) for scan in middle_page.scans] == [SECOND_SCAN]
    assert middle_page.next_cursor

    response = client.get(
        "/api/history", params={**history_params, "cursor": middle_page.next_cursor}
    )
    assert response.status_code == 200
    last_page = HistoryPage.model_validate(response.json())
    assert [str(scan.scan_id) for scan in last_page.scans] == [FIRST_SCAN]
    assert last_page.scans[0].item_name == "Bottle"
    assert last_page.next_cursor is None

    response = client.get(f"/api/stats/{GUEST}")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": GUEST,
        "total_scans": 3,
        "eco_points": 30,
        "current_streak": 2,
        "category_counts": {"plastic": 1, "paper": 2},
    }

    response = client.get("/api/history", params={"user_id": OTHER_GUEST})
    assert response.status_code == 200
    assert response.json()["scans"] == []
    response = client.get(f"/api/stats/{OTHER_GUEST}")
    assert response.status_code == 200
    assert response.json()["total_scans"] == 0
    response = client.get(
        "/api/history", params={"user_id": OTHER_GUEST, "cursor": page.next_cursor}
    )
    assert_error(response, 400, "BAD_REQUEST", "Invalid history cursor")


def assert_error(response, status, code, message=None):
    assert response.status_code == status, response.text
    error = response.json()
    assert set(error) == {"error", "code", "message"}
    assert error["error"] is True
    assert error["code"] == code
    assert isinstance(error["message"], str) and error["message"]
    if message is not None:
        assert error["message"] == message


def test_bad_input_and_storage_failure_leave_pipeline_usable(pipeline, monkeypatch):
    client, history = pipeline
    corrupt_png = b"\x89PNG\r\n\x1a\n" + b"invalid chunks"
    response = client.post(
        "/api/classify", files={"file": ("corrupt.png", corrupt_png, "image/png")}
    )
    assert_error(response, 415, "INVALID_IMAGE_FORMAT")
    response = client.get("/api/history", params={"user_id": "no-uuid"})
    assert_error(response, 422, "VALIDATION_ERROR", "Request validation failed.")
    response = client.get("/api/history", params={"user_id": GUEST, "cursor": "!?"})
    assert_error(response, 400, "BAD_REQUEST", "Invalid history cursor")

    result = classify(client, "red")
    record = record_from(result, FIRST_SCAN, "2026-11-16T20:00:00Z")
    with monkeypatch.context() as failure:
        failure.setattr(history, "db", BoomDB())
        for response in (
            client.post("/api/history", json=record),
            client.get("/api/history", params={"user_id": GUEST}),
            client.get(f"/api/stats/{GUEST}"),
        ):
            assert_error(
                response,
                503,
                "SERVICE_UNAVAILABLE",
                "Service temporarily unavailable. Please try again.",
            )

    assert client.get(f"/api/stats/{GUEST}").json()["total_scans"] == 0
    assert client.post("/api/history", json=record).status_code == 201
    assert client.get(f"/api/stats/{GUEST}").json()["total_scans"] == 1
