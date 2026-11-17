"""Verify and package the selected PyTorch checkpoint for Sortify's API runtime."""

import argparse
import hashlib
import json
import pickle
import platform
import re
import shutil
import tempfile
from importlib.metadata import version
from pathlib import Path

import torch

from backend.app.routers.classify import LABEL_TO_CATEGORY
from backend.app.schemas import ClassificationAlternative
from backend.app.schemas.schemas import ALLOWED_CATEGORIES
from backend.app.services.inference import ModelService, detect_architecture


def file_sha256(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def checkpoint_metadata(path: Path) -> tuple[str, list[str], list[str]]:
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(checkpoint, dict):
        raise TypeError("Expected a PyTorch checkpoint with class_names metadata")
    labels = checkpoint.get("class_names")
    if not isinstance(labels, (list, tuple)) or any(
        not isinstance(label, str) for label in labels
    ):
        raise ValueError("Checkpoint must declare its ordered class_names")
    categories = [LABEL_TO_CATEGORY.get(label.strip().lower(), "") for label in labels]
    if (
        len(categories) != len(ALLOWED_CATEGORIES)
        or set(categories) != ALLOWED_CATEGORIES
    ):
        raise ValueError("Checkpoint labels must map one-to-one to the five API bins")
    return detect_architecture(checkpoint), list(labels), categories


def smoke_samples(service: ModelService, images: list[Path]) -> list[dict]:
    samples = []
    for image_path in images:
        data = image_path.read_bytes()
        first = service.predict(data)
        repeat = service.predict(data)
        if first["is_mock"] or repeat["is_mock"]:
            raise ValueError("The runtime used fallback inference")
        for result in (first, repeat):
            result.pop("latency_ms")
        if first != repeat:
            raise ValueError(f"Inference changed on repeated input: {image_path.name}")
        category = LABEL_TO_CATEGORY[first["category"].strip().lower()]
        prediction = ClassificationAlternative(
            category=category, confidence=first["confidence"]
        )
        alternatives = [
            ClassificationAlternative(
                category=LABEL_TO_CATEGORY[alt["category"].strip().lower()],
                confidence=alt["confidence"],
            ).model_dump()
            for alt in first["alternatives"]
        ]
        samples.append(
            {
                "file": image_path.name,
                "sha256": hashlib.sha256(data).hexdigest(),
                **prediction.model_dump(),
                "alternatives": alternatives,
            }
        )
    return samples


def package_release(
    checkpoint: Path,
    output: Path,
    *,
    source_commit: str,
    source: str,
    expected_sha256: str,
    images: list[Path],
) -> dict:
    if not checkpoint.is_file():
        raise FileNotFoundError(f"Checkpoint unavailable: {checkpoint}")
    if checkpoint.name.casefold() == "manifest.json":
        raise ValueError(
            "Use the checkpoint's artifact filename, distinct from manifest.json"
        )
    if not re.fullmatch(r"[0-9a-fA-F]{40}", source_commit):
        raise ValueError("Provide the full checkpoint source commit SHA")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
        raise ValueError("Provide the checkpoint owner's SHA-256 digest")
    if not source.strip():
        raise ValueError("Provide the checkpoint's authorized download location")
    if output.exists():
        raise FileExistsError(f"Output directory already exists: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".sortify-release-", dir=output.parent
    ) as temp:
        staging = Path(temp) / "package"
        staging.mkdir()
        artifact = staging / checkpoint.name
        shutil.copyfile(checkpoint, artifact)
        actual_sha256 = file_sha256(artifact)
        if actual_sha256 != expected_sha256.lower():
            raise ValueError("Checkpoint SHA-256 does not match the expected digest")
        architecture, labels, categories = checkpoint_metadata(artifact)

        ModelService.reset_instance()
        try:
            service = ModelService(model_path=artifact.resolve(), device="cpu")
            if service.model is None or service.class_names != labels:
                raise ValueError(
                    "Checkpoint did not load with the declared labels in ModelService"
                )
            resize, _, normalize = service.transform.transforms
            manifest = {
                "source_commit": source_commit.lower(),
                "download_location": source,
                "artifact": artifact.name,
                "sha256": actual_sha256,
                "architecture": architecture,
                "class_names": labels,
                "api_categories": categories,
                "runtime_preprocessing": {
                    "decode": "EXIF transpose, then RGB",
                    "resize_hw": list(resize.size),
                    "interpolation": resize.interpolation.value,
                    "antialias": resize.antialias,
                    "crop": None,
                    "tensor_scale": "[0, 1]",
                    "normalize_mean": normalize.mean,
                    "normalize_std": normalize.std,
                },
                "verification_device": "cpu",
                "versions": {
                    "python": platform.python_version(),
                    **{
                        name: version(name)
                        for name in ("torch", "torchvision", "Pillow", "numpy")
                    },
                },
                "confidence": "Top softmax score rounded to four decimals. No rejection threshold.",
                "direct_inference_samples": smoke_samples(service, images),
            }
        finally:
            ModelService.reset_instance()
        (staging / "manifest.json").write_text(
            json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8"
        )
        if output.exists():
            raise FileExistsError(f"Output directory already exists: {output}")
        staging.rename(output)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--source", required=True, help="Authorized artifact location")
    parser.add_argument(
        "--sha256", required=True, help="Digest from the artifact owner"
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="New package directory"
    )
    parser.add_argument("--image", type=Path, action="append", default=[])
    args = parser.parse_args()
    try:
        manifest = package_release(
            args.checkpoint,
            args.output,
            source_commit=args.source_commit,
            source=args.source,
            expected_sha256=args.sha256,
            images=args.image,
        )
    except (
        OSError,
        ValueError,
        RuntimeError,
        KeyError,
        TypeError,
        EOFError,
        pickle.UnpicklingError,
    ) as error:
        parser.exit(1, f"Model package failed: {error}\n")
    print(f"Verified {manifest['sha256']} and wrote {args.output / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
