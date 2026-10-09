"""Train a MobileNetV2 head and compare it with the ResNet-18 baseline.

Uses the same augmented train/val/test loaders as the baseline
(ml/scripts/dataset.py). ImageNet normalization stays in those loaders.

Run from the repo root with the venv activated:
    python ml/scripts/train_mobilenet.py --data-dir data/processed --epochs 10
"""

from __future__ import annotations

import argparse
import copy
import random
import sys
import time
from pathlib import Path

import torch
from torch import nn, optim
from torchvision import models

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.scripts.dataset import get_dataloaders
from ml.scripts.train_baseline import (
    CLASS_NAMES,
    get_device,
    load_baseline_checkpoint,
    require_best_checkpoint,
    run_epoch,
)
from ml.scripts.train_baseline import (
    build_model as build_resnet,
)

# ImageFolder order is alphabetical, so index 0 is compost, not paper:
# 0: compost, 1: glass, 2: landfill, 3: paper, 4: plastic.
# Downstream code must read checkpoint["class_names"] (or classes.json),
# not assume paper=0 from split_data.py.
NUM_CLASSES = len(CLASS_NAMES)
DEFAULT_OUTPUT = REPO_ROOT / "ml" / "models" / "mobilenet_v2.pth"
DEFAULT_RESNET = REPO_ROOT / "ml" / "models" / "resnet18_baseline.pth"
DEFAULT_DOC = REPO_ROOT / "docs" / "ml" / "architecture_comparison.md"
LATENCY_IMAGES = 100


def build_model() -> nn.Module:
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)
    return model


def load_mobilenet_checkpoint(
    checkpoint_path: Path, model: nn.Module
) -> tuple[nn.Module, dict]:
    return load_baseline_checkpoint(checkpoint_path, model)


def bin_confidences(logits: torch.Tensor) -> torch.Tensor:
    """Softmax over the 5 bins. These are percents-ready scores, not logits."""
    if logits.ndim != 2 or logits.shape[1] != NUM_CLASSES:
        raise ValueError(
            f"Expected logits (N, {NUM_CLASSES}), got {tuple(logits.shape)}"
        )
    return torch.softmax(logits, dim=1)


def same_class_order(left, right) -> bool:
    return list(left) == list(right)


def softmax_accuracy(model, loader, device) -> float:
    model.eval()
    correct, count = 0, 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            probs = bin_confidences(model(inputs))
            correct += (probs.argmax(dim=1) == labels).sum().item()
            count += inputs.size(0)
    if count == 0:
        return 0.0
    return correct / count


def print_softmax_examples(model, loader, device, class_names, num_examples=5) -> None:
    model.eval()
    shown = 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            probs = bin_confidences(model(inputs))
            for prob, label in zip(probs.cpu(), labels.cpu()):
                if shown >= num_examples:
                    return
                bins = "  ".join(
                    f"{name}={p:.1%}" for name, p in zip(class_names, prob.tolist())
                )
                print(f"  true={class_names[label]:<8} {bins}")
                shown += 1


def cpu_latency_ms(model, loader, max_images: int = LATENCY_IMAGES) -> float:
    """Mean CPU milliseconds per image, timed on up to max_images test photos."""
    device = torch.device("cpu")
    model = model.to(device)
    model.eval()
    seen = 0
    total_s = 0.0
    warmed = False
    with torch.no_grad():
        for inputs, _ in loader:
            inputs = inputs.to(device)
            if not warmed:
                model(inputs)
                warmed = True
            need = max_images - seen
            batch = inputs[:need]
            start = time.perf_counter()
            model(batch)
            total_s += time.perf_counter() - start
            seen += batch.size(0)
            if seen >= max_images:
                break
    if seen == 0:
        return 0.0
    return (total_s / seen) * 1000


