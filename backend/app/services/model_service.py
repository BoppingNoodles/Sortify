"""Model inference service for Sortify."""

import io
import logging
from pathlib import Path
from typing import Any

import torch
from PIL import Image, ImageOps, UnidentifiedImageError
from PIL.Image import DecompressionBombError
from torchvision import transforms

from backend.app.core.config import DEFAULT_MODEL_PATH, settings

__all__ = ["DEFAULT_CLASSES", "DEFAULT_MODEL_PATH", "ModelService", "model_service"]

# Cap maximum decompression pixels to 25 million (~5000x5000) to protect against memory exhaustion
Image.MAX_IMAGE_PIXELS = 25_000_000

IMAGE_DECODE_ERRORS = (
    UnidentifiedImageError,
    OSError,
    ValueError,
    SyntaxError,
    DecompressionBombError,
)

logger = logging.getLogger(__name__)

# Canonical raw model classes (5-class baseline)
DEFAULT_CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]


class ModelService:
    """Loads PyTorch model singleton and runs image inference."""

    def __init__(
        self,
        model_path: Path | str | None = None,
        class_names: list[str] | None = None,
    ):
        resolved_path = model_path if model_path is not None else settings.MODEL_PATH
        self.model_path = Path(resolved_path)
        if not self.model_path.is_absolute():
            self.model_path = Path(__file__).resolve().parents[3] / self.model_path

        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
            else "cpu"
        )
        self.model: torch.nn.Module | None = None
        self.class_names = class_names or list(DEFAULT_CLASSES)

        # Standard torchvision preprocessing pipeline
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        self._load_model()

    def _load_model(self) -> None:
        """Loads weights into eval mode if file exists, else sets fallback mode."""
        if self.model_path.exists():
            try:
                from torchvision import models

                checkpoint = torch.load(self.model_path, map_location=self.device)
                if isinstance(checkpoint, dict) and "class_names" in checkpoint:
                    if not isinstance(checkpoint["class_names"], (list, tuple)):
                        raise ValueError("Checkpoint class_names must be a sequence")
                    self.class_names = list(checkpoint["class_names"])

                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    state_dict = checkpoint["model_state_dict"]
                elif isinstance(checkpoint, dict) and "state_dict" in checkpoint:
                    state_dict = checkpoint["state_dict"]
                elif isinstance(checkpoint, dict):
                    state_dict = checkpoint
                else:
                    state_dict = checkpoint.state_dict()

                # Infer classification head dimension dynamically from state_dict
                if "classifier.1.weight" in state_dict:
                    num_classes = state_dict["classifier.1.weight"].shape[0]
                else:
                    num_classes = len(self.class_names)

                if (
                    num_classes != len(self.class_names)
                    or any(
                        not isinstance(name, str) or not name.strip()
                        for name in self.class_names
                    )
                    or len(set(self.class_names)) != num_classes
                ):
                    raise ValueError(
                        "Checkpoint labels must match the classifier outputs"
                    )

                model = models.mobilenet_v2(weights=None)
                model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)
                model.load_state_dict(state_dict)
                model.to(self.device)
                model.eval()
                self.model = model
                logger.info(
                    "Loaded model weights from %s on %s", self.model_path, self.device
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
            dict containing predicted category, confidence, and alternatives.
        """
        # Validate that image bytes can be decoded and preprocessed
        try:
            with Image.open(io.BytesIO(image_bytes)) as raw_img:
                if raw_img.width <= 0 or raw_img.height <= 0:
                    raise ValueError(f"Invalid image dimensions: {raw_img.size}")
                if raw_img.width > 8192 or raw_img.height > 8192:
                    raise ValueError(
                        f"Image dimensions {raw_img.size} exceed maximum permitted size 8192x8192."
                    )

                try:
                    img = ImageOps.exif_transpose(raw_img)
                except (TypeError, ValueError, OSError):
                    img = raw_img

                img = img.convert("RGB")
                tensor = self.transform(img).unsqueeze(0).to(self.device)
        except IMAGE_DECODE_ERRORS as exc:
            logger.warning("Failed to decode image payload: %s", exc)
            raise

        if self.model is None:
            # Fallback prediction if weights file is not yet deployed
            return {
                "category": "compost",
                "item_name": "Almond Milk Carton (Scaffold)",
                "confidence": 0.91,
                "alternatives": [
                    {"category": "paper", "confidence": 0.06},
                    {"category": "landfill", "confidence": 0.03},
                ],
                "is_mock": True,
            }

        try:
            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
                if probabilities.shape[0] != len(self.class_names):
                    raise RuntimeError("Model outputs do not match checkpoint labels")
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
        except (RuntimeError, MemoryError) as exc:
            del tensor
            if self.device.type == "cuda" and torch.cuda.is_available():
                torch.cuda.empty_cache()
            elif self.device.type == "mps" and hasattr(torch, "mps"):
                torch.mps.empty_cache()
            logger.error("Model forward pass failed on %s: %s", self.device, exc)
            raise

        return {
            "category": predicted_label,
            "item_name": predicted_label.title(),
            "confidence": round(confidence, 4),
            "alternatives": alternatives,
            "is_mock": False,
        }


# Global singleton instance configured from settings
model_service = ModelService()
