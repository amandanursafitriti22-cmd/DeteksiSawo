# 📂 Dataset Folder - Struktur Training Data

Folder ini siap untuk menyimpan gambar dan label hasil export dari Label Studio.

## 📁 Struktur Folder

```
train/dataset/
├── images/
│   ├── train/          ← Paste gambar training di sini (80%)
│   └── val/            ← Paste gambar validation di sini (20%)
├── labels/
│   ├── train/          ← Paste label training di sini (.txt files)
│   └── val/            ← Paste label validation di sini (.txt files)
├── data.yaml           ← Auto-generated oleh script
└── README.md           ← File ini
```

---

## 🎯 Cara Pakai

### **Step 1: Export dari Label Studio**

Export dataset dari Label Studio dalam format **YOLO**:
- Gambar: `image/` folder
- Label: `*.txt` files
- Metadata: `classes.txt`, `export.json`

### **Step 2: Manual Split (Jika Perlu)**

Jika Label Studio tidak auto-split, pisahkan manual:
- **80% → Train**
  - Gambar → `train/dataset/images/train/`
  - Label → `train/dataset/labels/train/`

- **20% → Validation**
  - Gambar → `train/dataset/images/val/`
  - Label → `train/dataset/labels/val/`

### **Step 3: Verify**

Pastikan:
```
✅ Setiap gambar punya label dengan nama yang sama
   Contoh: sawo_001.jpg ↔ sawo_001.txt

✅ Label dalam format YOLO (bukan XML, JSON, atau format lain)
   Format: class_id center_x center_y width height
   Contoh: 0 0.5 0.5 0.3 0.4

✅ Jumlah train:val ≈ 80:20
   Contoh: 120 train, 30 val

✅ Semua gambar di images/{train,val}/
✅ Semua label di labels/{train,val}/
```

### **Step 4: Verify dengan Script**

```bash
cd ../
python setup_dataset.py
```

### **Step 5: Train**

```bash
python train_local.py
# atau upload ke Colab
```

---

## 📋 Checklist Sebelum Training

- [ ] Gambar training ada di `images/train/`
- [ ] Gambar validation ada di `images/val/`
- [ ] Label training ada di `labels/train/`
- [ ] Label validation ada di `labels/val/`
- [ ] Jumlah gambar = jumlah label di setiap folder
- [ ] Format label sudah YOLO (bukan format lain)
- [ ] Metadata files ada di `train/dataset_metadata/`:
  - [ ] `classes.txt`
  - [ ] `export.json`
  - [ ] `notes.json` (updated)

---

## 🔍 Format Label YOLO

File `.txt` untuk setiap gambar:

```
class_id center_x center_y width height
0 0.512 0.445 0.123 0.234
2 0.612 0.545 0.143 0.254
```

**Penjelasan:**
- `class_id`: 0=belum_matang, 1=setengah_matang, 2=matang
- `center_x`, `center_y`: Koordinat pusat box (0-1 normalized)
- `width`, `height`: Lebar dan tinggi box (0-1 normalized)

**Contoh gambar dengan 2 bounding box:**
```
1 0.25 0.35 0.15 0.20
2 0.65 0.70 0.18 0.25
```

---

## 💡 Tips

**Jangan:**
❌ Campur gambar train dan val di 1 folder
❌ Gunakan format label selain YOLO
❌ Hapus file label jika tidak ada bounding box

**Lakukan:**
✅ Pisahkan 80% train, 20% val
✅ Gunakan format YOLO normalized
✅ Pastikan setiap gambar punya label (minimal 1 bounding box)

---

## 🚀 Struktur Lengkap Siap Dipakai

```
Project-Sawo/
└── train/
    ├── dataset/                          ← Folder ini
    │   ├── images/
    │   │   ├── train/                   ← Paste gambar training
    │   │   │   ├── sawo_001.jpg
    │   │   │   ├── sawo_002.jpg
    │   │   │   └── ... (120 images)
    │   │   └── val/                     ← Paste gambar validation
    │   │       ├── sawo_121.jpg
    │   │       └── ... (30 images)
    │   ├── labels/
    │   │   ├── train/                   ← Paste label training
    │   │   │   ├── sawo_001.txt
    │   │   │   ├── sawo_002.txt
    │   │   │   └── ... (120 labels)
    │   │   └── val/                     ← Paste label validation
    │   │       ├── sawo_121.txt
    │   │       └── ... (30 labels)
    │   └── data.yaml                    ← Auto-generated
    │
    ├── dataset_metadata/
    │   ├── classes.txt
    │   ├── export.json
    │   └── notes.json
    │
    ├── convert_label_studio.py
    ├── setup_dataset.py
    ├── train_local.py
    └── ...
```

---

**Siap paste gambar dan label? 🎉**
