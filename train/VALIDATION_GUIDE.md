# ✅ Bounding Box Validation Guide

## Setelah Training Selesai (60 epochs)

### Step 1️⃣: Export Model ke ONNX
```bash
# Ini auto-run di train_local.py, tapi bisa manual:
python -c "
from ultralytics import YOLO
model = YOLO('runs/sawo_detection/weights/best.pt')
model.export(format='onnx')
print('✅ Model exported to best.onnx')
"
```

---

### Step 2️⃣: Test Deteksi - 3 Method

#### Method A: Direct Python Test (Cepat)
```bash
cd train
python test_detection.py
```

#### Method B: Manual Validation (1 Image)
```python
from ultralytics import YOLO
from PIL import Image
import cv2

# Load model
model = YOLO('runs/sawo_detection/weights/best.pt')

# Test satu image
img = Image.open('dataset/valid/images/image_001.jpg')
results = model.predict(source=img, conf=0.5)

# Show hasil
results[0].show()  # Display dengan bounding box

# Print metrics
for r in results:
    print(f"Deteksi: {r.boxes}")
    print(f"Confidence: {r.boxes.conf}")
    print(f"Class: {r.boxes.cls}")
```

#### Method C: Batch Validation (Semua 9 test images)
```python
from ultralytics import YOLO
from pathlib import Path

model = YOLO('runs/sawo_detection/weights/best.pt')

# Predict all valid images
valid_dir = Path('dataset/valid/images')
results = model.predict(source=str(valid_dir), conf=0.5, save=True)

print(f"✅ Hasil tersimpan di: runs/sawo_detection/predict/")
```

---

### Step 3️⃣: Bounding Box Checklist

Validasi visual untuk setiap hasil:

```
☑️ AKURASI DETEKSI
   □ Buah terdeteksi (minimal 80% dari semua buah)
   □ Bounding box tepat mengelilingi buah (tight, bukan too loose)
   □ Tidak ada deteksi palsu (false positives)
   
☑️ KLASIFIKASI
   □ belum_matang (hijau) → Confidently classified
   □ matang (kuning/orange) → Confidently classified
   □ Confidence score > 0.5 untuk kebanyakan deteksi
   
☑️ METRICS TARGET
   □ mAP50 > 0.60 (acceptable)
   □ mAP50 > 0.75 (good)
   □ Precision > 0.60
   □ Recall > 0.60
```

---

### Step 4️⃣: Hasil Interpretasi

**HASIL BAIK ✅ → Lanjut ke 1000 images**
- mAP50 > 0.60
- Visual bounding boxes terlihat akurat
- Deteksi konsisten di berbagai angle

**HASIL KURANG ⚠️ → Optimization sebelum scale**
- Cek image quality (clarity, lighting)
- Cek label accuracy (correct annotations?)
- Coba epochs lebih banyak (80-100)
- Coba model lebih besar (yolov11s instead of yolov11n)

**HASIL BURUK ❌ → Restart dengan data quality check**
- Check dataset di `LABEL_STUDIO_GUIDE.md`
- Validate annotations accuracy
- Ensure balanced class distribution
- Collect more diverse images

---

### Step 5️⃣: Model Deployment

Setelah validasi OK, deploy ke frontend:

```bash
# Auto-copy by train_local.py, but manual copy:
cp train/runs/sawo_detection/weights/best.pt public/models/
python public/models/convert_to_onnx.py

# Atau quick copy:
cp train/runs/sawo_detection/weights/best.onnx public/models/best.onnx
```

---

### Step 6️⃣: Frontend Testing

1. Reload aplikasi SawoVision
2. Go to `/detect` route
3. Test dengan 3 fruit images:
   - 1 belum_matang (green)
   - 1 setengah_matang (transitioning)
   - 1 matang (yellow/orange)

4. Verify:
   - ✅ Bounding boxes drawn correctly
   - ✅ Class labels shown
   - ✅ Confidence scores displayed
   - ✅ Real-time detection smooth

---

## Quick Decision Tree

```
Training finished?
  ├─ YES: mAP > 0.60?
  │   ├─ YES ✅ → Deploy & Scale to 1000 images
  │   └─ NO ⚠️ → Check data quality & retry
  └─ NO: Still running?
      └─ WAIT: Monitor runs/sawo_detection/results.csv
```

---

## Useful Commands

```bash
# Monitor training live
tensorboard --logdir runs/sawo_detection

# Check final metrics
cat runs/sawo_detection/results.csv

# View training plots
python -c "import matplotlib.pyplot as plt; plt.show()"

# Test speed (inference time)
python -c "
from ultralytics import YOLO
import time
model = YOLO('runs/sawo_detection/weights/best.pt')
start = time.time()
results = model.predict(source='dataset/valid/images', conf=0.5)
print(f'Speed: {(time.time()-start):.2f}s for all images')
"
```

---

## Next Phase: 1000 Image Training

Checklist:
- [ ] Collected 1000+ diverse images
- [ ] Labeled semua dengan Label Studio
- [ ] Balanced class distribution (jeez, don't forget matang class!)
- [ ] Dataset split ke train/valid
- [ ] Update `switch_config.py` ke "large"
- [ ] Run training dengan parameter baru
- [ ] Compare metrics dengan 36-image baseline

**Estimated improvement:**
- mAP: 0.70+ (dari sebelumnya ~0.60)
- Robustness: lebih stabil di berbagai lighting/angle
- False positives: berkurang significantly

🚀 Ready to scale!
