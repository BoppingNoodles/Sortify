"""Evaluate Sortify waste classification models and generate confusion matrix heatmaps.

Computes overall accuracy, per-class Precision, Recall, and F1-Score via Scikit-learn,
and saves a normalized confusion matrix heatmap via Seaborn/Matplotlib.

Run from repository root:
    python ml/scripts/evaluate.py --model_path ml/models/resnet18_baseline.pth --test_dir data/processed/test
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

# Configure headless matplotlib backend before importing pyplot
os.environ.setdefault("MPLBACKEND", "Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import models
from torchvision.datasets import ImageFolder

try:
    import seaborn as sns
except ImportError:
    sns = None

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.dataset import (
    DEFAULT_NUM_WORKERS,
    get_eval_transforms,
)

# Standard Sortify 5-bin waste classification classes (ImageFolder alphabetical order)
DEFAULT_CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]
DEFAULT_MODEL_PATH = REPO_ROOT / "ml" / "models" / "resnet18_baseline.pth"
DEFAULT_TEST_DIR = REPO_ROOT / "data" / "processed" / "test"
DEFAULT_OUTPUT_PLOT = REPO_ROOT / "docs" / "ml" / "baseline_confusion_matrix.png"


def get_device(preference: str | None = None) -> torch.device:
    """Resolve compute device with optional preference override."""
    if preference:
        return torch.device(preference)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def build_model(
    arch: str = "resnet18", num_classes: int = len(DEFAULT_CLASSES)
) -> nn.Module:
    """Build evaluation model architecture with classifier head configured for num_classes."""
    arch_norm = arch.lower().strip()
    if arch_norm == "resnet18":
        model = models.resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model
    elif arch_norm in ("mobilenet", "mobilenet_v2"):
        model = models.mobilenet_v2(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
        return model
    else:
        raise ValueError(
            f"Unsupported architecture '{arch}'. Choose 'resnet18' or 'mobilenet_v2'."
        )


def load_classes_from_package(checkpoint_path: Path) -> list[str] | None:
    """Check if classes.json exists alongside the model checkpoint."""
    classes_json_path = checkpoint_path.parent / "classes.json"
    if classes_json_path.is_file():
        try:
            with open(classes_json_path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                # Format: {"0": "paper", "1": "plastic", ...}
                sorted_items = sorted(data.items(), key=lambda x: int(x[0]))
                return [name for _, name in sorted_items]
            elif isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError, ValueError) as err:
            print(
                f"Warning: Failed to parse {classes_json_path}: {err}", file=sys.stderr
            )
    return None


def load_checkpoint(
    model_path: Path | str,
    arch: str = "resnet18",
    device: torch.device | None = None,
    expected_classes: list[str] | None = None,
) -> tuple[nn.Module, list[str], dict]:
    """Load model weights and metadata from checkpoint.

    Supports both full checkpoint dicts (with 'model_state_dict' and 'class_names')
    and raw state_dict bundles.
    """
    path = Path(model_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(
            f"Checkpoint not found at: '{path}'. Please train a model or specify a valid checkpoint."
        )

    device = device or get_device()

    # Load checkpoint safely
    try:
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    except (RuntimeError, ValueError) as err:
        warnings.warn(
            f"Loading '{path}' with weights_only=True failed ({err}); "
            "falling back to weights_only=False. Ensure the checkpoint is from a trusted source.",
            UserWarning,
            stacklevel=2,
        )
        checkpoint = torch.load(path, map_location="cpu", weights_only=False)

    metadata: dict = {}
    if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
        state_dict = checkpoint["model_state_dict"]
        metadata = {k: v for k, v in checkpoint.items() if k != "model_state_dict"}
        classes = checkpoint.get("class_names")
    else:
        state_dict = checkpoint
        classes = None

    if not classes:
        classes = load_classes_from_package(path)
    if not classes:
        classes = expected_classes or list(DEFAULT_CLASSES)

    model = build_model(arch=arch, num_classes=len(classes))
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    return model, list(classes), metadata


class RemappedDataset(Dataset):
    """Wraps an ImageFolder dataset to align class indices with the model's class order."""

    def __init__(self, dataset: ImageFolder, target_classes: list[str]):
        self.dataset = dataset
        self.target_classes = target_classes

        # Validate that all dataset classes are recognized by the model
        for name in dataset.classes:
            if name not in target_classes:
                raise ValueError(
                    f"Dataset class '{name}' not found in target model classes: {target_classes}"
                )

        self.idx_mapping = [target_classes.index(name) for name in dataset.classes]

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int):
        img, label = self.dataset[idx]
        return img, self.idx_mapping[label]


