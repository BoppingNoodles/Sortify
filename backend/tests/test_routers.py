"""Modular router endpoint unit tests."""

import io

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_classify_endpoint_success():
    fake_image = io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01")
    response = client.post(
        "/api/classify",
        files={"file": ("sample.jpg", fake_image, "image/jpeg")},
        params={"location": "berkeley"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "compost"
    assert data["bin_color"] == "Green"
    assert "bin" in data
    assert "disposal_tips" in data
    assert len(data["alternatives"]) > 0


def test_classify_endpoint_invalid_file():
    fake_file = io.BytesIO(b"Hello plain text")
    response = client.post(
        "/api/classify",
        files={"file": ("test.txt", fake_file, "text/plain")},
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_rules_endpoint_get_city():
    response = client.get("/api/rules/berkeley")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "berkeley"
    assert "compost" in data["rules"]
    assert "source_url" in data


def test_rules_endpoint_not_found():
    response = client.get("/api/rules/nonexistent-city")
    assert response.status_code == 404
    assert "Supported cities" in response.json()["detail"]


def test_rules_endpoint_get_all():
    response = client.get("/api/rules")
    assert response.status_code == 200
    data = response.json()
    assert "supported_cities" in data
    assert "berkeley" in data["supported_cities"]


def test_auth_me_endpoint():
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert "email" in data
    assert "current_streak" in data


def test_auth_verify_endpoint():
    # Valid auth header
    response = client.post(
        "/api/auth/verify",
        headers={"Authorization": "Bearer test-token"},
    )
    assert response.status_code == 200
    assert response.json()["valid"] is True

    # Missing auth header
    bad_resp = client.post("/api/auth/verify")
    assert bad_resp.status_code == 401


def test_history_get_endpoint():
    response = client.get("/api/history?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "scans" in data
    assert data["limit"] == 10
    assert data["offset"] == 0


def test_history_post_endpoint():
    payload = {
        "scan_id": "scan-unit-test-1",
        "user_id": "user-test",
        "timestamp": "2026-10-07T12:00:00Z",
        "category": "paper",
        "item_name": "Cardboard Box",
        "confidence": 0.95,
        "location": "berkeley",
    }
    response = client.post("/api/history", json=payload)
    assert response.status_code == 201
    assert response.json()["status"] == "created"
    assert response.json()["scan_id"] == "scan-unit-test-1"


def test_cors_headers():
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:19006"},
    )
    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin") == "http://localhost:19006"
    )
