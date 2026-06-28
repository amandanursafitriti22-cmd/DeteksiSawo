# 🏷️ Struktur Folder Lengkap - Label Studio Export

## 📁 Lokasi Menyimpan File-File Label Studio

```
Project-Sawo/
│
├── train/
│   ├── dataset/                          ← Training data folder
│   │   ├── images/
│   │   │   ├── train/                   ← Gambar training (auto-created)
│   │   │   └── val/                     ← Gambar validation (auto-created)
│   │   ├── labels/
│   │   │   ├── train/                   ← Label YOLO (auto-created)
│   │   │   └── val/                     ← Label YOLO (auto-created)
│   │   └── data.yaml                    ← Config auto-generated
│   │
│   ├── dataset_metadata/                ← 🟢 SIMPAN FILE INI DI SINI!
│   │   ├── classes.txt                  ← Copy dari Label Studio export
│   │   ├── notes.json                   ← Template JSON (update statistics)
│   │   ├── export.json                  ← Copy dari Label Studio export (PENTING!)
│   │   └── README.md                    ← Info tentang dataset
│   │
│   ├── convert_label_studio.py          ← Script conversion
│   ├── setup_dataset.py                 ← Script validasi
│   ├── train_local.py                   ← Script training
│   ├── train_colab.ipynb                ← Notebook Colab
│   ├── README.md                        ← Panduan training
│   └── ...
│
├── public/
│   └── models/
│       └── best.onnx                    ← Model output
│
└── src/
    └── ...
```

---

## 🎯 Penjelasan File-File

### **📄 classes.txt**
**Lokasi:** `train/dataset_metadata/classes.txt`

Berisi daftar class yang ada di Label Studio:
```
belum_matang
setengah_matang
matang
```

**Cara menggunakan:**
- Copy langsung dari export Label Studio
- Simpan di folder `dataset_metadata/`
- Gunakan untuk reference/dokumentasi

### **📝 notes.json**
**Lokasi:** `train/dataset_metadata/notes.json`

Berisi catatan dataset dalam format JSON:
```json
{
  "dataset": {
    "name": "Sawo Ripeness Detection",
    "version": "1.0",
    "created": "2026-05-16",
    "annotator": "Tim Labeling"
  },
  "statistics": {
    "total_images": 150,
    "training_images": 120,
    "validation_images": 30,
    "total_bounding_boxes": 450
  },
  "classes": {
    "0": {"name": "belum_matang"},
    "1": {"name": "setengah_matang"},
    "2": {"name": "matang"}
  }
}
```

**Cara menggunakan:**
- Template sudah ada di file `notes.json`
- Update field `statistics` setelah export dari Label Studio
- Gunakan untuk dokumentasi dan reference

### **📦 export.json**
**Lokasi:** `train/dataset_metadata/export.json`

File PENTING dari Label Studio yang berisi:
- Metadata semua gambar
- Semua bounding box coordinates
- Label class untuk setiap box

**Cara menggunakan:**
- Copy dari export Label Studio
- Simpan di `dataset_metadata/` sebagai backup
- Script `convert_label_studio.py` akan menggunakan file ini

### **data.yaml**
**Lokasi:** `train/dataset/data.yaml`

Auto-generated oleh training script. Berisi konfigurasi YOLO:
```yaml
path: /path/to/train/dataset
train: images/train
val: images/val
nc: 3
names:
  0: belum_matang
  1: setengah_matang
  2: matang
```

---

## ✅ Step-by-Step Cara Menyimpan

### **1. Export dari Label Studio**
```
label_studio_export.zip
├── image/
├── label/
├── classes.txt     ← COPY INI
└── export.json     ← COPY INI (PENTING!)
```

### **2. Copy ke Folder Training**

Ekstrak ZIP, lalu copy file-file:
```
train/dataset_metadata/
├── classes.txt         ← Copy dari Label Studio export
├── notes.json          ← Update manual dengan template
└── export.json         ← Copy dari Label Studio export (PENTING!)
```

### **3. Jalankan Conversion Script**

```bash
cd train
python convert_label_studio.py
```

Script akan membaca file-file di folder `dataset_metadata/` dan:
- Parse `export.json`
- Gunakan `classes.txt` sebagai reference
- Generate label files otomatis di `train/dataset/labels/`

### **4. Verify**

```bash
python setup_dataset.py
```

---

## 📋 Checklist

Pastikan file-file ada di lokasi yang benar:

- [ ] `train/dataset_metadata/classes.txt` - ✓ Ada (copy dari Label Studio)
- [ ] `train/dataset_metadata/notes.json` - ✓ Ada (update statistics)
- [ ] `train/dataset_metadata/export.json` - ✓ Ada (PENTING!)
- [ ] `train/dataset/images/train/` - ✓ Berisi gambar
- [ ] `train/dataset/images/val/` - ✓ Berisi gambar

---

## 🚀 Struktur Lengkap Setelah Setup

```
train/
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   │   ├── sawo_001.jpg
│   │   │   ├── sawo_002.jpg
│   │   │   └── ... (120 images)
│   │   └── val/
│   │       ├── sawo_121.jpg
│   │       ├── sawo_122.jpg
│   │       └── ... (30 images)
│   ├── labels/
│   │   ├── train/
│   │   │   ├── sawo_001.txt
│   │   │   ├── sawo_002.txt
│   │   │   └── ... (120 labels)
│   │   └── val/
│   │       ├── sawo_121.txt
│   │       ├── sawo_122.txt
│   │       └── ... (30 labels)
│   └── data.yaml
│
├── dataset_metadata/
│   ├── classes.txt
│   ├── notes.json
│   └── export.json
│
├── runs/
│   └── sawo_detection/
│       ├── weights/
│       │   ├── best.pt
│       │   └── best.onnx
│       ├── results.json
│       └── TRAINING_REPORT.json
│
└── [scripts]
```

---

## 💡 Tips

**Jangan sampai:**
❌ Jangan langsung copy `export.json` ke `train/dataset/`
❌ Jangan mix file Label Studio dengan YOLO format files

**Benar:**
✅ Simpan Label Studio files di `train/dataset_metadata/` (backup/reference)
✅ Biarkan script auto-generate YOLO format di `train/dataset/labels/`

---

## 🔄 Workflow Lengkap

1. **Export Label Studio** → dapat ZIP
2. **Ekstrak** → dapat folder `label_studio_export`
3. **Copy ke metadata**: 
   - `classes.txt` → `train/dataset_metadata/`
   - `notes.txt` → `train/dataset_metadata/`
   - `export.json` → `train/dataset_metadata/`
   - `image/` → keep in temp folder
4. **Run conversion**:
   ```bash
   python convert_label_studio.py
   ```
5. **Verify**:
   ```bash
   python setup_dataset.py
   ```
6. **Train**:
   ```bash
   python train_local.py
   # atau upload ke Colab
   ```

---

**Semua jelas? 🎯**