def create_test_loader(
    test_dir: Path | str,
    target_classes: list[str],
    batch_size: int = 32,
    num_workers: int = DEFAULT_NUM_WORKERS,
) -> tuple[DataLoader, list[str]]:
    """Build a DataLoader for the evaluation dataset and verify/remap classes."""
    path = Path(test_dir).resolve()
    if not path.is_dir():
        raise FileNotFoundError(f"Test directory not found at: '{path}'")

    raw_dataset = ImageFolder(root=str(path), transform=get_eval_transforms())
    if len(raw_dataset) == 0:
        raise ValueError(f"No images found in test directory: '{path}'")

    if raw_dataset.classes == target_classes:
        eval_dataset: Dataset = raw_dataset
    else:
        eval_dataset = RemappedDataset(raw_dataset, target_classes)

    loader = DataLoader(
        eval_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    return loader, raw_dataset.classes


def evaluate_model_performance(
    model: nn.Module,
    test_loader: DataLoader,
    classes: list[str],
    device: torch.device,
) -> dict:
    """Run model inference across test_loader, computing accuracy, reports, and confusion matrices."""
    model.eval()
    all_preds: list[int] = []
    all_labels: list[int] = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy().tolist())
            all_labels.extend(labels.cpu().numpy().tolist())

    acc = float(accuracy_score(all_labels, all_preds)) if all_labels else 0.0

    target_labels = list(range(len(classes)))
    report_dict = classification_report(
        all_labels,
        all_preds,
        labels=target_labels,
        target_names=classes,
        digits=4,
        output_dict=True,
        zero_division=0,
    )
    report_str = classification_report(
        all_labels,
        all_preds,
        labels=target_labels,
        target_names=classes,
        digits=4,
        zero_division=0,
    )

    cm = confusion_matrix(all_labels, all_preds, labels=target_labels)
    cm_normalized = confusion_matrix(
        all_labels, all_preds, labels=target_labels, normalize="true"
    )
    cm_normalized = np.nan_to_num(cm_normalized, nan=0.0)

    return {
        "accuracy": acc,
        "classification_report_str": report_str,
        "classification_report_dict": report_dict,
        "confusion_matrix": cm,
        "normalized_confusion_matrix": cm_normalized,
        "predictions": all_preds,
        "labels": all_labels,
        "classes": classes,
    }


def plot_confusion_matrix(
    cm_normalized: np.ndarray,
    classes: list[str],
    output_path: Path | str,
    title: str | None = None,
    accuracy: float | None = None,
) -> Path:
    """Plot and save a normalized confusion matrix heatmap using Seaborn/Matplotlib."""
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if title is None:
        if accuracy is not None:
            title = f"Normalized Confusion Matrix (Overall Accuracy: {accuracy:.2%})"
        else:
            title = "Normalized Confusion Matrix"

    fig, ax = plt.subplots(figsize=(8, 6.5))
    if sns is not None:
        sns.heatmap(
            cm_normalized,
            annot=True,
            fmt=".2%",
            cmap="Blues",
            xticklabels=classes,
            yticklabels=classes,
            cbar=True,
            vmin=0.0,
            vmax=1.0,
            ax=ax,
        )
    else:
        im = ax.imshow(
            cm_normalized,
            interpolation="nearest",
            cmap="Blues",
            vmin=0.0,
            vmax=1.0,
        )
        ax.set_xticks(range(len(classes)))
        ax.set_yticks(range(len(classes)))
        ax.set_xticklabels(classes)
        ax.set_yticklabels(classes)
        for i in range(len(classes)):
            for j in range(len(classes)):
                val = cm_normalized[i, j]
                text_color = "white" if val > 0.5 else "black"
                ax.text(
                    j,
                    i,
                    f"{val:.2%}",
                    ha="center",
                    va="center",
                    color=text_color,
                    fontsize=9,
                )
        fig.colorbar(im, ax=ax)

    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Predicted Label", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_ylabel("True Label", fontsize=11, fontweight="bold", labelpad=10)
    fig.tight_layout()
    fig.savefig(out_file, dpi=300)
    plt.close(fig)

    return out_file


