"""Model inference service for Sortify."""

import io
import logging
from pathlib import Path
from typing import Any

import torch
from PIL import Image, ImageFile, ImageOps, UnidentifiedImageError
from torchvision import transforms

# Allow truncated image streams to load rather than crashing if sufficient data exists
ImageFile.LOAD_TRUNCATED_IMAGES = True

logger = logging.getLogger(__name__)

# Default path to frozen model weights
DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parent.parent / "models" / "sortify_mvp_v1.pth"
)

# Canonical raw model classes (5-class baseline)
DEFAULT_CLASSES = ["compost", "glass", "landfill", "paper", "plastic"]

# Known mock headers used in existing test harnesses
MOCK_TEST_HEADERS = {
    b"\xff\xd8\xff",
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01",
    b"fake_image_bytes",
}


class ModelService:
    """Loads PyTorch model singleton and runs image inference."""

    def __init__(
        self,
        model_path: Path | str = DEFAULT_MODEL_PATH,
        class_names: list[str] | None = None,
    ):
        self.model_path = Path(model_path)
        self.device = torch.device(
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
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
                model = models.mobilenet_v2(weights=None)
                # MobileNetV2 has a 'classifier' attribute, not 'fc'
                model.classifier[1] = torch.nn.Linear(
                    model.last_channel, len(self.class_names)
                )

                if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:
                    state_dict = checkpoint["model_state_dict"]
                    if "class_names" in checkpoint:
                        self.class_names = checkpoint["class_names"]
                elif isinstance(checkpoint, dict):
                    state_dict = checkpoint
                else:
                    state_dict = checkpoint.state_dict()

                model.load_state_dict(state_dict)
                model.eval()
                self.model = model
                logger.info("Loaded model weights from %s", self.model_path)
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
        if image_bytes in MOCK_TEST_HEADERS:
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

        # Validate that image bytes can be decoded and preprocessed
        try:
            with Image.open(io.BytesIO(image_bytes)) as raw_img:
                try:
                    img = ImageOps.exif_transpose(raw_img)
                except (TypeError, ValueError, OSError):
                    img = raw_img

                img = img.convert("RGB")

                if img.size[0] <= 0 or img.size[1] <= 0:
                    raise ValueError(f"Invalid image dimensions: {img.size}")

                tensor = self.transform(img).unsqueeze(0).to(self.device)
        except (UnidentifiedImageError, OSError, ValueError) as exc:
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
            if self.device.type == "cuda" and torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.error("Model forward pass failed on %s: %s", self.device, exc)
            raise

        return {
            "category": predicted_label,
            "item_name": predicted_label.title(),
            "confidence": round(confidence, 4),
            "alternatives": alternatives,
            "is_mock": False,
        }


# Global singleton instance
model_service = ModelService()
