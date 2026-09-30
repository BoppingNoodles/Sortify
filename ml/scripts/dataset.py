import argparse
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


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


def get_dataloaders(data_dir, batch_size=32, num_workers=2):
    data_dir = Path(data_dir)

    train_set = ImageFolder(root=data_dir / "train", transform=get_train_transforms())
    val_set = ImageFolder(root=data_dir / "val", transform=get_eval_transforms())
    test_set = ImageFolder(root=data_dir / "test", transform=get_eval_transforms())

    train_loader = DataLoader(
        train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    val_loader = DataLoader(
        val_set, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    test_loader = DataLoader(
        test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )

    return train_loader, val_loader, test_loader, train_set.classes


def visualize_batch(data_dir, out):
    import matplotlib.pyplot as plt

    train_loader, _, _, classes = get_dataloaders(data_dir, batch_size=8, num_workers=0)
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
    plt.savefig(out, dpi=150)
    print(f"Saved preview to {out}")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preview augmented training images")
    parser.add_argument("--data_dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--out", type=Path, default=Path("augmentation_preview.png"))
    args = parser.parse_args()
    visualize_batch(args.data_dir, args.out)
