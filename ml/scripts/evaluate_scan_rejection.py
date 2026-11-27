"""Compare capture and model rejection on labeled waste and non-waste cohorts."""

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import torch

from backend.app.services.inference import ModelService, decode_image
from backend.app.services.photo_quality import get_retake_reason
from ml.scripts.stress_test_ood import collect_images

BASELINE_CUTOFF = 0.60


@torch.inference_mode()
def score(service, payload):
    image = decode_image(payload)
    reason = get_retake_reason(image)
    logits = service.model(service.transform(image).unsqueeze(0).to(service.device))[0]
    if not torch.isfinite(logits).all().item():
        raise ValueError("Non-finite logits in rejection benchmark")
    probabilities = logits.softmax(dim=0)
    confidence, index = probabilities.max(dim=0)
    return {
        "reason": reason,
        "confidence": round(confidence.item(), 4),
        "energy": torch.logsumexp(logits, dim=0).item(),
        "prediction": service.class_names[index.item()],
    }


def summarize(rows, energy_cutoff):
    reasons = Counter(row["reason"] for row in rows if row["reason"])
    policies = {
        "softmax": lambda row: row["confidence"] >= BASELINE_CUTOFF,
        "quality_softmax": lambda row: (
            row["reason"] is None and row["confidence"] >= BASELINE_CUTOFF
        ),
        "quality_energy": lambda row: (
            row["reason"] is None and row["energy"] >= energy_cutoff
        ),
    }
    summary = {}
    for name, accepts in policies.items():
        accepted = [row for row in rows if accepts(row)]
        summary[name] = {
            "accepted": len(accepted),
            "correct_accepted": sum(
                row["prediction"] == row.get("label") for row in accepted
            ),
        }
    return {"total": len(rows), "retakes": dict(reasons), **summary}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--waste-index", type=Path, required=True)
    parser.add_argument("--stress", type=Path, required=True)
    parser.add_argument("--reviewed-non-waste", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    index = json.loads(args.waste_index.read_text(encoding="utf-8"))
    splits: dict[str, list] = {"val": [], "test": []}
    trained_on = {entry["sha256"] for entry in index if entry["split"] == "train"}
    ModelService.reset_instance()
    service = ModelService(model_path=args.checkpoint.resolve(), device="cpu")
    if service.model is None:
        raise SystemExit("A trained checkpoint is required")
    torch.set_num_threads(1)
    val_digests = {entry["sha256"] for entry in index if entry["split"] == "val"}
    for entry in index:
        split = entry["split"]
        if split not in splits:
            continue
        path = args.waste_index.parent / entry["file"].replace("\\", "/")
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if (
            digest != entry["sha256"]
            or digest in trained_on
            or (split == "test" and digest in val_digests)
        ):
            raise ValueError(f"Invalid or overlapping split entry: {path}")
        splits[split].append(
            {
                **score(service, payload),
                "label": entry["label"],
                "cohort": entry["cohort"],
            }
        )

    eligible = [row for row in splits["val"] if row["reason"] is None]
    matched_count = sum(row["confidence"] >= BASELINE_CUTOFF for row in eligible)
    if matched_count == 0:
        raise ValueError("Calibration requires valid waste photos accepted at baseline")
    energy_cutoff = sorted((row["energy"] for row in eligible), reverse=True)[
        matched_count - 1
    ]

    report = {
        "checkpoint_sha256": hashlib.sha256(args.checkpoint.read_bytes()).hexdigest(),
        "pytorch": str(torch.__version__),
        "softmax_cutoff": BASELINE_CUTOFF,
        "energy_accept_min": energy_cutoff,
        "waste_validation": summarize(splits["val"], energy_cutoff),
        "waste_test": summarize(splits["test"], energy_cutoff),
        "waste_test_by_bin": {
            label: summarize(
                [row for row in splits["test"] if row["label"] == label], energy_cutoff
            )
            for label in service.class_names
        },
        "waste_test_field": summarize(
            [row for row in splits["test"] if not row["cohort"].startswith("legacy")],
            energy_cutoff,
        ),
    }
    known_digests = trained_on | {entry["sha256"] for entry in index}
    for name, directory in (
        ("stress", args.stress),
        ("reviewed_non_waste", args.reviewed_non_waste),
    ):
        rows = []
        evidence = []
        for path in collect_images(directory):
            payload = path.read_bytes()
            digest = hashlib.sha256(payload).hexdigest()
            if digest in known_digests:
                raise ValueError(f"Duplicate evaluation input: {path}")
            known_digests.add(digest)
            rows.append(score(service, payload))
            evidence.append(
                {"file": path.relative_to(directory).as_posix(), "sha256": digest}
            )
        if not rows:
            raise ValueError(f"No evaluation images in {directory}")
        report[name] = {**summarize(rows, energy_cutoff), "images": evidence}

    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
