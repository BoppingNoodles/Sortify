# Sortify — AI / ML Subteam Starter Code & Technical Guidance (Weeks 1–12)

> **Subteam:** AI / ML (Computer Vision / PyTorch)  
> **Members:** Aarav, Kathleen, Max, Doil  
> **Tech Stack:** Python 3.11+, PyTorch 2.X, Torchvision, Scikit-learn, ONNX, OpenCV, Pillow, Pandas, Matplotlib  
> **Purpose:** Structural scaffolds, PyTorch training loops, evaluation harnesses, and step-by-step implementation guidance for each weekly deliverable.

---

# Week 1 — Setup, Onboarding & Learning Exercises

---

### Aarav (Week 1)
* **Task:** PyTorch Environment Setup & Transfer Learning Exercise
* **Target File / Output:** `ml/sandbox/transfer_learning_sandbox.py`
* **Starter Guidance & Structure:**

```python
# ml/sandbox/transfer_learning_sandbox.py
import torch
import torch.nn as nn
from torchvision import models

def setup_transfer_learning_model(num_classes: int = 6):
    # TODO: Load pre-trained ResNet-18 model weights
    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)

    # TODO: Freeze early feature extraction layers
    for param in model.parameters():
        param.requires_grad = False

    # TODO: Replace classification head with custom Linear layer
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)
    return model

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"PyTorch Version: {torch.__version__} | Active Device: {device}")
    model = setup_transfer_learning_model()
    print(f"Classification head initialized with {model.fc.out_features} output classes.")
```

---

### Kathleen (Week 1)
* **Task:** PyTorch Environment Setup & Transfer Learning Exercise
* **Target File / Output:** `ml/sandbox/dataloader_sandbox.py`
* **Starter Guidance & Structure:**

```python
# ml/sandbox/dataloader_sandbox.py
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

def get_sandbox_transforms():
    # TODO: Standard ImageNet transforms (Resize to 224x224 and normalize)
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
```

---

### Max (Week 1)
* **Task:** PyTorch Environment Setup & Transfer Learning Exercise
* **Target File / Output:** `ml/sandbox/train_step_sandbox.py`
* **Starter Guidance & Structure:**

```python
# ml/sandbox/train_step_sandbox.py
import torch
import torch.nn as nn
import torch.optim as optim

def run_single_train_step(model, inputs, labels):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

    model.train()
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
    return loss.item()
```

---

### Doil (Week 1)
* **Task:** PyTorch Environment Setup & Transfer Learning Exercise
* **Target File / Output:** `ml/sandbox/eval_metric_sandbox.py`
* **Starter Guidance & Structure:**

```python
# ml/sandbox/eval_metric_sandbox.py
import torch

def compute_batch_accuracy(outputs: torch.Tensor, labels: torch.Tensor) -> float:
    # TODO: Obtain predicted class indices from argmax
    _, preds = torch.max(outputs, 1)
    correct = torch.sum(preds == labels.data).item()
    return correct / len(labels)
```

---

# Week 2 — Design, Architecture & Data Preparation

---

### Aarav (Week 2)
* **Task:** Download and Assemble Composite Waste Classification Dataset
* **Target File / Output:** `ml/scripts/download_dataset.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/download_dataset.py
import urllib.request
import zipfile
from pathlib import Path

DATA_DIR = Path("ml/data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

TRASHNET_URL = "https://huggingface.co/datasets/garythung/trashnet/resolve/main/dataset-resized.zip"

def download_and_extract_trashnet():
    zip_path = DATA_DIR / "trashnet.zip"
    if not zip_path.exists():
        print("Downloading TrashNet dataset...")
        # TODO: Stream download with progress callback
        # urllib.request.urlretrieve(TRASHNET_URL, zip_path)
    # TODO: Extract into ml/data/raw/trashnet
```

---

