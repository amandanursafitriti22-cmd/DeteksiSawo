#!/usr/bin/env python3
"""
Convert Label Studio Export ke YOLO Format
Label Studio export biasanya dalam format JSON dengan metadata
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import os


def parse_label_studio_export(json_path: str, image_dir: str, output_label_dir: str):
    """
    Convert Label Studio JSON export ke YOLO format
    
    Label Studio JSON format:
    {
        "id": 1,
        "annotations": [{
            "id": "anno_1",
            "completed_by": 1,
            "result": [{
                "value": {
                    "x": 10,
                    "y": 20,
                    "width": 100,
                    "height": 150,
                    "rotation": 0
                },
                "from_name": "label",
                "to_name": "image",
                "type": "rectanglelabels",
                "labels": {
                    "choices": ["mentah"]  or ["setengah_matang"] or ["matang"]
                }
            }]
        }],
        "data": {
            "image": "/data/upload/1/image_001.jpg",
            "image_name": "image_001.jpg"
        },
        "meta": {}
    }
    """
    
    print(f"📖 Reading Label Studio export: {json_path}")
    
    with open(json_path) as f:
        data = json.load(f)
    
    # Handle both single object and list of objects
    if isinstance(data, dict):
        data = [data]
    
    class_names = ["mentah", "setengah_matang", "matang"]
    converted_count = 0
    
    # Get image info
    image_path = Path(image_dir)
    images_info = {}
    
    # Scan image directory untuk dapat ukuran gambar
    for img_file in image_path.glob("*"):
        if img_file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            try:
                from PIL import Image
                img = Image.open(img_file)
                images_info[img_file.name] = img.size  # (width, height)
                print(f"  ✓ Found image: {img_file.name} ({img.size[0]}x{img.size[1]})")
            except Exception as e:
                print(f"  ⚠️  Could not read {img_file.name}: {e}")
    
    # Process each annotation
    for item in data:
        image_name = item.get("data", {}).get("image_name")
        if not image_name:
            # Try to extract from path
            image_path_str = item.get("data", {}).get("image", "")
            image_name = Path(image_path_str).name
        
        if not image_name:
            print(f"⚠️  Could not find image name for item {item.get('id')}")
            continue
        
        # Get image dimensions
        if image_name not in images_info:
            print(f"⚠️  Image not found in directory: {image_name}")
            continue
        
        image_width, image_height = images_info[image_name]
        
        # Process annotations (bounding boxes)
        yolo_lines = []
        
        annotations = item.get("annotations", [])
        if annotations:
            for annotation in annotations:
                results = annotation.get("result", [])
                
                for result in results:
                    if result.get("type") != "rectanglelabels":
                        continue
                    
                    # Get bounding box coordinates
                    value = result.get("value", {})
                    x = value.get("x")  # 0-100 (percentage)
                    y = value.get("y")
                    w = value.get("width")
                    h = value.get("height")
                    
                    # Get class label
                    labels = result.get("labels", {}).get("choices", [])
                    if not labels:
                        continue
                    
                    class_name_raw = labels[0]
                    class_name = class_name_raw.strip().lower().replace(" ", "_")
                    if class_name == "belum_matang":
                        class_name = "mentah"
                    if class_name not in class_names:
                        print(f"    ⚠️  Unknown class: {class_name_raw}")
                        continue
                    
                    class_id = class_names.index(class_name)
                    
                    # Convert from percentage (0-100) to normalized (0-1)
                    x_center = (x / 100) + (w / 100) / 2
                    y_center = (y / 100) + (h / 100) / 2
                    width_norm = w / 100
                    height_norm = h / 100
                    
                    # Clamp values to [0, 1]
                    x_center = max(0, min(1, x_center))
                    y_center = max(0, min(1, y_center))
                    width_norm = max(0, min(1, width_norm))
                    height_norm = max(0, min(1, height_norm))
                    
                    yolo_lines.append(
                        f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}"
                    )
        
        # Write YOLO label file
        output_dir = Path(output_label_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        label_file = output_dir / f"{Path(image_name).stem}.txt"
        with open(label_file, "w") as f:
            if yolo_lines:
                f.write("\n".join(yolo_lines))
        
        print(f"  ✓ {image_name} → {label_file.name} ({len(yolo_lines)} boxes)")
        converted_count += 1
    
    print(f"\n✅ Converted {converted_count} files!")
    return converted_count


def setup_from_label_studio(label_studio_dir: str, train_dataset_dir: str, val_split: float = 0.2):
    """
    Setup training folder dari Label Studio export
    
    Struktur Label Studio export:
    label_studio_export/
    ├── image/
    │   ├── image_001.jpg
    │   ├── image_002.jpg
    │   └── ...
    ├── label/
    │   ├── image_001.json
    │   ├── image_002.json
    │   └── ...
    ├── export.json (main file dengan semua metadata)
    ├── classes.txt
    └── notes.txt
    """
    
    print("\n" + "="*60)
    print("🏷️  Label Studio → YOLO Training Setup")
    print("="*60)
    
    label_studio_path = Path(label_studio_dir)
    train_dataset_path = Path(train_dataset_dir)
    
    # Find export.json
    export_json = label_studio_path / "export.json"
    if not export_json.exists():
        # Try alternative names
        for json_file in label_studio_path.glob("*.json"):
            export_json = json_file
            break
    
    if not export_json.exists():
        print(f"❌ export.json tidak ditemukan di {label_studio_path}")
        return False
    
    print(f"📖 Found export: {export_json.name}")
    
    # Setup output directories
    train_img_dir = train_dataset_path / "images" / "train"
    val_img_dir = train_dataset_path / "images" / "val"
    train_label_dir = train_dataset_path / "labels" / "train"
    val_label_dir = train_dataset_path / "labels" / "val"
    
    for d in [train_img_dir, val_img_dir, train_label_dir, val_label_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Get all images
    image_dir = label_studio_path / "image"
    if not image_dir.exists():
        print(f"❌ Folder 'image' tidak ditemukan di {label_studio_path}")
        return False
    
    images = sorted([f for f in image_dir.glob("*") if f.suffix.lower() in [".jpg", ".jpeg", ".png"]])
    print(f"📷 Found {len(images)} images")
    
    if not images:
        print(f"❌ Tidak ada gambar di folder {image_dir}")
        return False
    
    # Split train/val
    split_idx = int(len(images) * (1 - val_split))
    train_images = images[:split_idx]
    val_images = images[split_idx:]
    
    print(f"\n📊 Split:")
    print(f"  Training: {len(train_images)} images ({len(train_images)/len(images)*100:.1f}%)")
    print(f"  Validation: {len(val_images)} images ({len(val_images)/len(images)*100:.1f}%)")
    
    # Convert and copy training images
    print(f"\n📁 Converting training set...")
    temp_label_dir = train_dataset_path / "temp_labels_train"
    temp_label_dir.mkdir(exist_ok=True)
    
    parse_label_studio_export(str(export_json), str(image_dir), str(temp_label_dir))
    
    for img_file in train_images:
        # Copy image
        dst_img = train_img_dir / img_file.name
        shutil.copy(img_file, dst_img)
        
        # Copy label
        label_file = temp_label_dir / f"{img_file.stem}.txt"
        if label_file.exists():
            dst_label = train_label_dir / label_file.name
            shutil.copy(label_file, dst_label)
    
    # Convert and copy validation images
    print(f"\n📁 Converting validation set...")
    temp_label_dir_val = train_dataset_path / "temp_labels_val"
    temp_label_dir_val.mkdir(exist_ok=True)
    
    parse_label_studio_export(str(export_json), str(image_dir), str(temp_label_dir_val))
    
    for img_file in val_images:
        # Copy image
        dst_img = val_img_dir / img_file.name
        shutil.copy(img_file, dst_img)
        
        # Copy label
        label_file = temp_label_dir_val / f"{img_file.stem}.txt"
        if label_file.exists():
            dst_label = val_label_dir / label_file.name
            shutil.copy(label_file, dst_label)
    
    # Cleanup temp
    shutil.rmtree(temp_label_dir, ignore_errors=True)
    shutil.rmtree(temp_label_dir_val, ignore_errors=True)
    
    print("\n" + "="*60)
    print("✅ SELESAI!")
    print("="*60)
    print(f"\n📁 Dataset tersimpan di:")
    print(f"  {train_dataset_path}")
    print(f"\n  images/train/  - {len(list(train_img_dir.glob('*')))} training images")
    print(f"  images/val/    - {len(list(val_img_dir.glob('*')))} validation images")
    print(f"  labels/train/  - {len(list(train_label_dir.glob('*.txt')))} training labels")
    print(f"  labels/val/    - {len(list(val_label_dir.glob('*.txt')))} validation labels")
    
    return True


def main():
    print("""
    🏷️  Label Studio Export Converter
    
    Gunakan script ini untuk convert export dari Label Studio ke YOLO format
    
    Usage:
    ======
    
    from convert_label_studio import setup_from_label_studio
    
    # Path ke folder Label Studio export
    label_studio_export = "path/to/label_studio_export"
    
    # Path ke training dataset folder
    train_dataset = "train/dataset"
    
    # Convert!
    setup_from_label_studio(label_studio_export, train_dataset, val_split=0.2)
    
    
    Atau langsung jalankan dengan:
    ======
    
    python convert_label_studio.py
    """)
    
    # Example usage
    try:
        label_studio_dir = input("\n📁 Path ke Label Studio export folder: ").strip()
        train_dataset_dir = input("📁 Path ke training dataset folder: ").strip()
        
        if label_studio_dir and train_dataset_dir:
            setup_from_label_studio(label_studio_dir, train_dataset_dir)
    except KeyboardInterrupt:
        print("\n❌ Cancelled")


if __name__ == "__main__":
    main()
