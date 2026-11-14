"""Evaluates precision and rejection rates across different confidence cutoffs."""

import argparse
import statistics
from pathlib import Path

import torch
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

MODEL_PATHS = (
    Path("ml/models/sortify_v2.pth"),
    Path("ml/models/sortify_mvp_v1.pth"),
)
TEST_DIR = Path("data/processed_v2/test")
REPORT_PATH = Path("docs/ml/threshold_calibration_results.md")
THRESHOLDS = [0.40, 0.50, 0.60]
TARGET_PRECISION = 90.0  # percent; used to pick the optimal threshold
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

transform = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def find_checkpoint():
    for path in MODEL_PATHS:
        if path.exists():
            return path
    return None


def load_model(checkpoint, class_names):
    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(class_names))

    state = torch.load(checkpoint, map_location="cpu")
    saved_classes = None
    if isinstance(state, dict) and "model_state_dict" in state:
        # Training checkpoint: weights plus metadata (class_names, best_epoch, ...).
        saved_classes = state.get("class_names")
        state = state["model_state_dict"]
    model.load_state_dict(state)
    model.eval()
    print(f"[*] Loaded model checkpoint from {checkpoint}")

    if saved_classes is not None and list(saved_classes) != list(class_names):
        print(
            "[!] WARNING: class order in the checkpoint differs from the test folders.\n"
            f"    checkpoint: {list(saved_classes)}\n"
            f"    test dir:   {list(class_names)}\n"
            "    Precision numbers are not valid unless these match."
        )
    return model


def evaluate_thresholds(model, dataset):
    loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)
    results = {t: {"accepted": 0, "correct": 0, "rejected": 0} for t in THRESHOLDS}
    confidences, correct = [], []

    with torch.no_grad():
        for img, label in loader:
            output = model(img)
            probs = torch.softmax(output, dim=1)[0]
            top_prob, pred = torch.max(probs, dim=0)
            confidences.append(top_prob.item())
            correct.append(pred.item() == label.item())

            for t in THRESHOLDS:
                if top_prob.item() >= t:
                    results[t]["accepted"] += 1
                    if pred.item() == label.item():
                        results[t]["correct"] += 1
                else:
                    results[t]["rejected"] += 1

    total = len(dataset)
    summary = []
    print("\n--- Confidence Threshold Calibration Results ---")
    for t in THRESHOLDS:
        r = results[t]
        precision = r["correct"] / r["accepted"] * 100 if r["accepted"] > 0 else 0.0
        rejection_rate = r["rejected"] / total * 100 if total > 0 else 0.0
        summary.append(
            {
                "threshold": t,
                "precision": precision,
                "rejection_rate": rejection_rate,
                "accepted": r["accepted"],
                "total": total,
            }
        )
        print(
            f"Cutoff {t:.2f} -> Precision: {precision:.2f}% | "
            f"Rejection Rate: {rejection_rate:.2f}% | Accepted: {r['accepted']}/{total}"
        )
    return summary, confidences, correct


def confidence_distribution(confidences, correct):
    """Mean/median/min/max top-1 softmax confidence for correct vs incorrect predictions."""
    rows = []
    for name, want in (("correct", True), ("incorrect", False)):
        vals = [c for c, ok in zip(confidences, correct) if ok == want]
        if vals:
            rows.append(
                {
                    "group": name,
                    "count": len(vals),
                    "mean": statistics.mean(vals),
                    "median": statistics.median(vals),
                    "min": min(vals),
                    "max": max(vals),
                }
            )
        else:
            rows.append({"group": name, "count": 0})
    print("\n--- Confidence Score Distribution (top-1 softmax) ---")
    for d in rows:
        if d["count"] == 0:
            print(f"{d['group']:>9}: none")
        else:
            print(
                f"{d['group']:>9}: n={d['count']} mean={d['mean']:.3f} "
                f"median={d['median']:.3f} min={d['min']:.3f} max={d['max']:.3f}"
            )
    return rows


def select_threshold(summary):
    """Lowest cutoff meeting TARGET_PRECISION; else the highest-precision cutoff."""
    meeting = [s for s in summary if s["precision"] >= TARGET_PRECISION]
    if meeting:
        return min(meeting, key=lambda s: s["threshold"])
    return max(summary, key=lambda s: s["precision"])


def image_confidences(model, folder):
    paths = sorted(
        p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )
    confidences = []
    with torch.no_grad():
        for path in paths:
            x = transform(Image.open(path).convert("RGB")).unsqueeze(0)
            confidences.append(torch.softmax(model(x), dim=1)[0].max().item())
    return confidences


