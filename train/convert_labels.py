#!/usr/bin/env python3
"""
Convert bounding box formats to YOLO format
Mendukung: Pascal VOC (XML), COCO JSON, CSV, dll
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
import csv
from typing import Tuple, List


def pascal_voc_to_yolo(xml_path: str, image_width: int, image_height: int) -> List[str]:
    """
    Convert Pascal VOC (XML) format to YOLO format
    
    XML Example:
    <annotation>
        <size>
            <width>640</width>
            <height>480</height>
        </size>
        <object>
            <name>mentah</name>
            <bndbox>
                <xmin>100</xmin>
                <ymin>100</ymin>
                <xmax>300</xmax>
                <ymax>300</ymax>
            </bndbox>
        </object>
    </annotation>
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    class_names = ["mentah", "setengah_matang", "matang"]
    yolo_lines = []
    
    for obj in root.findall("object"):
        class_name_raw = obj.find("name").text
        class_name = class_name_raw.strip().lower().replace(" ", "_")
        if class_name == "belum_matang":
            class_name = "mentah"
        if class_name not in class_names:
            continue
        
        class_id = class_names.index(class_name)
        bndbox = obj.find("bndbox")
        
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        
        # Convert to YOLO format (normalized center coordinates)
        x_center = (xmin + xmax) / 2 / image_width
        y_center = (ymin + ymax) / 2 / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height
        
        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    return yolo_lines


def coco_to_yolo(coco_json_path: str, image_width: int, image_height: int, image_id: int) -> List[str]:
    """
    Convert COCO JSON format to YOLO format
    
    COCO Format:
    {
        "categories": [
            {"id": 0, "name": "mentah"},
            {"id": 1, "name": "setengah_matang"},
            {"id": 2, "name": "matang"}
        ],
        "annotations": [
            {
                "image_id": 1,
                "category_id": 0,
                "bbox": [x, y, width, height]  // x, y = top-left corner
            }
        ]
    }
    """
    with open(coco_json_path) as f:
        coco_data = json.load(f)
    
    yolo_lines = []
    
    # Get image annotations
    for ann in coco_data.get("annotations", []):
        if ann["image_id"] != image_id:
            continue
        
        category_id = ann["category_id"]
        x, y, w, h = ann["bbox"]
        
        # Convert to YOLO format (center, normalized)
        x_center = (x + w / 2) / image_width
        y_center = (y + h / 2) / image_height
        width = w / image_width
        height = h / image_height
        
        yolo_lines.append(f"{category_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    return yolo_lines


def csv_to_yolo(csv_path: str, image_width: int, image_height: int, image_name: str) -> List[str]:
    """
    Convert CSV format to YOLO format
    
    CSV Format:
    image_name,class_name,xmin,ymin,xmax,ymax
    image_001.jpg,mentah,100,100,300,300
    image_001.jpg,setengah_matang,400,150,500,250
    """
    class_names = ["mentah", "setengah_matang", "matang"]
    yolo_lines = []
    
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["image_name"] != image_name:
                continue
            
            class_name_raw = row["class_name"]
            class_name = class_name_raw.strip().lower().replace(" ", "_")
            if class_name == "belum_matang":
                class_name = "mentah"
            if class_name not in class_names:
                continue
            
            class_id = class_names.index(class_name)
            xmin = int(row["xmin"])
            ymin = int(row["ymin"])
            xmax = int(row["xmax"])
            ymax = int(row["ymax"])
            
            # Convert to YOLO
            x_center = (xmin + xmax) / 2 / image_width
            y_center = (ymin + ymax) / 2 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height
            
            yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    return yolo_lines


def batch_convert(input_dir: str, output_dir: str, format_type: str, **kwargs):
    """
    Batch convert multiple files
    
    Args:
        input_dir: Folder containing annotation files
        output_dir: Output folder for YOLO labels
        format_type: "pascal_voc", "coco", or "csv"
        **kwargs: Additional parameters (image_width, image_height, etc)
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🔄 Converting from {format_type} to YOLO format...")
    
    if format_type == "pascal_voc":
        xml_files = list(input_path.glob("*.xml"))
        image_width = kwargs.get("image_width", 640)
        image_height = kwargs.get("image_height", 640)
        
        for xml_file in xml_files:
            yolo_lines = pascal_voc_to_yolo(str(xml_file), image_width, image_height)
            
            output_file = output_path / f"{xml_file.stem}.txt"
            with open(output_file, "w") as f:
                f.write("\n".join(yolo_lines))
            
            print(f"✓ {xml_file.name} → {output_file.name}")
    
    elif format_type == "coco":
        coco_json = kwargs.get("coco_json")
        image_mapping = kwargs.get("image_mapping", {})  # {image_id: (filename, width, height)}
        
        if not coco_json:
            print("❌ coco_json parameter required!")
            return
        
        for image_id, (filename, width, height) in image_mapping.items():
            yolo_lines = coco_to_yolo(coco_json, width, height, image_id)
            
            output_file = output_path / f"{Path(filename).stem}.txt"
            with open(output_file, "w") as f:
                f.write("\n".join(yolo_lines))
            
            print(f"✓ Image ID {image_id} → {output_file.name}")
    
    elif format_type == "csv":
        csv_file = kwargs.get("csv_file")
        image_width = kwargs.get("image_width", 640)
        image_height = kwargs.get("image_height", 640)
        
        if not csv_file:
            print("❌ csv_file parameter required!")
            return
        
        image_files = list(input_path.glob("*.jpg")) + list(input_path.glob("*.png"))
        
        for img_file in image_files:
            yolo_lines = csv_to_yolo(csv_file, image_width, image_height, img_file.name)
            
            output_file = output_path / f"{img_file.stem}.txt"
            with open(output_file, "w") as f:
                f.write("\n".join(yolo_lines))
            
            print(f"✓ {img_file.name} → {output_file.name}")
    
    print(f"✅ Conversion complete! Files saved to: {output_path}")


if __name__ == "__main__":
    print("""
    ✂️  Label Format Converter - YOLO Format
    
    Usage Examples:
    
    1. Convert Pascal VOC (XML) to YOLO:
       python convert_labels.py pascal_voc input_dir output_dir --width 640 --height 640
    
    2. Convert COCO JSON to YOLO:
       python convert_labels.py coco input_dir output_dir --coco-json annotations.json
    
    3. Convert CSV to YOLO:
       python convert_labels.py csv input_dir output_dir --csv-file labels.csv --width 640 --height 640
    
    Supported Formats:
    ✓ Pascal VOC (XML)
    ✓ COCO JSON
    ✓ CSV
    """)
