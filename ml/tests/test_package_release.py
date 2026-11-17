import json

import pytest
import torch
from PIL import Image

from backend.app.services.inference import ModelService, build_model
from ml.scripts.package_release import file_sha256, package_release

LABELS = ["plastic", "landfill", "compost", "glass", "paper"]


@pytest.fixture
def release(tmp_path, monkeypatch):
    monkeypatch.setattr(ModelService, "_instance", None)
    checkpoint = tmp_path / "fixture.pth"
    output = tmp_path / "package"
    image = tmp_path / "fixture.png"
    Image.new("RGB", (12, 8), "green").save(image)

    def run(digest=None):
        return package_release(
            checkpoint,
            output,
            source_commit="a" * 40,
            source="fixture storage",
            expected_sha256=digest or file_sha256(checkpoint),
            images=[image],
        )

    return checkpoint, output, image, run


def test_package_copies_exact_bytes_and_preserves_class_order(release):
    checkpoint, output, image, run = release
    model = build_model("mobilenet_v2", len(LABELS))
    torch.save(
        {"model_state_dict": model.state_dict(), "class_names": LABELS}, checkpoint
    )

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
    assert sample["category"] in LABELS
    assert 0 <= sample["confidence"] <= 1
    with pytest.raises(FileExistsError, match="already exists"):
        run()


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