def file_size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def write_comparison(path: Path, rows: list[dict], class_names: list[str]) -> None:
    lines = [
        "# MobileNetV2 vs ResNet-18",
        "",
        "Same split (`data/processed`, 70/15/15, seed 42) and the same",
        "`get_dataloaders` augmentations. Both models keep a frozen pretrained",
        "backbone and train only the new 5-bin layer. Accuracy below is the",
        "best-validation checkpoint, remeasured on the val and test loaders.",
        "Latency is the mean CPU time per image over 100 test photos.",
        "",
        "ImageFolder class order is alphabetical. Index 0 is compost, not paper:",
        "`0: compost`, `1: glass`, `2: landfill`, `3: paper`, `4: plastic`.",
        'Read `checkpoint["class_names"]` (or `classes.json`). Do not assume',
        "`paper=0` from `split_data.py`.",
        "",
        "| model | best epoch | val accuracy | test accuracy | file size | CPU latency |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['name']} | {row['epoch']} | {row['val_acc']:.2%} "
            f"| {row['test_acc']:.2%} | {row['size_mb']:.1f} MB "
            f"| {row['latency_ms']:.2f} ms |"
        )
    smaller = min(rows, key=lambda row: row["size_mb"])
    faster = min(rows, key=lambda row: row["latency_ms"])
    sharper = max(rows, key=lambda row: row["test_acc"])
    lines.extend(
        [
            "",
            f"Class order in both checkpoints: {class_names}.",
            "",
            (
                f"{smaller['name']} is the smaller weight file "
                f"({smaller['size_mb']:.1f} MB)."
            ),
            (
                f"{faster['name']} is faster on CPU "
                f"({faster['latency_ms']:.2f} ms per image)."
            ),
            (
                f"{sharper['name']} has the higher test accuracy "
                f"({sharper['test_acc']:.2%})."
            ),
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data-dir", type=Path, default=REPO_ROOT / "data/processed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--resnet-checkpoint", type=Path, default=DEFAULT_RESNET)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--epochs", type=int, default=10)
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
    if train_loader.batch_size != args.batch_size:
        raise RuntimeError(
            f"Train loader batch size is {train_loader.batch_size}, "
            f"not --batch-size {args.batch_size}."
        )
    if list(classes) != list(CLASS_NAMES):
        sys.exit(
            f"Error: expected class order {list(CLASS_NAMES)}, "
            f"ImageFolder returned {list(classes)}."
        )

    device = get_device()
    print(f"Device: {device}")
    print(
        f"Images: train={len(train_loader.dataset)} "
        f"val={len(val_loader.dataset)} test={len(test_loader.dataset)}  "
        f"classes={list(classes)}  batch_size={train_loader.batch_size}"
    )

    model = build_model().to(device)
    head = model.classifier[1]
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(head.parameters(), lr=args.lr)

    best_val_acc, best_epoch, best_state = -1.0, 0, None
    print(f"{'epoch':>5} {'train_loss':>11} {'val_loss':>9} {'val_acc':>8}")
    for epoch in range(1, args.epochs + 1):
        train_loss, _ = run_epoch(
            model, train_loader, criterion, device, optimizer, head=head
        )
        val_loss, val_acc = run_epoch(model, val_loader, criterion, device)
        print(f"{epoch:>5} {train_loss:>11.4f} {val_loss:>9.4f} {val_acc:>8.2%}")
        if val_acc > best_val_acc:
            best_val_acc, best_epoch = val_acc, epoch
            best_state = copy.deepcopy(model.state_dict())

    best_state = require_best_checkpoint(best_state)
    model.load_state_dict(best_state)
    print(f"Best val accuracy {best_val_acc:.2%} at epoch {best_epoch}")

    print("Test examples (softmax over all 5 bins):")
    print_softmax_examples(model, test_loader, device, list(classes))
    test_acc = softmax_accuracy(model, test_loader, device)
    val_acc = softmax_accuracy(model, val_loader, device)
    print(f"Test accuracy: {test_acc:.2%} on {len(test_loader.dataset)} images")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": {k: v.cpu() for k, v in best_state.items()},
            "class_names": list(classes),
            "best_epoch": best_epoch,
            "val_accuracy": best_val_acc,
            "architecture": "mobilenet_v2",
        },
        args.output,
    )
    _, mobilenet_ckpt = load_mobilenet_checkpoint(args.output, build_model())
    print(
        "Reloaded MobileNet checkpoint: "
        f"class_names={mobilenet_ckpt['class_names']} epoch={mobilenet_ckpt['best_epoch']}"
    )

    if not args.resnet_checkpoint.is_file():
        sys.exit(
            f"Error: ResNet baseline checkpoint not found: {args.resnet_checkpoint}"
        )
    resnet, resnet_ckpt = load_baseline_checkpoint(
        args.resnet_checkpoint, build_resnet()
    )
    resnet_names = list(resnet_ckpt.get("class_names", []))
    if not same_class_order(resnet_names, classes):
        sys.exit(
            f"Error: class order mismatch. MobileNet {list(classes)}, "
            f"ResNet checkpoint {resnet_names}."
        )

    resnet_device = get_device()
    resnet = resnet.to(resnet_device)
    resnet_val = softmax_accuracy(resnet, val_loader, resnet_device)
    resnet_test = softmax_accuracy(resnet, test_loader, resnet_device)
    mobilenet_cpu = load_mobilenet_checkpoint(args.output, build_model())[0]
    resnet_cpu = load_baseline_checkpoint(args.resnet_checkpoint, build_resnet())[0]

    rows = [
        {
            "name": "ResNet-18",
            "epoch": resnet_ckpt.get("best_epoch", ""),
            "val_acc": resnet_val,
            "test_acc": resnet_test,
            "size_mb": file_size_mb(args.resnet_checkpoint),
            "latency_ms": cpu_latency_ms(resnet_cpu, test_loader),
        },
        {
            "name": "MobileNetV2",
            "epoch": best_epoch,
            "val_acc": val_acc,
            "test_acc": test_acc,
            "size_mb": file_size_mb(args.output),
            "latency_ms": cpu_latency_ms(mobilenet_cpu, test_loader),
        },
    ]
    print(
        f"{'model':<14} {'epoch':>5} {'val_acc':>8} {'test_acc':>9} {'size':>10} {'cpu_ms':>8}"
    )
    for row in rows:
        print(
            f"{row['name']:<14} {row['epoch']:>5} {row['val_acc']:>8.2%} "
            f"{row['test_acc']:>9.2%} {row['size_mb']:>8.1f} MB {row['latency_ms']:>7.2f}"
        )
    write_comparison(args.doc, rows, list(classes))
    print(f"Saved weights to {args.output}")
    print(f"Saved comparison to {args.doc}")


if __name__ == "__main__":
    main()
