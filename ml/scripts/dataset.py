import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

DEFAULT_NUM_WORKERS = 2 if sys.platform != "win32" else 0


def get_train_transforms():
    return transforms.Compose(
        [
            transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )


def get_eval_transforms():
    return transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ]
    )


def get_dataloaders(data_dir, batch_size=32, num_workers=DEFAULT_NUM_WORKERS):
    data_dir = Path(data_dir)
    train_dir = data_dir / "train"
    if not train_dir.is_dir():
        raise FileNotFoundError(
            f"Directory not found: '{train_dir}'. "
            "Please run 'python ml/scripts/split_data.py' on the processed dataset first!"
        )

    train_set = ImageFolder(root=data_dir / "train", transform=get_train_transforms())
    val_set = ImageFolder(root=data_dir / "val", transform=get_eval_transforms())
    test_set = ImageFolder(root=data_dir / "test", transform=get_eval_transforms())

    if not (train_set.classes == val_set.classes == test_set.classes):
        raise ValueError(
            "Class folders differ across splits: "
            f"train={train_set.classes}, val={val_set.classes}, test={test_set.classes}"
        )

    train_loader = DataLoader(
        train_set,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
    )
    val_loader = DataLoader(
        val_set,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )
    test_loader = DataLoader(
        test_set,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )

    return train_loader, val_loader, test_loader, train_set.classes


def print_summary(train_loader, val_loader, test_loader, classes):
    print(f"Classes: {classes}")
    print(
        f"Images: train={len(train_loader.dataset)}, "
        f"val={len(val_loader.dataset)}, test={len(test_loader.dataset)}"
    )
    images, labels = next(iter(train_loader))
    print(f"Batch shape: {tuple(images.shape)}, labels shape: {tuple(labels.shape)}")


def visualize_batch(train_loader, classes, out):
    images, labels = next(iter(train_loader))

    mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
    std = torch.tensor(IMAGENET_STD).view(3, 1, 1)

    _, axes = plt.subplots(2, 4, figsize=(12, 6))
    for ax, img, label in zip(axes.flat, images, labels):
        img = (img * std + mean).clamp(0, 1)
        ax.imshow(img.permute(1, 2, 0).numpy())
        ax.set_title(classes[label.item()])
        ax.axis("off")

    plt.tight_layout()
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved preview to {out}")


REPO_ROOT = Path(__file__).resolve().parent.parent.parent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preview augmented training images")
    parser.add_argument(
        "--data-dir", type=Path, default=REPO_ROOT / "data" / "processed"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "docs" / "ml" / "augmentation_preview.png",
    )
    args = parser.parse_args()

    train_loader, val_loader, test_loader, classes = get_dataloaders(
        args.data_dir, num_workers=0
    )

    print_summary(train_loader, val_loader, test_loader, classes)
    visualize_batch(train_loader, classes, args.out)
