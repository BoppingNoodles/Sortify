"""Verify the exported model package loads with only state_dict + classes.json.

This deliberately does not import anything from ml/ or read the training
checkpoint, so it behaves like the backend team's loader.

Run from the repository root:
    python ml/tests/test_export_model.py
    python ml/tests/test_export_model.py --package-dir ml/models/mvp_package
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from torch import nn
from torchvision import models

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_PACKAGE = REPO_ROOT / "ml" / "models" / "mvp_package"
WEIGHTS_FILE = "resnet18_sortify.pth"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the exported Sortify model package."
    )
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE)
    args = parser.parse_args()

    # 1. classes.json
    with open(args.package_dir / "classes.json") as f:
        class_map = json.load(f)
    expected_keys = [str(i) for i in range(len(class_map))]
    assert sorted(class_map) == sorted(expected_keys), f"Bad keys: {list(class_map)}"
    classes = [class_map[k] for k in expected_keys]
    assert len(classes) == 5, f"Expected 5 classes, got {len(classes)}"
    print(f"classes.json OK: {class_map}")

    # 2. state_dict only (weights_only=True rejects anything but tensors/primitives)
    state_dict = torch.load(
        args.package_dir / WEIGHTS_FILE, map_location="cpu", weights_only=True
    )
    assert "model_state_dict" not in state_dict, "Expected a bare state_dict."

    # 3. Rebuild the architecture and load
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, len(classes))
    model.load_state_dict(state_dict)
    model.eval()
    print("state_dict loaded into resnet18 (strict)")

    # 4. Forward pass on a dummy 224x224 input
    with torch.no_grad():
        probs = torch.softmax(model(torch.randn(1, 3, 224, 224)), dim=1)[0]
    assert probs.shape == (len(classes),)
    assert torch.isfinite(probs).all()
    assert abs(probs.sum().item() - 1.0) < 1e-4

    print("Dummy forward pass OK:")
    for name, p in zip(classes, probs.tolist()):
        print(f"  {name:<9} {p:.1%}")
    print("PASS")


if __name__ == "__main__":
    main()
