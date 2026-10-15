"""Measure how lighting and clutter change 5-bin confidence.

Uses the eval transform from ml/scripts/dataset.py and the checkpoint
loader from the baseline. ImageNet normalization stays in that transform.

Kathleen's campus folder is not required to import this module. Point
--data-dir at a folder of class subfolders when you have photos.

Run from the repo root. Prefer CPU when the GPU is already full:
    python ml/scripts/domain_gap.py --checkpoint ml/models/mobilenet_v2.pth \
        --data-dir data/processed/test --batch-size 16 --device cpu
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch
from PIL import Image, ImageDraw, ImageEnhance, UnidentifiedImageError
from torch import nn
from torchvision import models

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.dataset import get_eval_transforms
from ml.scripts.train_baseline import CLASS_NAMES, get_device, load_baseline_checkpoint
from ml.scripts.train_mobilenet import bin_confidences, same_class_order

# ImageFolder order is alphabetical, so index 0 is compost, not paper:
# 0: compost, 1: glass, 2: landfill, 3: paper, 4: plastic.
# Downstream code must read checkpoint["class_names"], not assume paper=0.
CONDITIONS = ("clean", "shadow", "dim", "clutter")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
GOLDEN_CONFIDENCE = 0.90
INPUT_SHAPE = (3, 224, 224)


def build_bare_model(architecture: str, num_classes: int) -> nn.Module:
    """Match a saved head without downloading pretrained weights."""
    if architecture == "resnet18":
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model
    if architecture == "mobilenet_v2":
        model = models.mobilenet_v2(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
        return model
    raise ValueError(f"Unknown architecture: {architecture}")


def architecture_from_state(state_dict: dict) -> str:
    keys = state_dict.keys()
    if any(key.startswith("fc.") for key in keys):
        return "resnet18"
    if any(key.startswith("classifier.") for key in keys):
        return "mobilenet_v2"
    raise ValueError("Checkpoint state_dict is not ResNet-18 or MobileNetV2.")


def load_domain_checkpoint(path: Path) -> tuple[nn.Module, dict, list[str]]:
    """Load weights. A missing file raises before load_state_dict."""
    if not path.is_file():
        raise FileNotFoundError(f"Checkpoint not found: {path}")
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if not isinstance(checkpoint, dict):
        raise TypeError(f"Checkpoint is not a dict: {path}")
    state_dict = checkpoint.get("model_state_dict", checkpoint)
    if not isinstance(state_dict, dict) or not any(
        hasattr(value, "shape") for value in state_dict.values()
    ):
        raise ValueError(f"Checkpoint has no state_dict: {path}")
    names = checkpoint.get("class_names")
    if not names:
        raise KeyError("Checkpoint is missing class_names. Refusing to assume paper=0.")
    names = list(names)
    if not same_class_order(names, CLASS_NAMES):
        raise ValueError(
            f"Class order mismatch. Checkpoint has {names}, "
            f"ImageFolder order is {list(CLASS_NAMES)}."
        )
    model = build_bare_model(architecture_from_state(state_dict), len(names))
    loaded, checkpoint = load_baseline_checkpoint(path, model)
    loaded.eval()
    return loaded, checkpoint, names


def apply_condition(image: Image.Image, condition: str) -> Image.Image:
    """Copy a photo with one demo-day change. clean returns RGB unchanged."""
    image = image.convert("RGB")
    if condition == "clean":
        return image
    if condition == "dim":
        return ImageEnhance.Brightness(image).enhance(0.4)
    if condition == "shadow":
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([0, 0, image.width // 2, image.height], fill=(0, 0, 0, 150))
        return Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    if condition == "clutter":
        cluttered = image.copy()
        draw = ImageDraw.Draw(cluttered)
        band = max(4, image.width // 6)
        draw.rectangle([0, 0, image.width, band], fill=(220, 30, 30))
        draw.rectangle(
            [0, image.height - band, image.width, image.height], fill=(30, 30, 220)
        )
        return cluttered
    raise ValueError(f"Unknown condition: {condition}")


def check_batch_shape(batch: torch.Tensor) -> None:
    if tuple(batch.shape[1:]) != INPUT_SHAPE:
        raise ValueError(
            f"Expected NCHW shape (N, {INPUT_SHAPE[0]}, {INPUT_SHAPE[1]}, "
            f"{INPUT_SHAPE[2]}), got {tuple(batch.shape)}."
        )


def iter_chunks(items: list, batch_size: int):
    if batch_size < 1:
        raise ValueError(f"batch size must be positive, got {batch_size}")
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


def load_rgb(path: Path) -> Image.Image | None:
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            return image.convert("RGB")
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError):
        return None


def collect_images(root: Path) -> tuple[list[tuple[Path, str | None]], int]:
    if not root.is_dir():
        raise FileNotFoundError(f"Image folder not found: {root}")
    labeled = [root / name for name in CLASS_NAMES if (root / name).is_dir()]
    skipped = 0
    found: list[tuple[Path, str | None]] = []
    folders = [(path, path.name) for path in labeled] if labeled else [(root, None)]
    for folder, label in folders:
        files = sorted(
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        )
        for path in files:
            image = load_rgb(path)
            if image is None:
                skipped += 1
                continue
            found.append((path, label))
    if not found:
        raise ValueError(f"No readable images in {root}")
    return found, skipped


def predict_probs(
    model, images: list[Image.Image], device, batch_size: int
) -> torch.Tensor:
    if not images:
        raise ValueError("empty inputs")
    model.eval()
    transform = get_eval_transforms()
    tensors = [transform(image) for image in images]
    outputs = []
    with torch.inference_mode():
        for chunk in iter_chunks(tensors, batch_size):
            batch = torch.stack(chunk).to(device)
            check_batch_shape(batch)
            logits = model(batch)
            outputs.append(bin_confidences(logits).cpu())
    return torch.cat(outputs, dim=0)


def golden_items(
    records: list[dict], threshold: float = GOLDEN_CONFIDENCE, limit: int = 5
):
    """Items that stay on the labeled bin at >= threshold under every condition.

    A folder label that disagrees with the predicted bin is not a demo item,
    even when the confidence is high.
    """
    winners = []
    for record in records:
        label = record.get("label")
        if label is not None and record["top_name"] != label:
            continue
        if record["clean_confidence"] < threshold:
            continue
        if any(score < threshold for score in record["condition_confidence"].values()):
            continue
        winners.append(record)
    winners.sort(key=lambda record: record["clean_confidence"], reverse=True)
    return winners[:limit]


def class_mix(golden: list[dict]) -> str:
    counts: dict[str, int] = {}
    for item in golden:
        name = item["top_name"]
        counts[name] = counts.get(name, 0) + 1
    parts = [f"{count} {name}" for name, count in sorted(counts.items())]
    return "Class mix: " + ", ".join(parts) + "."


def photo_label(path: Path) -> str:
    parent = path.parent.name
    if parent and parent not in {".", path.anchor}:
        return f"{parent}/{path.name}"
    return path.name


def evaluate_images(model, class_names, items, device, batch_size: int) -> list[dict]:
    photos = [image for image, _path, _label in items]
    by_condition = {}
    for condition in CONDITIONS:
        print(f"Scoring {condition}...", flush=True)
        by_condition[condition] = predict_probs(
            model,
            [apply_condition(image, condition) for image in photos],
            device,
            batch_size,
        )
    records = []
    for index, (_image, path, label) in enumerate(items):
        clean = by_condition["clean"][index]
        top = int(clean.argmax())
        record = {
            "path": path,
            "label": label,
            "top_name": class_names[top],
            "clean_confidence": float(clean[top]),
            "condition_confidence": {
                condition: float(by_condition[condition][index][top])
                for condition in CONDITIONS
            },
        }
        records.append(record)
    return records


def condition_drops(records: list[dict]) -> dict[str, float]:
    drops = {}
    for condition in CONDITIONS:
        if condition == "clean" or not records:
            continue
        losses = [
            record["clean_confidence"] - record["condition_confidence"][condition]
            for record in records
        ]
        drops[condition] = sum(losses) / len(losses)
    return drops


def write_scanning_guide(path: Path, report: dict) -> None:
    lines = [
        "# Demo scanning guide",
        "",
        "Kathleen's campus folder (`data/campus_test`) is not on this machine.",
        "The numbers below are the lab test photos already here, plus three",
        "simulated demo-day changes: a side shadow, dim light, and colored",
        "clutter along the edges. Crumpled campus items were not photographed.",
        "",
        "Class order is ImageFolder alphabetical. Index 0 is compost, not paper.",
        'Read `checkpoint["class_names"]`. Do not assume `paper=0`.',
        "",
        f"Checkpoint: `{report['checkpoint']}`",
        f"Photos scored: {report['n_images']} (skipped unreadable: {report['n_skipped']})",
        f"Batch size: {report['batch_size']}",
        "",
        "| condition | mean drop in confidence on the clean prediction |",
        "|---|---:|",
    ]
    for condition, drop in report["drops"].items():
        lines.append(f"| {condition} | {drop:.1%} |")
    lines.extend(["", "## Golden demo items", ""])
    golden = report["golden"]
    if not golden:
        lines.append(
            f"No photo stayed at or above {GOLDEN_CONFIDENCE:.0%} confidence "
            "under clean, shadow, dim light, and clutter together."
        )
    else:
        lines.append(
            f"These stayed at or above {GOLDEN_CONFIDENCE:.0%} on the same bin "
            "for every condition."
        )
        lines.append("")
        lines.append("| file | bin | clean | shadow | dim | clutter |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for item in golden:
            scores = item["condition_confidence"]
            lines.append(
                f"| {photo_label(item['path'])} | {item['top_name']} | "
                f"{item['clean_confidence']:.1%} | {scores['shadow']:.1%} | "
                f"{scores['dim']:.1%} | {scores['clutter']:.1%} |"
            )
        lines.append("")
        lines.append(class_mix(golden))
        if len(golden) < 5:
            lines.append("")
            lines.append(
                f"Only {len(golden)} of the 5 requested photos cleared that bar. "
                "Weaker photos are left off the list."
            )
    lines.extend(
        [
            "",
            "## How to hold the phone",
            "",
            "Hold the phone about 8–12 inches away (about a hand's length) on a",
            "plain background. The clutter test paints color on the edges, and",
            "that is the change to avoid at the demo table. Keep the item in the",
            "light. Dim photos lose confidence even when the bin stays the same.",
            "A shadow across half the item does the same. Fill the frame so the",
            "item, not the table, is what the crop sees.",
            "",
            "These photos were not rechecked on Caden's or Mong's phones.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "docs" / "ml" / "demo_scanning_guide.md",
    )
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument(
        "--device", choices=("auto", "cpu", "mps", "cuda"), default="auto"
    )
    args = parser.parse_args()

    model, _checkpoint, class_names = load_domain_checkpoint(args.checkpoint)
    device = get_device() if args.device == "auto" else torch.device(args.device)
    model = model.to(device)
    listed, skipped = collect_images(args.data_dir)
    items = []
    for path, label in listed:
        image = load_rgb(path)
        if image is None:
            skipped += 1
            continue
        items.append((image, path, label))
    if not items:
        raise ValueError("empty inputs")
    print(f"Device: {device}")
    print(f"Images: {len(items)} skipped={skipped} batch_size={args.batch_size}")
    print(f"Classes: {class_names}")
    records = evaluate_images(model, class_names, items, device, args.batch_size)
    drops = condition_drops(records)
    golden = golden_items(records)
    report = {
        "checkpoint": args.checkpoint,
        "n_images": len(records),
        "n_skipped": skipped,
        "batch_size": args.batch_size,
        "drops": drops,
        "golden": golden,
    }
    write_scanning_guide(args.output, report)
    print(f"{'condition':<10} {'mean_drop':>10}")
    for condition, drop in drops.items():
        print(f"{condition:<10} {drop:>10.1%}")
    print(
        f"Golden items (>={GOLDEN_CONFIDENCE:.0%} under every condition): {len(golden)}"
    )
    for item in golden:
        print(
            f"  {item['path'].name} {item['top_name']} {item['clean_confidence']:.1%}"
        )
    print("Example softmax (first photo, clean):")
    example = predict_probs(model, [items[0][0]], device, args.batch_size)[0]
    print(
        "  "
        + "  ".join(f"{name}={score:.1%}" for name, score in zip(class_names, example))
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
