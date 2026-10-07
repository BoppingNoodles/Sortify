import io

from fastapi.testclient import TestClient

from sandbox.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Sortify Backend API Sandbox",
        "status": "online",
    }


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_image_success():
    fake_image = io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01")
    response = client.post(
        "/upload-image",
        files={"file": ("test_sample.jpg", fake_image, "image/jpeg")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["filename"] == "test_sample.jpg"
    assert data["size_bytes"] > 0


def test_upload_image_invalid_type():
    fake_text = io.BytesIO(b"Hello world, not an image")
    response = client.post(
        "/upload-image",
        files={"file": ("notes.txt", fake_text, "text/plain")},
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
