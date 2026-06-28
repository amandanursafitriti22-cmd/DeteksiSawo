# 🍌 SawoVision YOLOv11 Training Suite

Complete training pipeline untuk YOLOv11 deteksi kematangan buah sawo.
Updated untuk penelitian dengan fokus pada YOLOv11, testing 36 images, scaling ke 1000+.

## 📋 Daftar Isi
1. [Struktur Folder](#struktur-folder)
2. [Setup Dataset](#setup-dataset)
3. [Training di Colab](#training-di-colab)
4. [Training di VSCode](#training-di-vscode)
5. [Hasil Training](#hasil-training)
6. [Deploy Model](#deploy-model)

---

## 📁 Struktur Folder

```
train/
├── dataset/
│   ├── images/
│   │   ├── train/          ← Copy gambar training di sini
│   │   └── val/            ← Copy gambar validation di sini
│   └── labels/
│       ├── train/          ← File label .txt YOLO format
│       └── val/            ← File label .txt YOLO format
├── runs/                   ← Output hasil training (auto-generated)
│   └── sawo_detection/
│       ├── weights/
│       │   ├── best.pt
│       │   └── last.pt
│       ├── results.json
│       └── TRAINING_REPORT.json
├── train_local.py          ← Script training untuk VSCode
├── train_colab.ipynb       ← Notebook untuk Google Colab
├── requirements.txt        ← Dependencies Python
└── README.md               ← File ini
```

---

## 🎯 Setup Dataset

### Format Label YOLO

Setiap gambar harus punya file `.txt` dengan format:
```
<class_id> <x_center> <y_center> <width> <height>
<class_id> <x_center> <y_center> <width> <height>
...
```

**Class IDs:**
- `0` = belum_matang (unripe)
- `1` = setengah_matang (half-ripe)
- `2` = matang (ripe)

**Contoh** (`image_001.txt`):
```
0 0.5 0.5 0.3 0.4
1 0.7 0.3 0.25 0.35
```

### Tools Annotasi Bounding Box

Gunakan salah satu tools berikut untuk membuat label:

1. **Roboflow** (Recommended - Free)
   - Upload gambar → annotate → export YOLO format
   - https://roboflow.com/

2. **LabelImg** (Desktop)
   - Free tool open-source
   - Generate `.xml` → convert ke YOLO format

3. **Makesense.ai** (Web-based)
   - Browser-based, gratis
   - https://www.makesense.ai/

### Struktur Dataset yang Benar

```
dataset/
├── images/
│   ├── train/
│   │   ├── sawo_001.jpg
│   │   ├── sawo_002.jpg
│   │   ├── sawo_003.jpg
│   │   └── ... (80% dari total)
│   └── val/
│       ├── sawo_101.jpg
│       ├── sawo_102.jpg
│       └── ... (20% dari total)
└── labels/
    ├── train/
    │   ├── sawo_001.txt
    │   ├── sawo_002.txt
    │   ├── sawo_003.txt
    │   └── ...
    └── val/
        ├── sawo_101.txt
        ├── sawo_102.txt
        └── ...
```

**Rasio:** 80% training, 20% validation

---

## 🚀 Training di Google Colab

### Step 1: Setup Google Drive

1. Buka Google Drive
2. Buat folder: `/Sawo_Training/dataset/`
3. Upload struktur dataset ke sana:
   ```
   /MyDrive/Sawo_Training/
   └── dataset/
       ├── images/ (train & val)
       └── labels/ (train & val)
   ```

### Step 2: Buka Notebook di Colab

1. Buka file `train_colab.ipynb` di Google Colab
2. Atau copy ke Colab Anda:
   - Open: https://colab.research.google.com
   - Upload `train_colab.ipynb`

### Step 3: Jalankan Cells Secara Berurutan

```python
# 1. Install dependencies
!pip install -q ultralytics opencv-python torch torchvision

# 2. Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 3. Validasi dataset
# ... (cek jumlah gambar)

# 4. Create data.yaml
# ... (auto-generated)

# 5. Train Model
# Model akan training selama beberapa jam
# GPU T4 di Colab: ~50-100 epoch

# 6. Visualisasi hasil
# Akan generate grafik:
# - Loss (train vs val)
# - mAP50 & mAP50-95
# - Overfitting detection
# - Inference test

# 7. Export ke ONNX
# Download best.onnx
```

### Step 4: Download Model

1. Setelah training selesai, download `best.onnx`
2. Copy ke project React: `/public/models/best.onnx`

---

## 💻 Training di VSCode (Local)

### Step 1: Install Dependencies

```bash
# PowerShell
pip install -r train/requirements.txt
```

### Step 2: Prepare Dataset Lokal

Copy dataset ke folder:
```
train/dataset/
├── images/train/ (your images)
├── images/val/   (your images)
├── labels/train/ (label .txt files)
└── labels/val/   (label .txt files)
```

### Step 3: Jalankan Training Script

```bash
# PowerShell / Command Prompt
cd train
python train_local.py
```

### Output Training

Script akan generate:

```
train/
└── runs/
    └── sawo_detection/
        ├── weights/
        │   ├── best.pt      ← Best model
        │   └── last.pt      ← Last checkpoint
        ├── results.json     ← Metrics
        ├── TRAINING_REPORT.json
        ├── plots/
        │   ├── confusion_matrix.png
        │   ├── results.png
        │   └── ...
        └── detect/          ← Inference results
```

### Step 4: Check Results

Script otomatis akan:
1. ✅ Validasi dataset
2. ✅ Create data.yaml config
3. ✅ Train model YOLOv11
4. ✅ Evaluate pada validation set
5. ✅ Generate grafik training
6. ✅ Export ke ONNX
7. ✅ Copy `best.onnx` ke `/public/models/`

---

## 📊 Hasil Training

### Grafik yang Dihasilkan

1. **Loss Curve**
   - Training loss (blue)
   - Validation loss (red)
   - Jika validation > training = overfitting

2. **mAP50 (Mean Average Precision @ IoU=0.5)**
   - Semakin tinggi semakin baik
   - Target: > 0.8 (80%)

3. **mAP50-95 (Lebih strict)**
   - Average dari IoU 0.5 hingga 0.95
   - Target: > 0.7 (70%)

4. **Overfitting Detection**
   - Gap = Validation Loss - Training Loss
   - Gap < 0.05 = BAIK (no overfitting)
   - Gap 0.05-0.1 = MODERATE (sedikit overfitting)
   - Gap > 0.1 = TINGGI (overfitting)

### Contoh Output

```
============================================================
🍌 YOLOv11 Training - Deteksi Kematangan Buah Sawo
============================================================

📋 Validasi Dataset...
  ✓ Training images: 150
  ✓ Validation images: 30
  ✓ Training labels: 150
  ✓ Validation labels: 30

🚀 Memulai Training YOLOv11...
  📊 Image Size: 640
  🔢 Epochs: 100
  📦 Batch Size: 16
  🎯 Device: GPU

Epoch 1/100: 100%|██████| 10/10 [00:15<00:00, 1.50s/it]
Epoch 2/100: 100%|██████| 10/10 [00:14<00:00, 1.40s/it]
...
Epoch 100/100: 100%|██████| 10/10 [00:14<00:00, 1.40s/it]

✅ Training selesai!

🔍 Mengevaluasi Model...
  mAP50: 0.887
  mAP50-95: 0.756

============================================================
📊 ANALISIS OVERFITTING & PERFORMA MODEL
============================================================

📈 Metrik Performa:
   • mAP50 (Best):     88.70%
   • mAP50-95 (Best):  75.60%

📉 Loss Analysis (Last 10 Epochs):
   • Training Loss:    0.0234
   • Validation Loss:  0.0267
   • Gap (Val - Train): 0.0033

🔍 Status Overfitting:
   ✅ BAIK - Model tidak overfitting (gap: 0.0033)
      Training & validation loss seimbang

💡 Rekomendasi:
   ✅ Model performa SANGAT BAIK! Ready untuk production

============================================================
```

---

## 🔄 Deploy Model

### Step 1: Cari File Model ONNX

Lokasi tersimpan:
- **Colab:** Download dari output folder
- **VSCode:** `train/runs/sawo_detection/weights/best.onnx`

### Step 2: Copy ke Project React

```
Project-Sawo/
├── public/
│   └── models/
│       └── best.onnx  ← Copy file di sini
├── src/
├── package.json
└── ...
```

### Step 3: Reload Aplikasi

1. Aplikasi React sudah configured untuk load `/models/best.onnx`
2. Reload browser → akan auto-load model
3. Coba deteksi di halaman `/detect`

### Verifikasi Model Loaded

Di browser console:
```javascript
// Jika model loaded dengan benar:
[yolo] Model loaded successfully
```

---

## 🐛 Troubleshooting

### ❌ "Model not found"
**Solusi:**
- Pastikan file `best.onnx` ada di `/public/models/`
- Check console di browser (F12 → Console)

### ❌ "Overfitting detected"
**Solusi:**
1. Tambah data training (target: 500+ gambar)
2. Gunakan data augmentation
3. Reduce model size (gunakan `yolov11s` atau `yolov11m`)
4. Tambah regularization

### ❌ GPU memory error di Colab
**Solusi:**
- Reduce batch size: `batch=8` (default 16)
- Reduce image size: `imgsz=416` (default 640)
- Atau gunakan `yolov11n` (nano model)

### ❌ Training lambat di VSCode
**Solusi:**
- Pastikan GPU digunakan (install CUDA)
- Atau gunakan Colab yang punya free GPU T4

---

## 📚 Referensi

- **YOLOv11 Docs:** https://docs.ultralytics.com/models/yolo11/
- **Roboflow Dataset:** https://roboflow.com/
- **ONNX Export:** https://docs.ultralytics.com/modes/export/

---

## ✅ Checklist Sebelum Training

- [ ] Dataset sudah di-annotate (bounding box)
- [ ] Folder struktur sudah benar
- [ ] Minimum 50 gambar training, 10 validation
- [ ] Rasio 80% training, 20% validation
- [ ] Label file `.txt` sudah ada
- [ ] Requirements sudah diinstall

---

## 🎯 Expected Results

Dengan dataset yang baik (~200-500 gambar per kelas):

| Metric | Target |
|--------|--------|
| mAP50 | > 85% |
| mAP50-95 | > 75% |
| Overfitting Gap | < 0.05 |
| Inference Speed | 15+ FPS |

---

**Happy Training! 🚀**

Untuk pertanyaan, cek error logs di:
- **Colab:** Output cell
- **VSCode:** Terminal output
