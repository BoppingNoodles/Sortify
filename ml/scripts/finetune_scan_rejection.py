"""Fine-tune a MobileNetV2 head and compare scan decisions with the bundled model."""

import argparse
import csv
import hashlib
import json
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F

from backend.app.services.inference import DEFAULT_CLASSES, ModelService, decode_image
from backend.app.services.photo_quality import get_retake_reason
from ml.scripts.evaluate_scan_rejection import BASELINE_CUTOFF, score
from ml.scripts.stress_test_ood import collect_images
from ml.scripts.train_v2 import get_v2_train_transforms

SEED = 42
NON_WASTE = "non_waste"
THREADS = 4
CUTOFFS = (0.55, 0.58, 0.60, 0.62, 0.65, 0.68, 0.70, 0.74)


@dataclass(frozen=True)
class Photo:
    path: Path
    label: str
    sha256: str
    group: str

    def read(self) -> bytes:
        payload = self.path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != self.sha256:
            raise ValueError(f"Image digest changed: {self.path}")
        return payload


def read_pc46(path: Path):
    splits = {split: [] for split in ("train", "val", "test", "field")}
    digest_splits = {}
    for entry in json.loads(path.read_text(encoding="utf-8")):
        split = entry["split"]
        if entry["sha256"] in digest_splits:
            raise ValueError("PC46 index contains a duplicate image digest")
        digest_splits[entry["sha256"]] = split
        photo = Photo(
            path.parent / entry["file"].replace("\\", "/"),
            entry["label"],
            entry["sha256"],
            entry["cohort"],
        )
        splits[split].append(photo)
        if split == "test" and not entry["cohort"].startswith("legacy"):
            splits["field"].append(photo)
    return splits, set(digest_splits)


def read_reviewed(path: Path, photo_root: Path, known_digests: set[str]):
    splits = {split: [] for split in ("train", "calibration", "test")}
    group_splits = {}
    seen_digests = set(known_digests)
    with path.open(encoding="utf-8", newline="") as source:
        for entry in csv.DictReader(source):
            photo = Photo(
                photo_root / entry["file"],
                entry["label"],
                entry["sha256"],
                entry["group"],
            )
            split = entry["split"]
            if photo.label not in (*DEFAULT_CLASSES, NON_WASTE):
                raise ValueError(f"Unknown label: {photo.label}")
            if photo.label == NON_WASTE and split == "train":
                raise ValueError("This experiment only trains on waste")
            if not photo.group or group_splits.setdefault(photo.group, split) != split:
                raise ValueError(f"Source group overlaps splits: {photo.group}")
            if photo.sha256 in seen_digests:
                raise ValueError(f"Duplicate image digest: {photo.path}")
            seen_digests.add(photo.sha256)
            splits[split].append(photo)
    if any(not members for members in splits.values()):
        raise ValueError("Training, calibration, and test must contain reviewed images")
    return splits


def negative_photos(directory, seen):
    photos = []
    for path in collect_images(directory):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in seen:
            raise ValueError(
                f"Negative evaluation image overlaps another cohort: {path}"
            )
        seen.add(digest)
        photos.append(Photo(path, NON_WASTE, digest, path.name))
    if not photos:
        raise ValueError(f"No negative evaluation images in {directory}")
    return photos


def load_service(checkpoint):
    ModelService.reset_instance()
    service = ModelService(model_path=checkpoint.resolve(), device="cpu")
    if service.model is None or service.class_names != DEFAULT_CLASSES:
        raise ValueError("Expected a loaded five-bin MobileNetV2 checkpoint")
    torch.set_num_threads(THREADS)
    return service


@torch.no_grad()
def embed(service, photos, augmentations=0):
    train_transform = get_v2_train_transforms() if augmentations else None
    rows = []
    inputs = []
    embeddings = []
    for photo in photos:
        image = decode_image(photo.read())
        reason = get_retake_reason(image)
        for view in range(1 + augmentations):
            transform = train_transform if view else service.transform
            inputs.append(transform(image))
            rows.append((photo, reason))
            if len(inputs) == 32:
                feature_maps = service.model.features(torch.stack(inputs))
                embeddings.append(
                    F.adaptive_avg_pool2d(feature_maps, (1, 1)).flatten(1)
                )
                inputs.clear()
    if inputs:
        feature_maps = service.model.features(torch.stack(inputs))
        embeddings.append(F.adaptive_avg_pool2d(feature_maps, (1, 1)).flatten(1))
    return torch.cat(embeddings), rows


def decisions(logits, rows, cutoff):
    confidence, indices = logits.softmax(dim=1).max(dim=1)
    return [
        (
            photo.label,
            DEFAULT_CLASSES[index],
            reason is None and round(probability, 4) >= cutoff,
        )
        for (photo, reason), probability, index in zip(
            rows, confidence.tolist(), indices.tolist(), strict=True
        )
    ]


