# ml/scripts/evaluate_campus_photos.py
# Evaluate frozen model on real photos captured on UC Berkeley campus bins.
#
# Expected layout:
#   data/campus_test/{compost,glass,landfill,paper,plastic}/*.jpg
#
# Usage:
#   python ml/scripts/evaluate_campus_photos.py \
#       --checkpoint ml/models/mvp_frozen.pt \
#       --data-dir data/campus_test \
#       --lab-accuracy 0.85 \
#       --out-dir docs/ml/campus-evaluation-report

import argparse
import hashlib
import json
import math
import pickle
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image, ImageOps
from torchvision import transforms

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
    IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}
except ImportError:
    IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]


def build_transform():
    """Must be IDENTICAL to the eval transform used for the lab test split."""
    return transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


def load_model(checkpoint_path, device):
    """Build model (MobileNetV2 or ResNet-18) and load saved weights."""
    from torchvision import models

    try:
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=True)
    except (pickle.UnpicklingError, RuntimeError):
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)

    if isinstance(ckpt, torch.nn.Module):
        return ckpt.eval().to(device)
    state = ckpt
    if isinstance(ckpt, dict):
        for meta_key in ("class_names", "classes"):
            if meta_key in ckpt:
                ckpt_classes = list(ckpt[meta_key])
                if ckpt_classes != CLASSES:
                    raise SystemExit(
                        f"Class order mismatch: checkpoint '{meta_key}' is "
                        f"{ckpt_classes} but CLASSES is {CLASSES}."
                    )
                break
        for key in ("model_state_dict", "state_dict", "model"):
            if key in ckpt:
                state = ckpt[key]
                break
    state = {k.replace("module.", "", 1): v for k, v in state.items()}

    if "classifier.1.weight" in state:
        num_classes = state["classifier.1.weight"].shape[0]
        model = models.mobilenet_v2(weights=None)
        model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)
    elif "fc.weight" in state:
        num_classes = state["fc.weight"].shape[0]
        model = models.resnet18(weights=None)
        model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    else:
        raise ValueError("Unrecognized model architecture in state dict.")

    if num_classes != len(CLASSES):
        raise SystemExit(
            f"Checkpoint has {num_classes} outputs but CLASSES has {len(CLASSES)}."
        )

    model.load_state_dict(state, strict=True)
    return model.eval().to(device)


