"""Contracts later weeks depend on. CPU tensors and tmp images only."""

from __future__ import annotations

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

from ml.scripts.dataset import (
    get_dataloaders,
    get_eval_transforms,
    get_train_transforms,
)
from ml.scripts.preprocess import preprocess_directory, preprocess_image
from ml.scripts.split_data import CLASSES, create_dataset_splits
from ml.scripts.train_baseline import (
    CLASS_NAMES,
    load_baseline_checkpoint,
    require_best_checkpoint,
    run_epoch,
)
from ml.scripts.train_mobilenet import (
    bin_confidences,
    load_mobilenet_checkpoint,
    same_class_order,
    write_comparison,
)

RATIOS = {"train": 0.70, "val": 0.15, "test": 0.15}


def _solid(
    path: Path, color: tuple[int, int, int], size: tuple[int, int] = (32, 48)
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path, format="JPEG")


def _class_tree(root: Path, per_class: int) -> None:
    for name in CLASSES:
        for index in range(per_class):
            _solid(root / name / f"{name}_{index:02d}.jpg", (index * 10, 40, 80))


def test_preprocess_is_rgb_224_and_skips_broken_files(tmp_path: Path) -> None:
    source = tmp_path / "raw"
    output = tmp_path / "out"
    good = source / "compost" / "leaf.jpg"
    _solid(good, (128, 128, 128))
    original = good.read_bytes()
    broken = source / "compost" / "broken.jpg"
    broken.write_bytes(b"this is not a jpeg")

    written, skipped = preprocess_directory(source, output)

    assert (written, skipped) == (1, 1)
    assert good.read_bytes() == original
    saved = output / "compost" / "leaf.jpg"
    with Image.open(saved) as image:
        image.load()
        assert image.mode == "RGB"
        assert image.size == (224, 224)
        pixels = np.asarray(image)
    assert pixels.shape == (224, 224, 3)
    # Flat gray stays gray. ImageNet mean/std would pull the channels apart.
    assert max(pixels.mean(axis=(0, 1))) - min(pixels.mean(axis=(0, 1))) < 15


def test_preprocess_resize_is_bilinear(tmp_path: Path) -> None:
    source = tmp_path / "corners.png"
    image = Image.new("RGB", (2, 2))
    image.putpixel((0, 0), (0, 0, 0))
    image.putpixel((1, 0), (255, 0, 0))
    image.putpixel((0, 1), (0, 255, 0))
    image.putpixel((1, 1), (0, 0, 255))
    image.save(source)
    destination = tmp_path / "out.jpg"
    preprocess_image(source, destination)
    with Image.open(destination) as saved:
        colors = {tuple(pixel) for pixel in np.asarray(saved).reshape(-1, 3)}
    assert len(colors) > 4


def test_split_names_ratios_and_seed(tmp_path: Path) -> None:
    source = tmp_path / "raw"
    _class_tree(source, per_class=20)
    first = tmp_path / "split_a"
    second = tmp_path / "split_b"
    create_dataset_splits(source, first, RATIOS, seed=42)
    create_dataset_splits(source, second, RATIOS, seed=42)

    for split_root in (first, second):
        for class_name in CLASSES:
            counts = {
                split: len(list((split_root / split / class_name).glob("*.jpg")))
                for split in ("train", "val", "test")
            }
            total = sum(counts.values())
            assert counts["train"] / total == pytest.approx(0.70, abs=0.02)
            assert counts["val"] / total == pytest.approx(0.15, abs=0.02)
            assert counts["test"] / total == pytest.approx(0.15, abs=0.02)
            assert set(counts) == {"train", "val", "test"}

    for split in ("train", "val", "test"):
        for class_name in CLASSES:
            left = sorted(p.name for p in (first / split / class_name).glob("*.jpg"))
            right = sorted(p.name for p in (second / split / class_name).glob("*.jpg"))
            assert left == right
            assert left


