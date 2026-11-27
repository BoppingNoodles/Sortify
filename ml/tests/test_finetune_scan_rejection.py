import csv

import pytest
import torch

from ml.scripts.finetune_scan_rejection import Photo, decisions, read_reviewed, totals


def test_reviewed_manifest_rejects_a_source_shared_between_splits(tmp_path):
    manifest = tmp_path / "photos.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "label", "sha256", "group", "split"])
        writer.writerow(["train.jpg", "glass", "digest-1", "one-source", "train"])
        writer.writerow(["test.jpg", "glass", "digest-2", "one-source", "test"])

    with pytest.raises(ValueError, match="Source group overlaps splits"):
        read_reviewed(manifest, tmp_path, set())


def test_reviewed_manifest_rejects_a_pc46_duplicate(tmp_path):
    manifest = tmp_path / "photos.csv"
    manifest.write_text(
        "file,label,sha256,group,split\nnew-name.jpg,plastic,pc46-digest,new-group,test\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate image digest"):
        read_reviewed(manifest, tmp_path, {"pc46-digest"})


def test_decision_totals_include_retakes_and_separate_non_waste(tmp_path):
    rows = [
        (Photo(tmp_path / name, label, name, name), reason)
        for name, label, reason in (
            ("correct", "glass", None),
            ("wrong", "plastic", None),
            ("retake", "glass", "too_dark"),
            ("negative", "non_waste", None),
            ("uncertain", "glass", None),
        )
    ]
    logits = torch.tensor([[0.0, 5.0, 0.0, 0.0, 0.0]] * 4 + [[0.0] * 5])
    assert totals(decisions(logits, rows, 0.60)) == {
        "total": 5,
        "correct": 1,
        "wrong": 1,
        "non_waste_accepted": 1,
        "abstained": 2,
    }
