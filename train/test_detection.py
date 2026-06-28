#!/usr/bin/env python3
"""
Quick Bounding Box Validation Script
Jalankan setelah training selesai untuk validate deteksi hasil
"""

import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
from PIL import Image
import numpy as np

def validate_bbox(model_path="runs/sawo_detection/weights/best.pt", 
                  test_dir="dataset/valid/images",
                  conf_threshold=0.5):
    """
    Validate bounding box accuracy
    """
    print("\n" + "="*70)
    print("🍌 Bounding Box Validation")
    print("="*70)
    
    # Load model
    try:
        model = YOLO(model_path)
        print(f"✅ Model loaded: {model_path}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return
    
    # Get test images
    test_path = Path(test_dir)
    if not test_path.exists():
        print(f"❌ Test directory not found: {test_dir}")
        return
    
    images = list(test_path.glob("*.jpg")) + list(test_path.glob("*.png"))
    if not images:
        print(f"❌ No images found in {test_dir}")
        return
    
    print(f"📊 Found {len(images)} test images")
    
    # Run prediction
    print(f"\n🔍 Running inference with confidence threshold: {conf_threshold}...")
    results = model.predict(source=str(test_path), conf=conf_threshold, save=True)
    
    # Analyze results
    print(f"\n📈 Validation Results:")
    print("-" * 70)
    
    total_detections = 0
    total_boxes = 0
    class_counts = {}
    confidences = []
    
    for i, result in enumerate(results):
        image_name = Path(images[i]).name if i < len(images) else f"image_{i}"
        boxes = result.boxes
        
        if len(boxes) > 0:
            total_detections += 1
            total_boxes += len(boxes)
            
            # Analyze detections
            for box, cls, conf in zip(boxes.xyxy, boxes.cls, boxes.conf):
                class_name = result.names[int(cls)]
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
                confidences.append(float(conf))
    
    # Print summary
    print(f"\n✅ Detection Summary:")
    print(f"   • Images with detections: {total_detections}/{len(images)}")
    print(f"   • Total detections: {total_boxes}")
    print(f"   • Average confidence: {np.mean(confidences):.3f}" if confidences else "   • No detections")
    
    if class_counts:
        print(f"\n📊 Detections by class:")
        for class_name, count in sorted(class_counts.items()):
            print(f"   • {class_name}: {count}")
    
    print(f"\n📁 Results saved to: runs/sawo_detection/predict/")
    print("\n💡 Next steps:")
    print("   1. Check visual results in runs/sawo_detection/predict/")
    print("   2. Verify bounding boxes are accurate")
    print("   3. If good ✅ → Ready to scale to 1000 images")
    print("   4. If bad ❌ → Check VALIDATION_GUIDE.md for troubleshooting")
    
    print("\n" + "="*70)
    
    # Return metrics for programmatic use
    return {
        "total_images": len(images),
        "detected_images": total_detections,
        "total_detections": total_boxes,
        "class_distribution": class_counts,
        "avg_confidence": np.mean(confidences) if confidences else 0.0,
        "detection_rate": total_detections / len(images) if len(images) > 0 else 0
    }

if __name__ == "__main__":
    # Get parameters
    model_path = sys.argv[1] if len(sys.argv) > 1 else "runs/sawo_detection/weights/best.pt"
    test_dir = sys.argv[2] if len(sys.argv) > 2 else "dataset/valid/images"
    conf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    
    metrics = validate_bbox(model_path, test_dir, conf)
    
    # Exit with appropriate code
    if metrics and metrics["detection_rate"] > 0.7:
        print("\n✨ Detection rate good! Ready for next phase.")
        sys.exit(0)
    else:
        print("\n⚠️  Detection rate low. Review data quality.")
        sys.exit(1)
