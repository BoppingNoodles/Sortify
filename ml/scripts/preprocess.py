"""
Week 2 — turn messy photos into the exact pictures ResNet expects.

ResNet-18 was trained on square, 3-color (RGB), 224×224 images. Real datasets
are not like that: some files are broken, some are grayscale (1 channel), some
have transparency (4 channels), phone cameras store rotation in EXIF, and
sizes vary. This script:

    1. Rejects files Pillow cannot fully decode (Image.verify + reload).
    2. Applies the EXIF orientation tag so phone photos are upright.
    3. Composites transparent pixels onto white, then converts to RGB.
    4. Resizes it to exactly 224×224 with bilinear interpolation.
    5. Writes a JPEG copy. Originals are left untouched.

Normalization (ImageNet mean/std) is NOT baked into the saved files. That step
happens later, in memory, when the training loop turns pixels into tensors.
Saving already-normalized numbers as JPEGs would wreck them.

Run from the repo root, with the venv activated:

    python ml/scripts/preprocess.py --input data/raw --output data/preprocessed
    python ml/scripts/preprocess.py --demo
"""

from __future__ import annotations

import argparse
import logging
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
from torchvision.transforms import InterpolationMode
from torchvision.transforms.functional import resize as tv_resize

TARGET_SIZE = (224, 224)
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".gif"}

logger = logging.getLogger("preprocess")


def image_is_intact(path: Path) -> bool:
    """Return False when the file is truncated, empty, or not a real image.

    verify() only checks the file structure. Pillow then requires a second open
    before the pixels can be read, so a file that fails either step is skipped.
    """
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        logger.warning("Skipping %s — unreadable image (%s)", path, exc)
        return False
    return True


def _to_rgb(image: Image.Image) -> Image.Image:
    """Orient from EXIF, then composite transparency onto white.

    ``convert("RGB")`` turns transparent pixels black. Phone photos also
    store rotation in an EXIF tag that Pillow does not apply on open.
    """
    oriented = ImageOps.exif_transpose(image)
    if oriented.mode in ("RGBA", "LA") or (
        oriented.mode == "P" and "transparency" in oriented.info
    ):
        background = Image.new("RGB", oriented.size, (255, 255, 255))
        alpha = oriented.convert("RGBA").split()[-1]
        background.paste(oriented, mask=alpha)
        return background
    return oriented.convert("RGB")


def preprocess_image(source: Path, destination: Path) -> None:
    """Convert one intact image to a 224×224 RGB JPEG."""
    with Image.open(source) as image:
        rgb = _to_rgb(image)
        # Week 2 stretches to a square. Week 3 should letterbox or
        # Resize(256) + CenterCrop(224) so rectangular items keep their shape.
        resized = tv_resize(
            rgb,
            list(TARGET_SIZE),
            interpolation=InterpolationMode.BILINEAR,
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    resized.save(destination, format="JPEG", quality=95)


def preprocess_directory(input_dir: Path, output_dir: Path) -> tuple[int, int]:
    """Copy a cleaned 224×224 RGB version of every image under input_dir.

    Class folders are preserved, so data/raw/compost/a.png becomes
    data/preprocessed/compost/a.jpg. Returns (written_count, skipped_count).
    """
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    written = 0
    skipped = 0
    for source in sorted(input_dir.rglob("*")):
        if not source.is_file() or source.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        relative = source.relative_to(input_dir)
        destination = (output_dir / relative).with_suffix(".jpg")
        if not image_is_intact(source):
            skipped += 1
            continue
        preprocess_image(source, destination)
        written += 1
        logger.info("Wrote %s", destination)

    logger.info("Done. Wrote %s images, skipped %s.", written, skipped)
    return written, skipped


def output_shapes_are_resnet_ready(output_dir: Path) -> bool:
    """Every saved file must be (height=224, width=224, channels=3)."""
    paths = sorted(output_dir.rglob("*.jpg"))
    if not paths:
        logger.warning("No output images found in %s", output_dir)
        return False
    for path in paths:
        with Image.open(path) as image:
            image.load()
            array = np.asarray(image)
        if array.shape != (224, 224, 3):
            logger.warning("%s has shape %s, expected (224, 224, 3)", path, array.shape)
            return False
    return True


def _write_sample_image(path: Path, mode: str, seed: int) -> None:
    color = ((seed * 40) % 256, (seed * 70) % 256, (seed * 15) % 256)
    if mode == "L":
        image = Image.new("L", (320 + seed % 40, 180 + seed % 30), color=color[0])
    elif mode == "RGBA":
        image = Image.new("RGBA", (100, 400), color=(*color, 180))
    else:
        image = Image.new("RGB", (640, 480), color=color)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def run_demo() -> None:
    """Build 100 mixed images plus 1 broken file, then check the outputs."""
    modes = ("RGB", "L", "RGBA")
    with (
        tempfile.TemporaryDirectory() as raw_name,
        tempfile.TemporaryDirectory() as out_name,
    ):
        raw_dir = Path(raw_name)
        out_dir = Path(out_name)
        for index in range(100):
            class_name = ("paper", "plastic", "glass", "compost", "landfill")[index % 5]
            mode = modes[index % len(modes)]
            suffix = ".png" if mode != "RGB" else ".jpg"
            _write_sample_image(
                raw_dir / class_name / f"sample_{index:03d}{suffix}", mode, index
            )

        broken = raw_dir / "landfill" / "truncated.jpg"
        broken.write_bytes(b"\xff\xd8\xff\xd9not-a-real-jpeg")

        written, skipped = preprocess_directory(raw_dir, out_dir)
        ready = output_shapes_are_resnet_ready(out_dir)
        print(f"Demo wrote {written} images, skipped {skipped}.")
        print(f"All outputs are (224, 224, 3): {ready}")
        if written != 100 or skipped != 1 or not ready:
            raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resize and convert images to 224x224 RGB."
    )
    parser.add_argument(
        "--input", type=Path, help="Folder of raw images (class subfolders optional)."
    )
    parser.add_argument("--output", type=Path, help="Where to write cleaned JPEGs.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Preprocess 100 synthetic images of mixed types and check their shapes.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if args.demo:
        run_demo()
        return
    if args.input is None or args.output is None:
        parser.error("Pass --input and --output, or use --demo.")
    preprocess_directory(args.input, args.output)


if __name__ == "__main__":
    main()
