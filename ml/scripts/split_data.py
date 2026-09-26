import argparse
import hashlib
import random
import shutil
import sys
import tempfile
from pathlib import Path

CLASSES = ["paper", "plastic", "glass", "compost", "landfill"]
SPLITS = ["train", "val", "test"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15
SEED = 42
RATIO_TOLERANCE = 0.02


def die(message: str) -> None:
    sys.exit(f"Error: {message}")


def validate_dirs(source_dir: Path, dest_dir: Path) -> None:
    if not source_dir.is_dir():
        die(f"input_dir does not exist or is not a directory: {source_dir}")
    if dest_dir.exists() and not dest_dir.is_dir():
        die(f"output_dir exists and is not a directory: {dest_dir}")
    if dest_dir.resolve() == source_dir.resolve():
        die("output_dir must not be the same as input_dir.")
    if dest_dir.exists() and any((dest_dir / split).exists() for split in SPLITS):
        die(
            f"train/val/test folders already exist in {dest_dir}. "
            "Delete them or choose a new --output_dir."
        )


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def check_for_duplicate_content(class_images: dict[str, list[Path]]) -> None:
    hash_to_locations: dict[str, list[tuple[str, Path]]] = {}
    for class_name, images in class_images.items():
        for f in images:
            hash_to_locations.setdefault(file_hash(f), []).append((class_name, f))

    within_class_dupes = []
    for locations in hash_to_locations.values():
        if len(locations) < 2:
            continue
        classes_involved = {c for c, _ in locations}
        if len(classes_involved) > 1:
            listing = ", ".join(f"{c}/{f.name}" for c, f in locations)
            die(f"identical image content found under different classes: {listing}")
        within_class_dupes.append(locations)

    if within_class_dupes:
        print(
            f"Warning: found {len(within_class_dupes)} set(s) of duplicate images within the same class."
        )
        for locations in within_class_dupes:
            class_name = locations[0][0]
            names = ", ".join(f.name for _, f in locations)
            print(f"  {class_name}: {names}")


def compute_split_counts(total: int, tie_break_priority: list[str]) -> dict[str, int]:
    ideal = {
        "train": total * TRAIN_RATIO,
        "val": total * VAL_RATIO,
        "test": total * TEST_RATIO,
    }
    counts = {split: int(ideal[split]) for split in SPLITS}
    remainder = total - sum(counts.values())
    by_fraction = sorted(
        tie_break_priority, key=lambda s: ideal[s] - counts[s], reverse=True
    )
    for split in by_fraction[:remainder]:
        counts[split] += 1
    return counts


def collect_class_images(source_dir: Path) -> dict[str, list[Path]]:
    class_images: dict[str, list[Path]] = {}
    for class_name in CLASSES:
        class_folder = source_dir / class_name
        if not class_folder.is_dir():
            die(f"class folder not found: {class_folder}")

        images = sorted(
            f
            for f in class_folder.iterdir()
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
        )
        if not images:
            die(f"no images found in {class_folder}")
        class_images[class_name] = images

    return class_images


def create_dataset_splits(source_dir: Path, dest_dir: Path) -> None:
    validate_dirs(source_dir, dest_dir)
    staging_dir = None
    try:
        class_images = collect_class_images(source_dir)
        check_for_duplicate_content(class_images)

        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        staging_dir = Path(
            tempfile.mkdtemp(prefix=f".{dest_dir.name}_staging_", dir=dest_dir.parent)
        )

        rng = random.Random(SEED)
        zero_count_warnings = []

        for idx, (class_name, images) in enumerate(class_images.items()):
            rng.shuffle(images)
            total = len(images)
            priority = SPLITS[idx % len(SPLITS) :] + SPLITS[: idx % len(SPLITS)]
            counts = compute_split_counts(total, priority)

            partitions = {
                "train": images[: counts["train"]],
                "val": images[counts["train"] : counts["train"] + counts["val"]],
                "test": images[counts["train"] + counts["val"] :],
            }

            for split, files in partitions.items():
                if not files:
                    zero_count_warnings.append(f"{class_name}/{split}")
                target_dir = staging_dir / split / class_name
                target_dir.mkdir(parents=True, exist_ok=True)
                for file in files:
                    shutil.copy2(file, target_dir / file.name)

        if zero_count_warnings:
            print(
                f"Warning: these splits ended up with 0 images: {zero_count_warnings}"
            )

        if dest_dir.exists() and any((dest_dir / split).exists() for split in SPLITS):
            die(f"train/val/test folders already exist in {dest_dir}.")

        dest_dir.mkdir(parents=True, exist_ok=True)
        for split in SPLITS:
            staged_split = staging_dir / split
            if staged_split.exists():
                shutil.move(str(staged_split), str(dest_dir / split))

    except (OSError, shutil.Error) as e:
        die(
            f"failed while preparing dataset ({e}). Output may be incomplete: {dest_dir}."
        )
    finally:
        if staging_dir is not None:
            shutil.rmtree(staging_dir, ignore_errors=True)


def print_split_summary(dest_dir: Path) -> None:
    target = dict(zip(SPLITS, (TRAIN_RATIO, VAL_RATIO, TEST_RATIO)))
    print(f"{'class':<10}" + "".join(f"{split:>15}" for split in SPLITS))

    totals = [0] * len(SPLITS)
    ratio_warnings = []
    for class_name in CLASSES:
        counts = [
            sum(1 for f in (dest_dir / split / class_name).glob("*") if f.is_file())
            for split in SPLITS
        ]
        class_total = sum(counts)
        if class_total == 0:
            print(f"{class_name:<10}  (no files found)")
            continue

        print(
            f"{class_name:<10}"
            + "".join(f"{c:>6} ({c / class_total:6.1%})" for c in counts)
        )
        for split, c in zip(SPLITS, counts):
            actual_ratio = c / class_total
            if abs(actual_ratio - target[split]) > RATIO_TOLERANCE:
                ratio_warnings.append(
                    f"  {class_name}/{split}: {actual_ratio:.1%} vs target {target[split]:.0%}"
                )
        totals = [t + c for t, c in zip(totals, counts)]

    grand_total = sum(totals)
    if grand_total:
        print(
            f"{'ALL':<10}" + "".join(f"{c:>6} ({c / grand_total:6.1%})" for c in totals)
        )

    if ratio_warnings:
        print(
            f"\nWarning: some splits deviate from target by more than {RATIO_TOLERANCE:.0%}:"
        )
        print("\n".join(ratio_warnings))


def main():
    parser = argparse.ArgumentParser(
        description="Split a dataset into stratified train/val/test sets (70/15/15, seed=42)."
    )
    parser.add_argument(
        "--input_dir",
        type=Path,
        required=True,
        help="Folder with one sub-folder per class.",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=Path("data/processed"),
        help="Where to write train/val/test (default: data/processed).",
    )
    args = parser.parse_args()

    create_dataset_splits(args.input_dir, args.output_dir)
    print_split_summary(args.output_dir)


if __name__ == "__main__":
    main()
