"""Issue #66 OOD stress test contract. Fake models and tmp images only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.stress_test_ood import (
    DEFAULT_MODEL,
    EXPECTED_PREPROCESSING,
    OnnxClassifier,
    center_crop,
    collect_images,
    evaluate,
    main,
    parse_metadata,
    preprocess,
    render_markdown,
    resize_short_edge,
    score,
    softmax,
    summarize,
)

CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]


class FakeClassifier:
    """Returns fixed logits per call, cycling through ``rows``."""

    class_names = CLASSES

    def __init__(self, rows):
        self.rows = [np.asarray(row, dtype=np.float32) for row in rows]
        self.calls = 0
        self.shapes = []

    def __call__(self, batch):
        self.shapes.append(batch.shape)
        row = self.rows[self.calls % len(self.rows)]
        self.calls += 1
        return row[None, :]


def logits_for(confidence: float, index: int = 0) -> np.ndarray:
    """Logits whose softmax puts ``confidence`` on ``index``, rest uniform."""
    rest = (1.0 - confidence) / (len(CLASSES) - 1)
    probs = np.full(len(CLASSES), rest)
    probs[index] = confidence
    return np.log(probs)


def write_image(path: Path, size=(300, 200), mode="RGB", color=128) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new(mode, size, color).save(path)
    return path


def metadata(**overrides) -> dict[str, str]:
    meta = {
        "class_names": json.dumps(CLASSES),
        "preprocessing": json.dumps(EXPECTED_PREPROCESSING),
    }
    meta.update(overrides)
    return meta


# ---------------------------------------------------------------- scoring
def test_threshold_boundary_is_strict():
    at_cutoff = score(np.array([0.5, 0.2, 0.1, 0.1, 0.1]), CLASSES, 0.5)
    below = score(np.array([0.4999, 0.2001, 0.1, 0.1, 0.1]), CLASSES, 0.5)
    assert at_cutoff == {"top_class": "compost", "confidence": 0.5, "uncertain": False}
    assert below["uncertain"] is True


def test_softmax_is_stable_and_float64():
    probs = softmax(np.array([[1000.0, 0.0, 0.0, 0.0, 0.0]], dtype=np.float32))
    assert probs.dtype == np.float64
    assert np.isclose(probs.sum(), 1.0)
    assert probs[0, 0] == pytest.approx(1.0)


# ---------------------------------------------------------- preprocessing
@pytest.mark.parametrize("mode", ["eval", "backend"])
@pytest.mark.parametrize("image_mode", ["RGB", "L", "RGBA"])
def test_preprocess_shape_and_dtype(mode, image_mode):
    tensor = preprocess(Image.new(image_mode, (333, 517)), mode)
    assert tensor.shape == (1, 3, 224, 224)
    assert tensor.dtype == np.float32
    assert tensor.flags["C_CONTIGUOUS"]


def test_preprocess_normalizes_with_imagenet_stats():
    tensor = preprocess(Image.new("RGB", (256, 256), (255, 0, 128)), "eval")
    mean, std = EXPECTED_PREPROCESSING["mean"], EXPECTED_PREPROCESSING["std"]
    expected = [(1 - mean[0]) / std[0], (0 - mean[1]) / std[1]]
    assert tensor[0, 0, 0, 0] == pytest.approx(expected[0], abs=1e-5)
    assert tensor[0, 1, 0, 0] == pytest.approx(expected[1], abs=1e-5)


def test_resize_truncates_long_side_like_torchvision():
    assert resize_short_edge(Image.new("RGB", (333, 517))).size == (256, 397)
    assert resize_short_edge(Image.new("RGB", (517, 333))).size == (397, 256)


def test_center_crop_rounds_odd_margins():
    rows, cols = np.mgrid[0:227, 0:229].astype(np.uint8)
    pixels = np.stack([cols, rows, np.zeros_like(rows)], axis=2)
    cropped = np.asarray(center_crop(Image.fromarray(pixels), 224))
    # Margins are 5 (width) and 3 (height): round(2.5) == 2, round(1.5) == 2.
    assert cropped.shape == (224, 224, 3)
    assert tuple(cropped[0, 0, :2]) == (2, 2)


def test_unknown_preprocess_mode_raises():
    with pytest.raises(ValueError, match="Unknown preprocessing mode"):
        preprocess(Image.new("RGB", (256, 256)), "squash")


def test_eval_preprocess_matches_torchvision_eval_transform():
    pytest.importorskip("torchvision")
    from ml.scripts.dataset import get_eval_transforms

    rng = np.random.default_rng(0)
    image = Image.fromarray(rng.integers(0, 256, (391, 517, 3), dtype=np.uint8))
    expected = get_eval_transforms()(image).unsqueeze(0).numpy()
    np.testing.assert_allclose(preprocess(image, "eval"), expected, atol=1e-5)


# --------------------------------------------------------------- metadata
def test_parse_metadata_accepts_export_contract():
    names, preprocessing = parse_metadata(metadata())
    assert names == CLASSES
    assert preprocessing == EXPECTED_PREPROCESSING


@pytest.mark.parametrize(
    "meta",
    [
        {"class_names": json.dumps(CLASSES)},
        metadata(class_names="not json"),
        metadata(class_names=json.dumps(["compost", "compost"])),
        metadata(preprocessing=json.dumps({"resize_short_edge": 224})),
    ],
)
def test_parse_metadata_rejects_bad_contracts(meta):
    with pytest.raises(ValueError):
        parse_metadata(meta)


# ------------------------------------------------------------- evaluation
def test_evaluate_counts_errors_as_not_rejected(tmp_path):
    write_image(tmp_path / "a_ok.png")
    (tmp_path / "b_broken.jpg").write_bytes(b"not an image")
    classifier = FakeClassifier([logits_for(0.3)])
    records = evaluate(
        classifier, collect_images(tmp_path), tmp_path, 0.5, ["eval", "backend"]
    )
    summary = summarize(records, "eval", 0.9)
    assert [r["image"] for r in records] == ["a_ok.png", "b_broken.jpg"]
    assert "error" in records[1]["results"]["eval"]
    assert (summary["total"], summary["scored"], summary["errors"]) == (2, 1, 1)
    assert summary["rejected"] == 1
    assert summary["rejection_rate"] == pytest.approx(0.5)
    assert summary["passed"] is False
    assert all(shape == (1, 3, 224, 224) for shape in classifier.shapes)


def test_summary_groups_sweep_and_false_positives(tmp_path):
    for name in ("a.png", "b.png", "c.png", "d.png"):
        write_image(tmp_path / name)
    (tmp_path / "manifest.csv").write_text(
        "filename,group\na.png,real_non_waste\nb.png,real_non_waste\n"
        "c.png,near_domain\n",
        encoding="utf-8",
    )
    classifier = FakeClassifier(
        [logits_for(0.2), logits_for(0.95, 3), logits_for(0.7, 2), logits_for(0.55)]
    )
    records = evaluate(classifier, collect_images(tmp_path), tmp_path, 0.5, ["eval"])
    summary = summarize(records, "eval", 0.9)

    assert [r["group"] for r in records] == [
        "real_non_waste",
        "real_non_waste",
        "near_domain",
        "uncategorized",
    ]
    assert summary["groups"]["real_non_waste"] == {
        "total": 2,
        "rejected": 1,
        "rate": 0.5,
    }
    assert summary["excluding_near_domain"] == {
        "total": 3,
        "rejected": 1,
        "rate": pytest.approx(1 / 3),
    }
    assert [fp["image"] for fp in summary["false_positives"]] == [
        "b.png",
        "c.png",
        "d.png",
    ]
    assert summary["false_positives"][0]["top_class"] == "paper"
    assert summary["threshold_sweep"]["0.50"] == pytest.approx(0.25)
    assert summary["threshold_sweep"]["0.60"] == pytest.approx(0.5)
    assert summary["threshold_sweep"]["0.90"] == pytest.approx(0.75)


def test_render_markdown_lists_every_image():
    records = [
        {
            "image": "x.png",
            "group": "synthetic",
            "results": {
                "eval": {"top_class": "glass", "confidence": 0.8, "uncertain": False}
            },
        }
    ]
    report = {
        "modes": ["eval"],
        "summary": {"eval": summarize(records, "eval", 0.9)},
        "records": records,
    }
    markdown = render_markdown(report)
    assert "| `x.png` | synthetic | glass | 80.0% | FALSE POSITIVE |" in markdown
    assert "FAIL" in markdown


# --------------------------------------------------------------------- cli
def test_main_returns_2_without_images(tmp_path, capsys):
    assert main(["--data-dir", str(tmp_path)]) == 2
    assert "No images found" in capsys.readouterr().out


def test_main_returns_2_for_missing_model(tmp_path):
    write_image(tmp_path / "a.png")
    missing = tmp_path / "missing.onnx"
    assert main(["--model", str(missing), "--data-dir", str(tmp_path)]) == 2


def test_main_rejects_invalid_threshold(tmp_path):
    assert main(["--data-dir", str(tmp_path), "--threshold", "0"]) == 2


@pytest.mark.parametrize(
    "error", [ImportError("no onnxruntime"), ValueError("bad metadata")]
)
def test_main_returns_2_when_model_cannot_load(tmp_path, monkeypatch, capsys, error):
    import ml.scripts.stress_test_ood as runner

    def broken(_path):
        raise error

    write_image(tmp_path / "a.png")
    model = tmp_path / "model.onnx"
    model.write_bytes(b"junk")
    monkeypatch.setattr(runner, "OnnxClassifier", broken)
    assert main(["--model", str(model), "--data-dir", str(tmp_path)]) == 2
    assert "[!]" in capsys.readouterr().out


def test_main_returns_2_for_corrupt_onnx(tmp_path):
    pytest.importorskip("onnxruntime")
    write_image(tmp_path / "a.png")
    model = tmp_path / "corrupt.onnx"
    model.write_bytes(b"not a protobuf")
    assert main(["--model", str(model), "--data-dir", str(tmp_path)]) == 2


# ------------------------------------------------- integration (real ONNX)
def test_shipped_onnx_end_to_end(tmp_path):
    pytest.importorskip("onnxruntime")
    if not DEFAULT_MODEL.is_file():
        pytest.skip("ml/models/sortify_v2.onnx is not present")
    classifier = OnnxClassifier(DEFAULT_MODEL)
    assert classifier.class_names == CLASSES
    write_image(tmp_path / "black.png", color=0)
    write_image(tmp_path / "gray.png", size=(517, 333), color=128)
    json_out = tmp_path / "out" / "results.json"
    markdown_out = tmp_path / "out" / "tables.md"

    code = main(
        [
            "--data-dir",
            str(tmp_path),
            "--json-out",
            str(json_out),
            "--markdown-out",
            str(markdown_out),
        ]
    )

    report = json.loads(json_out.read_text(encoding="utf-8"))
    assert code in (0, 1)
    assert report["model"] == "ml/models/sortify_v2.onnx"
    assert report["modes"] == ["eval", "backend"]
    assert {r["image"] for r in report["records"]} == {"black.png", "gray.png"}
    for record in report["records"]:
        for result in record["results"].values():
            assert result["top_class"] in CLASSES
            assert 0.0 < result["confidence"] <= 1.0
    assert str(tmp_path) not in json_out.read_text(encoding="utf-8")
    assert markdown_out.read_text(encoding="utf-8").startswith("| Preprocessing")
