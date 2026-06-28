# 🍌 YOLOv11 Training Parameters Guide

## Current Setup (36 Images Test)
```
Model: YOLOv11n (nano - fastest & lightweight)
Epochs: 60
Image Size: 640x640
Batch Size: 16
Device: CPU
Expected Duration: 30-60 minutes
```

---

## Bounding Box Validation Checklist

Sebelum scale ke 1000 images, pastikan:

✅ **Model Learning**
- Loss menurun seiring epoch bertambah
- Validation metrics meningkat
- mAP > 0.5 minimal untuk akurasi decent

✅ **Deteksi Akurat**
- Bounding box mendeteksi sawo dengan benar
- Bisa membedakan belum_matang vs matang
- Tidak ada false positives berlebihan

---

## Scale ke 1000 Images - Parameter Adjustments

### Untuk 1000 images, gunakan config:
```python
epochs=40,        # Cukup 40 epoch untuk dataset besar (best practice)
batch_size=32,    # Tingkatkan ke 32 untuk better gradient stability
img_size=640,     # Tetap 640 untuk optimal accuracy
```

### Atau jika GPU tersedia:
```python
epochs=40,
batch_size=64,    # Lebih besar jika GPU memory cukup
img_size=640,
device='cuda'     # Lebih cepat ~10x
```

---

## Model Size Options (untuk scale testing)

| Model | Param | Speed | Accuracy | Recommended For |
|-------|-------|-------|----------|-----------------|
| yolov11n | 2.6M | ⚡⚡⚡ | Good | Edge devices, Real-time |
| yolov11s | 9.3M | ⚡⚡ | Better | Balanced (current) |
| yolov11m | 20.1M | ⚡ | Best | High accuracy needed |
| yolov11l | 25.3M | - | Excellent | Server/GPU only |

**Untuk penelitian dengan 1000 images, coba yolov11s untuk lebih akurat!**

---

## Training Monitoring

Saat training, check di `runs/sawo_detection/`:
- `results.csv` - Metrics per epoch
- `plots/` - Visualization graphs
- `weights/best.pt` - Best model weights
- `weights/last.pt` - Last epoch weights

---

## Script Modifications untuk Scale

Edit `train/train_local.py` line 611-618:

```python
trainer = SawoYOLOTrainer(
    project_root=project_root,
    img_size=640,
    epochs=40,           # ← Ubah ke 40
    batch_size=32,       # ← Ubah ke 32
)
```

---

## Checklist Sebelum Scale

- [ ] Current 36-image model sudah trained & exported
- [ ] Bounding box validation passed
- [ ] Siap collect 1000 images
- [ ] Data terorganisir di `dataset/`
- [ ] Run script dengan parameter baru
- [ ] Monitor training metrics

🚀 **Ready to scale!**
