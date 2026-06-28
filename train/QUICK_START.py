#!/usr/bin/env python3
"""
Quick Start Guide - YOLOv11 Sawo Training
"""

COMMANDS = {
    "setup": {
        "description": "Validasi dan setup dataset",
        "command": "python train/setup_dataset.py",
    },
    "convert": {
        "description": "Convert label format (VOC, COCO, CSV) ke YOLO",
        "command": "python train/convert_labels.py",
    },
    "train_local": {
        "description": "Train di VSCode/Local dengan GPU",
        "command": "python train/train_local.py",
    },
    "colab": {
        "description": "Train di Google Colab (recommended)",
        "command": "Open: train/train_colab.ipynb di Colab",
    },
}


def print_menu():
    print("\n" + "="*70)
    print("🍌 YOLOv11 Training - Deteksi Kematangan Buah Sawo")
    print("="*70)
    
    print("\n📖 QUICK START GUIDE")
    print("\nStep 1: Prepare Dataset")
    print("  a) Annotate your images with bounding boxes")
    print("     → Use: Roboflow.com, LabelImg, or Makesense.ai")
    print("  b) Export labels in YOLO format")
    print("  c) Organize into train/dataset/images/{train,val}/")
    print("                      train/dataset/labels/{train,val}/")
    
    print("\nStep 2: Validate Dataset")
    print(f"  Command: {COMMANDS['setup']['command']}")
    print("  This will check structure and class distribution")
    
    print("\nStep 3: Train Model")
    print("  Option A - Google Colab (RECOMMENDED):")
    print(f"    {COMMANDS['colab']['command']}")
    print("    → Free GPU (T4), fast training")
    print("\n  Option B - Local/VSCode:")
    print(f"    {COMMANDS['train_local']['command']}")
    print("    → Need GPU installed (CUDA)")
    
    print("\nStep 4: Deploy Model")
    print("  After training:")
    print("  a) Download or find best.onnx")
    print("  b) Copy to: /public/models/best.onnx")
    print("  c) Reload browser → Model will auto-load")
    
    print("\n" + "="*70)
    print("📊 WHAT YOU'LL GET")
    print("="*70)
    
    print("\n📈 Training Metrics (automatically generated):")
    print("  ✓ Loss curve (training vs validation)")
    print("  ✓ mAP50 & mAP50-95 scores")
    print("  ✓ Overfitting detection")
    print("  ✓ Confusion matrix")
    print("  ✓ Inference test on sample images")
    
    print("\n📁 Output Files:")
    print("  ✓ best.pt - Best PyTorch model")
    print("  ✓ best.onnx - Optimized for browser deployment")
    print("  ✓ results.json - All metrics")
    print("  ✓ training_metrics.png - Visualization")
    print("  ✓ TRAINING_REPORT.json - Full report")
    
    print("\n" + "="*70)
    print("💡 TIPS & TRICKS")
    print("="*70)
    
    print("""
    ✓ Dataset Preparation:
      - Minimum 50 images (better: 200+)
      - Balanced classes (not too skewed)
      - 80% train, 20% validation split
      - Clear, well-lit images
    
    ✓ Training:
      - Start with yolov11n (nano) for fast training
      - Use Colab for free GPU
      - Monitor loss curve - should be decreasing
      - If overfitting: add more data or augmentation
    
    ✓ Performance:
      - Target mAP50 > 0.85 (85%)
      - Target mAP50-95 > 0.75 (75%)
      - Inference should be 15+ FPS on browser
    
    ✓ Troubleshooting:
      - Model not loading? Check console (F12)
      - Overfitting? Get more training data
      - Slow training? Use smaller model (yolov11n)
      - GPU memory error? Reduce batch size
    """)
    
    print("="*70)
    print("📚 REFERENCES")
    print("="*70)
    print("""
    - YOLOv11 Docs: https://docs.ultralytics.com/models/yolo11/
    - Roboflow: https://roboflow.com/
    - LabelImg: https://github.com/heartexlabs/labelImg
    - Makesense: https://www.makesense.ai/
    - ONNX: https://onnx.ai/
    """)
    
    print("="*70)
    print("✅ READY TO START? Follow these commands:")
    print("="*70)
    print("\n1. Setup dataset:")
    print(f"   {COMMANDS['setup']['command']}")
    
    print("\n2. Choose training method:")
    print(f"   A) Colab: {COMMANDS['colab']['command']}")
    print(f"   B) Local: {COMMANDS['train_local']['command']}")
    
    print("\n3. Deploy model:")
    print("   Copy best.onnx to /public/models/best.onnx")
    print("   Reload browser")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    print_menu()