def test_dataloaders_honor_batch_size_and_class_order(tmp_path: Path) -> None:
    data = tmp_path / "processed"
    for split in ("train", "val", "test"):
        _class_tree(data / split, per_class=2)
    train_loader, val_loader, test_loader, classes = get_dataloaders(
        data, batch_size=8, num_workers=0
    )
    assert train_loader.batch_size == 8
    assert val_loader.batch_size == 8
    assert test_loader.batch_size == 8
    assert list(classes) == ["compost", "glass", "landfill", "paper", "plastic"]
    assert classes[0] == "compost"
    assert classes[0] != "paper"
    train_names = [type(step).__name__ for step in get_train_transforms().transforms]
    eval_names = [type(step).__name__ for step in get_eval_transforms().transforms]
    assert "RandomResizedCrop" in train_names
    assert "RandomResizedCrop" not in eval_names
    assert "CenterCrop" in eval_names


def test_checkpoint_helper_loads_metadata_and_raw_state_dict(tmp_path: Path) -> None:
    model = nn.Linear(3, 5)
    raw_path = tmp_path / "raw.pth"
    meta_path = tmp_path / "meta.pth"
    torch.save(model.state_dict(), raw_path)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_names": list(CLASS_NAMES),
            "best_epoch": 6,
            "val_accuracy": 0.8458,
        },
        meta_path,
    )
    fresh = nn.Linear(3, 5)
    _, meta = load_baseline_checkpoint(meta_path, fresh)
    assert meta["class_names"] == list(CLASS_NAMES)
    assert meta["best_epoch"] == 6
    torch.testing.assert_close(fresh.weight, model.weight)

    other = nn.Linear(3, 5)
    _, raw = load_mobilenet_checkpoint(raw_path, other)
    assert "class_names" not in raw
    torch.testing.assert_close(other.weight, model.weight)


def test_empty_loader_and_missing_checkpoint() -> None:
    model = nn.Linear(4, 5)
    loss, accuracy = run_epoch(model, [], nn.CrossEntropyLoss(), torch.device("cpu"))
    assert (loss, accuracy) == (0.0, 0.0)
    with pytest.raises(RuntimeError, match="without any valid evaluation epochs"):
        require_best_checkpoint(None)


def test_softmax_over_five_bins_sums_to_one() -> None:
    logits = torch.tensor([[4.0, 1.0, 0.0, -1.0, 2.0]])
    probs = bin_confidences(logits)
    assert probs.shape == (1, 5)
    assert torch.allclose(probs.sum(dim=1), torch.ones(1), atol=1e-6)
    assert probs.min() >= 0
    assert not torch.allclose(probs, logits)
    assert list(CLASS_NAMES) == ["compost", "glass", "landfill", "paper", "plastic"]
    assert CLASS_NAMES[0] != "paper"


def test_comparison_reports_both_models_and_class_order(tmp_path: Path) -> None:
    rows = [
        {
            "name": "ResNet-18",
            "epoch": 6,
            "val_acc": 0.8458,
            "test_acc": 0.8433,
            "size_mb": 42.7,
            "latency_ms": 12.5,
        },
        {
            "name": "MobileNetV2",
            "epoch": 4,
            "val_acc": 0.80,
            "test_acc": 0.79,
            "size_mb": 9.1,
            "latency_ms": 6.2,
        },
    ]
    path = tmp_path / "architecture_comparison.md"
    write_comparison(path, rows, list(CLASS_NAMES))
    text = path.read_text(encoding="utf-8")
    assert "ResNet-18" in text and "MobileNetV2" in text
    assert "val accuracy" in text and "file size" in text and "CPU latency" in text
    assert "42.7 MB" in text and "12.50 ms" in text
    assert "compost" in text and "paper=0" in text
    assert same_class_order(
        CLASS_NAMES, ["compost", "glass", "landfill", "paper", "plastic"]
    )
    assert not same_class_order(
        CLASS_NAMES, ["paper", "plastic", "glass", "compost", "landfill"]
    )
