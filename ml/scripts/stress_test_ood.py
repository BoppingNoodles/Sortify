"""Out-of-distribution (OOD) non-waste robustness stress test runner.

Passes every image in ``--data-dir`` through the shipped ONNX model, logs the
top class and max softmax probability, and flags an image ``uncertain`` when
that probability is strictly below ``--threshold`` (``p == threshold`` counts
as accepted, i.e. a false positive). The test passes when at least
``--target-rate`` of non-waste images are flagged uncertain.

Preprocessing is pinned so results are reproducible:

* ``eval``    — the contract stored in the ONNX metadata (and
  ``ml/scripts/dataset.get_eval_transforms``): resize the short side to 256
  with PIL bilinear (long side ``int(256 * long / short)``), center-crop 224
  with ``round()`` offsets.
* ``backend`` — what ``backend/app/services/inference.ModelService`` does
  today: squash straight to 224x224 with PIL bilinear.

Both modes apply EXIF orientation (the backend does), convert to RGB, scale
by 1/255, normalize with ImageNet mean/std and feed NCHW float32. Images that
cannot be read stay in the denominator and count as NOT rejected.

Usage:
  python ml/scripts/stress_test_ood.py
  python ml/scripts/stress_test_ood.py --data-dir data/ood_test \\
      --json-out docs/ml/robustness_stress_test_results.json

Exit codes: 0 every evaluated mode passed, 1 a mode missed the target,
2 no images, invalid arguments, or a model that cannot be loaded (missing
onnxruntime, unreadable file, or metadata that breaks the contract).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL = REPO_ROOT / "ml" / "models" / "sortify_v2.onnx"
DEFAULT_DATA_DIR = REPO_ROOT / "data" / "ood_test"
DEFAULT_THRESHOLD = 0.50
DEFAULT_TARGET_RATE = 0.90
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
MODES = ("eval", "backend")
NEAR_DOMAIN_GROUP = "near_domain"
SWEEP_THRESHOLDS = (0.5, 0.6, 0.7, 0.8, 0.9)
EXPECTED_PREPROCESSING = {
    "resize_short_edge": 256,
    "center_crop": [224, 224],
    "color": "RGB",
    "scale": "divide by 255",
    "mean": [0.485, 0.456, 0.406],
    "std": [0.229, 0.224, 0.225],
    "layout": "NCHW float32",
}


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------
def parse_metadata(meta: dict[str, str]) -> tuple[list[str], dict[str, Any]]:
    """Return (class_names, preprocessing) from ONNX metadata, strictly."""
    try:
        class_names = json.loads(meta["class_names"])
        preprocessing = json.loads(meta["preprocessing"])
    except KeyError as exc:
        raise ValueError(f"ONNX metadata is missing {exc.args[0]!r}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"ONNX metadata is not valid JSON: {exc}") from exc
    if (
        not isinstance(class_names, list)
        or not class_names
        or not all(isinstance(name, str) and name.strip() for name in class_names)
        or len(set(class_names)) != len(class_names)
    ):
        raise ValueError(f"Invalid class_names metadata: {class_names!r}")
    if preprocessing != EXPECTED_PREPROCESSING:
        raise ValueError(
            "ONNX preprocessing metadata differs from the pinned contract: "
            f"{preprocessing!r}"
        )
    return class_names, preprocessing


class OnnxClassifier:
    """CPU ONNX Runtime wrapper that returns logits for an NCHW batch."""

    def __init__(self, model_path: Path):
        import onnxruntime as ort

        options = ort.SessionOptions()
        options.intra_op_num_threads = 1
        self.session = ort.InferenceSession(
            str(model_path), sess_options=options, providers=["CPUExecutionProvider"]
        )
        meta = self.session.get_modelmeta().custom_metadata_map
        self.class_names, self.preprocessing = parse_metadata(meta)
        self.metadata = dict(meta)
        inputs, outputs = self.session.get_inputs(), self.session.get_outputs()
        if len(inputs) != 1 or len(outputs) != 1:
            raise ValueError("Expected a single-input, single-output ONNX model")
        self.input_name = inputs[0].name
        self.output_name = outputs[0].name
        width = outputs[0].shape[-1]
        if isinstance(width, int) and width != len(self.class_names):
            raise ValueError(
                f"Model outputs {width} logits but metadata lists "
                f"{len(self.class_names)} classes"
            )

    def __call__(self, batch: np.ndarray) -> np.ndarray:
        logits = self.session.run([self.output_name], {self.input_name: batch})[0]
        if logits.shape[-1] != len(self.class_names):
            raise ValueError("Model outputs do not match class_names metadata")
        return logits


# --------------------------------------------------------------------------
# Preprocessing
# --------------------------------------------------------------------------
def load_image(path: Path) -> Image.Image:
    """Open an image, apply EXIF orientation like the backend, return RGB."""
    with Image.open(path) as raw:
        try:
            image = ImageOps.exif_transpose(raw)
        except (TypeError, ValueError, OSError):
            image = raw
        return image.convert("RGB")


def resize_short_edge(image: Image.Image, size: int = 256) -> Image.Image:
    """Match torchvision ``Resize(int)`` on PIL input (truncating long side)."""
    width, height = image.size
    if width <= height:
        new_size = (size, int(size * height / width))
    else:
        new_size = (int(size * width / height), size)
    return image.resize(new_size, Image.Resampling.BILINEAR)


def center_crop(image: Image.Image, size: int = 224) -> Image.Image:
    """Match torchvision ``CenterCrop`` offsets (``round`` of the margin)."""
    width, height = image.size
    if width < size or height < size:
        raise ValueError(f"Image {image.size} is smaller than crop {size}")
    top = round((height - size) / 2.0)
    left = round((width - size) / 2.0)
    return image.crop((left, top, left + size, top + size))


def preprocess(image: Image.Image, mode: str = "eval") -> np.ndarray:
    """Return a (1, 3, 224, 224) float32 tensor for ``mode`` in MODES."""
    image = image.convert("RGB")
    if mode == "eval":
        image = center_crop(resize_short_edge(image, 256), 224)
    elif mode == "backend":
        image = image.resize((224, 224), Image.Resampling.BILINEAR)
    else:
        raise ValueError(f"Unknown preprocessing mode: {mode!r}")
    pixels = np.asarray(image, dtype=np.float32) / 255.0
    mean = np.array(EXPECTED_PREPROCESSING["mean"], dtype=np.float32)
    std = np.array(EXPECTED_PREPROCESSING["std"], dtype=np.float32)
    pixels = (pixels - mean) / std
    return np.ascontiguousarray(pixels.transpose(2, 0, 1)[None, ...], np.float32)


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------
def softmax(logits: np.ndarray) -> np.ndarray:
    """Numerically stable softmax over the last axis, in float64."""
    values = np.asarray(logits, dtype=np.float64)
    values = values - values.max(axis=-1, keepdims=True)
    exp = np.exp(values)
    return exp / exp.sum(axis=-1, keepdims=True)


def score(probs: np.ndarray, class_names: list[str], threshold: float) -> dict:
    """Top class, max probability and the strict ``p < threshold`` decision."""
    index = int(np.argmax(probs))
    confidence = float(probs[index])
    return {
        "top_class": class_names[index],
        "confidence": confidence,
        "uncertain": confidence < threshold,
    }


def collect_images(data_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in data_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMG_EXTS
    )


def read_manifest(data_dir: Path) -> dict[str, dict[str, str]]:
    """Map relative filename -> manifest row, if ``manifest.csv`` exists."""
    manifest = data_dir / "manifest.csv"
    if not manifest.is_file():
        return {}
    with manifest.open(newline="", encoding="utf-8") as handle:
        return {row["filename"]: row for row in csv.DictReader(handle)}


def group_for(relative: str, manifest: dict[str, dict[str, str]]) -> str:
    row = manifest.get(relative)
    if row and row.get("group"):
        return row["group"]
    parent = Path(relative).parent.name
    return parent or "uncategorized"


def evaluate(
    classifier, images: list[Path], data_dir: Path, threshold: float, modes
) -> list[dict]:
    """Score each image under every preprocessing mode."""
    manifest = read_manifest(data_dir)
    records = []
    for path in images:
        relative = path.relative_to(data_dir).as_posix()
        record: dict[str, Any] = {
            "image": relative,
            "group": group_for(relative, manifest),
            "results": {},
        }
        try:
            image = load_image(path)
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            image = None
            error = f"{type(exc).__name__}: {exc}"
        for mode in modes:
            if image is None:
                record["results"][mode] = {"error": error, "uncertain": False}
                continue
            try:
                logits = classifier(preprocess(image, mode))[0]
                record["results"][mode] = score(
                    softmax(logits), classifier.class_names, threshold
                )
            except (ValueError, RuntimeError) as exc:
                record["results"][mode] = {
                    "error": f"{type(exc).__name__}: {exc}",
                    "uncertain": False,
                }
        records.append(record)
    return records


def _rate(part: int, whole: int) -> float:
    return part / whole if whole else 0.0


def summarize(records: list[dict], mode: str, target_rate: float) -> dict:
    """Overall, per-group and near-domain-excluded rejection rates for a mode."""
    results = [(r, r["results"][mode]) for r in records]
    total = len(results)
    errors = sum("error" in res for _, res in results)
    rejected = sum(res["uncertain"] for _, res in results)
    groups: dict[str, dict[str, Any]] = {}
    for record, res in results:
        stats = groups.setdefault(record["group"], {"total": 0, "rejected": 0})
        stats["total"] += 1
        stats["rejected"] += int(res["uncertain"])
    for stats in groups.values():
        stats["rate"] = _rate(stats["rejected"], stats["total"])
    core = [res for r, res in results if r["group"] != NEAR_DOMAIN_GROUP]
    false_positives = sorted(
        (
            {
                "image": r["image"],
                "group": r["group"],
                "top_class": res["top_class"],
                "confidence": res["confidence"],
            }
            for r, res in results
            if "error" not in res and not res["uncertain"]
        ),
        key=lambda item: item["confidence"],
        reverse=True,
    )
    rate = _rate(rejected, total)
    scored = [res["confidence"] for _, res in results if "error" not in res]
    sweep = {
        f"{cutoff:.2f}": _rate(sum(conf < cutoff for conf in scored), total)
        for cutoff in SWEEP_THRESHOLDS
    }
    return {
        "total": total,
        "scored": total - errors,
        "errors": errors,
        "rejected": rejected,
        "rejection_rate": rate,
        "passed": total > 0 and rate >= target_rate,
        "excluding_near_domain": {
            "total": len(core),
            "rejected": sum(res["uncertain"] for res in core),
            "rate": _rate(sum(res["uncertain"] for res in core), len(core)),
        },
        "groups": dict(sorted(groups.items())),
        "threshold_sweep": sweep,
        "false_positives": false_positives,
    }


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------
def _outcome(result: dict) -> str:
    if "error" in result:
        return "ERROR (not rejected)"
    return "Safe (uncertain)" if result["uncertain"] else "FALSE POSITIVE"


def _cell(result: dict) -> str:
    if "error" in result:
        return "error"
    return f"{result['top_class']} {result['confidence'] * 100:.1f}%"


def format_table(records: list[dict], modes) -> str:
    header = f"{'Image':<34} | {'Group':<16}"
    for mode in modes:
        header += f" | {mode + ' prediction':<22} | {mode + ' outcome':<20}"
    lines = [header, "-" * len(header)]
    for record in records:
        line = f"{record['image'][:34]:<34} | {record['group'][:16]:<16}"
        for mode in modes:
            result = record["results"][mode]
            line += f" | {_cell(result):<22} | {_outcome(result):<20}"
        lines.append(line)
    return "\n".join(lines)


def render_markdown(report: dict) -> str:
    """Markdown tables for the report: summary, groups, per-image, FPs."""
    modes = report["modes"]
    pct = "{:.1%}".format
    lines = [
        "| Preprocessing | Rejected | Rate | Excl. near-domain | Errors | Target |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for mode in modes:
        s = report["summary"][mode]
        core = s["excluding_near_domain"]
        verdict = "PASS" if s["passed"] else "FAIL"
        lines.append(
            f"| `{mode}` | {s['rejected']}/{s['total']} | {pct(s['rejection_rate'])} "
            f"| {core['rejected']}/{core['total']} ({pct(core['rate'])}) "
            f"| {s['errors']} | {verdict} |"
        )
    lines += ["", "| Group | " + " | ".join(f"`{m}` rejected" for m in modes) + " |"]
    lines.append("|---|" + "---:|" * len(modes))
    for group in report["summary"][modes[0]]["groups"]:
        cells = []
        for mode in modes:
            g = report["summary"][mode]["groups"][group]
            cells.append(f"{g['rejected']}/{g['total']} ({pct(g['rate'])})")
        lines.append(f"| {group} | " + " | ".join(cells) + " |")
    lines += [
        "",
        "| Cutoff | " + " | ".join(f"`{m}` rejected" for m in modes) + " |",
        "|---:|" + "---:|" * len(modes),
    ]
    for cutoff in report["summary"][modes[0]]["threshold_sweep"]:
        lines.append(
            f"| {cutoff} | "
            + " | ".join(
                pct(report["summary"][m]["threshold_sweep"][cutoff]) for m in modes
            )
            + " |"
        )
    head = "| Image | Group | " + " | ".join(
        f"`{m}` top class | `{m}` max prob | `{m}` outcome" for m in modes
    )
    lines += ["", head + " |", "|---|---|" + "---|---:|---|" * len(modes)]
    for record in report["records"]:
        cells = []
        for mode in modes:
            r = record["results"][mode]
            if "error" in r:
                cells.append(f"error | — | {_outcome(r)}")
            else:
                cells.append(
                    f"{r['top_class']} | {r['confidence'] * 100:.1f}% | {_outcome(r)}"
                )
        lines.append(
            f"| `{record['image']}` | {record['group']} | " + " | ".join(cells) + " |"
        )
    for mode in modes:
        fps = report["summary"][mode]["false_positives"]
        lines += ["", f"False positives under `{mode}` ({len(fps)}):", ""]
        if not fps:
            lines.append("None.")
            continue
        lines += ["| Image | Group | Top class | Max prob |", "|---|---|---|---:|"]
        lines += [
            f"| `{fp['image']}` | {fp['group']} | {fp['top_class']} "
            f"| {fp['confidence'] * 100:.1f}% |"
            for fp in fps
        ]
    return "\n".join(lines) + "\n"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _display(path: Path) -> str:
    """Repo-relative path when possible so outputs never leak home folders."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.name


