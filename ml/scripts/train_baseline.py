"""Train the Sortify ResNet-18 baseline (frozen backbone, new 5-bin head).

Expects the train/val/test folders written by ml/scripts/split_data.py, built
from 224x224 images written by ml/scripts/preprocess.py:

    <data-dir>/{train,val,test}/{compost,paper,plastic,glass,landfill}/*.jpg

ImageNet normalization is applied here at load time, never baked into files.

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
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

CLASS_NAMES = ["compost", "glass", "landfill", "paper", "plastic"]
NUM_CLASSES = len(CLASS_NAMES)
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "ml" / "models" / "resnet18_baseline.pth"


def get_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def get_transforms() -> transforms.Compose:
    return transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )


def build_model() -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model


def set_train_mode(model: nn.Module) -> None:
    # Frozen BatchNorm layers must keep their ImageNet running stats, so only the
    # new head is put in train mode.
    model.eval()
    model.fc.train()


def load_split(data_dir: Path, split: str) -> datasets.ImageFolder:
    split_dir = data_dir / split
    if not split_dir.is_dir():
        sys.exit(
            f"Error: {split_dir} not found. Run ml/scripts/split_data.py on the "
            "preprocessed 5-class data first."
        )
    dataset = datasets.ImageFolder(split_dir, transform=get_transforms())
    if dataset.classes != CLASS_NAMES:
        sys.exit(
            f"Error: expected class folders {CLASS_NAMES} in {split_dir}, "
            f"found {dataset.classes}."
        )
    return dataset


def run_epoch(model, loader, criterion, device, optimizer=None):
    training = optimizer is not None
    if training:
        set_train_mode(model)
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
    return total_loss / count, correct / count


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
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    torch.manual_seed(args.seed)

    train_set = load_split(args.data_dir, "train")
    val_set = load_split(args.data_dir, "val")
    test_dir = args.data_dir / "test"
    test_set = load_split(args.data_dir, "test") if test_dir.is_dir() else None

    device = get_device()
    print(f"Device: {device}")
    print(f"Images: train={len(train_set)} val={len(val_set)}", end=" ")
    print(f"test={len(test_set) if test_set else 0}  classes={CLASS_NAMES}")

    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=args.batch_size)

    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=args.lr)

    best_val_acc, best_epoch, best_state = -1.0, 0, None
    print(f"{'epoch':>5} {'train_loss':>11} {'val_loss':>9} {'val_acc':>8}")
    for epoch in range(1, args.epochs + 1):
        train_loss, _ = run_epoch(model, train_loader, criterion, device, optimizer)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, device)
        print(f"{epoch:>5} {train_loss:>11.4f} {val_loss:>9.4f} {val_acc:>8.2%}")
        if val_acc > best_val_acc:
            best_val_acc, best_epoch = val_acc, epoch
            best_state = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)
    print(f"Best val accuracy {best_val_acc:.2%} at epoch {best_epoch}")

    if test_set:
        print("Test examples (softmax over all 5 bins):")
        test_acc = report_test(model, DataLoader(test_set, batch_size=32), device)
        print(f"Test accuracy: {test_acc:.2%} on {len(test_set)} images")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": {k: v.cpu() for k, v in best_state.items()},
            "class_names": CLASS_NAMES,
            "best_epoch": best_epoch,
            "val_accuracy": best_val_acc,
        },
        args.output,
    )
    print(f"Saved weights to {args.output}")


if __name__ == "__main__":
    main()
