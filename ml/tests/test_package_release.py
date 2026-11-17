import json
import sys

import pytest
import torch
from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app, fastapi_app
from backend.app.routers.classify import get_model_service
from backend.app.services.inference import ModelService, build_model
from ml.scripts.package_release import file_sha256, main, package_release

LABELS = ["plastic", "landfill", "compost", "glass", "paper"]


@pytest.fixture
def release(tmp_path, monkeypatch):
    monkeypatch.setattr(ModelService, "_instance", None)
    checkpoint = tmp_path / "fixture.pth"
    output = tmp_path / "package"
    image = tmp_path / "fixture.png"
    Image.new("RGB", (12, 8), "green").save(image)

    def run(digest=None, *, images=None):
        return package_release(
            checkpoint,
            output,
            source_commit="a" * 40,
            source="fixture storage",
            expected_sha256=digest or file_sha256(checkpoint),
            images=[image] if images is None else images,
        )

    return checkpoint, output, image, run


def write_compatible_checkpoint(checkpoint):
    model = build_model("mobilenet_v2", len(LABELS))
    torch.save(
        {"model_state_dict": model.state_dict(), "class_names": LABELS}, checkpoint
    )


def test_package_copies_exact_bytes_and_preserves_class_order(release):
    checkpoint, output, image, run = release
    write_compatible_checkpoint(checkpoint)

    manifest = run()

    assert manifest == json.loads(
        (output / "manifest.json").read_text(encoding="utf-8")
    )
    assert (
        manifest["sha256"]
        == file_sha256(output / checkpoint.name)
        == file_sha256(checkpoint)
    )
    assert manifest["architecture"] == "mobilenet_v2"
    assert manifest["class_names"] == LABELS
    assert manifest["api_categories"] == LABELS
    assert manifest["runtime_preprocessing"]["resize_hw"] == [224, 224]
    (sample,) = manifest["direct_inference_samples"]
    assert sample["sha256"] == file_sha256(image)
    assert sample["content_type"] == "image/png"
    assert sample["category"] in LABELS
    assert 0 <= sample["confidence"] <= 1
    with pytest.raises(FileExistsError, match="already exists"):
        run()


def test_smoke_prediction_matches_classify_response(release, monkeypatch):
    checkpoint, output, image, run = release
    write_compatible_checkpoint(checkpoint)
    (sample,) = run()["direct_inference_samples"]

    service = ModelService(output / checkpoint.name, device="cpu")
    monkeypatch.setitem(
        fastapi_app.dependency_overrides, get_model_service, lambda: service
    )
    with image.open("rb") as file:
        response = TestClient(app).post(
            "/api/classify", files={"file": (image.name, file, sample["content_type"])}
        )

    assert response.status_code == 200
    prediction = response.json()
    for key in ("category", "confidence", "alternatives"):
        assert prediction[key] == sample[key]


def test_package_requires_a_smoke_sample(release):
    _, output, _, run = release
    with pytest.raises(ValueError, match="at least one image"):
        run("f" * 64, images=[])
    assert not output.exists()


def test_cli_requires_a_smoke_sample(release, monkeypatch, capsys):
    checkpoint, output, _, _ = release
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "package_release",
            "--checkpoint",
            str(checkpoint),
            "--source-commit",
            "a" * 40,
            "--source",
            "fixture storage",
            "--sha256",
            "f" * 64,
            "--output",
            str(output),
        ],
    )
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "--image" in capsys.readouterr().err
    assert not output.exists()


@pytest.mark.parametrize(
    ("filename", "image_format", "message"),
    [
        ("fixture.gif", "GIF", "File signature mismatch"),
        ("fixture.jpg", "PNG", "File extension does not match JPEG"),
    ],
)
def test_rejects_smoke_samples_the_api_cannot_upload(
    release, filename, image_format, message
):
    checkpoint, output, _, run = release
    write_compatible_checkpoint(checkpoint)
    image = checkpoint.with_name(filename)
    Image.new("RGB", (12, 8), "green").save(image, format=image_format)

    with pytest.raises(ValueError, match=message):
        run(images=[image])
    assert not output.exists()


def test_rejects_smoke_sample_above_api_upload_limit(release, monkeypatch):
    checkpoint, output, _, run = release
    write_compatible_checkpoint(checkpoint)
    monkeypatch.setattr(
        "backend.app.utils.upload_validator.settings.MAX_UPLOAD_SIZE_MB", 0
    )

    with pytest.raises(ValueError, match="exceeds the API upload limit"):
        run()
    assert not output.exists()


def test_missing_input_and_wrong_checksum_do_not_publish(release):
    checkpoint, output, _, run = release
    with pytest.raises(FileNotFoundError, match="Checkpoint unavailable"):
        run("f" * 64)
    checkpoint.write_bytes(b"wrong artifact")
    with pytest.raises(ValueError, match="SHA-256"):
        run("f" * 64)
    assert not output.exists()


@pytest.mark.parametrize(
    ("bundle", "message"),
    [
        ({"classes": LABELS}, "ordered class_names"),
        ({"class_names": ["plastic"] * 5}, "one-to-one"),
        ({"class_names": LABELS, "architecture": "resnet50"}, "Unsupported checkpoint"),
        (
            {
                "class_names": LABELS,
                "architecture": "resnet18",
                "fc.weight": torch.zeros(4, 1),
            },
            "did not load",
        ),
    ],
)
def test_rejects_ambiguous_or_incompatible_checkpoints(release, bundle, message):
    checkpoint, output, _, run = release
    torch.save(bundle, checkpoint)
    with pytest.raises(ValueError, match=message):
        run()
    assert not output.exists()
