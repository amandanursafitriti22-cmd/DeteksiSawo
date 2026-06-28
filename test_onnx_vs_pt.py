#!/usr/bin/env python3
"""
Test ONNX model inference vs PyTorch - debug missing detections
"""
import cv2
import numpy as np
from pathlib import Path
from PIL import Image

# Try different imports
try:
    import onnxruntime as ort
    HAS_ONNX = True
except:
    HAS_ONNX = False
    print("⚠️  onnxruntime not installed")

from ultralytics import YOLO

def test_single_image():
    """Test one validation image with both models"""
    print("\n" + "="*70)
    print("🧪 ONNX vs PyTorch Model Comparison")
    print("="*70)
    
    # Get first validation image
    dataset_dir = Path("dataset/valid/images")
    images = list(dataset_dir.glob("*.jpg")) + list(dataset_dir.glob("*.png"))
    if not images:
        print("❌ No validation images found")
        return
    
    test_image_path = images[0]
    print(f"\n📸 Testing with: {test_image_path.name}")
    
    # Load image
    img = Image.open(test_image_path)
    img_array = cv2.imread(str(test_image_path))
    h, w = img_array.shape[:2]
    print(f"   Image size: {w}x{h}")
    
    # ======== PyTorch Model ========
    print("\n📊 PyTorch Model (best.pt):")
    print("-" * 70)
    try:
        pt_model = YOLO("models/best.pt")
        results = pt_model(test_image_path, conf=0.5, imgsz=512)
        
        if results:
            r = results[0]
            dets = r.boxes
            print(f"   ✅ Detections: {len(dets)}")
            for det in dets:
                x1, y1, x2, y2 = det.xyxy[0].tolist()
                conf = det.conf.item()
                cls_id = int(det.cls.item())
                class_name = pt_model.names[cls_id]
                print(f"      - {class_name:15} conf={conf:.2%} bbox=({x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f})")
        else:
            print("   ❌ No detections")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # ======== ONNX Model ========
    if HAS_ONNX:
        print("\n📊 ONNX Model (best.onnx):")
        print("-" * 70)
        try:
            onnx_path = "public/models/best.onnx"
            if not Path(onnx_path).exists():
                print(f"   ❌ ONNX file not found: {onnx_path}")
            else:
                sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
                input_name = sess.get_inputs()[0].name
                input_shape = sess.get_inputs()[0].shape
                print(f"   Input: {input_name} shape={input_shape}")
                
                # Preprocess: letterbox to 512
                img_array_512 = cv2.resize(img_array, (512, 512))
                # Normalize to [0, 1]
                img_normalized = img_array_512.astype(np.float32) / 255.0
                # Convert BGR to RGB and to channels-first
                img_rgb = cv2.cvtColor(img_array_512, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
                # Channels first: [3, 512, 512]
                img_chw = np.transpose(img_rgb, (2, 0, 1))
                # Batch: [1, 3, 512, 512]
                input_tensor = np.expand_dims(img_chw, 0).astype(np.float32)
                
                print(f"   Input tensor shape: {input_tensor.shape}")
                
                # Run inference
                result = sess.run(None, {input_name: input_tensor})
                output = result[0]
                print(f"   Output shape: {output.shape}")
                print(f"   Output: [batch={output.shape[0]}, channels={output.shape[1]}, anchors={output.shape[2]}]")
                
                # Parse output
                # Expected: [1, 6, 5376] for 512x512 (or 8400 for 640x640)
                # [1, 4+nc, anchors] where 4=bbox, nc=2 (matang, belum_matang)
                batch = output.shape[0]
                channels = output.shape[1]
                anchors = output.shape[2]
                nc = channels - 4
                
                print(f"   Channels: {channels} (4 bbox + {nc} class probs)")
                print(f"   Anchors: {anchors}")
                print(f"   Expected for 512x512: 4+2=6 channels, ~5376 anchors")
                
                # Extract detections (simple thresholding)
                detections = []
                conf_threshold = 0.5
                
                for i in range(anchors):
                    # Get confidence scores for each class
                    scores = output[0, 4:4+nc, i]
                    max_score = np.max(scores)
                    class_id = np.argmax(scores)
                    
                    if max_score >= conf_threshold:
                        # Get bbox
                        cx = output[0, 0, i]
                        cy = output[0, 1, i]
                        w = output[0, 2, i]
                        h = output[0, 3, i]
                        
                        detections.append({
                            'class': class_id,
                            'conf': max_score,
                            'x1': cx - w/2,
                            'y1': cy - h/2,
                            'x2': cx + w/2,
                            'y2': cy + h/2,
                        })
                
                print(f"   ✅ Detections: {len(detections)}")
                class_names = ["matang", "belum_matang"]
                for det in detections[:10]:  # Show first 10
                    print(f"      - {class_names[det['class']]:15} conf={det['conf']:.2%} bbox=({det['x1']:.0f},{det['y1']:.0f},{det['x2']:.0f},{det['y2']:.0f})")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)

if __name__ == "__main__":
    test_single_image()
