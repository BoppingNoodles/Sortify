"""
Week 1 AI/ML Learning Exercise — ResNet-18 Transfer Learning
Author: Max
Branch: feat/ml/max/resnet-transfer-learning

This is the exact Sortify classifier workflow, scaled down:
    1. Load a pretrained ResNet-18 (already learned ImageNet visual features)
    2. Replace the final layer so it outputs 5 waste classes
    3. Train only that new layer on a tiny sample for 2–3 epochs
    4. Run inference on one image and print the predicted class

Reference: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

Run from the repo root, with the venv activated:
    python ml/resnet_transfer_learning.py
"""

from __future__ import annotations

import random
from pathlib import Path

import torch
from PIL import Image, ImageDraw
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

CLASS_NAMES = [
    "compost",
    "recycling_paper",
    "recycling_plastic",
    "recycling_glass",
    "landfill",
]
NUM_CLASSES = len(CLASS_NAMES)

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DIR = REPO_ROOT / "data" / "sample"
TEST_IMAGE_PATH = REPO_ROOT / "data" / "test_image.jpg"

# Distinctive RGB colors so a tiny synthetic set is actually learnable in 3 epochs.
# Week 2 replaces this with a real waste dataset (TrashNet / Kaggle / Hugging Face).
CLASS_COLORS = {
    "compost": (34, 139, 34),
    "recycling_paper": (245, 222, 179),
    "recycling_plastic": (30, 144, 255),
    "recycling_glass": (64, 224, 208),
    "landfill": (105, 105, 105),
}


def get_device() -> torch.device:
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def get_transforms() -> transforms.Compose:
    """ImageNet preprocessing that pretrained ResNet-18 expects."""
    return transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


def build_model() -> nn.Module:
    """Load pretrained ResNet-18 and swap the classifier head for 5 classes."""
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    # Freeze the backbone: keep ImageNet features, train only the new head.
    for param in model.parameters():
        param.requires_grad = False

    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, NUM_CLASSES)
    return model


def _make_class_image(class_name: str, seed: int, size: int = 256) -> Image.Image:
    rng = random.Random(seed)
    base = CLASS_COLORS[class_name]
    image = Image.new("RGB", (size, size), base)
    draw = ImageDraw.Draw(image)
    for _ in range(8):
        x0, y0 = rng.randint(0, size - 40), rng.randint(0, size - 40)
        x1, y1 = x0 + rng.randint(20, 80), y0 + rng.randint(20, 80)
        shift = tuple(max(0, min(255, c + rng.randint(-40, 40))) for c in base)
        draw.rectangle([x0, y0, x1, y1], fill=shift)
    return image


def ensure_sample_dataset(images_per_class: int = 10) -> None:
    """Create ~50 tiny synthetic images (gitignored under data/)."""
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    for class_index, class_name in enumerate(CLASS_NAMES):
        class_dir = SAMPLE_DIR / class_name
        class_dir.mkdir(parents=True, exist_ok=True)
        existing = list(class_dir.glob("*.jpg"))
        if len(existing) >= images_per_class:
            continue
        for i in range(images_per_class):
            image = _make_class_image(class_name, seed=class_index * 100 + i)
            image.save(class_dir / f"{class_name}_{i:02d}.jpg", quality=95)

    if not TEST_IMAGE_PATH.exists():
        # Held-out compost-style image, not one of the training files.
        _make_class_image("compost", seed=999).save(TEST_IMAGE_PATH, quality=95)


def train_one_epoch(model, dataloader, criterion, optimizer, device) -> float:
    model.train()
    running_loss = 0.0
    num_samples = 0

    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        batch_size = inputs.size(0)
        running_loss += loss.item() * batch_size
        num_samples += batch_size

    return running_loss / max(num_samples, 1)


def run_training(data_dir: str, epochs: int = 3) -> nn.Module:
    device = get_device()
    dataset = datasets.ImageFolder(data_dir, transform=get_transforms())
    if set(dataset.classes) != set(CLASS_NAMES):
        raise ValueError(
            f"Expected folders {CLASS_NAMES}, found {dataset.classes} in {data_dir}"
        )

    dataloader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=0)
    model = build_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=1e-3)

    print(f"Device: {device}")
    print(f"Images: {len(dataset)} across {dataset.classes}")

    for epoch in range(1, epochs + 1):
        average_loss = train_one_epoch(model, dataloader, criterion, optimizer, device)
        print(f"Epoch {epoch}/{epochs} — loss: {average_loss:.4f}")

    model.class_names = dataset.classes
    return model


def predict(model, image_path: str, device) -> str:
    image = Image.open(image_path).convert("RGB")
    tensor = get_transforms()(image).unsqueeze(0).to(device)

    model.eval()
    with torch.no_grad():
        logits = model(tensor)
        class_index = int(logits.argmax(dim=1).item())

    class_names = getattr(model, "class_names", sorted(CLASS_NAMES))
    return class_names[class_index]


if __name__ == "__main__":
    ensure_sample_dataset(images_per_class=10)
    device = get_device()
    trained_model = run_training(data_dir=str(SAMPLE_DIR), epochs=3)
    predicted_class = predict(trained_model, str(TEST_IMAGE_PATH), device)
    print(f"Predicted class: {predicted_class}")
