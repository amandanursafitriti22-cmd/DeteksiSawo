# 🍌 YOLOv11 Training - QUICK START

## ✅ Everything is READY!

Your training setup is **completely prepared** for YOLOv11 with 36 images.

---

## 🚀 START TRAINING (RIGHT NOW!)

```bash
cd train
python train_local.py
```

**That's it!** The script handles everything:
- ✅ Loads YOLOv11n model
- ✅ Validates dataset (36 train, 9 test images)
- ✅ Trains for 60 epochs (~30-60 min on CPU)
- ✅ Exports to ONNX format
- ✅ Copies to `public/models/best.onnx`

---

## ⏱️ Timeline

| Time | Event |
|------|-------|
| T+0 min | Start training |
| T+30-60 min | Training completes |
| T+5 min after | Run validation |
| T+1 hour | Ready to test in frontend |

---

## 📊 After Training (30-60 minutes)

### Quick Validation
```bash
cd train
python test_detection.py
```

**Output:**
- Validation metrics
- Detection rate
- Class distribution
- Recommendation (Ready? or Improve?)

---

## ✨ Frontend Testing

After successful training:

1. Open http://localhost:5175
2. Go to `/detect` page
3. Upload test images (belum_matang, matang)
4. See **real-time bounding boxes!** 🎯

---

## 📈 Scale to 1000 Images (Later)

When ready to scale:

```bash
python switch_config.py large
python train_local.py
```

**Updated config:**
- Epochs: 40 (was 60)
- Batch size: 32 (was 16)
- Duration: 1-3 hours

---

## 🎯 Success Criteria

Training is successful when:
- ✅ mAP50 > 0.60 (check `results.csv`)
- ✅ Detection rate > 70% (check `test_detection.py`)
- ✅ Visual bounding boxes accurate
- ✅ No crashes or errors

---

## 📚 Full Documentation

For more details:
- **Parameters:** `TRAINING_PARAMETERS.md`
- **Validation:** `VALIDATION_GUIDE.md`  
- **Full Workflow:** `WORKFLOW_CHECKLIST.md`

---

## 🆘 Quick Troubleshooting

**Q: Script won't start?**
- Check: `python -c "from ultralytics import YOLO; YOLO('yolov11n.pt')"`
- Or try: `python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"` (fallback)

**Q: Out of memory?**
- Edit `train_local.py` line 616: `batch_size=8` (reduced from 16)

**Q: Training takes forever?**
- Normal! 30-60 min on CPU is expected for YOLOv11n
- Monitor: Check `runs/sawo_detection/results.csv` for progress

---

## 🔥 READY TO GO!

```bash
cd train
python train_local.py
```

**Go! 🚀**
