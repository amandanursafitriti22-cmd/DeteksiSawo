#!/usr/bin/env python3
import shutil
from pathlib import Path
import random

train_dir = Path("dataset/train/images")
valid_dir = Path("dataset/valid/images")
train_labels = Path("dataset/train/labels")
valid_labels = Path("dataset/valid/labels")

# Get all images
images = sorted(list(train_dir.glob("*.jpg")) + list(train_dir.glob("*.png")))
print(f"Total images: {len(images)}")

# Random seed for reproducibility
random.seed(42)
random.shuffle(images)

# Take 9 for validation (20% of 45)
val_images = images[:9]

# Move to valid
for img_path in val_images:
    lbl_path = train_labels / f"{img_path.stem}.txt"
    if img_path.exists():
        shutil.move(str(img_path), str(valid_dir / img_path.name))
        print(f"  Moved image: {img_path.name}")
    if lbl_path.exists():
        shutil.move(str(lbl_path), str(valid_labels / f"{img_path.stem}.txt"))
        print(f"  Moved label: {img_path.stem}.txt")

print(f"\nDone!")
print(f"Train now: {len(list(train_dir.glob('*')))}")
print(f"Valid now: {len(list(valid_dir.glob('*')))}")
