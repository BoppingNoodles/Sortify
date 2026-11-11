# Sortify — AI / ML Subteam Starter Code & Technical Guidance (Weeks 6–12)

> **Subteam:** AI / Machine Learning (Computer Vision)  
> **Tech Stack:** Python 3.11+, PyTorch 2.X, Torchvision, Scikit-Learn, ONNX Runtime, Matplotlib / Seaborn, Pillow  
> **Purpose:** Concrete code scaffolds, training templates, quantization scripts, and threshold calibration tools for the 2-week sprint cycle.

---

# Sprints Navigation
- [Sprint 1: Weeks 6–7 — Dataset Expansion, Model v2 & INT8 Quantization](#sprint-1-weeks-67--dataset-expansion-model-v2--int8-quantization)
  - [Ticket: Dataset v2 Curation & Balance Verification (`ml/scripts/curate_dataset_v2.py`)](#ticket-dataset-v2-curation)
  - [Ticket: Model Retraining Pipeline v2 (`ml/scripts/train_v2.py`)](#ticket-model-retraining-v2)
  - [Ticket: Dynamic INT8 Quantization Experiment (`ml/scripts/quantize_model.py`)](#ticket-dynamic-int8-quantization)
- [Sprint 2: Weeks 8–9 — Threshold Calibration, ONNX Export & OOD Stress Testing](#sprint-2-weeks-89--threshold-calibration-onnx-export--ood-stress-testing)
  - [Ticket: Empirical Confidence Threshold Calibration (`ml/scripts/calibrate_threshold.py`)](#ticket-confidence-threshold-calibration)
  - [Ticket: PyTorch to ONNX Export & Parity Test (`ml/scripts/export_onnx.py`)](#ticket-onnx-export--parity-check)
  - [Ticket: Out-of-Distribution & Non-Waste Stress Test (`ml/scripts/stress_test_ood.py`)](#ticket-out-of-distribution-stress-test)
- [Sprint 3: Weeks 10–11 — Presentation Figures, Benchmarks & Release Packaging](#sprint-3-weeks-1011--presentation-figures-benchmarks--release-packaging)
  - [Ticket: High-Resolution Presentation Visualizer (`ml/scripts/generate_presentation_charts.py`)](#ticket-presentation-visualizer)
  - [Ticket: Campus Real-World Evaluation Benchmark (`CAMPUS_BENCHMARKS.md`)](#ticket-campus-benchmark-report)
  - [Ticket: Production Checkpoint Release Packaging (`ml/scripts/package_release.py`)](#ticket-release-packaging-script)
- [Week 12 — Final Milestone & Portfolio Showcase](#week-12--final-milestone--portfolio-showcase)
  - [Ticket: Final Technical Slides & Metrics Summary](#ticket-presentation-metrics)

---

# Sprint 1: Weeks 6–7 — Dataset Expansion, Model v2 & INT8 Quantization

---

### Ticket: Dataset v2 Curation & Balance Verification
* **Target File:** `ml/scripts/curate_dataset_v2.py`
* **Goal:** Ingest 100–150 challenging campus waste photos, verify category distribution, and generate an updated train/val/test split.
* **Starter Scaffold:**

```python
"""Dataset v2 curation and split preparation helper."""

from pathlib import Path
import shutil
from sklearn.model_selection import train_test_split

RAW_EXPANDED_DIR = Path("data/raw_expanded")
PROCESSED_V2_DIR = Path("data/processed_v2")
CATEGORIES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]


def inspect_raw_distribution(source_dir: Path) -> dict[str, int]:
    """Counts available images per waste category."""
    counts = {}
    for cat in CATEGORIES:
        cat_dir = source_dir / cat
        if cat_dir.exists():
            files = [
                f
                for f in cat_dir.iterdir()
                if f.suffix.lower() in [".jpg", ".jpeg", ".png"]
            ]
            counts[cat] = len(files)
        else:
            counts[cat] = 0
    return counts


def create_split_v2(
    source_dir: Path = RAW_EXPANDED_DIR,
    target_dir: Path = PROCESSED_V2_DIR,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
):
    """Splits collected images into stratified train/val/test directories."""
    print("[Dataset v2] Preparing stratified split...")
    counts = inspect_raw_distribution(source_dir)
    print(f"[Dataset v2] Found counts: {counts}")

    for split in ["train", "val", "test"]:
        for cat in CATEGORIES:
            (target_dir / split / cat).mkdir(parents=True, exist_ok=True)

    for cat in CATEGORIES:
        cat_dir = source_dir / cat
        if not cat_dir.exists():
            continue

        images = [
            f
            for f in cat_dir.iterdir()
            if f.suffix.lower() in [".jpg", ".jpeg", ".png"]
        ]
        if not images:
            continue

        train_imgs, temp_imgs = train_test_split(
            images, test_size=(val_ratio + test_ratio), random_state=42
        )
        val_imgs, test_imgs = train_test_split(
            temp_imgs,
            test_size=(test_ratio / (val_ratio + test_ratio)),
            random_state=42,
        )

        for img in train_imgs:
            shutil.copy2(img, target_dir / "train" / cat / img.name)
        for img in val_imgs:
            shutil.copy2(img, target_dir / "val" / cat / img.name)
        for img in test_imgs:
            shutil.copy2(img, target_dir / "test" / cat / img.name)

    print(f"[Dataset v2] Complete. Data written to {target_dir}")


if __name__ == "__main__":
    create_split_v2()
```

---

### Ticket: Model Retraining Pipeline v2
* **Target File:** `ml/scripts/train_v2.py`
* **Goal:** Fine-tune the computer vision backbone on dataset v2 using cosine decay scheduling and checkpoint saving.
* **Starter Scaffold:**

```python
"""Model retraining pipeline for Sortify v2."""

from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

DATA_DIR = Path("data/processed_v2")
OUTPUT_MODEL_PATH = Path("ml/models/sortify_v2.pth")


def get_data_loaders(data_dir: Path, batch_size: int = 32):
    train_transform = transforms.Compose(
        [
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.1, contrast=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    val_transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    train_ds = datasets.ImageFolder(data_dir / "train", transform=train_transform)
    val_ds = datasets.ImageFolder(data_dir / "val", transform=val_transform)

    train_loader = DataLoader(
        train_ds, batch_size=batch_size, shuffle=True, num_workers=2
    )
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=2)
    return train_loader, val_loader, train_ds.classes


def train_model(epochs: int = 15, lr: float = 1e-4):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader, classes = get_data_loaders(DATA_DIR)

    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, len(classes))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_val_acc = 0.0
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        scheduler.step()

        # Validation phase
        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                preds = model(images).argmax(dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        val_acc = correct / total if total > 0 else 0
        print(
            f"Epoch {epoch + 1}/{epochs} - Loss: {running_loss:.4f} - Val Acc: {val_acc * 100:.2f}%"
        )

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            OUTPUT_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), OUTPUT_MODEL_PATH)
            print(f"[*] Saved new best model to {OUTPUT_MODEL_PATH}")


if __name__ == "__main__":
    train_model()
```

---

### Ticket: Dynamic INT8 Quantization Experiment
* **Target File:** `ml/scripts/quantize_model.py`
* **Goal:** Quantize model weights to INT8 and benchmark size reduction and CPU inference speed.
* **Starter Scaffold:**

```python
"""Dynamic INT8 model quantization script."""

import os
from pathlib import Path
import time
import torch
import torchvision.models as models

MODEL_FP32_PATH = Path("ml/models/sortify_v2.pth")
MODEL_INT8_PATH = Path("ml/models/sortify_quantized.pth")


def run_quantization():
    print("[Quantization] Loading FP32 model checkpoint...")
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, 6)
    if MODEL_FP32_PATH.exists():
        model.load_state_dict(torch.load(MODEL_FP32_PATH, map_location="cpu"))
    model.eval()

    # Apply PyTorch dynamic quantization to linear layers
    print("[Quantization] Applying dynamic quantization (nn.Linear -> qint8)...")
    quantized_model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )

    MODEL_INT8_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(quantized_model.state_dict(), MODEL_INT8_PATH)

    # Benchmark file size
    fp32_size_mb = (
        os.path.getsize(MODEL_FP32_PATH) / (1024 * 1024)
        if MODEL_FP32_PATH.exists()
        else 45.0
    )
    int8_size_mb = os.path.getsize(MODEL_INT8_PATH) / (1024 * 1024)

    print(f"FP32 Model Size: {fp32_size_mb:.2f} MB")
    print(f"INT8 Model Size: {int8_size_mb:.2f} MB")
    print(
        f"Compression Ratio: {(1 - int8_size_mb / fp32_size_mb) * 100:.1f}% reduction"
    )

    # Latency benchmark on 50 dummy passes
    dummy_input = torch.randn(1, 3, 224, 224)
    start = time.time()
    for _ in range(50):
        _ = quantized_model(dummy_input)
    elapsed = (time.time() - start) / 50 * 1000
    print(f"Mean CPU Forward Pass Latency: {elapsed:.2f} ms")


if __name__ == "__main__":
    run_quantization()
```

---

# Sprint 2: Weeks 8–9 — Threshold Calibration, ONNX Export & OOD Stress Testing

---

### Ticket: Empirical Confidence Threshold Calibration
* **Target File:** `ml/scripts/calibrate_threshold.py`
* **Goal:** Measure accuracy vs rejection trade-offs at 0.40, 0.50, and 0.60 confidence cutoffs.
* **Starter Scaffold:**

```python
"""Evaluates precision and rejection rates across different confidence cutoffs."""

from pathlib import Path
import torch
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms


def evaluate_thresholds(model_path: Path, test_dir: Path):
    transform = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    dataset = datasets.ImageFolder(test_dir, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)

    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, len(dataset.classes))
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()

    thresholds = [0.40, 0.50, 0.60]
    results = {t: {"accepted": 0, "correct": 0, "rejected": 0} for t in thresholds}

    with torch.no_grad():
        for img, label in loader:
            output = model(img)
            probs = torch.softmax(output, dim=1)[0]
            top_prob, pred = torch.max(probs, dim=0)

            for t in thresholds:
                if top_prob.item() >= t:
                    results[t]["accepted"] += 1
                    if pred.item() == label.item():
                        results[t]["correct"] += 1
                else:
                    results[t]["rejected"] += 1

    print("\n--- Confidence Threshold Calibration Results ---")
    for t in thresholds:
        acc = (
            results[t]["correct"] / results[t]["accepted"] * 100
            if results[t]["accepted"] > 0
            else 0
        )
        rej_rate = results[t]["rejected"] / len(dataset) * 100
        print(
            f"Cutoff {t:.2f} -> Precision: {acc:.2f}% | Rejection Rate: {rej_rate:.2f}%"
        )


if __name__ == "__main__":
    evaluate_thresholds(
        Path("ml/models/sortify_v2.pth"), Path("data/processed_v2/test")
    )
```

---

### Ticket: PyTorch to ONNX Export & Parity Test
* **Target File:** `ml/scripts/export_onnx.py`
* **Goal:** Export model to vendor-neutral `.onnx` and verify inference parity within `1e-4`.
* **Starter Scaffold:**

```python
"""Export PyTorch weights to ONNX format with parity verification."""

from pathlib import Path
import numpy as np
import onnx
import onnxruntime as ort
import torch
import torchvision.models as models

PYTORCH_MODEL_PATH = Path("ml/models/sortify_v2.pth")
ONNX_OUTPUT_PATH = Path("ml/models/sortify_v2.onnx")


def export_and_verify():
    print("[ONNX Export] Loading PyTorch model...")
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, 6)
    if PYTORCH_MODEL_PATH.exists():
        model.load_state_dict(torch.load(PYTORCH_MODEL_PATH, map_location="cpu"))
    model.eval()

    dummy_input = torch.randn(1, 3, 224, 224)

    print(f"[ONNX Export] Exporting graph to {ONNX_OUTPUT_PATH}...")
    torch.onnx.export(
        model,
        dummy_input,
        ONNX_OUTPUT_PATH,
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}},
    )

    # Validate ONNX model integrity
    onnx_model = onnx.load(str(ONNX_OUTPUT_PATH))
    onnx.checker.check_model(onnx_model)
    print("[ONNX Export] Model validation passed.")

    # Parity check
    ort_session = ort.InferenceSession(str(ONNX_OUTPUT_PATH))
    ort_inputs = {ort_session.get_inputs()[0].name: dummy_input.numpy()}
    ort_outs = ort_session.run(None, ort_inputs)[0]

    with torch.no_grad():
        pytorch_outs = model(dummy_input).numpy()

    diff = np.max(np.abs(pytorch_outs - ort_outs))
    print(f"[ONNX Export] Maximum numerical difference: {diff:.6f}")
    assert diff < 1e-4, "Parity check failed: output difference exceeds tolerance."
    print("[ONNX Export] Verification successfully completed!")


if __name__ == "__main__":
    export_and_verify()
```

---

### Ticket: Out-of-Distribution & Non-Waste Stress Test
* **Target File:** `ml/scripts/stress_test_ood.py`
* **Goal:** Verify that non-trash images return confidence < 0.50 so the backend flags them as uncertain.

---

# Sprint 3: Weeks 10–11 — Presentation Figures, Benchmarks & Release Packaging

---

### Ticket: High-Resolution Presentation Visualizer
* **Target File:** `ml/scripts/generate_presentation_charts.py`
* **Goal:** Generate 300 DPI loss curves, side-by-side confusion matrices, and accuracy bar charts for Google Slides.

---

### Ticket: Campus Benchmark Report
* **Target File:** `data/campus_test/CAMPUS_BENCHMARKS.md`
* **Goal:** Document empirical accuracy (85%+) across UC Berkeley locations (Moffitt, MLK Union, Glade).

---

### Ticket: Release Packaging Script
* **Target File:** `ml/scripts/package_release.py`
* **Goal:** Generate MD5 checksums, copy weights to `ml/models/release_v1/`, and author `ml/README.md`.

---

# Week 12 — Final Milestone & Portfolio Showcase

---

### Ticket: Final Technical Slides & Metrics Summary
* Embed visual figures in final team Google Slides deck.
* Co-present computer vision architecture, transfer learning results, and empirical campus sorting benchmarks.
