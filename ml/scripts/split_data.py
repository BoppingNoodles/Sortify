import argparse
import random
import shutil
import sys
from pathlib import Path

CLASSES = ["paper", "plastic", "glass", "compost", "landfill"]
SPLITS = ["train", "val", "test"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
RATIO_TOLERANCE = 0.02


def die(message: str) -> None:
    sys.exit(f"Error: {message}")


def collect_class_images(source_dir: Path) -> dict[str, list[Path]]:
    if not source_dir.is_dir():
        die(f"input directory not found: {source_dir}")

    class_images = {}
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


def compute_split_counts(
    total: int, tie_break_priority: list[str], ratios: dict[str, float]
) -> dict[str, int]:
    ideal = {split: total * ratios[split] for split in SPLITS}
    counts = {split: int(ideal[split]) for split in SPLITS}
    remainder = total - sum(counts.values())
    by_fraction = sorted(
        tie_break_priority, key=lambda s: ideal[s] - counts[s], reverse=True
    )
    for split in by_fraction[:remainder]:
        counts[split] += 1
    return counts


def create_dataset_splits(
    source_dir: Path,
    dest_dir: Path,
    ratios: dict[str, float],
    seed: int,
    overwrite: bool = False,
) -> None:
    if dest_dir.exists() and any((dest_dir / split).exists() for split in SPLITS):
        if not overwrite:
            die(
                f"train/val/test folders already exist in {dest_dir}. "
                "Use --overwrite to replace them."
            )
        for split in SPLITS:
            split_path = dest_dir / split
            if split_path.exists():
                shutil.rmtree(split_path)

    class_images = collect_class_images(source_dir)
    rng = random.Random(seed)

    for idx, (class_name, images) in enumerate(class_images.items()):
        rng.shuffle(images)
        total = len(images)
        # Rotate which split gets the leftover file(s) so rounding doesn'
        # always favor the same split across every class.
        priority = SPLITS[idx % len(SPLITS) :] + SPLITS[: idx % len(SPLITS)]
        counts = compute_split_counts(total, priority, ratios)

        partitions = {
            "train": images[: counts["train"]],
            "val": images[counts["train"] : counts["train"] + counts["val"]],
            "test": images[counts["train"] + counts["val"] :],
        }

        for split, files in partitions.items():
            if not files:
                print(
                    f"Warning: '{class_name}' ended up with 0 images in the '{split}' split."
                )
                continue
            target_dir = dest_dir / split / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
            for file in files:
                shutil.copy2(file, target_dir / file.name)


def print_split_summary(dest_dir: Path, ratios: dict[str, float]) -> None:
    print(f"{'class':<10}" + "".join(f"{split:>15}" for split in SPLITS))

    ratio_warnings = []
    totals = [0] * len(SPLITS)
    for class_name in CLASSES:
        counts = [
            sum(
                1
                for f in (dest_dir / split / class_name).glob("*")
                if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
            )
            for split in SPLITS
        ]
        totals = [t + c for t, c in zip(totals, counts)]
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
            if abs(actual_ratio - ratios[split]) > RATIO_TOLERANCE:
                ratio_warnings.append(
                    f"  {class_name}/{split}: {actual_ratio:.1%} vs target {ratios[split]:.0%}"
                )

    grand_total = sum(totals)
    if grand_total > 0:
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
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing split folders."
    )
    parser.add_argument(
        "--train_ratio",
        type=float,
        default=0.70,
        help="Train split ratio (default: 0.70)",
    )
    parser.add_argument(
        "--val_ratio", type=float, default=0.15, help="Val split ratio (default: 0.15)"
    )
    parser.add_argument(
        "--test_ratio",
        type=float,
        default=0.15,
        help="Test split ratio (default: 0.15)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Seed for reproducibility (default: 42)"
    )
    args = parser.parse_args()

    ratios = {
        "train": args.train_ratio,
        "val": args.val_ratio,
        "test": args.test_ratio,
    }
    create_dataset_splits(
        args.input_dir, args.output_dir, ratios, args.seed, overwrite=args.overwrite
    )
    print_split_summary(args.output_dir, ratios)


if __name__ == "__main__":
    main()
