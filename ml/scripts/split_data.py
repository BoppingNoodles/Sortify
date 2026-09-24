import argparse
import random
import shutil
import sys
from pathlib import Path

CLASSES = ["paper", "plastic", "glass", "compost", "landfill"]
SPLITS = ["train", "val", "test"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def create_dataset_splits(
    source_dir: Path,
    dest_dir: Path,
    train_ratio=0.70,
    val_ratio=0.15,
    test_ratio=0.15,
    seed=42,
):
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-9:
        sys.exit("Error: train, val and test ratios must add up to 1.")
    class_images = {}
    for class_name in CLASSES:
        class_folder = source_dir / class_name
        if not class_folder.is_dir():
            sys.exit(f"Error: class folder not found: {class_folder}")
        images = sorted(
            f for f in class_folder.iterdir()
            if f.is_file()
            and f.suffix.lower() in IMAGE_EXTENSIONS
            and not f.name.startswith(".") 
        )
        if not images:
            sys.exit(f"Error: no images found in {class_folder}")
        class_images[class_name] = images

    if any((dest_dir / split).exists() for split in SPLITS):
        sys.exit(f"Error: train/val/test folders already exist in {dest_dir}. "
                 "Delete them or choose a new --output_dir.")
    rng = random.Random(seed)
    for class_name, images in class_images.items():
        rng.shuffle(images)
        total = len(images)
        train_count = round(total * train_ratio)
        val_count = round(total * val_ratio)
        partitions = {
            "train": images[:train_count],
            "val": images[train_count:train_count + val_count],
            "test": images[train_count + val_count:],
        }

        for split, files in partitions.items():
            target_dir = dest_dir / split / class_name
            target_dir.mkdir(parents=True, exist_ok=True)
            for file in files:
                shutil.copy2(file, target_dir / file.name)

 
def print_split_summary(dest_dir: Path):
    """Count the files that actually landed on disk and print the split."""
    print(f"{'class':<10}" + "".join(f"{split:>15}" for split in SPLITS))
    totals = [0] * len(SPLITS)
    for class_name in CLASSES:
        counts = [len(list((dest_dir / split / class_name).iterdir()))
                  for split in SPLITS]
        class_total = sum(counts)
        print(f"{class_name:<10}"
              + "".join(f"{c:>6} ({c / class_total:6.1%})" for c in counts))
        totals = [t + c for t, c in zip(totals, counts)]
    grand_total = sum(totals)
    print(f"{'ALL':<10}"
          + "".join(f"{c:>6} ({c / grand_total:6.1%})" for c in totals))

def main():
    parser = argparse.ArgumentParser(
        description="Split a dataset into stratified train/val/test sets (70/15/15)."
    )
    parser.add_argument("--input_dir", type=Path, required=True,
                        help="Folder with one sub-folder per class.")
    parser.add_argument("--output_dir", type=Path, required=True,
                        help="Where to write train/val/test (e.g. data/processed).")
    args = parser.parse_args()
 
    create_dataset_splits(args.input_dir, args.output_dir)
    print_split_summary(args.output_dir)
 
 
if __name__ == "__main__":
    main()





