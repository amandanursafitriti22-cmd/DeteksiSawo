# ✅ YOLOv11 Training Workflow Checklist

## Phase 1️⃣: Dataset Preparation ✅ DONE
- [x] Collected 45 images from Label Studio
- [x] Organized 45 corresponding label files (.txt format)
- [x] Copied to `train/dataset/` structure
- [x] Auto-split: 36 train images + 9 validation images
- [x] Validated YOLO format (normalized bbox coordinates)

**Issue Found:** Only 2 classes detected (belum_matang, matang) - missing setengah_matang
- Add more "setengah_matang" labeled images in future iterations

---

## Phase 2️⃣: Environment Setup ✅ DONE
- [x] Node.js 22.12.0 installed (Vite 7.3.1 compatibility)
- [x] Python environment configured
- [x] PyTorch 2.4.1 + ultralytics 8.4.51 installed
- [x] ONNX runtime dependencies ready

---

## Phase 3️⃣: Model Training 🔴 IN PROGRESS (Need to start)

### Pre-Training Verification
- [x] Script updated to use YOLOv11n
- [x] Epochs changed to 60 (best for <200 images)
- [ ] **NEXT: Start training with YOLOv11n**

### Training Execution
```bash
cd train
python train_local.py
```

**Expected Output:**
- ✅ Model loads: "📥 Loading YOLOv11n model..."
- ✅ Validation passes
- ✅ Training starts with epoch 1/60
- ⏱️ Duration: 30-60 minutes (CPU)
- 📊 Metrics: Check `runs/sawo_detection/results.csv`
- 💾 Output: `runs/sawo_detection/weights/best.pt`

### Checklist During Training
- [ ] Monitor terminal for any errors
- [ ] Loss should decrease over epochs
- [ ] Validation metrics should improve
- [ ] No out-of-memory errors
- [ ] Training completes all 60 epochs

---

## Phase 4️⃣: Bounding Box Validation

### After Training Finishes
```bash
python test_detection.py
```

**Validation Criteria:**
- [ ] Detection rate > 70% (at least 7/9 images detected something)
- [ ] mAP50 > 0.60 (check results.csv)
- [ ] Average confidence > 0.50
- [ ] Bounding boxes look visually correct
- [ ] No excessive false positives

### Review Visual Results
```bash
# Check saved predictions
ls -la runs/sawo_detection/predict/
# Open in image viewer to verify boxes
```

### Pass/Fail Decision
```
IF validation OK ✅
  → Proceed to Phase 5 (Export & Deploy)
  
IF validation NOT OK ❌
  → Check data quality
  → Consider more epochs
  → Try larger model (yolov11s)
  → Re-collect images if needed
```

---

## Phase 5️⃣: Model Export & Deployment

### Export to ONNX (Auto by train_local.py)
```
✅ Auto-exported to: runs/sawo_detection/weights/best.onnx
✅ Auto-copied to: public/models/best.onnx
```

### Deploy to Frontend
```bash
# Verify copy successful
ls -la public/models/best.onnx
# Should show file size ~6-8 MB
```

### Frontend Testing
1. Open http://localhost:5175
2. Navigate to `/detect`
3. Test with real images:
   - [ ] Upload belum_matang (green) image
   - [ ] Upload matang (yellow) image
   - [ ] Check detection accuracy
   - [ ] Verify class labels correct
   - [ ] Check confidence scores

---

## Phase 6️⃣: Scale to 1000 Images 📈

### When to Start Scaling
✅ Only if Phase 4 validation passed with good metrics!

### Preparation Steps
- [ ] Collect 1000+ diverse mango images
- [ ] Ensure balanced class distribution:
  - [ ] ~333 belum_matang images
  - [ ] ~333 setengah_matang images (MUST include!)
  - [ ] ~333 matang images
- [ ] Label all images using Label Studio
- [ ] Export and organize into `train/dataset/`

### Config Update for 1000 Images
Edit `train/train_local.py` line 611-618:
```python
trainer = SawoYOLOTrainer(
    project_root=project_root,
    img_size=640,
    epochs=40,           # ← Changed from 60
    batch_size=32,       # ← Changed from 16
)
```

Or use utility:
```bash
python switch_config.py large
```

### Run Large Dataset Training
```bash
python train_local.py
# Duration: 1-3 hours depending on hardware
```

### Expected Improvements
- mAP: 0.70+ (from ~0.60 baseline)
- Precision: Better accuracy
- Recall: Fewer missed detections
- Robustness: Better generalization

---

## 🆘 Troubleshooting

### Issue: Training doesn't start
```bash
# Check YOLOv11n download
python -c "from ultralytics import YOLO; m = YOLO('yolov11n.pt'); print('✅')"
```

### Issue: Out of memory
```
• Reduce batch_size to 8
• Reduce img_size to 512
• Close other applications
```

### Issue: Poor detection accuracy
```
• Check image quality in dataset
• Verify labels are correct (VALIDATION_GUIDE.md)
• Collect more diverse images
• Try yolov11s instead of yolov11n
```

### Issue: ONNX export fails
```bash
python -c "
from ultralytics import YOLO
model = YOLO('runs/sawo_detection/weights/best.pt')
model.export(format='onnx')
"
```

---

## 📊 Progress Summary

| Phase | Task | Status | Notes |
|-------|------|--------|-------|
| 1 | Dataset prep | ✅ | 45 images organized |
| 2 | Environment | ✅ | Node.js 22, Python ready |
| 3 | Training | 🔴 | **NEXT STEP** |
| 4 | Validation | ⏳ | After training |
| 5 | Deploy | ⏳ | After export |
| 6 | Scale 1000x | ⏳ | After Phase 5 |

---

## 🚀 Quick Start

```bash
# 1. Start training (right now!)
cd train
python train_local.py

# 2. After 30-60 minutes, validate
python test_detection.py

# 3. If good, test in frontend
# Navigate to http://localhost:5175/detect

# 4. Ready to scale?
# python switch_config.py large
# python train_local.py
```

---

## 📚 Documentation Files

- `TRAINING_PARAMETERS.md` - Config options explained
- `VALIDATION_GUIDE.md` - Detailed validation procedures  
- `QUICK_START.md` - 5-minute quick reference
- `train_local.py` - Main training script (execute this!)
- `test_detection.py` - Validation utility
- `switch_config.py` - Config switcher

---

## 🎯 Research Goals

✅ Must use **YOLOv11** (Done - script updated)
✅ Test with **36 images** first (Ready to start)
✅ Scale to **1000+ images** if good results (Next phase)
✅ Achieve **real-time detection** on browser (After export)

**Status: Ready for Phase 3 Training! 🚀**