### Kathleen (Week 2)
* **Task:** Train / Validation / Test Partitioning Script
* **Target File / Output:** `ml/scripts/split_dataset.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/split_dataset.py
import shutil
import random
from pathlib import Path

def create_dataset_splits(
    source_dir: Path, 
    dest_dir: Path, 
    train_ratio=0.70, 
    val_ratio=0.15, 
    test_ratio=0.15,
    seed=42
):
    random.seed(seed)
    # TODO: Stratify split by class folder (cardboard, glass, metal, paper, plastic, trash)
    for class_folder in source_dir.iterdir():
        if not class_folder.is_dir(): continue
        images = list(class_folder.glob("*.jpg"))
        random.shuffle(images)
        # TODO: Copy partitioned images into dest_dir/train, val, and test subdirectories
```

---

### Max (Week 2)
* **Task:** Image Preprocessing Pipeline & Color Normalization
* **Target File / Output:** `ml/scripts/transforms.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/transforms.py
from torchvision import transforms

def get_train_transforms():
    # TODO: Data augmentations (RandomResizedCrop, RandomHorizontalFlip, ColorJitter)
    return transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def get_eval_transforms():
    # Deterministic preprocessing for validation and test splits
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
```

---

### Doil (Week 2)
* **Task:** Exploratory Data Analysis (EDA) Notebook
* **Target File / Output:** `ml/notebooks/01_eda_dataset.ipynb`
* **Starter Guidance & Structure:**

```python
# ml/notebooks/01_eda_dataset.py (Notebook script equivalent)
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter

def plot_class_distribution(dataset_path: Path):
    classes = [p.name for p in dataset_path.iterdir() if p.is_dir()]
    counts = {cls: len(list((dataset_path / cls).glob("*.jpg"))) for cls in classes}
    
    plt.figure(figsize=(8, 4))
    plt.bar(counts.keys(), counts.values(), color='#16A34A')
    plt.title("Class Sample Distribution")
    plt.xlabel("Category")
    plt.ylabel("Number of Images")
    plt.tight_layout()
    plt.savefig("ml/data/class_distribution.png")
```

---

# Week 3 — Foundation Building & Scaffolding

---

### Aarav (Week 3)
* **Task:** End-to-End PyTorch Training Pipeline Script
* **Target File / Output:** `ml/train.py`
* **Starter Guidance & Structure:**

```python
# ml/train.py
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path

def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss, correct, total = 0.0, 0, 0
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, preds = torch.max(outputs, 1)
        correct += torch.sum(preds == labels.data).item()
        total += labels.size(0)

    return running_loss / total, correct / total
```

---

### Kathleen (Week 3)
* **Task:** PyTorch DataLoaders with Augmentations
* **Target File / Output:** `ml/dataset.py`
* **Starter Guidance & Structure:**

```python
# ml/dataset.py
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from ml.scripts.transforms import get_train_transforms, get_eval_transforms
from pathlib import Path

def get_dataloaders(data_dir: Path, batch_size=32, num_workers=2):
    train_set = ImageFolder(root=data_dir / "train", transform=get_train_transforms())
    val_set = ImageFolder(root=data_dir / "val", transform=get_eval_transforms())
    test_set = ImageFolder(root=data_dir / "test", transform=get_eval_transforms())

    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, val_loader, test_loader, train_set.classes
```

---

### Max (Week 3)
* **Task:** Baseline ResNet-18 Training Run
* **Target File / Output:** `ml/scripts/train_baseline.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/train_baseline.py
# Execute 10 baseline epochs on frozen backbone
# Track training loss, validation loss, and val accuracy
```

---

### Doil (Week 3)
* **Task:** Model Evaluation & Confusion Matrix Script
* **Target File / Output:** `ml/evaluate.py`
* **Starter Guidance & Structure:**

```python
# ml/evaluate.py
import torch
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model_performance(model, test_loader, classes, device):
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    # TODO: Print classification report (precision, recall, f1)
    print(classification_report(all_labels, all_preds, target_names=classes))
```

---

# Week 4 — Core MVP Build (Part 1: Fine-Tuning & Export)

---

