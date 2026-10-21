"""Unit tests for model evaluation and confusion matrix reporting."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest
import torch
from PIL import Image
from torch import nn

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.evaluate import (
    DEFAULT_CLASSES,
    RemappedDataset,
    build_model,
    create_test_loader,
    detect_architecture,
    evaluate_model_performance,
    get_device,
    load_checkpoint,
    load_classes_from_package,
    plot_confusion_matrix,
    run_evaluation,
)


def _create_dummy_image(
    path: Path, color: tuple[int, int, int] = (100, 150, 200)
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (224, 224), color)
    img.save(path, format="JPEG")


def _create_dummy_test_dataset(
    root: Path, classes: list[str], per_class: int = 2
) -> Path:
    for idx, cls_name in enumerate(classes):
        for i in range(per_class):
            img_path = root / cls_name / f"img_{i}.jpg"
            color = (idx * 40, (idx + 1) * 30, (i + 1) * 50)
            _create_dummy_image(img_path, color)
    return root


def test_build_model():
    model_res = build_model("resnet18", num_classes=5)
    assert isinstance(model_res, nn.Module)
    assert model_res.fc.out_features == 5

    model_mobile = build_model("mobilenet_v2", num_classes=5)
    assert isinstance(model_mobile, nn.Module)
    assert model_mobile.classifier[1].out_features == 5

    with pytest.raises(ValueError, match="Unsupported architecture"):
        build_model("unsupported_model_arch")


def test_detect_architecture():
    # Explicit metadata
    assert detect_architecture({"architecture": "mobilenet_v2"}) == "mobilenet_v2"
    assert detect_architecture({"base_architecture": "resnet18"}) == "resnet18"

    # State dict key inspection
    mobile_sd = {"classifier.1.weight": torch.zeros(5, 1280)}
    assert detect_architecture(mobile_sd) == "mobilenet_v2"
    resnet_sd = {"fc.weight": torch.zeros(5, 512)}
    assert detect_architecture(resnet_sd) == "resnet18"

    # Path fallback
    assert (
        detect_architecture({}, Path("models/mobilenet_v2_frozen.pth"))
        == "mobilenet_v2"
    )
    assert detect_architecture({}, Path("models/model.pth")) == "resnet18"


def test_load_checkpoint_dict(tmp_path: Path):
    classes = ["compost", "glass", "landfill", "paper", "plastic"]
    model = build_model("resnet18", num_classes=len(classes))
    checkpoint_file = tmp_path / "checkpoint.pth"

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_names": classes,
            "best_epoch": 5,
            "val_accuracy": 0.85,
        },
        checkpoint_file,
    )

    loaded_model, loaded_classes, metadata = load_checkpoint(
        checkpoint_file,
        arch="resnet18",
        device=torch.device("cpu"),
    )
    assert loaded_classes == classes
    assert metadata["best_epoch"] == 5
    assert metadata["val_accuracy"] == 0.85
    assert isinstance(loaded_model, nn.Module)


def test_load_checkpoint_raw_with_classes_json(tmp_path: Path):
    classes = ["compost", "glass", "landfill", "paper", "plastic"]
    model = build_model("resnet18", num_classes=len(classes))
    weights_file = tmp_path / "resnet18_sortify.pth"
    torch.save(model.state_dict(), weights_file)

    classes_json = tmp_path / "classes.json"
    with open(classes_json, "w", encoding="utf-8") as f:
        json.dump({str(i): c for i, c in enumerate(classes)}, f)

    loaded_model, loaded_classes, _ = load_checkpoint(
        weights_file,
        arch="resnet18",
        device=torch.device("cpu"),
    )
    assert loaded_classes == classes
    assert isinstance(loaded_model, nn.Module)


def test_load_checkpoint_missing():
    with pytest.raises(FileNotFoundError, match="Checkpoint not found"):
        load_checkpoint(Path("non_existent_model_checkpoint.pth"))


def test_create_test_loader_and_remapped(tmp_path: Path):
    classes = ["compost", "glass", "landfill", "paper", "plastic"]
    test_dir = _create_dummy_test_dataset(tmp_path / "test_data", classes, per_class=2)

    loader, detected = create_test_loader(
        test_dir=test_dir,
        target_classes=classes,
        batch_size=4,
        num_workers=0,
    )
    assert len(loader.dataset) == 10
    assert detected == classes

    # Test remapped dataset with non-standard class order
    reversed_classes = list(reversed(classes))
    loader_rev, _ = create_test_loader(
        test_dir=test_dir,
        target_classes=reversed_classes,
        batch_size=4,
        num_workers=0,
    )
    assert isinstance(loader_rev.dataset, RemappedDataset)
    assert len(loader_rev.dataset) == 10


def test_evaluate_model_performance(tmp_path: Path):
    classes = ["compost", "glass", "landfill", "paper", "plastic"]
    test_dir = _create_dummy_test_dataset(tmp_path / "test_data", classes, per_class=2)

    loader, _ = create_test_loader(
        test_dir=test_dir,
        target_classes=classes,
        batch_size=4,
        num_workers=0,
    )

    model = build_model("resnet18", num_classes=len(classes))
    device = torch.device("cpu")
    results = evaluate_model_performance(model, loader, classes, device)

    assert "accuracy" in results
    assert 0.0 <= results["accuracy"] <= 1.0
    assert "classification_report_str" in results
    assert "classification_report_dict" in results
    assert "confusion_matrix" in results
    assert "normalized_confusion_matrix" in results

    cm = results["confusion_matrix"]
    cm_norm = results["normalized_confusion_matrix"]
    assert cm.shape == (5, 5)
    assert cm_norm.shape == (5, 5)
    assert np.all(cm_norm >= 0.0) and np.all(cm_norm <= 1.0)
    for c in classes:
        assert c in results["classification_report_dict"]


def test_plot_confusion_matrix(tmp_path: Path):
    classes = ["compost", "glass", "landfill", "paper", "plastic"]
    cm_norm = np.eye(5)
    plot_file = tmp_path / "docs" / "confusion_matrix.png"

    saved_path = plot_confusion_matrix(
        cm_normalized=cm_norm,
        classes=classes,
        output_path=plot_file,
        accuracy=1.0,
    )
    assert saved_path.is_file()
    assert saved_path.stat().st_size > 0


def test_run_evaluation_pipeline(tmp_path: Path):
    classes = DEFAULT_CLASSES
    model = build_model("resnet18", num_classes=len(classes))
    checkpoint_file = tmp_path / "test_model.pth"
    torch.save(
        {"model_state_dict": model.state_dict(), "class_names": classes},
        checkpoint_file,
    )

    test_dir = _create_dummy_test_dataset(tmp_path / "test_split", classes, per_class=1)
    plot_file = tmp_path / "eval_plot.png"

    results = run_evaluation(
        model_path=checkpoint_file,
        test_dir=test_dir,
        output_plot=plot_file,
        batch_size=2,
        num_workers=0,
        arch="resnet18",
        device=get_device("cpu"),
    )

    assert results["accuracy"] >= 0.0
    assert plot_file.is_file()
    assert plot_file.stat().st_size > 0


def test_run_evaluation_mobilenet_v2_auto_detect(tmp_path: Path):
    classes = DEFAULT_CLASSES
    model = build_model("mobilenet_v2", num_classes=len(classes))
    checkpoint_file = tmp_path / "mobilenet_test.pth"
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_names": classes,
            "architecture": "mobilenet_v2",
        },
        checkpoint_file,
    )

    test_dir = _create_dummy_test_dataset(
        tmp_path / "test_split_mobile", classes, per_class=1
    )
    plot_file = tmp_path / "eval_plot_mobile.png"

    results = run_evaluation(
        model_path=checkpoint_file,
        test_dir=test_dir,
        output_plot=plot_file,
        batch_size=2,
        num_workers=0,
        arch="auto",
        device=get_device("cpu"),
    )

    assert results["accuracy"] >= 0.0
    assert plot_file.is_file()
    assert plot_file.stat().st_size > 0


def test_load_classes_from_package_invalid_keys(tmp_path: Path):
    classes_json = tmp_path / "classes.json"
    with open(classes_json, "w", encoding="utf-8") as f:
        json.dump({"non_integer_key": "compost"}, f)

    checkpoint_file = tmp_path / "dummy.pth"
    # Should catch ValueError and return None without throwing an exception
    assert load_classes_from_package(checkpoint_file) is None


def test_load_checkpoint_fallback_warning(tmp_path: Path, monkeypatch):
    checkpoint_file = tmp_path / "checkpoint.pth"
    classes = ["compost", "glass", "landfill", "paper", "plastic"]
    model = build_model("resnet18", num_classes=len(classes))

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_names": classes,
        },
        checkpoint_file,
    )

    orig_torch_load = torch.load

    def mock_torch_load(*args, **kwargs):
        if kwargs.get("weights_only", True):
            raise RuntimeError("Simulated weights_only failure")
        return orig_torch_load(*args, **kwargs)

    monkeypatch.setattr(torch, "load", mock_torch_load)

    with pytest.warns(UserWarning, match="weights_only=True failed"):
        loaded_model, loaded_classes, _ = load_checkpoint(
            checkpoint_file,
            arch="resnet18",
            device=torch.device("cpu"),
        )
    assert loaded_classes == classes
    assert isinstance(loaded_model, nn.Module)
