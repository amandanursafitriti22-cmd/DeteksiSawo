#!/usr/bin/env python3
"""
Dataset Preparation Helper untuk YOLOv11 Sawo Training
Bantuan setup dan validasi dataset
"""

import os
import sys
from pathlib import Path
from collections import defaultdict


def create_dummy_labels(dataset_path):
    """Create dummy label files untuk testing (optional)"""
    print("🔧 Creating dummy label files for testing...")
    
    images_train = list((dataset_path / "images" / "train").glob("*"))
    images_val = list((dataset_path / "images" / "val").glob("*"))
    
    # Create dummy labels
    for img in images_train:
        label_file = dataset_path / "labels" / "train" / f"{img.stem}.txt"
        if not label_file.exists():
            with open(label_file, "w") as f:
                f.write("0 0.5 0.5 0.3 0.4\n")  # Class 0, centered
    
    for img in images_val:
        label_file = dataset_path / "labels" / "val" / f"{img.stem}.txt"
        if not label_file.exists():
            with open(label_file, "w") as f:
                f.write("1 0.4 0.6 0.25 0.35\n")  # Class 1, centered
    
    print("✓ Dummy labels created (you should replace with real annotations)")


def analyze_dataset(dataset_path):
    """Analyze dan print dataset statistics"""
    print("\n" + "="*60)
    print("📊 DATASET ANALYSIS")
    print("="*60)
    
    images_train = list((dataset_path / "images" / "train").glob("*"))
    images_val = list((dataset_path / "images" / "val").glob("*"))
    labels_train = list((dataset_path / "labels" / "train").glob("*.txt"))
    labels_val = list((dataset_path / "labels" / "val").glob("*.txt"))
    
    print(f"\n📁 Train Set:")
    print(f"   Images: {len(images_train)}")
    print(f"   Labels: {len(labels_train)}")
    if len(images_train) != len(labels_train):
        print(f"   ⚠️  MISMATCH! {abs(len(images_train) - len(labels_train))} files missing")
    
    print(f"\n📁 Validation Set:")
    print(f"   Images: {len(images_val)}")
    print(f"   Labels: {len(labels_val)}")
    if len(images_val) != len(labels_val):
        print(f"   ⚠️  MISMATCH! {abs(len(images_val) - len(labels_val))} files missing")
    
    total_images = len(images_train) + len(images_val)
    train_ratio = len(images_train) / total_images * 100 if total_images > 0 else 0
    
    print(f"\n📊 Statistics:")
    print(f"   Total Images: {total_images}")
    print(f"   Train Ratio: {train_ratio:.1f}% (Target: 80%)")
    print(f"   Val Ratio: {100-train_ratio:.1f}% (Target: 20%)")
    
    # Analyze classes
    class_count = defaultdict(int)
    for label_file in labels_train + labels_val:
        with open(label_file) as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    class_count[class_id] += 1
    
    class_names = ["mentah", "setengah_matang", "matang"]
    print(f"\n🎯 Class Distribution:")
    for class_id, count in sorted(class_count.items()):
        class_name = class_names[class_id] if class_id < len(class_names) else f"Unknown({class_id})"
        print(f"   {class_id}: {class_name:20} - {count} boxes")
    
    print("\n" + "="*60)
    
    # Validation
    print("\n✓ Recommendations:")
    if total_images < 50:
        print("   ⚠️  Need at least 50 images (currently: {})".format(total_images))
    elif total_images < 200:
        print("   ⚠️  Recommend at least 200 images for good results")
    else:
        print("   ✅ Image count is good!")
    
    if abs(train_ratio - 80) > 5:
        print("   ⚠️  Train/Val ratio is not optimal (Target: 80/20)")
    else:
        print("   ✅ Train/Val ratio is good!")
    
    if len(class_count) < 3:
        print("   ⚠️  Missing classes! Should have 3 classes")
    else:
        print("   ✅ All 3 classes present!")


def show_label_format():
    """Show contoh label format"""
    print("\n" + "="*60)
    print("📝 LABEL FORMAT EXPLANATION")
    print("="*60)
    print("""
Each .txt label file contains one line per bounding box:

Format: <class_id> <x_center> <y_center> <width> <height>

Where:
- class_id:  0 = mentah, 1 = setengah_matang, 2 = matang
- x_center:  X coordinate of box center (0.0 - 1.0, normalized to image width)
- y_center:  Y coordinate of box center (0.0 - 1.0, normalized to image height)
- width:     Width of box (0.0 - 1.0, normalized to image width)
- height:    Height of box (0.0 - 1.0, normalized to image height)

Example file (image_001.txt):
    0 0.5 0.5 0.3 0.4    <- mentah at center
    1 0.7 0.3 0.25 0.35  <- setengah_matang at top-right
    2 0.3 0.7 0.2 0.3    <- matang at bottom-left

Tips:
✓ Use Roboflow.com for easy annotation & export to YOLO format
✓ Or use LabelImg desktop tool
✓ Coordinates must be between 0.0 and 1.0
    """)
    print("="*60)


def main():
    project_root = Path(__file__).parent.parent
    dataset_path = Path(__file__).parent / "dataset"
    
    print("\n" + "="*60)
    print("🍌 YOLOv11 Sawo Training - Dataset Setup Helper")
    print("="*60)
    
    # Show label format
    show_label_format()
    
    # Check dataset
    print("\n🔍 Checking dataset...")
    
    if not dataset_path.exists():
        print("❌ Dataset folder not found!")
        print(f"   Expected: {dataset_path}")
        return
    
    # Analyze
    analyze_dataset(dataset_path)
    
    # Check if empty
    images_train = list((dataset_path / "images" / "train").glob("*"))
    if len(images_train) == 0:
        print("\n💡 Next Steps:")
        print("   1. Place your training images in: train/dataset/images/train/")
        print("   2. Place your validation images in: train/dataset/images/val/")
        print("   3. Place corresponding label files in: train/dataset/labels/train/")
        print("   4. And: train/dataset/labels/val/")
        print("   5. Run this script again to validate")
        
        create_sample = input("\n   Create dummy labels for testing? (y/n): ")
        if create_sample.lower() == "y":
            create_dummy_labels(dataset_path)
    else:
        print("\n✅ Dataset is ready for training!")
        print("   Run: python train_local.py")


if __name__ == "__main__":
    main()
