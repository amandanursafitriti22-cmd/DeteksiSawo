# 📂 Dataset Metadata Folder

Folder ini berisi file-file reference dan dokumentasi dari Label Studio export.

## 📁 Isi Folder

- **`classes.txt`** - Daftar semua class (copy dari Label Studio)
- **`notes.json`** - Catatan dataset dalam format JSON (dokumentasi)
- **`export.json`** - File utama dari Label Studio export (PENTING!)
- **`STRUKTUR_FOLDER.md`** - Dokumentasi struktur folder lengkap

## 🎯 Fungsi

Folder ini menyimpan:
✅ Backup file Label Studio export
✅ Dokumentasi dataset
✅ Reference untuk class names
✅ Catatan tentang dataset

## 🔄 Workflow

1. **Export dari Label Studio** → dapatkan folder dengan:
   - `image/` - Gambar
   - `label/` - Metadata per file
   - `classes.txt` - Daftar class
   - `notes.txt` - Catatan
   - `export.json` - Main export file

2. **Copy ke folder ini:**
   ```
   train/dataset_metadata/
   ├── classes.txt       ← Copy
   ├── notes.txt         ← Copy
   ├── export.json       ← Copy (PENTING!)
   └── ...
   ```

3. **Conversion script akan:**
   - Membaca `export.json`
   - Menggunakan `classes.txt` sebagai reference
   - Menghasilkan YOLO format di `train/dataset/labels/`

## 📝 File Format

### classes.txt
```
belum_matang
setengah_matang
matang
```

### notes.txt
```
Dataset: Sawo Ripeness Detection
Created: 2026-05-16
Total images: 150
...
```

### export.json
File JSON besar yang berisi semua metadata dan annotations dari Label Studio.

---

## 💾 Storage

```
train/
├── dataset_metadata/          ← Folder INI
│   ├── classes.txt
│   ├── notes.txt
│   ├── export.json
│   └── STRUKTUR_FOLDER.md
│
└── dataset/                   ← Data training
    ├── images/
    ├── labels/
    └── data.yaml
```

---

## ⚠️ Penting!

- **Jangan hapus `export.json`** - File ini dibutuhkan untuk conversion
- **Backup file-file ini** sebelum menjalankan conversion script
- **classes.txt harus match** dengan yang ada di Label Studio

---

## 🚀 Next Step

Setelah file-file ada di folder ini, jalankan:

```bash
cd ../
python convert_label_studio.py
```

---

**Last updated: 2026-05-16**
