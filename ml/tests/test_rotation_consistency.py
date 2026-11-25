"""Tests for v2 orientation augmentation, inference parity, and rotation consistency."""

from __future__ import annotations

import io
import json
import pickle
import sys
from pathlib import Path

import pytest
import torch
from PIL import Image, ImageDraw, ImageOps
from torch import nn
from torchvision import models

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.inference import ModelService
from ml.scripts import check_rotation_consistency
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


def test_predict_raw_exif_matches_upright_pixels(tmp_path: Path) -> None:
    # Build an asymmetric image so raw pixel orientation affects non-constant weights.
    upright = Image.new("RGB", (64, 48), (20, 40, 60))
    draw = ImageDraw.Draw(upright)
    draw.rectangle((0, 0, 28, 22), fill=(230, 30, 30))
    draw.rectangle((36, 26, 63, 47), fill=(30, 220, 80))

    upright_buf = io.BytesIO()
    upright.save(upright_buf, format="JPEG", quality=95)
    upright_bytes = upright_buf.getvalue()

    # Rotate 90 CCW (270 CW) and tag EXIF Orientation=6 (90 CW) so exif_transpose restores upright.
    stored = upright.rotate(90, expand=True)
    exif = stored.getexif()
    exif[274] = 6
    exif_buf = io.BytesIO()
    stored.save(exif_buf, format="JPEG", quality=95, exif=exif.tobytes())
    raw_exif_bytes = exif_buf.getvalue()

    torch.manual_seed(7)
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, len(CLASSES))
    ckpt = tmp_path / "seeded.pth"
    torch.save(
        {
            "architecture": "mobilenet_v2",
            "model_state_dict": model.state_dict(),
            "class_names": list(CLASSES),
        },
        ckpt,
    )

    ModelService.reset_instance()
    try:
        svc = ModelService(model_path=ckpt, device="cpu")
        pred_upright = svc.predict(upright_bytes)
        pred_exif = svc.predict(raw_exif_bytes)
        assert pred_exif["is_mock"] is False
        assert pred_exif["category"] == pred_upright["category"]
        assert abs(pred_exif["confidence"] - pred_upright["confidence"]) < 0.02
    finally:
        ModelService.reset_instance()


def test_exif_pil_loader_handles_malformed_exif(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "sample.jpg"
    _save_exif_rotated_jpeg(sample)

    def _raise_exif_error(_img: Image.Image) -> Image.Image:
        raise ValueError("corrupt exif tag")

    monkeypatch.setattr(ImageOps, "exif_transpose", _raise_exif_error)
    loaded = exif_pil_loader(str(sample))
    assert loaded.mode == "RGB"
    assert loaded.size == (40, 20)


def test_rotation_consistency_rejects_mock_and_handles_partial_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sample = tmp_path / "cup.jpg"
    raw = _save_exif_rotated_jpeg(sample)

    ModelService.reset_instance()
    try:
        mock_svc = ModelService(model_path=tmp_path / "missing.pth", device="cpu")
        with pytest.raises(RuntimeError, match="fallback mock"):
            evaluate_image_rotations(mock_svc, raw, expected_label="compost")
    finally:
        ModelService.reset_instance()

    ckpt = tmp_path / "plastic_const.pth"
    _save_constant_prediction_checkpoint(ckpt, target_class="plastic", logit_val=8.0)

    ModelService.reset_instance()
    try:
        svc = ModelService(model_path=ckpt, device="cpu")
        calls = {"n": 0}

        def _flip_second_call(_image_bytes: bytes) -> dict[str, object]:
            calls["n"] += 1
            cat = "glass" if calls["n"] == 2 else "plastic"
            return {
                "category": cat,
                "confidence": 0.9,
                "alternatives": [],
                "is_mock": False,
            }

        monkeypatch.setattr(svc, "predict", _flip_second_call)
        report = evaluate_rotation_batch(
            svc, [(sample, "plastic")], confidence_cutoff=0.60, angles=(0, 180)
        )
        assert report["total_angle_evals"] == 2
        assert report["correct_angle_evals"] == 1
        assert report["all_angles_correct_images"] == 0
        assert report["samples"][0]["all_correct"] is False
    finally:
        ModelService.reset_instance()


def test_check_rotation_consistency_cli_manifest_relative_and_empty_split(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ckpt = tmp_path / "plastic_const.pth"
    _save_constant_prediction_checkpoint(ckpt, target_class="plastic", logit_val=8.0)

    img_dir = tmp_path / "bundle" / "images"
    img_dir.mkdir(parents=True)
    img_path = img_dir / "cup.jpg"
    _save_exif_rotated_jpeg(img_path)

    manifest = tmp_path / "bundle" / "manifest.csv"
    manifest.write_text(
        "filename,class,split\nimages/cup.jpg,plastic,test\n", encoding="utf-8"
    )
    out_json = tmp_path / "report.json"

    other_cwd = tmp_path / "other"
    other_cwd.mkdir()
    monkeypatch.chdir(other_cwd)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "check_rotation_consistency.py",
            "--checkpoint",
            str(ckpt),
            "--manifest",
            str(manifest),
            "--split",
            "test",
            "--out",
            str(out_json),
        ],
    )
    try:
        check_rotation_consistency.main()
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload["images"] == 1
        assert payload["all_angles_correct_images"] == 1

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "check_rotation_consistency.py",
                "--checkpoint",
                str(ckpt),
                "--manifest",
                str(manifest),
                "--split",
                "nonexistent",
            ],
        )
        with pytest.raises(SystemExit, match="No manifest rows matched"):
            check_rotation_consistency.main()
    finally:
        ModelService.reset_instance()