def totals(rows):
    return {
        "total": len(rows),
        "correct": sum(
            accept and actual == predicted for actual, predicted, accept in rows
        ),
        "wrong": sum(
            accept and actual != NON_WASTE and actual != predicted
            for actual, predicted, accept in rows
        ),
        "non_waste_accepted": sum(
            accept and actual == NON_WASTE for actual, _, accept in rows
        ),
        "abstained": sum(not accept for _, _, accept in rows),
    }


@torch.no_grad()
def select_head(base, train, labels, curated, calibration):
    generator = torch.Generator().manual_seed(SEED)
    reference = base(train)
    baseline_calibration = [
        totals(decisions(base(inputs), rows, BASELINE_CUTOFF))
        for inputs, rows in calibration
    ]
    class_weight = labels.bincount(minlength=len(DEFAULT_CLASSES)).float().rsqrt()
    class_weight /= class_weight.mean()
    weights = torch.where(curated, 2.5, 1.0)
    candidates = []
    for learning_rate, anchor_weight in ((0.00012, 0.3), (0.00030, 0.15)):
        head = nn.Linear(base.in_features, base.out_features)
        head.load_state_dict(base.state_dict())
        optimizer = torch.optim.AdamW(head.parameters(), lr=learning_rate)
        for epoch in range(1, 13):
            with torch.enable_grad():
                for index in torch.randperm(len(labels), generator=generator).split(96):
                    logits = head(train[index])
                    loss = F.cross_entropy(
                        logits, labels[index], weight=class_weight, reduction="none"
                    )
                    anchor = (head.weight - base.weight.detach()).square().sum()
                    replay = ~curated[index]
                    if replay.any():
                        distillation = F.kl_div(
                            logits[replay].log_softmax(dim=1),
                            reference[index][replay].softmax(dim=1),
                            reduction="batchmean",
                        )
                    else:
                        distillation = 0.0
                    objective = (
                        (loss * weights[index]).mean()
                        + anchor_weight * anchor
                        + 0.25 * distillation
                    )
                    optimizer.zero_grad()
                    objective.backward()
                    optimizer.step()
            if epoch not in (3, 6, 12):
                continue
            logits = [head(inputs) for inputs, _ in calibration]
            for cutoff in CUTOFFS:
                metrics = [
                    totals(decisions(values, rows, cutoff))
                    for values, (_, rows) in zip(logits, calibration, strict=True)
                ]
                penalty = sum(
                    max(0, current["wrong"] - prior["wrong"])
                    + max(
                        0, current["non_waste_accepted"] - prior["non_waste_accepted"]
                    )
                    + max(0, prior["correct"] - current["correct"])
                    for current, prior in zip(
                        metrics, baseline_calibration, strict=True
                    )
                )
                rank = (
                    -penalty,
                    metrics[1]["correct"],
                    sum(row["correct"] for row in metrics),
                    -abs(cutoff - BASELINE_CUTOFF),
                )
                candidates.append(
                    (
                        rank,
                        {
                            "learning_rate": learning_rate,
                            "anchor_weight": anchor_weight,
                            "epoch": epoch,
                            "cutoff": cutoff,
                            "calibration_penalty": penalty,
                            "baseline_calibration": baseline_calibration,
                            "candidate_calibration": metrics,
                        },
                        {
                            key: tensor.clone()
                            for key, tensor in head.state_dict().items()
                        },
                    )
                )
    return max(candidates, key=lambda result: result[0])


def evaluate(service, photos, cutoff):
    decisions_by_photo = {}
    for photo in photos:
        outcome = score(service, photo.read())
        decisions_by_photo[photo.sha256] = (
            photo.label,
            outcome["prediction"],
            outcome["reason"] is None and outcome["confidence"] >= cutoff,
        )
    return decisions_by_photo


