"""Tests for v2 orientation augmentation, inference parity, and rotation consistency."""

from __future__ import annotations

import io
import pickle
import sys
from pathlib import Path

import torch
from PIL import Image, ImageDraw
from torch import nn
from torchvision import models

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.inference import ModelService
from ml.scripts.check_rotation_consistency import (
    evaluate_image_rotations,
    evaluate_rotation_batch,
)
from ml.scripts.train_v2 import (
    RandomRightAngleRotation,
    exif_pil_loader,
    get_v2_eval_transforms,
    get_v2_train_transforms,
)

CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]


def _save_exif_rotated_jpeg(path: Path) -> bytes:
    """Create a 40x20 rectangular JPEG tagged with EXIF Orientation=6 (needs 90 CW)."""
    img = Image.new("RGB", (40, 20), (200, 120, 40))
    exif = img.getexif()
    exif[274] = 6
    buf = io.BytesIO()
    img.save(buf, format="JPEG", exif=exif.tobytes())
    raw = buf.getvalue()
    path.write_bytes(raw)
    return raw


def test_train_v2_exif_and_eval_transform_parity(tmp_path: Path) -> None:
    sample_path = tmp_path / "rotated.jpg"
    raw = _save_exif_rotated_jpeg(sample_path)

    loaded = exif_pil_loader(str(sample_path))
    assert loaded.mode == "RGB"
    # EXIF orientation 6 rotates 40x20 into portrait 20x40.
    assert loaded.size == (20, 40)

    eval_t = get_v2_eval_transforms()
    tensor = eval_t(loaded)
    assert tensor.shape == (3, 224, 224)

    ModelService.reset_instance()
    try:
        svc = ModelService(model_path=tmp_path / "missing.pth", device="cpu")
        svc_steps = [type(t).__name__ for t in svc.transform.transforms]
        val_steps = [type(t).__name__ for t in eval_t.transforms]
        assert svc_steps == val_steps
        assert svc.transform(loaded).shape == tensor.shape
        assert torch.allclose(svc.transform(loaded), tensor)
    finally:
        ModelService.reset_instance()
    assert len(raw) > 0


def test_random_right_angle_rotation_is_picklable_and_covers_all_angles() -> None:
    rotator = RandomRightAngleRotation()
    reloaded = pickle.loads(pickle.dumps(rotator))
    img = Image.new("RGB", (30, 16), (10, 20, 30))

    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 8, 8), fill=(255, 0, 0))

    seen_signatures = set()
    for _ in range(120):
        out = reloaded(img)
        seen_signatures.add(
            (out.size, out.getpixel((2, 2)), out.getpixel((2, out.height - 3)))
        )
    # Distinct corner marker + 30x16 dims yields 4 unique signatures across 0/90/180/270.
    assert len(seen_signatures) == 4

    train_t = get_v2_train_transforms()
    assert isinstance(pickle.loads(pickle.dumps(train_t))(img), torch.Tensor)


def _save_constant_prediction_checkpoint(
    path: Path, target_class: str = "plastic", logit_val: float = 8.0
) -> None:
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, len(CLASSES))
    with torch.no_grad():
        model.classifier[1].weight.zero_()
        model.classifier[1].bias.zero_()
        model.classifier[1].bias[CLASSES.index(target_class)] = logit_val
    torch.save(
        {
            "architecture": "mobilenet_v2",
            "model_state_dict": model.state_dict(),
            "class_names": list(CLASSES),
        },
        path,
    )


def test_rotation_consistency_evaluator_passes_and_catches_angle_flips(
    tmp_path: Path,
) -> None:
    ckpt = tmp_path / "plastic_const.pth"
    _save_constant_prediction_checkpoint(ckpt, target_class="plastic", logit_val=8.0)

    sample = tmp_path / "cup.jpg"
    raw = _save_exif_rotated_jpeg(sample)

    ModelService.reset_instance()
    try:
        svc = ModelService(model_path=ckpt, device="cpu")
        single = evaluate_image_rotations(
            svc, raw, expected_label="plastic", confidence_cutoff=0.60
        )
        assert single["correct_angles"] == 4
        assert single["all_confident_correct"] is True

        wrong_expected = evaluate_rotation_batch(
            svc, [(sample, "paper")], confidence_cutoff=0.60
        )
        assert wrong_expected["correct_angle_evals"] == 0
        assert wrong_expected["all_angles_correct_images"] == 0
    finally:
        ModelService.reset_instance()