### Aarav (Week 4)
* **Task:** Fine-Tune ResNet-18 & Optimize Learning Rate Schedule
* **Target File / Output:** `ml/scripts/fine_tune.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/fine_tune.py
import torch
import torch.optim as optim

def setup_fine_tuning(model, base_lr=1e-4, fc_lr=1e-3):
    # Unfreeze Layer 4 of ResNet-18
    for param in model.layer4.parameters():
        param.requires_grad = True

    # Differential learning rates
    optimizer = optim.Adam([
        {'params': model.layer4.parameters(), 'lr': base_lr},
        {'params': model.fc.parameters(), 'lr': fc_lr}
    ])
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=15)
    return optimizer, scheduler
```

---

### Kathleen (Week 4)
* **Task:** Model Export & Packaging with `classes.json`
* **Target File / Output:** `ml/scripts/export_model.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/export_model.py
import torch
import json
from pathlib import Path

def package_checkpoint(model, classes, output_dir: Path, filename="resnet18_sortify.pth"):
    output_dir.mkdir(parents=True, exist_ok=True)
    # Save classes.json
    with open(output_dir / "classes.json", "w") as f:
        json.dump(classes, f, indent=2)

    # Save state dict
    torch.save(model.state_dict(), output_dir / filename)
    print(f"Saved weights and classes.json to {output_dir}")
```

---

### Max (Week 4)
* **Task:** MobileNetV2 Benchmark & Architecture Comparison
* **Target File / Output:** `ml/scripts/train_mobilenet.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/train_mobilenet.py
from torchvision import models
import torch.nn as nn

def get_mobilenet_v2(num_classes=6):
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)
    return model
```

---

### Doil (Week 4)
* **Task:** Detailed Error Analysis & Misclassification Breakdown
* **Target File / Output:** `ml/scripts/error_analysis.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/error_analysis.py
# Identify top-5 most confused item pairs (e.g. Glass vs Plastic)
# Save visual collage of misclassified test images
```

---

# Week 5 — Core MVP Build (Part 2: Domain Gap & Freeze)

---

### Aarav (Week 5)
* **Task:** Hyperparameter Optimization & Model Checkpoint Freeze
* **Target File / Output:** `ml/models/sortify_v1_frozen.pth`
* **Starter Guidance & Structure:** Freeze weights and save production SHA256 checksum.

---

### Kathleen (Week 5)
* **Task:** Campus Test Dataset Collection & Real-World Evaluation
* **Target File / Output:** `ml/scripts/evaluate_campus_photos.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/evaluate_campus_photos.py
# Evaluate frozen model on 50 real photos captured on UC Berkeley campus bins
```

---

### Max (Week 5)
* **Task:** Domain Gap Evaluation Report & Demo Items Selection
* **Target File / Output:** `docs/ml/domain-gap-report.md`
* **Starter Guidance & Structure:** Quantify accuracy degradation between laboratory TrashNet and raw smartphone camera photos.

---

### Doil (Week 5)
* **Task:** ML Presentation Visualizer Script & Metrics Summary
* **Target File / Output:** `ml/scripts/visualize_metrics.py`
* **Starter Guidance & Structure:** Plot train/val loss curves and confusion matrices for presentation slide deck.

---

# Week 6 — Mid-Semester Presentation (Benchmarks & Retro)

---

### Aarav (Week 6)
* **Task:** Mid-Sem Model Benchmark & Metrics Summary
* **Target File / Output:** `ml/models/MIDSEM_METRICS.md`
* **Starter Guidance & Structure:**

```markdown
<!-- ml/models/MIDSEM_METRICS.md -->
# Sortify Mid-Semester ML Metrics
- Model: Fine-Tuned ResNet-18
- Top-1 Accuracy: 83.4%
- CPU Inference Latency: 48ms
- Model Weights Size: 44.7 MB
```

---

### Kathleen (Week 6)
* **Task:** Physical Demo Items Benchmark & Preparation
* **Target File / Output:** `docs/ml/kathleen/demo-items-benchmark.md`
* **Starter Guidance & Structure:** Test and verify stable items for live video demo (plastic bottle, paper cup, aluminum can).

---

### Max (Week 6)
* **Task:** Catalog of Known Limitations & Failure Modes
* **Target File / Output:** `docs/ml/known-limitations.md`
* **Starter Guidance & Structure:** Technical documentation of model failure modes (transparent glass, black plastics, food residue).