def verify(model, threshold, clear_dir, blurry_dir):
    """Clear images should pass; ambiguous/blurry ones should return uncertain."""
    clear = image_confidences(model, clear_dir)
    blurry = image_confidences(model, blurry_dir)
    result = {
        "clear_n": len(clear),
        "clear_pass_rate": sum(c >= threshold for c in clear) / len(clear) * 100 if clear else None,
        "blurry_n": len(blurry),
        "blurry_uncertain_rate": (
            sum(c < threshold for c in blurry) / len(blurry) * 100 if blurry else None
        ),
    }
    print(f"\n--- Verification at cutoff {threshold:.2f} ---")
    print(f"Clear images passing:         {fmt(result['clear_pass_rate'])} of {result['clear_n']}")
    print(
        f"Blurry images flagged uncertain: {fmt(result['blurry_uncertain_rate'])} "
        f"of {result['blurry_n']}"
    )
    return result


def fmt(value):
    return "n/a" if value is None else f"{value:.1f}%"


def write_report(summary, distribution, chosen, verification, checkpoint):
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Confidence Threshold Calibration Results",
        "",
        f"Checkpoint: `{checkpoint}`",
        "",
        "| Cutoff | Precision | Rejection Rate | Accepted |",
        "|--------|-----------|----------------|----------|",
    ]
    for s in summary:
        lines.append(
            f"| {s['threshold']:.2f} | {s['precision']:.2f}% | "
            f"{s['rejection_rate']:.2f}% | {s['accepted']}/{s['total']} |"
        )
    lines += [
        "",
        "## Confidence score distribution",
        "",
        "| Group | Count | Mean | Median | Min | Max |",
        "|-------|-------|------|--------|-----|-----|",
    ]
    for d in distribution:
        if d["count"] == 0:
            lines.append(f"| {d['group']} | 0 | - | - | - | - |")
        else:
            lines.append(
                f"| {d['group']} | {d['count']} | {d['mean']:.3f} | "
                f"{d['median']:.3f} | {d['min']:.3f} | {d['max']:.3f} |"
            )
    lines += [
        "",
        f"**Selected threshold:** `{chosen['threshold']:.2f}` "
        f"(lowest cutoff with precision >= {TARGET_PRECISION:.0f}%, else highest precision).",
        "",
        "## Verification",
        "",
    ]
    if verification:
        lines += [
            f"- Clear images passing: {fmt(verification['clear_pass_rate'])} "
            f"of {verification['clear_n']}",
            f"- Blurry/ambiguous images flagged uncertain: "
            f"{fmt(verification['blurry_uncertain_rate'])} of {verification['blurry_n']}",
        ]
    else:
        lines.append("Not run (no `--clear-dir` / `--blurry-dir` provided).")
    lines += [
        "",
        "## Backend handoff",
        "",
        f"`CONFIDENCE_THRESHOLD = {chosen['threshold']:.2f}`",
        "",
        "In `POST /api/classify`, if the top softmax probability is below the threshold, "
        'return `"uncertain": true` with advice to check physical bin signs.',
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines))
    print(f"[*] Wrote report to {REPORT_PATH}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clear-dir", type=Path, help="Folder of clear, high-quality images.")
    parser.add_argument("--blurry-dir", type=Path, help="Folder of blurry/ambiguous images.")
    args = parser.parse_args()

    if not TEST_DIR.exists():
        print(f"[!] Test directory not found at {TEST_DIR}. Please run dataset split first.")
        return

    checkpoint = find_checkpoint()
    if checkpoint is None:
        print(f"[!] No checkpoint found ({', '.join(str(p) for p in MODEL_PATHS)}).")
        return

    dataset = datasets.ImageFolder(TEST_DIR, transform=transform)
    model = load_model(checkpoint, dataset.classes)

    summary, confidences, correct = evaluate_thresholds(model, dataset)
    distribution = confidence_distribution(confidences, correct)
    chosen = select_threshold(summary)
    print(f"\n[*] Selected threshold: {chosen['threshold']:.2f}")

    verification = None
    if args.clear_dir and args.blurry_dir:
        verification = verify(model, chosen["threshold"], args.clear_dir, args.blurry_dir)
    else:
        print("[!] Verification skipped: pass both --clear-dir and --blurry-dir.")

    write_report(summary, distribution, chosen, verification, checkpoint)


if __name__ == "__main__":
    main()