"""Conservative checks for obvious camera capture failures."""

from typing import Literal

from PIL import Image

RetakeReason = Literal["too_dark", "too_bright", "no_visible_detail"]


def get_retake_reason(image: Image.Image) -> RetakeReason | None:
    """Check a small RGB copy of the decoded and oriented scan image."""
    scale = 96 / max(image.size)
    sample = image
    if scale < 1:
        sample = image.resize(
            (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
            Image.Resampling.BOX,
        )
    luminance = sample.convert("L").histogram()
    almost_all_pixels = sample.width * sample.height * 0.99
    if sum(luminance[:9]) >= almost_all_pixels:
        return "too_dark"
    if sum(luminance[247:]) >= almost_all_pixels:
        return "too_bright"
    if all(high - low <= 8 for low, high in sample.getextrema()):
        return "no_visible_detail"
    return None
