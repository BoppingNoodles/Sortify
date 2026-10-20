import io

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_check():
    """Verify /health returns HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classify_endpoint_success():
    """Verify /api/classify returns a valid response for a real image."""
    # Create a small fake jpeg header
    file_content = b"\xff\xd8\xff" + b"0" * 1024
    fake_file = io.BytesIO(file_content)

    response = client.post(
        "/api/classify?location=berkeley",
        files={"file": ("test.jpg", fake_file, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "item_name" in data
    assert "category" in data
    assert "disposal_tip" in data


def test_classify_invalid_file():
    """Verify .txt file triggers 415 error (via your validator)."""
    fake_file = io.BytesIO(b"this is just text")
    response = client.post(
        "/api/classify", files={"file": ("test.txt", fake_file, "text/plain")}
    )
    # Note: Your current validator raises 415 for invalid MIME types
    assert response.status_code == 415


def test_rules_endpoint():
    """Verify rules for berkeley return valid schema."""
    response = client.get("/api/rules/berkeley")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "berkeley"
    assert "rules" in data
