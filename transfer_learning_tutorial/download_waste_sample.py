"""Download a small, label-filtered image sample from a Hugging Face dataset.

Source: https://huggingface.co/datasets/rootstrap-org/waste-classifier
It has 7 labels; Sortify uses 5 of them (cardboard and metal are dropped).

The dataset ships as a single 1.15 GB zip, so we do NOT download the whole thing.
`HfFileSystem` gives us a seekable file object over HTTPS, which lets `zipfile`
read only the archive's central directory (a few hundred KB) and then pull out
just the members we picked, one HTTP range request each. Grabbing 50 images
transfers ~50 images' worth of bytes, not 1.15 GB.

Output is an ImageFolder tree that `torchvision.datasets.ImageFolder` reads
directly, under `data/` (gitignored):

    data/waste_sample/
        train/compost/compost_000.jpg
        train/glass/...
        val/compost/...

Usage:

    python download_waste_sample.py                       # 10 train + 5 val per class
    python download_waste_sample.py --per-class 50        # 50 train per class
    python download_waste_sample.py --labels glass paper  # just two labels
    python download_waste_sample.py --list                # show what's available
"""

from __future__ import annotations

import argparse
import io
import random
import shutil
import zipfile
from collections import defaultdict
from pathlib import Path

from huggingface_hub import HfFileSystem
from PIL import Image

DATASET_ID = "rootstrap-org/waste-classifier"
ZIP_PATH = f"datasets/{DATASET_ID}/dataset-splits-custom.zip"

# The 5 of the dataset's 7 labels that map onto Sortify's bins.
WANTED_LABELS = ["compost", "glass", "paper", "plastic", "trash"]

# Inside the zip, paths look like dataset_splits/<split>/<label>/<file>.
# The dataset's "test" split becomes our "val" folder.
SPLIT_MAP = {"train": "train", "test": "val"}

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "data" / "waste_sample"


def index_archive(zf: zipfile.ZipFile) -> dict[tuple[str, str], list[str]]:
    """Group the archive's member names by (split, label) from their paths."""
    members: dict[tuple[str, str], list[str]] = defaultdict(list)
    for name in zf.namelist():
        if name.endswith("/"):
            continue
        parts = name.split("/")
        if len(parts) < 4:
            continue
        _root, split, label, _filename = parts[0], parts[1], parts[2], parts[3]
        if split in SPLIT_MAP:
            members[(SPLIT_MAP[split], label)].append(name)
    return members


def _save_member(zf: zipfile.ZipFile, name: str, dest: Path, max_size: int) -> bool:
    """Extract one member, convert to RGB JPEG, and save. False if unreadable.

    The dataset mixes .jpg/.png/.gif/.webp and a couple of broken files, so a
    failure here is expected and we just move on to the next candidate.
    """
    try:
        raw = zf.read(name)
        image = Image.open(io.BytesIO(raw)).convert("RGB")
        if max_size:
            image.thumbnail((max_size, max_size))
        image.save(dest, "JPEG", quality=90)
        return True
    except Exception as exc:  # noqa: BLE001 - any decode failure is a skip
        print(f"    skipped {name}: {type(exc).__name__}")
        return False


def download_sample(
    out_dir: Path = DEFAULT_OUT_DIR,
    labels: list[str] | None = None,
    per_class: int = 10,
    val_per_class: int = 5,
    max_size: int = 512,
    seed: int = 42,
    clean: bool = True,
) -> dict[str, dict[str, int]]:
    """Write `per_class` train and `val_per_class` val images for each label.

    Returns {split: {label: count}} of what was actually saved.
    """
    labels = labels or WANTED_LABELS
    quotas = {"train": per_class, "val": val_per_class}
    rng = random.Random(seed)

    if clean and out_dir.exists():
        shutil.rmtree(out_dir)

    saved: dict[str, dict[str, int]] = {split: {} for split in quotas}

    fs = HfFileSystem()
    print(f"Opening {DATASET_ID} archive (reading index only)...")
    with fs.open(ZIP_PATH) as raw:
        zf = zipfile.ZipFile(raw)
        members = index_archive(zf)

        available = sorted({label for _split, label in members})
        unknown = [label for label in labels if label not in available]
        if unknown:
            raise ValueError(f"Unknown label(s) {unknown}. Available: {available}")

        for split, quota in quotas.items():
            if quota <= 0:
                continue
            for label in labels:
                pool = list(members[(split, label)])
                rng.shuffle(pool)

                dest_dir = out_dir / split / label
                dest_dir.mkdir(parents=True, exist_ok=True)

                count = 0
                for name in pool:
                    if count >= quota:
                        break
                    dest = dest_dir / f"{label}_{count:03d}.jpg"
                    if _save_member(zf, name, dest, max_size):
                        count += 1

                saved[split][label] = count
                print(f"  {split:<5} {label:<9} {count}/{quota}")

    print(f"\nSaved to {out_dir}")
    for split in quotas:
        if saved[split]:
            print(f"  {split}: {sum(saved[split].values())} images")

    short = [
        f"{split}/{label}"
        for split, quota in quotas.items()
        for label in labels
        if quota > 0 and saved[split].get(label, 0) < quota
    ]
    if short:
        print(f"\nWarning: quota not met for {short}")

    return saved


def list_available() -> None:
    """Print how many images each label has, per split, without downloading."""
    fs = HfFileSystem()
    with fs.open(ZIP_PATH) as raw:
        members = index_archive(zipfile.ZipFile(raw))

    labels = sorted({label for _split, label in members})
    print(f"{'label':<12}{'train':>8}{'val':>8}   (val = the dataset's test split)")
    for label in labels:
        marker = "" if label in WANTED_LABELS else "   (unused)"
        train_n = len(members.get(("train", label), []))
        val_n = len(members.get(("val", label), []))
        print(f"{label:<12}{train_n:>8}{val_n:>8}{marker}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list",
        action="store_true",
        help="Show available labels and counts, then exit.",
    )
    parser.add_argument(
        "--per-class",
        type=int,
        default=10,
        help="Train images per label (default: 10).",
    )
    parser.add_argument(
        "--val-per-class",
        type=int,
        default=5,
        help="Val images per label (default: 5).",
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        default=None,
        help=f"Labels to fetch (default: {' '.join(WANTED_LABELS)}).",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Output ImageFolder root."
    )
    parser.add_argument(
        "--max-size", type=int, default=512, help="Longest side in px, 0 to keep full."
    )
    parser.add_argument("--seed", type=int, default=42, help="Sampling seed.")
    parser.add_argument(
        "--keep-existing", action="store_true", help="Do not wipe out-dir first."
    )
    args = parser.parse_args()

    if args.list:
        list_available()
        return

    download_sample(
        out_dir=args.out_dir,
        labels=args.labels,
        per_class=args.per_class,
        val_per_class=args.val_per_class,
        max_size=args.max_size,
        seed=args.seed,
        clean=not args.keep_existing,
    )


if __name__ == "__main__":
    main()
