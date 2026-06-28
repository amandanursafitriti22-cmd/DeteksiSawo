#!/usr/bin/env python3
"""
Pre-Flight Checklist for YOLOv11 Training
Verify everything is ready before starting training
"""

import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info >= (3, 8):
        print(f"✅ Python {version}")
        return True
    print(f"❌ Python {version} (need >= 3.8)")
    return False

def check_imports():
    """Check required packages"""
    packages = {
        "ultralytics": "YOLOv11 framework",
        "torch": "PyTorch",
        "torchvision": "Vision utilities",
        "PIL": "Image processing",
        "numpy": "Numerical computing",
        "matplotlib": "Plotting",
        "cv2": "OpenCV",
    }
    
    all_good = True
    for pkg, desc in packages.items():
        try:
            __import__(pkg)
            print(f"✅ {pkg:15} ({desc})")
        except ImportError:
            print(f"❌ {pkg:15} ({desc}) - NOT INSTALLED")
            all_good = False
    
    return all_good

def check_dataset():
    """Check dataset structure"""
    paths = {
        "train/dataset/train/images": "Training images",
        "train/dataset/train/labels": "Training labels",
        "train/dataset/valid/images": "Validation images",
        "train/dataset/valid/labels": "Validation labels",
        "train/dataset/data.yaml": "YAML config",
    }
    
    all_good = True
    for path, desc in paths.items():
        p = Path(path)
        if p.exists():
            if path.endswith('.yaml'):
                print(f"✅ {path:40} ({desc})")
            else:
                count = len(list(p.glob("*")))
                print(f"✅ {path:40} ({desc}) - {count} files")
        else:
            print(f"❌ {path:40} ({desc}) - NOT FOUND")
            all_good = False
    
    return all_good

def check_training_script():
    """Check training script"""
    script = Path("train_local.py")
    if script.exists():
        print(f"✅ train_local.py found")
        return True
    else:
        print(f"❌ train_local.py NOT FOUND")
        return False

def check_output_dir():
    """Check output directory"""
    output_dir = Path("public/models")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Output directory ready: {output_dir}")
    return True

def check_yolo_models():
    """Check if YOLO models can load"""
    try:
        from ultralytics import YOLO
        
        print("\n🔍 Testing model loading...")
        
        # Try YOLOv11n
        try:
            print("  Checking YOLOv11n...", end=" ", flush=True)
            model = YOLO("yolov11n.pt")
            print("✅")
            return True
        except:
            # Try YOLOv8n as fallback
            try:
                print("\n  YOLOv11n not available, checking YOLOv8n...", end=" ", flush=True)
                model = YOLO("yolov8n.pt")
                print("✅ (fallback)")
                print("  ⚠️  YOLOv11n not available - will use YOLOv8n fallback")
                return True
            except Exception as e:
                print(f"\n  ❌ Neither YOLOv11n nor YOLOv8n available")
                print(f"     Error: {e}")
                return False
    except ImportError:
        print("  ❌ Could not import YOLO")
        return False

def main():
    print("\n" + "="*70)
    print("🍌 YOLOv11 Training - PRE-FLIGHT CHECKLIST")
    print("="*70 + "\n")
    
    # Change to train directory
    train_dir = Path("train")
    if train_dir.exists():
        import os
        os.chdir(train_dir)
    else:
        print("❌ Not in project root directory!")
        print("   Please run this from project root: cd Project-Sawo")
        return False
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_imports),
        ("Dataset Structure", check_dataset),
        ("Training Script", check_training_script),
        ("Output Directory", check_output_dir),
        ("YOLO Models", check_yolo_models),
    ]
    
    print()
    results = []
    for name, check_fn in checks:
        print(f"\n📋 Checking {name}...")
        print("-" * 70)
        try:
            result = check_fn()
            results.append(result)
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*70)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("="*70)
        print("\n🚀 READY TO TRAIN!\n")
        print("Start training with:")
        print("  python train_local.py\n")
        return True
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total})")
        print("="*70)
        print("\n🔧 Please fix issues above before training\n")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
