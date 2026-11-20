
"""OOD robustness stress test using the real ResNet18 checkpoint."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


import argparse
import csv
from pathlib import Path

import torch
from PIL import Image, ImageOps
from torchvision import transforms

from backend.app.services.inference import build_model, detect_architecture

ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT = ROOT / "ml/models/resnet18_finetuned.pth"
OOD_DIR = ROOT / "data/ood_non_waste"
OUTPUT = ROOT / "docs/ml/ood_results.csv"
THRESHOLD = 0.50
EXPECTED_IMAGES = 30

CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]

PREPROCESS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=OOD_DIR)
    args = parser.parse_args()

    images = sorted(
        p for p in args.data_dir.rglob("*")
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )

    if len(images) != EXPECTED_IMAGES:
        raise SystemExit(
            f"Expected exactly 30 OOD images; found {len(images)}."
        )

    device = torch.device("cpu")

    checkpoint = torch.load(
        CHECKPOINT, map_location="cpu", weights_only=False
    )
    architecture = detect_architecture(checkpoint)
    classes = checkpoint["class_names"]
    state = checkpoint["model_state_dict"]

    model = build_model(architecture, len(classes))
    model.load_state_dict(state)
    model.eval().to(device)

    results = []

    with torch.inference_mode():
        for path in images:
            try:
                with Image.open(path) as image:
                    image = ImageOps.exif_transpose(image).convert("RGB")
                    tensor = PREPROCESS(image).unsqueeze(0).to(device)

                probabilities = torch.softmax(model(tensor), dim=1)[0]
                confidence, index = probabilities.max(dim=0)

                confidence = confidence.item()
                predicted = classes[index.item()]
                uncertain = confidence < THRESHOLD

                results.append({
                    "image": str(path.relative_to(args.data_dir)),
                    "predicted_category": predicted,
                    "confidence": round(confidence, 4),
                    "uncertain": uncertain,
                })

            except Exception as exc:
                raise RuntimeError(f"Failed on {path}: {exc}") from exc

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    rejected = sum(r["uncertain"] for r in results)
    false_positives = sum(not r["uncertain"] for r in results)
    rate = rejected / len(results) * 100

    print(f"Images tested: {len(results)}")
    print(f"Threshold: {THRESHOLD}")
    print(f"Rejected: {rejected}/30 ({rate:.1f}%)")
    print(f"False positives: {false_positives}/30")
    print(f"Target >= 90%: {'PASS' if rate >= 90 else 'FAIL'}")
    print(f"Results saved to: {OUTPUT}")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
