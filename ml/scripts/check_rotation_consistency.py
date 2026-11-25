"""Rotation consistency evaluator for Sortify ModelService checkpoints."""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.inference import ModelService

ROTATION_ANGLES = (0, 90, 180, 270)


def evaluate_image_rotations(
    service: ModelService,
    image_bytes: bytes,
    expected_label: str,
    *,
    confidence_cutoff: float = 0.60,
    angles: tuple[int, ...] = ROTATION_ANGLES,
) -> dict[str, Any]:
    """Evaluate ModelService predictions across EXIF-corrected rotations of one image."""
    with Image.open(io.BytesIO(image_bytes)) as raw:
        try:
            transposed = ImageOps.exif_transpose(raw)
        except (TypeError, ValueError, OSError):
            transposed = raw
        upright = transposed.convert("RGB")

    per_angle: list[dict[str, Any]] = []
    for angle in angles:
        rotated = upright if angle == 0 else upright.rotate(angle, expand=True)
        buf = io.BytesIO()
        rotated.save(buf, format="JPEG", quality=92)
        pred = service.predict(buf.getvalue())
        if pred.get("is_mock"):
            raise RuntimeError(
                "ModelService returned fallback mock inference; load a valid checkpoint."
            )
        confident = pred["confidence"] >= confidence_cutoff
        per_angle.append(
            {
                "angle": angle,
                "predicted": pred["category"],
                "confidence": pred["confidence"],
                "correct": pred["category"] == expected_label,
                "confident_correct": pred["category"] == expected_label and confident,
                "unsure": not confident,
                "alternatives": pred.get("alternatives", []),
            }
        )

    return {
        "expected": expected_label,
        "all_correct": all(item["correct"] for item in per_angle),
        "all_confident_correct": all(item["confident_correct"] for item in per_angle),
        "correct_angles": sum(1 for item in per_angle if item["correct"]),
        "confident_correct_angles": sum(
            1 for item in per_angle if item["confident_correct"]
        ),
        "angles": per_angle,
    }


def evaluate_rotation_batch(
    service: ModelService,
    samples: list[tuple[Path, str]],
    *,
    confidence_cutoff: float = 0.60,
    angles: tuple[int, ...] = ROTATION_ANGLES,
) -> dict[str, Any]:
    """Run rotation consistency checks over a list of (image_path, expected_label)."""
    results = []
    for path, label in samples:
        item = evaluate_image_rotations(
            service,
            path.read_bytes(),
            label,
            confidence_cutoff=confidence_cutoff,
            angles=angles,
        )
        item["file"] = str(path)
        results.append(item)

    total_images = len(results)
    total_angles = sum(len(r["angles"]) for r in results)
    return {
        "images": total_images,
        "total_angle_evals": total_angles,
        "all_angles_correct_images": sum(1 for r in results if r["all_correct"]),
        "all_angles_confident_images": sum(
            1 for r in results if r["all_confident_correct"]
        ),
        "correct_angle_evals": sum(r["correct_angles"] for r in results),
        "confident_correct_angle_evals": sum(
            r["confident_correct_angles"] for r in results
        ),
        "samples": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--split", default="test")
    parser.add_argument("--cutoff", type=float, default=0.60)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    import csv

    manifest_dir = args.manifest.resolve().parent
    samples: list[tuple[Path, str]] = []
    with args.manifest.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("split") != args.split:
                continue
            raw_path = Path(row["filename"])
            img_path = (
                raw_path
                if raw_path.is_absolute() or raw_path.exists()
                else manifest_dir / raw_path
            )
            samples.append((img_path, row["class"]))

    if not samples:
        raise SystemExit(
            f"No manifest rows matched split={args.split!r} in {args.manifest}"
        )

    ModelService.reset_instance()
    service = ModelService(model_path=args.checkpoint.resolve(), device="cpu")
    if service.model is None:
        raise SystemExit(f"Failed to load {args.checkpoint}")

    report = evaluate_rotation_batch(service, samples, confidence_cutoff=args.cutoff)
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    angle_count = len(ROTATION_ANGLES)
    print(
        f"Rotation consistency ({args.checkpoint.name}): "
        f"{report['correct_angle_evals']}/{report['total_angle_evals']} angle-evals correct, "
        f"{report['all_angles_correct_images']}/{report['images']} images {angle_count}/{angle_count} correct, "
        f"{report['all_angles_confident_images']}/{report['images']} images {angle_count}/{angle_count} confident>={args.cutoff}"
    )
    for item in report["samples"]:
        summary = [
            (a["angle"], a["predicted"], a["confidence"]) for a in item["angles"]
        ]
        print(f"  {Path(item['file']).name} ({item['expected']}): {summary}")


if __name__ == "__main__":
    main()