def build_report(
    classifier, model_path: Path, data_dir: Path, records, modes, threshold, target
) -> dict:
    return {
        "evaluated_at": datetime.now(UTC).strftime("%Y-%m-%d"),
        "model": _display(model_path),
        "model_sha256": sha256_file(model_path),
        "source_checkpoint": classifier.metadata.get("source_checkpoint"),
        "source_checkpoint_sha256": classifier.metadata.get("source_checkpoint_sha256"),
        "class_names": classifier.class_names,
        "data_dir": _display(data_dir),
        "threshold": threshold,
        "uncertain_rule": "max softmax probability < threshold",
        "target_rejection_rate": target,
        "modes": list(modes),
        "summary": {mode: summarize(records, mode, target) for mode in modes},
        "records": records,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--target-rate", type=float, default=DEFAULT_TARGET_RATE)
    parser.add_argument(
        "--preprocess", choices=[*MODES, "both"], default="both", dest="preprocess"
    )
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not 0.0 < args.threshold <= 1.0 or not 0.0 < args.target_rate <= 1.0:
        print("[!] --threshold and --target-rate must be in (0, 1].")
        return 2
    if not args.model.is_file():
        print(f"[!] Model not found: {args.model}. Refusing to test untrained weights.")
        return 2
    if not args.data_dir.is_dir():
        print(
            f"[!] {args.data_dir} does not exist. Run "
            "`python ml/scripts/build_ood_testset.py` or add non-waste images."
        )
        return 2
    images = collect_images(args.data_dir)
    if not images:
        print(f"[!] No images found in {args.data_dir}.")
        return 2

    modes = list(MODES) if args.preprocess == "both" else [args.preprocess]
    try:
        classifier = OnnxClassifier(args.model)
    except ImportError as exc:
        print(f"[!] onnxruntime is required: {exc}")
        return 2
    except Exception as exc:  # noqa: BLE001 - onnxruntime raises its own types
        print(f"[!] Could not load {args.model}: {type(exc).__name__}: {exc}")
        return 2
    records = evaluate(classifier, images, args.data_dir, args.threshold, modes)
    report = build_report(
        classifier,
        args.model,
        args.data_dir,
        records,
        modes,
        args.threshold,
        args.target_rate,
    )

    print(f"\n--- OOD robustness stress test: {len(images)} images ---")
    print(f"Model: {report['model']} | uncertain if max prob < {args.threshold:.2f}\n")
    print(format_table(records, modes))
    for mode in modes:
        s = report["summary"][mode]
        core = s["excluding_near_domain"]
        print(
            f"\n[{mode}] flagged uncertain: {s['rejected']}/{s['total']} "
            f"({s['rejection_rate']:.1%}); excluding near-domain: "
            f"{core['rejected']}/{core['total']} ({core['rate']:.1%}); "
            f"errors: {s['errors']}"
        )
        print(
            f"[{mode}] Pass criterion (>= {args.target_rate:.0%} uncertain): "
            f"{'PASSED' if s['passed'] else 'FAILED'}"
        )

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(render_markdown(report), encoding="utf-8")
    return 0 if all(report["summary"][m]["passed"] for m in modes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
