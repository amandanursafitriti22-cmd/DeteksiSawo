# 🏷️ Menggunakan Export Label Studio

Panduan lengkap untuk menggunakan hasil export dari Label Studio dan menyiapkannya untuk training YOLOv11.

## 📋 Daftar Isi
1. [Struktur Export Label Studio](#struktur-export-label-studio)
2. [File-file yang Dihasilkan](#file-file-yang-dihasilkan)
3. [Cara Setup](#cara-setup)
4. [Troubleshooting](#troubleshooting)

---

## 📁 Struktur Export Label Studio

Ketika Anda export project dari Label Studio, struktur folder-nya seperti ini:

```
label_studio_export/
├── image/                    ← Folder berisi semua gambar yang sudah di-bounding box
│   ├── image_001.jpg
│   ├── image_002.jpg
│   ├── image_003.png
│   └── ... (semua gambar)
│
├── label/                    ← Folder berisi metadata per gambar (JSON)
│   ├── image_001.json
│   ├── image_002.json
│   ├── image_003.json
│   └── ...
│
├── export.json               ← MAIN FILE: Semua data & annotations
├── classes.txt               ← Daftar class (opsional)
└── notes.txt                 ← Catatan (opsional)
```

---

## 📄 File-file yang Dihasilkan

### 1. **export.json** (PENTING!)
File utama yang berisi:
- Metadata setiap gambar
- Semua bounding boxes
- Label class untuk setiap box
- User yang menganotasi
- Timestamp

**Format:**
```json
[
  {
    "id": 1,
    "data": {
      "image": "/data/upload/1/image_001.jpg",
      "image_name": "image_001.jpg"
    },
    "annotations": [{
      "id": "anno_1",
      "completed_by": 1,
      "result": [{
        "value": {
          "x": 10,
          "y": 20,
          "width": 100,
          "height": 150,
          "rotation": 0
        },
        "from_name": "label",
        "to_name": "image",
        "type": "rectanglelabels",
        "labels": {
          "choices": ["belum_matang"]
        }
      }]
    }]
  }
]
```

### 2. **image/** (Gambar)
Folder berisi semua gambar original yang sudah Anda annotate di Label Studio.

**Format:** JPG, PNG, BMP, etc.

### 3. **label/** (Per-image JSON)
Folder berisi JSON metadata untuk setiap gambar (opsional, tidak diperlukan untuk training).

### 4. **classes.txt** (Opsional)
Daftar semua class yang ada:
```
belum_matang
setengah_matang
matang
```

### 5. **notes.txt** (Opsional)
Catatan umum tentang project.

---

## 🔧 Cara Setup - Step by Step

### **Step 1: Export dari Label Studio**

1. Buka Label Studio web interface
2. Di project Anda, click **Export**
3. Pilih format: **JSON** atau **JSON-MIN**
4. Download file ZIP

```
📦 label_studio_export.zip
 └─ Ekstrak di komputer Anda
```

### **Step 2: Copy Ke Folder Training**

❌ **JANGAN** langsung copy ke `train/dataset/`

✅ **BENAR**: Copy ke folder sementara terlebih dahulu

```
C:\Users\YourName\Downloads\
└── label_studio_export/
    ├── image/
    ├── label/
    ├── export.json
    └── ...
```

### **Step 3: Jalankan Conversion Script**

**Option A: Interactive Mode**

```bash
cd train
python convert_label_studio.py
```

Akan minta input:
```
📁 Path ke Label Studio export folder: C:\Users\YourName\Downloads\label_studio_export
📁 Path ke training dataset folder: train/dataset

# Script akan otomatis:
# ✓ Membaca export.json
# ✓ Convert koordinat Label Studio → YOLO
# ✓ Split 80% train, 20% validation
# ✓ Copy gambar ke folder train/images/
# ✓ Generate label files ke train/labels/
```

**Option B: Programmatic Mode**

```python
from convert_label_studio import setup_from_label_studio

label_studio_dir = "C:/Users/YourName/Downloads/label_studio_export"
train_dataset_dir = "train/dataset"

setup_from_label_studio(label_studio_dir, train_dataset_dir, val_split=0.2)
```

### **Step 4: Verify Result**

Setelah script selesai, check struktur:

```bash
python train/setup_dataset.py
```

Output seharusnya:
```
✓ Training images: 120
✓ Validation images: 30
✓ Training labels: 120
✓ Validation labels: 30

✅ Dataset siap untuk training!
```

---

## 🎯 Koordinat Conversion

Label Studio menyimpan koordinat dalam **percentage (0-100)**:
```
x = 10      (10% dari kiri)
y = 20      (20% dari atas)
width = 100 (100% lebar box)
height = 150 (150% tinggi box)
```

Script otomatis convert ke **YOLO normalized format (0-1)**:
```
x_center = 0.5
y_center = 0.5
width = 0.3
height = 0.4
```

---

## ✅ Checklist

Sebelum menjalankan script, pastikan:

- [ ] Sudah export project dari Label Studio
- [ ] File `export.json` ada di folder export
- [ ] Folder `image/` berisi gambar-gambar
- [ ] Minimal 20-50 gambar (untuk testing), 200+ ideal
- [ ] Semua gambar sudah di-annotate dengan bounding boxes
- [ ] Label class yang digunakan: belum_matang, setengah_matang, matang

---

## 🐛 Troubleshooting

### ❌ "export.json tidak ditemukan"
**Solusi:**
- Pastikan Anda export sebagai format **JSON** (bukan COCO atau XML)
- Ekstrak file ZIP dengan benar
- File seharusnya ada di root folder export

### ❌ "Image not found"
**Solusi:**
- Pastikan folder `image/` ada dan berisi gambar
- Nama file gambar harus match antara `export.json` dan folder `image/`

### ❌ "Unknown class"
**Solusi:**
- Script expect 3 class: `belum_matang`, `setengah_matang`, `matang`
- Jika Anda gunakan nama berbeda, edit script
- Atau gunakan `classes.txt` untuk reference

### ❌ "Koordinat out of range"
**Warna:** Script otomatis clamp ke [0, 1]
- Ini normal, biasanya terjadi karena rounding error
- Tidak akan mempengaruhi training

### ❌ "Missing labels for some images"
**Solusi:**
- Pastikan semua gambar sudah di-annotate di Label Studio
- Kalau ada gambar tanpa bounding box, tetap akan di-include tapi label file kosong
- Ini OK untuk training (image tanpa object)

---

## 📊 Hasil Akhir

Setelah script selesai, struktur folder akan jadi:

```
train/dataset/
├── images/
│   ├── train/
│   │   ├── image_001.jpg
│   │   ├── image_002.jpg
│   │   └── ... (80% dari gambar)
│   └── val/
│       ├── image_081.jpg
│       ├── image_082.jpg
│       └── ... (20% dari gambar)
└── labels/
    ├── train/
    │   ├── image_001.txt
    │   ├── image_002.txt
    │   └── ...
    └── val/
        ├── image_081.txt
        ├── image_082.txt
        └── ...
```

---

## 🎯 Next Steps

1. ✅ Export dari Label Studio
2. ✅ Jalankan `convert_label_studio.py`
3. ✅ Verify dengan `setup_dataset.py`
4. ✅ Siap untuk training!

```bash
# Validasi
python train/setup_dataset.py

# Lalu training
python train/train_local.py
# atau upload ke Colab
```

---

## 💡 Tips

✓ **Backup** folder label studio export sebelum convert
✓ **Check data.yaml** yang auto-generated di `train/dataset/`
✓ **Balance classes** - pastikan setiap class punya jumlah yang seimbang
✓ **Augmentasi** - YOLOv11 auto-augment during training

---

**Happy Annotating! 🏷️**