---

### Doil (Week 6)
* **Task:** Presentation Rehearsal Timing & Speaker Coordination
* **Target File / Output:** `docs/presentation_cue_sheet.md`
* **Starter Guidance & Structure:** Speaker schedule and slide transition cue sheet.

---

# Week 7 — Authentication & User Accounts

---

### Aarav (Week 7)
* **Task:** Dynamic PyTorch Model Quantization Experiment
* **Target File / Output:** `ml/scripts/quantize.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/quantize.py
import torch
import torch.nn as nn

def apply_dynamic_quantization(model):
    # Quantize linear layers to INT8
    quantized_model = torch.quantization.quantize_dynamic(
        model, {nn.Linear}, dtype=torch.qint8
    )
    return quantized_model
```

---

### Kathleen (Week 7)
* **Task:** Targeted Dataset Expansion for Weak Classes
* **Target File / Output:** `ml/scripts/expand_dataset.py`
* **Starter Guidance & Structure:** Ingest supplemental campus photos specifically targeting plastic and glass categories.

---

### Max (Week 7)
* **Task:** Retrain Model on Expanded Dataset v2
* **Target File / Output:** `ml/scripts/train_v2.py`
* **Starter Guidance & Structure:** Retraining pipeline on augmented and expanded composite dataset.

---

### Doil (Week 7)
* **Task:** Comprehensive Model Evaluation Report v2
* **Target File / Output:** `docs/ml/evaluation_report_v2.md`
* **Starter Guidance & Structure:** Comparative metrics between v1 and v2 models.

---

# Week 8 — Engagement Tracker, Streaks & Gamification

---

### Aarav (Week 8)
* **Task:** Test-Time Augmentation (TTA) Experimentation
* **Target File / Output:** `ml/scripts/tta_inference.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/tta_inference.py
import torch

def predict_with_tta(model, image_tensor):
    # Predict original, horizontal flip, and slight rotation; average softmax outputs
    pass
```

---

### Kathleen (Week 8)
* **Task:** Model Version Logging & Loading Helper Script
* **Target File / Output:** `ml/utils/model_loader.py`
* **Starter Guidance & Structure:**

```python
# ml/utils/model_loader.py
# Loads appropriate model checkpoint with fallback and metadata validation
```

---

### Max (Week 8)
* **Task:** PyTorch to ONNX Export Pipeline & Validation
* **Target File / Output:** `ml/scripts/export_onnx.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/export_onnx.py
import torch

def export_to_onnx(model, output_path="ml/models/sortify.onnx"):
    dummy_input = torch.randn(1, 3, 224, 224)
    torch.onnx.export(
        model, dummy_input, output_path,
        input_names=["input"], output_names=["output"],
        dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
    )
```

---

### Doil (Week 8)
* **Task:** Prototype ONNX to TensorFlow Lite (`.tflite`) Conversion
* **Target File / Output:** `ml/scripts/onnx_to_tflite.py`
* **Starter Guidance & Structure:** Pipeline exploring on-device conversion feasibility.

---

# Week 9 — System Integration Testing & Robustness

---

### Aarav (Week 9)
* **Task:** Adversarial & Out-of-Distribution Input Stress Testing
* **Target File / Output:** `ml/scripts/stress_test.py`
* **Starter Guidance & Structure:** Test model predictions on non-waste images (faces, animals, landscapes) to test anomaly behavior.

---

### Kathleen (Week 9)
* **Task:** Empirical Confidence Threshold Calibration
* **Target File / Output:** `ml/scripts/calibrate_threshold.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/calibrate_threshold.py
# Calibrate threshold (e.g. 0.50): items below return uncertain status
```

---

### Max (Week 9)
* **Task:** Comparative Model Evaluation & Checkpoint Recommendation
* **Target File / Output:** `docs/ml/model_comparison_report.md`
* **Starter Guidance & Structure:** Comparison table of all checkpoints: Accuracy, F1-Score, Inference Time, and Size.

---

### Doil (Week 9)
* **Task:** Author Official Model Card Documentation
* **Target File / Output:** `ml/MODEL_CARD.md`
* **Starter Guidance & Structure:**