def run_evaluation(
    model_path: Path | str,
    test_dir: Path | str,
    output_plot: Path | str = DEFAULT_OUTPUT_PLOT,
    batch_size: int = 32,
    num_workers: int = DEFAULT_NUM_WORKERS,
    arch: str = "resnet18",
    device: torch.device | None = None,
) -> dict:
    """High-level evaluation pipeline taking model and test directory and producing plot and metrics."""
    target_device = device or get_device()
    print(f"Loading checkpoint: {model_path}")
    model, classes, metadata = load_checkpoint(
        model_path=model_path,
        arch=arch,
        device=target_device,
    )
    print(f"Target classes ({len(classes)}): {classes}")
    if metadata:
        print(f"Checkpoint metadata: {metadata}")

    print(f"Building test DataLoader from: {test_dir}")
    test_loader, detected_classes = create_test_loader(
        test_dir=test_dir,
        target_classes=classes,
        batch_size=batch_size,
        num_workers=num_workers,
    )
    print(
        f"Evaluation samples: {len(test_loader.dataset)} across {len(detected_classes)} folder classes"
    )

    print("Running model inference...")
    results = evaluate_model_performance(model, test_loader, classes, target_device)

    print("\n" + "=" * 60)
    print("CLASSIFICATION REPORT")
    print("=" * 60)
    print(results["classification_report_str"])
    print(f"Overall Accuracy: {results['accuracy']:.2%}")
    print("=" * 60)

    plot_path = plot_confusion_matrix(
        results["normalized_confusion_matrix"],
        classes=classes,
        output_path=output_plot,
        accuracy=results["accuracy"],
    )
    print(f"\nSaved normalized confusion matrix heatmap to: {plot_path}")
    results["plot_path"] = plot_path

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate Sortify model performance and generate confusion matrix heatmap."
    )
    parser.add_argument(
        "--model_path",
        "--model-path",
        dest="model_path",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help=f"Path to trained model checkpoint (.pth). Default: {DEFAULT_MODEL_PATH}",
    )
    parser.add_argument(
        "--test_dir",
        "--test-dir",
        dest="test_dir",
        type=Path,
        default=DEFAULT_TEST_DIR,
        help=f"Path to evaluation image directory. Default: {DEFAULT_TEST_DIR}",
    )
    parser.add_argument(
        "--output_plot",
        "--output-plot",
        dest="output_plot",
        type=Path,
        default=DEFAULT_OUTPUT_PLOT,
        help=f"Path to save confusion matrix heatmap image. Default: {DEFAULT_OUTPUT_PLOT}",
    )
    parser.add_argument(
        "--batch_size",
        "--batch-size",
        dest="batch_size",
        type=int,
        default=32,
        help="Batch size for evaluation. Default: 32",
    )
    parser.add_argument(
        "--num_workers",
        "--num-workers",
        dest="num_workers",
        type=int,
        default=DEFAULT_NUM_WORKERS,
        help=f"DataLoader num_workers. Default: {DEFAULT_NUM_WORKERS}",
    )
    parser.add_argument(
        "--arch",
        type=str,
        default="resnet18",
        choices=["resnet18", "mobilenet_v2"],
        help="Model architecture ('resnet18' or 'mobilenet_v2'). Default: resnet18",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device override (e.g. 'cpu', 'cuda', 'mps'). Default: auto-detect",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    device = get_device(args.device)
    print(f"Using device: {device}")
    run_evaluation(
        model_path=args.model_path,
        test_dir=args.test_dir,
        output_plot=args.output_plot,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        arch=args.arch,
        device=device,
    )


if __name__ == "__main__":
    main()
