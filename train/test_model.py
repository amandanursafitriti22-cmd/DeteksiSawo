#!/usr/bin/env python3
"""Quick test to load YOLOv11 model"""

from ultralytics import YOLO
import sys
from pathlib import Path

try:
    print("Attempting to load YOLOv11n model...")
    
    # Get the ultralytics cfg path
    import ultralytics
    ultralytics_path = Path(ultralytics.__file__).parent
    yaml_path = ultralytics_path / "cfg" / "models" / "11" / "yolo11.yaml"
    
    print(f"YAML path: {yaml_path}")
    print(f"Exists: {yaml_path.exists()}")
    
    if yaml_path.exists():
        model = YOLO(str(yaml_path))
        print("✅ Model loaded successfully!")
        model.info()
    else:
        print("❌ YAML file not found")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