```markdown
<!-- ml/MODEL_CARD.md -->
# Model Card: Sortify ResNet-18 Waste Classifier
## Model Details
- Architecture: ResNet-18
- Input Resolution: 224x224 RGB
- Output Classes: 6 (cardboard, glass, metal, paper, plastic, trash)
## Intended Use
- Student recycling classification for UC Berkeley campus.
## Limitations
- Sensitive to extreme lighting and crumpled/translucent plastics.
```

---

# Week 10 — Production Hardening & UX Polish

---

### Aarav (Week 10)
* **Task:** Verify Dockerized Model Inference Performance
* **Target File / Output:** `ml/tests/test_docker_inference.py`
* **Starter Guidance & Structure:** Benchmark memory and CPU usage inside container with `--memory=1g`.

---

### Kathleen (Week 10)
* **Task:** Build Interactive Model Demo Jupyter Notebook
* **Target File / Output:** `ml/notebooks/02_interactive_demo.ipynb`
* **Starter Guidance & Structure:** Interactive widget allowing team members to upload any photo and view top-3 confidence scores.

---

### Max (Week 10)
* **Task:** On-Device Mobile Inference Research & Benchmarks
* **Target File / Output:** `docs/ml/mobile-inference-research.md`
* **Starter Guidance & Structure:** Technical comparison of CoreML vs TFLite on iOS and Android.

---

### Doil (Week 10)
* **Task:** Author Verified Model Retraining Guide in `ml/README.md`
* **Target File / Output:** `ml/README.md`
* **Starter Guidance & Structure:** Step-by-step reproducible instructions for future model training and exports.

---

# Week 11 — Stretch Goals & Deployment

---

### Aarav (Week 11)
* **Task:** Prototype Multi-Object Waste Detection with YOLOv8
* **Target File / Output:** `ml/scripts/yolo_prototype.py`
* **Starter Guidance & Structure:**

```python
# ml/scripts/yolo_prototype.py
# Scaffolding for multi-bounding-box waste detection
```

---

### Kathleen (Week 11)
* **Task:** Contamination Classification Heuristic Prototype
* **Target File / Output:** `ml/scripts/contamination_heuristics.py`
* **Starter Guidance & Structure:** Color variance and texture heuristics detecting grease stains on paper boxes.

---

### Max (Week 11)
* **Task:** Final Performance Metrics & Comparative Presentation Visuals
* **Target File / Output:** `ml/scripts/generate_final_charts.py`
* **Starter Guidance & Structure:** Script generating polished bar charts and confusion matrices for presentation slides.

---

### Doil (Week 11)
* **Task:** Author Future Work & Edge Hardware Roadmap
* **Target File / Output:** `docs/ml/future-work-roadmap.md`
* **Starter Guidance & Structure:** Architectural design for smart physical bins with motorized lids and Google Coral accelerators.

---

# Week 12 — Final Presentation & Portfolio Release

---

### Aarav (Week 12)
* **Task:** Model Optimization & Quantization Final Report
* **Target File / Output:** `ml/docs/OPTIMIZATION.md`
* **Starter Guidance & Structure:** Comprehensive review of dynamic quantization and CPU optimization techniques.

---

### Kathleen (Week 12)
* **Task:** Campus Real-World Testing Final Report
* **Target File / Output:** `data/campus_test/CAMPUS_BENCHMARKS.md`
* **Starter Guidance & Structure:** Empirical evaluation summary across UC Berkeley campus bins.

---

### Max (Week 12)
* **Task:** Semester Model Evolution Technical Summary
* **Target File / Output:** `ml/docs/MODEL_EVOLUTION.md`
* **Starter Guidance & Structure:** Chronological progression of model architectures, loss functions, and accuracy gains.

---

### Doil (Week 12)
* **Task:** Project Wrap-Up Summary & Individual Contribution Log
* **Target File / Output:** `docs/CONTRIBUTIONS.md` & root `README.md`
* **Starter Guidance & Structure:** Celebrating contributions across Frontend, Backend, and ML subteams!