def compare(photos, baseline, candidate):
    before = [baseline[photo.sha256] for photo in photos]
    after = [candidate[photo.sha256] for photo in photos]
    transitions = Counter()
    for previous, current in zip(before, after, strict=True):
        statuses = [
            ("correct" if actual == predicted else "wrong") if accepted else "abstained"
            for actual, predicted, accepted in (previous, current)
        ]
        transitions[" → ".join(statuses)] += 1
    return {
        "baseline": totals(before),
        "candidate": totals(after),
        "paired": dict(transitions),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in (
        "checkpoint",
        "waste-index",
        "reviewed",
        "photo-root",
        "stress",
        "reviewed-non-waste",
        "output-dir",
    ):
        parser.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    random.seed(SEED)
    torch.manual_seed(SEED)
    pc46, seen = read_pc46(args.waste_index)
    reviewed = read_reviewed(args.reviewed, args.photo_root, seen)
    seen.update(photo.sha256 for photos in reviewed.values() for photo in photos)
    stress = negative_photos(args.stress, seen)
    reviewed_ood = negative_photos(args.reviewed_non_waste, seen)
    calibration_waste = [
        photo for photo in reviewed["calibration"] if photo.label != NON_WASTE
    ]
    calibration_ood = [
        photo for photo in reviewed["calibration"] if photo.label == NON_WASTE
    ]
    if not calibration_waste or not calibration_ood:
        raise ValueError("Fresh calibration requires both waste and non-waste")
    fresh_waste = [photo for photo in reviewed["test"] if photo.label != NON_WASTE]
    fresh_ood = [photo for photo in reviewed["test"] if photo.label == NON_WASTE]
    replay = [
        photo
        for label in DEFAULT_CLASSES
        for photo in random.sample([p for p in pc46["train"] if p.label == label], 110)
    ]
    base = load_service(args.checkpoint)
    base.model.eval()
    print("Extracting replay and reviewed training features", flush=True)
    train_x, train_rows = embed(base, replay)
    fresh_x, fresh_rows = embed(base, reviewed["train"], augmentations=3)
    labels = torch.tensor(
        [DEFAULT_CLASSES.index(photo.label) for photo, _ in train_rows + fresh_rows]
    )
    curated = torch.arange(len(labels)) >= len(train_rows)
    calibration = [
        embed(base, cohort)
        for cohort in (pc46["val"], calibration_waste, calibration_ood)
    ]
    _, selected, state = select_head(
        base.model.classifier[1],
        torch.cat([train_x, fresh_x]),
        labels,
        curated,
        calibration,
    )
    print(f"Selected calibration candidate: {selected}", flush=True)
    tested_photos = pc46["test"] + fresh_waste + stress + reviewed_ood + fresh_ood
    baseline = evaluate(base, tested_photos, BASELINE_CUTOFF)

    base.model.classifier[1].load_state_dict(state)
    candidate_path = args.output_dir / "candidate.pth"
    torch.save(
        {
            "architecture": "mobilenet_v2",
            "class_names": DEFAULT_CLASSES,
            "model_state_dict": base.model.state_dict(),
        },
        candidate_path,
    )
    candidate = evaluate(
        load_service(candidate_path), tested_photos, selected["cutoff"]
    )
    cohorts = {
        "pc46_test": pc46["test"],
        "pc46_field": pc46["field"],
        "fresh_waste": fresh_waste,
        "stress": stress,
        "reviewed_non_waste": reviewed_ood,
        "fresh_non_waste": fresh_ood,
    }
    comparisons = {
        name: compare(cohort, baseline, candidate) for name, cohort in cohorts.items()
    }
    by_bin = {
        label: compare(
            [photo for photo in pc46["test"] if photo.label == label],
            baseline,
            candidate,
        )
        for label in DEFAULT_CLASSES
    }
    fresh_counts = Counter(photo.label for photo in fresh_waste)
    fresh_groups = len({photo.group for photo in fresh_waste})
    checks = {
        "calibration_constraints": selected["calibration_penalty"] == 0,
        "fresh_coverage": len(fresh_waste) >= 20
        and len(fresh_ood) >= 12
        and fresh_groups >= 12
        and min(fresh_counts["plastic"], fresh_counts["glass"]) >= 8,
        "correct_field": comparisons["pc46_field"]["candidate"]["correct"]
        > comparisons["pc46_field"]["baseline"]["correct"],
        "correct_fresh": comparisons["fresh_waste"]["candidate"]["correct"]
        > comparisons["fresh_waste"]["baseline"]["correct"],
        "correct_full": comparisons["pc46_test"]["candidate"]["correct"]
        >= comparisons["pc46_test"]["baseline"]["correct"],
        "per_bin": all(
            row["candidate"]["correct"] >= row["baseline"]["correct"] - 2
            for row in by_bin.values()
        ),
        "wrong_and_non_waste": all(
            row["candidate"][metric] <= row["baseline"][metric]
            for row in comparisons.values()
            for metric in ("wrong", "non_waste_accepted")
        ),
    }
    report = {
        "seed": SEED,
        "pytorch": str(torch.__version__),
        "base_checkpoint_sha256": hashlib.sha256(
            args.checkpoint.read_bytes()
        ).hexdigest(),
        "candidate_sha256": hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
        "manifest_sha256": hashlib.sha256(args.reviewed.read_bytes()).hexdigest(),
        "calibration_order": ["pc46_val", "fresh_waste", "fresh_non_waste"],
        "training": {
            "replay": dict(Counter(photo.label for photo in replay)),
            "fresh": dict(Counter(photo.label for photo in reviewed["train"])),
        },
        "fresh_test_by_label": dict(fresh_counts),
        "fresh_test_waste_source_groups": fresh_groups,
        "selected": selected,
        "comparisons": comparisons,
        "pc46_test_by_bin": by_bin,
        "checks": checks,
        "eligible_for_release_checks": all(checks.values()),
    }
    (args.output_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Eligibility: {checks}", flush=True)


if __name__ == "__main__":
    main()
