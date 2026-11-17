import hashlib
import json
import sys

import pytest
import torch
from PIL import Image

from backend.app.services.inference import ModelService, build_model
from ml.scripts import evaluate_campus_photos


def test_release_evaluation_reports_checkpoint_dataset_and_failures(
    monkeypatch, tmp_path
):
    monkeypatch.setattr(ModelService, "_instance", None)
    labels = ["plastic", "compost", "landfill", "paper", "glass"]
    model = build_model("mobilenet_v2", len(labels))
    with torch.no_grad():
        model.classifier[1].weight.zero_()
        model.classifier[1].bias.zero_()
        model.classifier[1].bias[0] = 10
    checkpoint = tmp_path / "fixture.pth"
    torch.save(
        {"model_state_dict": model.state_dict(), "class_names": labels}, checkpoint
    )
    manifest = tmp_path / "manifest.json"
    digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    manifest.write_text(
        json.dumps(
            {
                "sha256": digest,
                "class_names": labels,
                "source_commit": "a" * 40,
                "architecture": "mobilenet_v2",
            }
        ),
        encoding="utf-8",
    )

    data_dir = tmp_path / "campus"
    plastic = data_dir / "plastic"
    plastic.mkdir(parents=True)
    photo = plastic / "valid.png"
    Image.new("RGB", (14, 12), "green").save(photo)
    (plastic / "unreadable.png").write_bytes(b"corrupt image")
    output = tmp_path / "report"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "evaluate_campus_photos",
            "--checkpoint",
            str(checkpoint),
            "--release-manifest",
            str(manifest),
            "--candidate-sha",
            "b" * 40,
            "--data-dir",
            str(data_dir),
            "--dataset-id",
            "fixture",
            "--out-dir",
            str(output),
        ],
    )

    with pytest.raises(SystemExit) as exit_info:
        evaluate_campus_photos.main()
    assert exit_info.value.code == 1
    metrics = json.loads((output / "metrics.json").read_text(encoding="utf-8"))
    predictions = json.loads((output / "predictions.json").read_text(encoding="utf-8"))
    assert metrics["attempted_images"] == 2
    assert metrics["attempted_class_counts"]["plastic"] == 2
    assert metrics["n_images"] == 1
    assert metrics["campus_accuracy"] == 1
    assert metrics["release_provenance"]["checkpoint_sha256"] == digest
    assert metrics["release_provenance"]["class_names"] == labels
    assert (
        "Resize(size=(224, 224)"
        in metrics["release_provenance"]["runtime_preprocessing"]["transform"]
        or "Resize(size=[224, 224]"
        in metrics["release_provenance"]["runtime_preprocessing"]["transform"]
    )
    assert metrics["failures"][0]["path"] == "plastic/unreadable.png"
    assert predictions[0]["pred"] == "plastic"
    assert predictions[0]["sha256"] == hashlib.sha256(photo.read_bytes()).hexdigest()
    with Image.open(output / "confusion_matrix.png") as chart:
        assert chart.width == 2400
        assert chart.info["dpi"][0] == pytest.approx(300, abs=0.01)