def load_image(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")


def collect_samples(data_dir):
    samples = []
    for label_idx, cls in enumerate(CLASSES):
        cls_dir = data_dir / cls
        if not cls_dir.is_dir():
            print(f"[warn] missing folder: {cls_dir}")
            continue
        for p in sorted(cls_dir.iterdir()):
            if p.is_file() and p.suffix.lower() in IMG_EXTS:
                samples.append((p, label_idx))
    return samples


@torch.no_grad()
def predict(model, samples, transform, device):
    results = []
    for path, true_idx in samples:
        x = transform(load_image(path)).unsqueeze(0).to(device)
        probs = torch.softmax(model(x), dim=1)[0].cpu().numpy()
        pred_idx = int(probs.argmax())
        results.append(
            {
                "path": str(path),
                "true": CLASSES[true_idx],
                "pred": CLASSES[pred_idx],
                "confidence": float(probs[pred_idx]),
                "correct": pred_idx == true_idx,
                "_true_idx": true_idx,
                "_pred_idx": pred_idx,
            }
        )
    return results


def predict_release(checkpoint, manifest, samples, data_dir):
    from backend.app.routers.classify import LABEL_TO_CATEGORY
    from backend.app.services.inference import ModelService

    with checkpoint.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    if digest != manifest["sha256"]:
        raise ValueError("Checkpoint SHA-256 does not match the release manifest")
    ModelService.reset_instance()
    try:
        service = ModelService(model_path=checkpoint.resolve(), device="cpu")
        if service.model is None or service.class_names != manifest["class_names"]:
            raise ValueError(
                "The API runtime could not load the manifest's checkpoint and labels"
            )
        results, failures, inputs = [], [], []
        applied_transform = repr(service.transform)
        for path, true_idx in samples:
            relative_path = path.relative_to(data_dir).as_posix()
            sample = {"path": relative_path, "true": CLASSES[true_idx], "sha256": None}
            try:
                data = path.read_bytes()
                sample["sha256"] = hashlib.sha256(data).hexdigest()
                prediction = service.predict(data)
                category = LABEL_TO_CATEGORY.get(prediction["category"].strip().lower())
                score = prediction["confidence"]
                if (
                    prediction["is_mock"]
                    or category not in CLASSES
                    or not math.isfinite(score)
                    or not 0 <= score <= 1
                ):
                    raise ValueError("Invalid release inference result")
            except (
                OSError,
                ValueError,
                RuntimeError,
                SyntaxError,
                Image.DecompressionBombError,
            ) as error:
                failures.append(
                    {**sample, "error": str(error).replace(str(path), relative_path)}
                )
            else:
                results.append(
                    {
                        **sample,
                        "pred": category,
                        "confidence": score,
                        "correct": category == sample["true"],
                        "_true_idx": true_idx,
                        "_pred_idx": CLASSES.index(category),
                    }
                )
            inputs.append(sample)
    finally:
        ModelService.reset_instance()
    return results, failures, inputs, applied_transform


def confusion(results):
    n = len(CLASSES)
    cm = np.zeros((n, n), dtype=int)
    for r in results:
        cm[r["_true_idx"], r["_pred_idx"]] += 1
    return cm


def plot_confusion(cm, accuracy, out_path, title="Campus evaluation"):
    row_sums = cm.sum(axis=1, keepdims=True)
    norm = np.divide(
        cm, row_sums, out=np.zeros_like(cm, dtype=float), where=row_sums != 0
    )

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(CLASSES)), CLASSES)
    ax.set_yticks(range(len(CLASSES)), CLASSES)
    ax.set_xlabel("Predicted Label", fontweight="bold")
    ax.set_ylabel("True Label", fontweight="bold")
    ax.set_title(
        f"{title}\nNormalized confusion matrix (accuracy {accuracy:.2%})",
        fontweight="bold",
    )
    for i in range(len(CLASSES)):
        for j in range(len(CLASSES)):
            ax.text(
                j,
                i,
                f"{norm[i, j]:.2%}",
                ha="center",
                va="center",
                color="white" if norm[i, j] > 0.5 else "black",
            )
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def write_report(metrics, wrong, out_dir):
    """Write a markdown report summarizing the evaluation."""
    n = metrics["n_images"]
    acc = metrics["campus_accuracy"]
    lab = metrics["lab_accuracy"]

    lines = ["# Campus Evaluation Report", ""]
    provenance = metrics.get("release_provenance")
    if provenance:
        lines += [
            f"Candidate `{provenance['candidate_sha']}` evaluated with the deployed API preprocessing on CPU.",
            f"Dataset `{provenance['dataset_id']}` and checkpoint `{provenance['checkpoint_sha256']}`.",
            f"{metrics['attempted_images']} attempted, {len(metrics['failures'])} failed. Accuracy uses successfully evaluated images.",
            "See `metrics.json` and `predictions.json` for artifact, sample, and failure provenance.",
        ]
    else:
        lines.append(
            "Frozen MVP evaluated on real waste photos from UC Berkeley campus."
        )
    lines += [
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Images evaluated | {n} |",
        f"| Campus accuracy | {acc:.1%} |",
    ]
    if lab is not None:
        lines += [
            f"| Lab test split accuracy | {lab:.1%} |",
            f"| Gap (lab - campus) | {metrics['gap']:.1%} |",
        ]
    lines += ["", "![Confusion matrix](confusion_matrix.png)", ""]

    lines += [
        "## Per-class accuracy",
        "",
        "| Class | Images | Accuracy |",
        "|---|---|---|",
    ]
    ranked = metrics["most_reliable_classes"]
    for cls in CLASSES:
        m = metrics["per_class"][cls]
        class_accuracy = "n/a" if m["accuracy"] is None else f"{m['accuracy']:.0%}"
        lines.append(f"| {cls} | {m['n']} | {class_accuracy} |")
    if ranked:
        worst = metrics["per_class"][ranked[-1]]["accuracy"]
        bottom = [c for c in ranked if metrics["per_class"][c]["accuracy"] == worst]
        lines += [
            "",
            (
                f"Most reliably recognized: **{ranked[0]}**. "
                f"Least reliably recognized: **{', '.join(bottom)}**"
                f"{' (tied)' if len(bottom) > 1 else ''}."
            ),
            "",
        ]

    lines += [
        "## Prediction distribution",
        "",
        "| Predicted class | Count | Share |",
        "|---|---|---|",
    ]
    for cls, c in metrics["prediction_counts"].items():
        lines.append(f"| {cls} | {c} | {c / n:.0%} |")
    lines.append("")

    # Auto-generated observations
    obs = []
    top_cls, top_n = max(metrics["prediction_counts"].items(), key=lambda kv: kv[1])
    if top_n / n > 0.4:
        obs.append(
            f"The model over-predicts **{top_cls}** ({top_n / n:.0%} of all "
            f"predictions), which suggests it falls back to one class on "
            f"unfamiliar real-world images."
        )
    never = [c for c, k in metrics["prediction_counts"].items() if k == 0]
    if never:
        obs.append(f"The model never predicted: {', '.join(never)}.")
    if lab is not None and metrics["gap"] > 0.1:
        obs.append(
            f"Campus accuracy is {metrics['gap']:.0%} lower than lab accuracy, "
            f"indicating a domain gap between lab images and real photos."
        )
    if obs:
        lines += ["## Observations", ""] + [f"- {o}" for o in obs] + [""]

    if wrong:
        lines += [
            "## Most confident misclassifications",
            "",
            "| Confidence | True | Predicted | File |",
            "|---|---|---|---|",
        ]
        for r in wrong[:10]:
            lines.append(
                f"| {r['confidence']:.2f} | {r['true']} | {r['pred']} | "
                f"`{Path(r['path']).name}` |"
            )
        lines.append("")

    (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--data-dir", default="data/campus_test")
    ap.add_argument(
        "--lab-accuracy",
        type=float,
        default=None,
        help="Accuracy on the lab test split (0-1) for comparison",
    )
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument(
        "--release-manifest",
        type=Path,
        help="Use the release checkpoint and API preprocessing",
    )
    ap.add_argument(
        "--candidate-sha", help="Full application SHA for the release evaluation"
    )
    ap.add_argument("--dataset-id", help="Identifier of the frozen labeled campus set")
    args = ap.parse_args()

    if args.release_manifest and (
        not args.candidate_sha
        or not re.fullmatch(r"[0-9a-fA-F]{40}", args.candidate_sha)
        or not args.dataset_id
        or args.out_dir is None
        or args.lab_accuracy is not None
    ):
        ap.error(
            "Release evaluation requires a candidate SHA, dataset ID, and explicit new output directory. Use the same campus set for model comparisons."
        )
    out_dir = args.out_dir or Path("docs/ml/campus-evaluation-report")
    if args.release_manifest and out_dir.exists():
        ap.error("Choose a new release report directory")

    data_dir = Path(args.data_dir)
    samples = collect_samples(data_dir)
    if not samples:
        raise SystemExit("No images found. Check --data-dir and folder names.")
    print(f"Found {len(samples)} images")

    release_evidence = {}
    if args.release_manifest:
        try:
            manifest = json.loads(args.release_manifest.read_text(encoding="utf-8"))
            results, failures, inputs, applied_transform = predict_release(
                Path(args.checkpoint), manifest, samples, data_dir
            )
            model_provenance = {
                key: manifest[key]
                for key in ("sha256", "source_commit", "architecture", "class_names")
            }
        except (ValueError, KeyError, TypeError, OSError) as error:
            ap.exit(1, f"Release evaluation failed: {error}\n")
        release_evidence = {
            "attempted_images": len(samples),
            "attempted_class_counts": {
                label: sum(row["true"] == label for row in inputs) for label in CLASSES
            },
            "failures": failures,
            "release_provenance": {
                "candidate_sha": args.candidate_sha,
                "dataset_id": args.dataset_id,
                "dataset_sha256": hashlib.sha256(
                    json.dumps(inputs, sort_keys=True).encode()
                ).hexdigest(),
                "checkpoint_sha256": model_provenance["sha256"],
                "model_source_commit": model_provenance["source_commit"],
                "architecture": model_provenance["architecture"],
                "class_names": model_provenance["class_names"],
                "runtime_preprocessing": {
                    "decode": "EXIF transpose, then RGB",
                    "transform": applied_transform,
                },
                "device": "cpu",
            },
        }
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = load_model(args.checkpoint, device)
        results = predict(model, samples, build_transform(), device)

    out_dir.mkdir(parents=True, exist_ok=not args.release_manifest)
    if not results:
        (out_dir / "metrics.json").write_text(
            json.dumps(release_evidence, indent=2), encoding="utf-8"
        )
        ap.exit(1, f"No images could be evaluated. See {out_dir / 'metrics.json'}\n")

    cm = confusion(results)
    accuracy = float(np.trace(cm) / cm.sum())

    per_class = {}
    for i, cls in enumerate(CLASSES):
        total = int(cm[i].sum())
        per_class[cls] = {
            "n": total,
            "accuracy": float(cm[i, i] / total) if total else None,
        }

    pred_counts = {cls: int(cm[:, i].sum()) for i, cls in enumerate(CLASSES)}

    metrics = {
        **release_evidence,
        "n_images": len(results),
        "campus_accuracy": accuracy,
        "lab_accuracy": args.lab_accuracy,
        "gap": (args.lab_accuracy - accuracy)
        if args.lab_accuracy is not None
        else None,
        "per_class": per_class,
        "prediction_counts": pred_counts,
        "most_reliable_classes": sorted(
            [c for c in per_class if per_class[c]["accuracy"] is not None],
            key=lambda c: per_class[c]["accuracy"],
            reverse=True,
        ),
    }

    title = (
        "Release candidate campus evaluation"
        if args.release_manifest
        else "MVP campus evaluation"
    )
    plot_confusion(cm, accuracy, out_dir / "confusion_matrix.png", title)
    (out_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    clean = [{k: v for k, v in r.items() if not k.startswith("_")} for r in results]
    (out_dir / "predictions.json").write_text(
        json.dumps(clean, indent=2), encoding="utf-8"
    )

    # Misclassified, most confident first (the most informative failures)
    wrong = sorted(
        [r for r in clean if not r["correct"]],
        key=lambda r: r["confidence"],
        reverse=True,
    )
    with open(out_dir / "misclassified.txt", "w", encoding="utf-8") as f:
        f.writelines(
            f"{r['confidence']:.2f}  true={r['true']:<9} pred={r['pred']:<9} {r['path']}\n"
            for r in wrong
        )

    write_report(metrics, wrong, out_dir)

    print(f"\nCampus accuracy: {accuracy:.2%}")
    if args.lab_accuracy is not None:
        print(f"Lab accuracy:    {args.lab_accuracy:.2%}  (gap: {metrics['gap']:.2%})")
    print("\nPer-class accuracy:")
    for cls, m in per_class.items():
        acc = "n/a" if m["accuracy"] is None else f"{m['accuracy']:.0%}"
        print(f"  {cls:<9} {acc:>5}  (n={m['n']})")
    print("\nPrediction counts:", pred_counts)
    print(f"\nOutputs written to {out_dir}/")
    if release_evidence.get("failures"):
        ap.exit(
            1,
            "Some campus images could not be evaluated. Review the failure list before reporting.\n",
        )


if __name__ == "__main__":
    main()
