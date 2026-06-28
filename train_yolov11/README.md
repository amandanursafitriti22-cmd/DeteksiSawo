# 🍌 YOLOv11 Training - Deteksi Kematangan Buah Sawo

Folder ini **KHUSUS** untuk training model **YOLOv11** di Google Colab.

> ⚠️ Folder `/train/` yang sudah ada adalah fallback **YOLOv8**. Jangan dicampur!

---

## 📁 Struktur Folder

```
train_yolov11/
├── 📄 README.md                ← File ini
├── 📓 yolov11.ipynb            ← Notebook Colab (UPLOAD INI)
│
├── 📂 data/                    ← ISI FOLDER INI → ZIP jadi data.zip
│   ├── 📄 classes.txt          ← Daftar kelas
│   ├── 📄 notes.json           ← Metadata project
│   ├── 📂 images/
│   │   ├── train/              ← Gambar training (80%)
│   │   └── val/                ← Gambar validasi (20%)
│   └── 📂 labels/
│       ├── train/              ← Label training (.txt YOLO)
│       └── val/                ← Label validasi (.txt YOLO)
│
└── 📂 results/                 ← OUTPUT dari training (auto-generated)
    ├── weights/
    │   ├── best.pt
    │   └── last.pt
    ├── best.onnx
    ├── confusion_matrix.png
    ├── results.png
    ├── results.csv
    └── ...
```

---

## 🚀 Cara Pakai

### 1. Siapkan Dataset
- Letakkan gambar di `data/images/train/` dan `data/images/val/`
- Letakkan label di `data/labels/train/` dan `data/labels/val/`

### 2. ZIP folder data
```
# ZIP isi folder data/ menjadi data.zip
# Saat di-extract, harus jadi:
#   data/images/train/...
#   data/images/val/...
#   data/labels/train/...
#   data/labels/val/...
#   data/classes.txt
#   data/notes.json
```

### 3. Upload ke Colab
Upload 2 file saja:
1. **`yolov11.ipynb`** → Open with Google Colab
2. **`data.zip`** → Upload ke Colab runtime (atau Google Drive)

### 4. Jalankan Notebook
Ikuti instruksi di notebook dari atas ke bawah.

### 5. Download Hasil
Ambil `best.onnx` → copy ke `public/models/best.onnx` di project React.

---

## 🔢 Kelas Deteksi

| ID | Nama YOLO       | Display    | Keterangan                     |
|----|----------------|------------|--------------------------------|
| 0  | `matang`       | Matang     | Buah sawo matang               |
| 1  | `belum_matang` | Mentah     | Buah sawo belum matang         |
