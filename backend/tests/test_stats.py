"""Unit tests for user eco-stats aggregation."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.routers.history import get_history_service
from backend.app.services import streak_calculator
from backend.app.services.history_service import HistoryService, HistoryServiceError


class FrozenDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 11, 11, 1, tzinfo=UTC).astimezone(tz)


@pytest.fixture
def stats_client(monkeypatch):
    history = HistoryService()
    monkeypatch.setitem(app.dependency_overrides, get_history_service, lambda: history)
    monkeypatch.setattr(streak_calculator, "datetime", FrozenDatetime)

    with TestClient(app) as client:
        yield client, history


def save_scan(history, user_id, category, timestamp):
    history.save_scan(
        {
            "user_id": user_id,
            "item_name": "Test item",
            "category": category,
            "confidence": 0.95,
            "timestamp": timestamp,
        }
    )


def test_empty_history(stats_client):
    client, _ = stats_client
    user_id = uuid4()
    response = client.get(f"/api/stats/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(user_id),
        "total_scans": 0,
        "eco_points": 0,
        "current_streak": 0,
        "category_counts": {},
    }


def test_populated_history(stats_client):
    client, history = stats_client
    user_id = uuid4()
    save_scan(history, user_id, "plastic", "2026-11-10T22:00:00Z")
    save_scan(history, user_id, "compost", "2026-11-10T22:00:00Z")

    response = client.get(f"/api/stats/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(user_id),
        "total_scans": 2,
        "eco_points": 20,
        "current_streak": 1,
        "category_counts": {"plastic": 1, "compost": 1},
    }


def test_lifetime_stats_include_the_second_page(stats_client):
    client, history = stats_client
    user_id = uuid4()
    save_scan(history, user_id, "glass", "2026-11-09T22:00:00Z")

    for _ in range(100):
        save_scan(history, user_id, "plastic", "2026-11-10T22:00:00Z")

    response = client.get(f"/api/stats/{user_id}")

    assert response.status_code == 200
    assert response.json() == {
        "user_id": str(user_id),
        "total_scans": 101,
        "eco_points": 1010,
        "current_streak": 2,
        "category_counts": {"plastic": 100, "glass": 1},
    }


def test_malformed_device_id_returns_422(stats_client):
    client, _ = stats_client
    assert client.get("/api/stats/invalid-uuid").status_code == 422


def test_later_page_failure_returns_503(stats_client, monkeypatch):
    client, history = stats_client

    def read_page(user_id, limit, cursor):
        if cursor is not None:
            raise HistoryServiceError("Could not read scan history")
        return {
            "scans": [{"category": "plastic", "timestamp": "2026-11-10T22:00:00Z"}],
            "next_cursor": "second-page",
        }

    monkeypatch.setattr(history, "get_user_history", read_page)
    response = client.get(f"/api/stats/{uuid4()}")

    assert response.status_code == 503
    assert response.json() == {"detail": "Scan history storage is unavailable"}


def test_stats_openapi_contract(stats_client):
    client, _ = stats_client
    operation = client.get("/openapi.json").json()["paths"]["/api/stats/{user_id}"][
        "get"
    ]

    parameter = next(p for p in operation["parameters"] if p["name"] == "user_id")
    assert parameter["in"] == "path"
    assert parameter["schema"]["format"] == "uuid"

    schema = operation["responses"]["200"]["content"]["application/json"]["schema"]
    assert schema["$ref"] == "#/components/schemas/UserStatsResponse"
