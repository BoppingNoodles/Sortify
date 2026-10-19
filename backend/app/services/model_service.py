# TEMPORARY LOCAL STAND-IN. DO NOT COMMIT.
# Someone else's task is to create this file.
# I just created this file to test my Week 4 task.
# Someone else must own the real file.

import io

from PIL import Image


class ModelService:
    def predict(self, image_bytes: bytes) -> dict:
        # Opening the image makes a corrupted file raise, like the real model would
        Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return {"category": "plastic", "confidence": 0.94}


model_service = ModelService()
