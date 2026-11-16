"""Evaluates precision and rejection rates across different confidence cutoffs."""

import argparse
import json
import statistics
from hashlib import file_digest
from pathlib import Path

import torch
from PIL import Image
from torchvision import datasets, models, transforms

MODEL_PATHS = (
    Path("ml/models/sortify_v2.pth"),
    Path("ml/models/sortify_mvp_v1.pth"),
)
TEST_DIR = Path("data/processed_v2/test")
REPORT_PATH = Path("docs/ml/threshold_calibration_results.md")
THRESHOLDS = [0.40, 0.50, 0.60]
TARGET_PRECISION = 90.0  # percent; a cutoff must reach this to be eligible
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


def load_model(checkpoint, class_names, checkpoint_classes_path=None):
    state = torch.load(checkpoint, map_location="cpu")
    saved_classes = None
    if isinstance(state, dict) and "model_state_dict" in state:
        saved_classes = state.get("class_names")
        state = state["model_state_dict"]

    if saved_classes is None and checkpoint_classes_path is not None:
        saved_classes = json.loads(checkpoint_classes_path.read_text(encoding="utf-8"))

    if saved_classes is None:
        raise ValueError(
            "Checkpoint class order is missing. Pass --checkpoint-classes "
            "with the verified labels in model output order."
        )

    if not isinstance(saved_classes, (list, tuple)):
        raise TypeError("Checkpoint class order must be a list of class labels.")

    if list(saved_classes) != list(class_names):
        raise ValueError(
            f"Checkpoint class order {list(saved_classes)!r} differs from "
            f"test dataset class order {list(class_names)!r}."
        )

    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(
        model.classifier[1].in_features, len(class_names)
    )
    model.load_state_dict(state)
    model.eval()
    print(f"[*] Loaded model checkpoint from {checkpoint}")
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


def image_confidences(model, folder):
    paths = sorted(
        p
        for p in folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )
    confidences = []
    with torch.no_grad():
        for path in paths:
            x = transform(Image.open(path).convert("RGB")).unsqueeze(0)
            confidences.append(torch.softmax(model(x), dim=1)[0].max().item())
    return confidences


def verify_cutoffs(model, summary, clear_dir, blurry_dir):
    """Score the clear and blurry images once, then evaluate every cutoff."""
    clear = image_confidences(model, clear_dir)
    blurry = image_confidences(model, blurry_dir)
    if not clear or not blurry:
        raise ValueError("Both verification folders must contain images.")

    rows = []
    for row in summary:
        cutoff = row["threshold"]
        rows.append(
            {
                **row,
                "clear_pass_rate": 100 * sum(c >= cutoff for c in clear) / len(clear),
                "blurry_uncertain_rate": 100
                * sum(c < cutoff for c in blurry)
                / len(blurry),
            }
        )
    return rows


def select_verified_threshold(rows, min_clear_pass, min_blurry_uncertain):
    eligible = [
        row
        for row in rows
        if row["precision"] >= TARGET_PRECISION
        and row["clear_pass_rate"] >= min_clear_pass
        and row["blurry_uncertain_rate"] >= min_blurry_uncertain
    ]
    return min(eligible, key=lambda row: row["threshold"], default=None)


def backend_handoff_lines(chosen, checkpoint):
    lines = ["## Backend handoff", ""]
    if chosen is None:
        return lines + [
            (
                "No cutoff passed the configured verification criteria, "
                "or verification was skipped."
            )
        ]

    with checkpoint.open("rb") as weights:
        checkpoint_sha256 = file_digest(weights, "sha256").hexdigest()

    return lines + [
        f"- Candidate cutoff: `{chosen['threshold']:.2f}`",
        f"- Checkpoint: `{checkpoint}`",
        f"- Checkpoint SHA-256: `{checkpoint_sha256}`",
        (
            "- Calibration inputs: RGB conversion, `Resize(256)`, "
            "`CenterCrop(224)`, and ImageNet normalization."
        ),
        (
            "- Before enabling this cutoff in `/api/classify`, rerun the "
            "cutoff comparison and clear/blurry verification using the "
            "checkpoint and preprocessing configured for that endpoint."
        ),
    ]


def write_report(summary, distribution, rows, chosen, checkpoint):
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
    if rows:
        lines += [
            "",
            "## Verification",
            "",
            "| Cutoff | Precision | Clear accepted | Blurry flagged uncertain |",
            "|--------|-----------|----------------|--------------------------|",
        ]
        for row in rows:
            lines.append(
                f"| {row['threshold']:.2f} | {row['precision']:.2f}% | "
                f"{row['clear_pass_rate']:.1f}% | {row['blurry_uncertain_rate']:.1f}% |"
            )
    lines.append("")
    lines += backend_handoff_lines(chosen, checkpoint)
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines))
    print(f"[*] Wrote report to {REPORT_PATH}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--clear-dir", type=Path, help="Folder of clear, high-quality images."
    )
    parser.add_argument(
        "--blurry-dir", type=Path, help="Folder of blurry/ambiguous images."
    )
    parser.add_argument(
        "--min-clear-pass-rate",
        type=float,
        help="Minimum percent of clear images a cutoff must accept.",
    )
    parser.add_argument(
        "--min-blurry-uncertain-rate",
        type=float,
        help="Minimum percent of blurry images a cutoff must flag uncertain.",
    )
    parser.add_argument(
        "--checkpoint-classes",
        type=Path,
        help="JSON array of class labels in model output order (weights-only checkpoints).",
    )
    args = parser.parse_args()

    verification_options = (
        args.clear_dir,
        args.blurry_dir,
        args.min_clear_pass_rate,
        args.min_blurry_uncertain_rate,
    )
    verify = any(value is not None for value in verification_options)
    if verify:
        if any(value is None for value in verification_options):
            parser.error("Verification requires both folders and both minimum rates.")
        if not all(0 <= rate <= 100 for rate in verification_options[2:]):
            parser.error("Minimum rates must be percentages between 0 and 100.")

    if not TEST_DIR.exists():
        print(
            f"[!] Test directory not found at {TEST_DIR}. Please run dataset split first."
        )
        return

    checkpoint = find_checkpoint()
    if checkpoint is None:
        print(f"[!] No checkpoint found ({', '.join(str(p) for p in MODEL_PATHS)}).")
        return

    dataset = datasets.ImageFolder(TEST_DIR, transform=transform)
    model = load_model(checkpoint, dataset.classes, args.checkpoint_classes)

    summary, confidences, correct = evaluate_thresholds(model, dataset)
    distribution = confidence_distribution(confidences, correct)

    rows = None
    chosen = None
    if verify:
        rows = verify_cutoffs(model, summary, args.clear_dir, args.blurry_dir)
        chosen = select_verified_threshold(
            rows, args.min_clear_pass_rate, args.min_blurry_uncertain_rate
        )
    else:
        print("[!] Verification skipped: pass both folders and both minimum rates.")

    write_report(summary, distribution, rows, chosen, checkpoint)


if __name__ == "__main__":
    main()
