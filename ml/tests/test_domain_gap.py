"""Week 5 domain-gap contract. CPU tensors and tmp images only."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import torch
from PIL import Image
from torch import nn

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.domain_gap import (
    CLASS_NAMES,
    apply_condition,
    check_batch_shape,
    collect_images,
    evaluate_images,
    golden_items,
    iter_chunks,
    load_domain_checkpoint,
    predict_probs,
    write_scanning_guide,
)
from ml.scripts.train_baseline import CLASS_NAMES as BASELINE_NAMES


class ConstantModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.batch_sizes: list[int] = []

    def forward(self, batch):
        self.batch_sizes.append(batch.shape[0])
        logits = torch.zeros(batch.shape[0], 5)
        logits[:, 0] = 4
        return logits


def _jpeg(path: Path, color: tuple[int, int, int] = (40, 180, 40)) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (32, 40), color).save(path)


def test_missing_checkpoint_raises_before_load(tmp_path: Path) -> None:
    missing = tmp_path / "nope.pth"
    with pytest.raises(FileNotFoundError):
        load_domain_checkpoint(missing)


def test_non_dict_checkpoint_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "tensor.pth"
    torch.save(torch.zeros(2), path)
    with pytest.raises(TypeError, match="not a dict"):
        load_domain_checkpoint(path)


def test_empty_state_dict_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "empty.pth"
    torch.save({"model_state_dict": {}, "class_names": list(CLASS_NAMES)}, path)
    with pytest.raises(ValueError, match="no state_dict"):
        load_domain_checkpoint(path)


def test_incompatible_weights_fail_on_load(tmp_path: Path) -> None:
    path = tmp_path / "partial.pth"
    torch.save(
        {
            "model_state_dict": {
                "fc.weight": torch.zeros(5, 1),
                "fc.bias": torch.zeros(5),
            },
            "class_names": list(CLASS_NAMES),
        },
        path,
    )
    with pytest.raises(RuntimeError, match="state_dict"):
        load_domain_checkpoint(path)


def test_checkpoint_without_class_names_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "raw.pth"
    torch.save({"weight": torch.zeros(1)}, path)
    with pytest.raises(KeyError, match="class_names"):
        load_domain_checkpoint(path)


def test_class_order_mismatch_raises_before_load(tmp_path: Path) -> None:
    path = tmp_path / "wrong_order.pth"
    torch.save(
        {
            "model_state_dict": {
                "fc.weight": torch.zeros(5, 1),
                "fc.bias": torch.zeros(5),
            },
            "class_names": ["paper", "plastic", "glass", "compost", "landfill"],
        },
        path,
    )
    with pytest.raises(ValueError, match="Class order mismatch"):
        load_domain_checkpoint(path)


def test_broken_image_is_skipped_and_empty_folder_fails(tmp_path: Path) -> None:
    root = tmp_path / "photos"
    _jpeg(root / "compost" / "ok.jpg")
    (root / "compost" / "broken.jpg").write_bytes(b"not-an-image")
    found, skipped = collect_images(root)
    assert skipped == 1
    assert [path.name for path, _label in found] == ["ok.jpg"]

    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(ValueError, match="No readable images"):
        collect_images(empty)
    with pytest.raises(FileNotFoundError):
        collect_images(tmp_path / "missing")


def test_wrong_shape_and_empty_inputs() -> None:
    with pytest.raises(ValueError, match="NCHW"):
        check_batch_shape(torch.zeros(2, 1, 8, 8))
    model = ConstantModel()
    with pytest.raises(ValueError, match="empty inputs"):
        predict_probs(model, [], torch.device("cpu"), batch_size=4)


def test_batch_size_is_honored_and_softmax_sums_to_one(tmp_path: Path) -> None:
    images = [Image.new("RGB", (30, 30), (20, 200, 20)) for _ in range(5)]
    model = ConstantModel()
    probs = predict_probs(model, images, torch.device("cpu"), batch_size=2)
    assert model.batch_sizes == [2, 2, 1]
    assert probs.shape == (5, 5)
    assert torch.allclose(probs.sum(dim=1), torch.ones(5), atol=1e-5)
    assert list(CLASS_NAMES) == list(BASELINE_NAMES)
    assert CLASS_NAMES[0] == "compost"
    chunks = [len(chunk) for chunk in iter_chunks(images, 2)]
    assert chunks == [2, 2, 1]
    with pytest.raises(ValueError, match="batch size"):
        list(iter_chunks(images, 0))
    assert (tmp_path / "unused").exists() is False


def test_conditions_change_the_photo_and_golden_bar() -> None:
    image = Image.new("RGB", (60, 40), (180, 180, 180))
    dim = apply_condition(image, "dim")
    assert dim.getpixel((10, 10))[0] < image.getpixel((10, 10))[0]
    shadow = apply_condition(image, "shadow")
    assert shadow.getpixel((2, 2))[0] < shadow.getpixel((image.width - 2, 2))[0]
    clutter = apply_condition(image, "clutter")
    assert clutter.getpixel((2, 2)) != image.getpixel((2, 2))
    with pytest.raises(ValueError, match="Unknown condition"):
        apply_condition(image, "crumple")

    strong = {
        "path": Path("cup.jpg"),
        "top_name": "plastic",
        "clean_confidence": 0.97,
        "condition_confidence": {
            "clean": 0.97,
            "shadow": 0.95,
            "dim": 0.93,
            "clutter": 0.91,
        },
    }
    fragile = {
        "path": Path("napkin.jpg"),
        "top_name": "compost",
        "clean_confidence": 0.96,
        "condition_confidence": {
            "clean": 0.96,
            "shadow": 0.40,
            "dim": 0.96,
            "clutter": 0.96,
        },
    }
    wrong = {
        "path": Path("glass") / "shiny.jpg",
        "label": "glass",
        "top_name": "plastic",
        "clean_confidence": 0.99,
        "condition_confidence": {
            "clean": 0.99,
            "shadow": 0.99,
            "dim": 0.99,
            "clutter": 0.99,
        },
    }
    chosen = golden_items([fragile, strong, wrong])
    assert [item["path"].name for item in chosen] == ["cup.jpg"]


def _qualifying(cls: str, confidence: float, filename: str) -> dict:
    return {
        "path": Path(cls) / filename,
        "label": cls,
        "top_name": cls,
        "clean_confidence": confidence,
        "condition_confidence": {
            "clean": confidence,
            "shadow": confidence,
            "dim": confidence,
            "clutter": confidence,
        },
    }


def test_one_class_cannot_fill_the_list_when_others_qualify() -> None:
    records = [
        _qualifying("compost", 0.99, "a.jpg"),
        _qualifying("compost", 0.98, "b.jpg"),
        _qualifying("compost", 0.97, "c.jpg"),
        _qualifying("compost", 0.96, "d.jpg"),
        _qualifying("compost", 0.95, "e.jpg"),
        _qualifying("glass", 0.91, "g.jpg"),
        _qualifying("landfill", 0.94, "l.jpg"),
        _qualifying("paper", 0.92, "p.jpg"),
        _qualifying("plastic", 0.93, "pl.jpg"),
    ]
    chosen = golden_items(records)
    assert len(chosen) == 5
    assert [item["top_name"] for item in chosen].count("compost") == 1
    assert {item["top_name"] for item in chosen} == {
        "compost",
        "glass",
        "landfill",
        "paper",
        "plastic",
    }


def test_guide_reports_drops_and_does_not_invent_items(tmp_path: Path) -> None:
    model = ConstantModel()
    image = Image.new("RGB", (28, 28), (10, 160, 10))
    items = [(image, Path("leaf.jpg"), "compost")]
    records = evaluate_images(model, list(CLASS_NAMES), items, torch.device("cpu"), 4)
    assert records[0]["top_name"] == "compost"
    assert records[0]["clean_confidence"] > 0.5
    report = {
        "checkpoint": Path("mobilenet_v2.pth"),
        "n_images": 1,
        "n_skipped": 1,
        "batch_size": 4,
        "drops": {"shadow": 0.12, "dim": 0.08, "clutter": 0.2},
        "golden": [],
    }
    destination = tmp_path / "demo_scanning_guide.md"
    write_scanning_guide(destination, report)
    text = destination.read_text(encoding="utf-8")
    assert "shadow" in text and "dim" in text and "clutter" in text
    assert "campus_test" in text
    assert "paper=0" in text
    assert "No photo stayed" in text
    assert "8–12 inches" in text

    report["golden"] = [
        {
            "path": Path("plastic") / "cup.jpg",
            "top_name": "plastic",
            "clean_confidence": 0.97,
            "object_name": "plastic milk jug",
            "condition_confidence": {
                "clean": 0.97,
                "shadow": 0.95,
                "dim": 0.93,
                "clutter": 0.91,
            },
        }
    ]
    report["missing_bins"] = ["glass"]
    write_scanning_guide(destination, report)
    listed = destination.read_text(encoding="utf-8")
    assert "plastic/cup.jpg" in listed
    assert "plastic milk jug" in listed
    assert "Only 1 of the 5" in listed
    assert "Class mix: 1 plastic." in listed
    assert "No qualifying photo in: glass" in listed
    assert "not lowered" in listed
