
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
RATIO_TOLERANCE = 0.02
RATIO_SUM_TOLERANCE = 1e-6
 
 
def die(message: str) -> None:
    sys.exit(f"Error: {message}")
 
 
def validate_ratios(train_ratio: float, val_ratio: float, test_ratio: float) -> None:
    for name, r in (
        ("train_ratio", train_ratio),
        ("val_ratio", val_ratio),
        ("test_ratio", test_ratio),
    ):
        if not (0.0 <= r <= 1.0):
            die(f"{name} must be between 0 and 1, got {r}.")
    total = train_ratio + val_ratio + test_ratio
    if abs(total - 1.0) > RATIO_SUM_TOLERANCE:
        die(f"train_ratio + val_ratio + test_ratio must equal 1.0, got {total}.")
 
 
def validate_dirs(source_dir: Path, dest_dir: Path) -> None:
    if not source_dir.exists():
        die(f"input_dir does not exist: {source_dir}")
    if not source_dir.is_dir():
        die(f"input_dir is not a directory: {source_dir}")
    if dest_dir.exists() and not dest_dir.is_dir():
        die(f"output_dir exists and is not a directory: {dest_dir}")
 
    source_resolved = source_dir.resolve()
    dest_resolved = dest_dir.resolve()
    if dest_resolved == source_resolved or source_resolved in dest_resolved.parents:
        die("output_dir must not be the same as, or nested inside, input_dir.")
    if dest_resolved in source_resolved.parents:
        die("output_dir must not be an ancestor of input_dir.")
 
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
            die(
                f"identical image content found under different classes: {listing}"
            )
        within_class_dupes.append(locations)
 
    if within_class_dupes:
        print(
            f"Warning: found {len(within_class_dupes)} set(s) of duplicate images within the same class. "
        )
        for locations in within_class_dupes:
            class_name = locations[0][0]
            names = ", ".join(f.name for _, f in locations)
            print(f"  {class_name}: {names}")
 
 
def compute_split_counts(
    total: int,
    train_ratio: float,
    val_ratio: float,
    test_ratio: float,
    tie_break_priority: list[str] = SPLITS,
) -> dict[str, int]:
    ideal = {
        "train": total * train_ratio,
        "val": total * val_ratio,
        "test": total * test_ratio,
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
    subfolders_by_lower: dict[str, list[Path]] = {}
    for p in source_dir.iterdir():
        if p.is_dir():
            subfolders_by_lower.setdefault(p.name.lower(), []).append(p)
 
    recognized_lower = {c.lower() for c in CLASSES}
    unexpected = [
        p.name
        for lower, paths in subfolders_by_lower.items()
        if lower not in recognized_lower
        for p in paths
    ]
    if unexpected:
        print(
            f"Note: ignoring unrecognized folder(s) in {source_dir}: {sorted(unexpected)}"
        )
 
    class_images: dict[str, list[Path]] = {}
    for class_name in CLASSES:
        matches = subfolders_by_lower.get(class_name.lower(), [])
        if not matches:
            die(f"class folder not found: {source_dir / class_name}")
        if len(matches) > 1:
            die(
                f"multiple folders match class '{class_name}' case insensitively "
                f"({[p.name for p in matches]}) — rename so only one remains."
            )
        class_folder = matches[0]
        if class_folder.name != class_name:
            print(f"Note: using folder '{class_folder.name}' for class '{class_name}' (case differs).")
 
        entries = list(class_folder.iterdir())
        subdirs = [e for e in entries if e.is_dir()]
        if subdirs:
            print(
                f"Note: {class_folder} contains {len(subdirs)} subdirector"
                f"{'y' if len(subdirs) == 1 else 'ies'} — nested files are ignored "
            )
 
        all_files = [f for f in entries if f.is_file() and not f.name.startswith(".")]
        images = sorted(f for f in all_files if f.suffix.lower() in IMAGE_EXTENSIONS)
        skipped = len(all_files) - len(images)
        if skipped:
            print(f"Note: skipped {skipped} non-image file(s) in {class_folder}")
        seen_lower = {}
        for f in images:
            key = f.name.lower()
            if key in seen_lower:
                die(
                    f"filename collision in {class_folder}: "
                    f"'{seen_lower[key].name}' and '{f.name}' differ only by case."
                )
            seen_lower[key] = f
 
        if not images:
            die(f"no images found in {class_folder}")
        class_images[class_name] = images
 
    return class_images
 
 
def create_dataset_splits(
    source_dir: Path,
    dest_dir: Path,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
    skip_duplicate_check: bool = False,
) -> None:
    validate_ratios(train_ratio, val_ratio, test_ratio)
    validate_dirs(source_dir, dest_dir)
    staging_dir = None
    try:
        class_images = collect_class_images(source_dir)
 
        if not skip_duplicate_check:
            check_for_duplicate_content(class_images)
 
        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        staging_dir = Path(
            tempfile.mkdtemp(prefix=f".{dest_dir.name}_staging_", dir=dest_dir.parent)
        )
 
        rng = random.Random(seed)
        zero_count_warnings = []
 
        for idx, (class_name, images) in enumerate(class_images.items()):
            rng.shuffle(images)
            total = len(images)
            priority = SPLITS[idx % len(SPLITS) :] + SPLITS[: idx % len(SPLITS)]
            counts = compute_split_counts(total, train_ratio, val_ratio, test_ratio, priority)
 
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
            f"failed while preparing/writing dataset ({e}). "
            f"Output may be incomplete: {dest_dir}."
        )
    finally:
        if staging_dir is not None:
            shutil.rmtree(staging_dir, ignore_errors=True)
 
 
def print_split_summary(
    dest_dir: Path,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> None:
    target = dict(zip(SPLITS, (train_ratio, val_ratio, test_ratio)))
    print(f"{'class':<10}" + "".join(f"{split:>15}" for split in SPLITS))
 
    totals = [0] * len(SPLITS)
    ratio_warnings = []
    for class_name in CLASSES:
        counts = [
            sum(
                1
                for f in (dest_dir / split / class_name).glob("*")
                if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
            )
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
        description="Split a dataset into stratified train/val/test sets (70/15/15)."
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
        required=True,
        help="Where to write train/val/test.",
    )
    parser.add_argument("--train_ratio", type=float, default=0.70)
    parser.add_argument("--val_ratio", type=float, default=0.15)
    parser.add_argument("--test_ratio", type=float, default=0.15)
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible shuffling (default: 42).",
    )
    parser.add_argument(
        "--skip_duplicate_check",
        action="store_true",
        help="Skip hashing images to detect duplicate/conflicting content ",
    )
    args = parser.parse_args()
 
    create_dataset_splits(
        args.input_dir,
        args.output_dir,
        train_ratio=args.train_ratio,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        seed=args.seed,
        skip_duplicate_check=args.skip_duplicate_check,
    )
    print_split_summary(
        args.output_dir, args.train_ratio, args.val_ratio, args.test_ratio
    )
 
 
if __name__ == "__main__":
    main()