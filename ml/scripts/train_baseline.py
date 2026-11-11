"""Train the Sortify ResNet-18 baseline (frozen backbone, new 5-bin head).

Expects the train/val/test folders written by ml/scripts/split_data.py, built
from 224x224 images written by ml/scripts/preprocess.py:

    <data-dir>/{train,val,test}/{compost,paper,plastic,glass,landfill}/*.jpg

Training images are augmented by ml/scripts/dataset.py. ImageNet normalization
is applied there at load time, never baked into files. After training, loss
and validation-accuracy curves are written to docs/ml/baseline_loss_curves.png.

Run from the repo root with the venv activated:
    python ml/scripts/train_baseline.py --data-dir data/processed --epochs 12
"""

from __future__ import annotations

import argparse
import copy
import random
import sys
from pathlib import Path

import torch
from torch import nn, optim
from torchvision import models

# Running this file as a script puts ml/scripts/ on sys.path, not the repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.dataset import get_dataloaders

# ImageFolder order is alphabetical, so index 0 is compost, not paper:
# 0: compost, 1: glass, 2: landfill, 3: paper, 4: plastic.
# Downstream code must read checkpoint["class_names"] (or classes.json),
# not assume paper=0 from split_data.py.
CLASS_NAMES = ["compost", "glass", "landfill", "paper", "plastic"]
NUM_CLASSES = len(CLASS_NAMES)
DEFAULT_OUTPUT = REPO_ROOT / "ml" / "models" / "resnet18_baseline.pth"
DEFAULT_PLOT = REPO_ROOT / "docs" / "ml" / "baseline_loss_curves.png"


def get_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def build_model() -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model


def set_train_mode(model: nn.Module, head: nn.Module | None = None) -> None:
    # Frozen BatchNorm layers must keep their ImageNet running stats, so only the
    # new head is put in train mode. `head` lets MobileNet train its linear layer
    # without a second copy of this helper.
    model.eval()
    trainable = model.fc if head is None else head
    trainable.train()


def require_best_checkpoint(best_state: dict | None) -> dict:
    """Refuse to call load_state_dict when training never produced a checkpoint."""
    if best_state is None:
        raise RuntimeError("Training finished without any valid evaluation epochs.")
    return best_state


def load_baseline_checkpoint(
    checkpoint_path: Path, model: nn.Module
) -> tuple[nn.Module, dict]:
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    state_dict = checkpoint.get("model_state_dict", checkpoint)
    model.load_state_dict(state_dict)
    return model, checkpoint


def run_epoch(model, loader, criterion, device, optimizer=None, head=None):
    training = optimizer is not None
    if training:
        set_train_mode(model, head)
    else:
        model.eval()

    total_loss, correct, count = 0.0, 0, 0
    with torch.set_grad_enabled(training):
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            logits = model(inputs)
            loss = criterion(logits, labels)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * inputs.size(0)
            correct += (logits.argmax(dim=1) == labels).sum().item()
            count += inputs.size(0)
    if count == 0:
        return 0.0, 0.0
    return total_loss / count, correct / count


def save_training_curves(
    history: list[tuple[int, float, float, float]], path: Path
) -> None:
    """Write train/val loss and validation accuracy for one training run.

    Each history row is (epoch, train_loss, val_loss, val_accuracy).
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    epochs = [row[0] for row in history]
    train_loss = [row[1] for row in history]
    val_loss = [row[2] for row in history]
    val_acc = [row[3] * 100 for row in history]
    best_index = max(range(len(history)), key=lambda i: history[i][3])

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].plot(epochs, train_loss, marker="o", label="Train loss")
    axes[0].plot(epochs, val_loss, marker="o", label="Validation loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Loss")
    axes[0].set_xticks(epochs)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(epochs, val_acc, marker="o", label="Validation accuracy")
    axes[1].scatter(
        [epochs[best_index]],
        [val_acc[best_index]],
        s=80,
        zorder=3,
        label=f"Best ({val_acc[best_index]:.2f}%)",
    )
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy (%)")
    axes[1].set_title("Validation accuracy")
    axes[1].set_xticks(epochs)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.suptitle("ResNet-18 baseline, frozen backbone, 5 bins")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def report_test(model, loader, device, num_examples: int = 5) -> float:
    model.eval()
    correct, count, shown = 0, 0, 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            probs = torch.softmax(model(inputs), dim=1)
            correct += (probs.argmax(dim=1) == labels).sum().item()
            count += inputs.size(0)
            for prob, label in zip(probs.cpu(), labels.cpu()):
                if shown >= num_examples:
                    break
                bins = "  ".join(
                    f"{name}={p:.1%}" for name, p in zip(CLASS_NAMES, prob.tolist())
                )
                print(f"  true={CLASS_NAMES[label]:<8} {bins}")
                shown += 1
    return correct / count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-dir", type=Path, default=REPO_ROOT / "data/processed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--plot", type=Path, default=DEFAULT_PLOT)
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    train_loader, val_loader, test_loader, classes = get_dataloaders(
        args.data_dir,
        batch_size=args.batch_size,
    )
    if list(classes) != CLASS_NAMES:
        sys.exit(
            f"Error: expected class order {CLASS_NAMES}, "
            f"ImageFolder returned {list(classes)}."
        )

    device = get_device()
    print(f"Device: {device}")
    print(
        f"Images: train={len(train_loader.dataset)} "
        f"val={len(val_loader.dataset)} test={len(test_loader.dataset)}  "
        f"classes={list(classes)}"
    )

    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=args.lr)

    best_val_acc, best_epoch, best_state = -1.0, 0, None
    history: list[tuple[int, float, float, float]] = []
    print(f"{'epoch':>5} {'train_loss':>11} {'val_loss':>9} {'val_acc':>8}")
    for epoch in range(1, args.epochs + 1):
        train_loss, _ = run_epoch(model, train_loader, criterion, device, optimizer)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, device)
        history.append((epoch, train_loss, val_loss, val_acc))
        print(f"{epoch:>5} {train_loss:>11.4f} {val_loss:>9.4f} {val_acc:>8.2%}")
        if val_acc > best_val_acc:
            best_val_acc, best_epoch = val_acc, epoch
            best_state = copy.deepcopy(model.state_dict())

    best_state = require_best_checkpoint(best_state)
    model.load_state_dict(best_state)
    print(f"Best val accuracy {best_val_acc:.2%} at epoch {best_epoch}")

    print("Test examples (softmax over all 5 bins):")
    test_acc = report_test(model, test_loader, device)
    print(f"Test accuracy: {test_acc:.2%} on {len(test_loader.dataset)} images")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": {k: v.cpu() for k, v in best_state.items()},
            "class_names": list(classes),
            "best_epoch": best_epoch,
            "val_accuracy": best_val_acc,
        },
        args.output,
    )
    print(f"Saved weights to {args.output}")
    _, checkpoint = load_baseline_checkpoint(args.output, build_model())
    print(
        "Reloaded checkpoint: "
        f"class_names={checkpoint['class_names']} epoch={checkpoint['best_epoch']}"
    )
    save_training_curves(history, args.plot)
    print(f"Saved curves to {args.plot}")


if __name__ == "__main__":
    main()
