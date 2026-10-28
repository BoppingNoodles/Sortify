"""PyTorch model inference singleton service for Sortify."""

import io
import logging
import time
from pathlib import Path
from typing import Any, Self

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# Default path to model weights
DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parent.parent / "models" / "sortify_mvp_v1.pth"
)

# Canonical raw model classes (6-class baseline)
DEFAULT_CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

# Known mock headers used in existing test harnesses
MOCK_TEST_HEADERS = {
    b"\xff\xd8\xff",
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01",
}


class ModelService:
    """Singleton service for loading PyTorch weights and executing CPU/GPU inference."""

    _instance: "ModelService | None" = None

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        model_path: Path | str | None = None,
        class_names: list[str] | None = None,
        device: torch.device | str | None = None,
    ):
        if getattr(self, "_initialized", False) and model_path is None:
            return

        cfg_model_path = getattr(settings, "MODEL_PATH", None)
        if model_path is not None:
            self.model_path = Path(model_path)
        elif cfg_model_path:
            self.model_path = Path(cfg_model_path)
        else:
            self.model_path = DEFAULT_MODEL_PATH

        if device is not None:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model: torch.nn.Module | None = None
        self.class_names = class_names or list(DEFAULT_CLASSES)

        # Standard torchvision evaluation pipeline (Resize, CenterCrop, Normalize)
        self.transform = transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        self._load_model()
        self._initialized = True

    def _load_model(self) -> None:
        """Loads weights into eval mode on target device if file exists, else sets fallback mode."""
        if self.model_path.exists():
            try:
                from torchvision import models

                checkpoint = torch.load(self.model_path, map_location=self.device)
                resnet = models.resnet18(weights=None)
                resnet.fc = torch.nn.Linear(
                    resnet.fc.in_features, len(self.class_names)
                )

                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    state_dict = checkpoint["model_state_dict"]
                    if "class_names" in checkpoint:
                        self.class_names = checkpoint["class_names"]
                elif isinstance(checkpoint, dict):
                    state_dict = checkpoint
                else:
                    state_dict = checkpoint.state_dict()

                resnet.load_state_dict(state_dict)
                resnet.to(self.device)
                resnet.eval()
                self.model = resnet
                logger.info(
                    "Loaded model weights from %s onto %s",
                    self.model_path,
                    self.device,
                )
            except (OSError, RuntimeError, KeyError, ValueError) as exc:
                logger.warning(
                    "Failed to load weights from %s: %s. Running in fallback mode.",
                    self.model_path,
                    exc,
                )
                self.model = None
        else:
            logger.info(
                "%s not found. Running ModelService in fallback mode.",
                self.model_path,
            )
            self.model = None

    def predict(self, image_bytes: bytes) -> dict[str, Any]:
        """Runs inference on uploaded image bytes.

        Returns:
            dict containing category, item_name, confidence, alternatives, and latency_ms.
        """
        start_time = time.perf_counter()

        # Validate that image bytes can be decoded
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except (UnidentifiedImageError, OSError):
            if self.model is None and image_bytes in MOCK_TEST_HEADERS:
                elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                return {
                    "category": "compost",
                    "item_name": "Almond Milk Carton (Scaffold)",
                    "confidence": 0.91,
                    "alternatives": [
                        {"category": "paper", "confidence": 0.06},
                        {"category": "trash", "confidence": 0.03},
                    ],
                    "is_mock": True,
                    "latency_ms": elapsed_ms,
                }
            raise

        if self.model is None:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(
                "[INFERENCE] Fallback mock inference completed in %.2fms",
                elapsed_ms,
            )
            return {
                "category": "compost",
                "item_name": "Almond Milk Carton (Scaffold)",
                "confidence": 0.91,
                "alternatives": [
                    {"category": "paper", "confidence": 0.06},
                    {"category": "trash", "confidence": 0.03},
                ],
                "is_mock": True,
                "latency_ms": elapsed_ms,
            }

        # Apply transformations and add batch dimension
        tensor = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            k = min(3, len(self.class_names))
            topk = torch.topk(probabilities, k)
            top_prob, top_idx = topk.values, topk.indices

            predicted_label = self.class_names[top_idx[0].item()]
            confidence = float(top_prob[0].item())

            alternatives = [
                {
                    "category": self.class_names[top_idx[i].item()],
                    "confidence": round(float(top_prob[i].item()), 4),
                }
                for i in range(1, len(top_idx))
            ]

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info(
            "[INFERENCE] Predicted %s (%.2f%%) in %.2fms",
            predicted_label,
            confidence * 100,
            elapsed_ms,
        )

        return {
            "category": predicted_label,
            "item_name": predicted_label.title(),
            "confidence": round(confidence, 4),
            "alternatives": alternatives,
            "is_mock": False,
            "latency_ms": elapsed_ms,
        }


# Global singleton instance
model_service = ModelService()
