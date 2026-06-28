# SawoVision

Sistem berbasis web untuk **deteksi dan klasifikasi tingkat kematangan buah sawo
(_Manilkara zapota_) secara real-time** menggunakan **YOLOv11**, berjalan 100%
di browser dengan **ONNX Runtime Web**.

> Implementasi proposal skripsi: _"Deteksi dan Klasifikasi Tingkat Kematangan
> Buah Sawo Menggunakan Algoritma YOLOv11 Secara Real-Time Berbasis Web"_.

## Fitur

- **Live Webcam Detection** — bounding box, label kelas, confidence, FPS counter
- **Image & Video Upload** — proses file lokal di browser
- **Riwayat Deteksi** — tersimpan di `localStorage`, export JSON / PDF
- **Dashboard Statistik** — pie chart distribusi kelas, bar chart 7 hari terakhir
- **Halaman Informasi Kematangan** — panduan visual + tabel ciri tiap kelas
- **Pengaturan** — confidence/IoU threshold, toggle kelas, kamera, dark mode
- **Privasi penuh** — tidak ada frame yang dikirim ke server

## Tech Stack

- **Framework**: TanStack Start (React 19 + Vite 7) di Cloudflare Workers
- **UI**: Tailwind CSS v4, shadcn/ui, Radix UI, Framer Motion, lucide-react
- **State**: Zustand (persisted)
- **Inference**: `onnxruntime-web` (WASM) — backend WebGL otomatis bila tersedia
- **Charts**: Recharts
- **Export PDF**: jsPDF
- **TypeScript** strict mode

## Tiga Kelas Kematangan

| Kelas              | Ciri Visual                                       |
| ------------------ | ------------------------------------------------- |
| `mentah`           | Kulit hijau, keras, banyak getah putih            |
| `setengah_matang`  | Hijau kekuningan, mulai melunak, aroma samar      |
| `matang`           | Kulit cokelat sawo, lunak, manis dan beraroma     |

## Menjalankan Lokal

```bash
bun install
bun run dev
```

Buka `http://localhost:5173`.

## Memasang Model

Aplikasi memuat model dari `public/models/best.onnx`. Jika file belum ada,
sistem otomatis berjalan dalam **Mode Demo** (dummy detector) sehingga UI tetap
bisa diuji.

### 1. Train YOLOv11

```bash
pip install ultralytics
yolo train model=yolo11n.pt data=sawo.yaml imgsz=640 epochs=100
```

`sawo.yaml`:

```yaml
path: ./datasets/sawo
train: images/train
val: images/val
names:
  0: mentah
  1: setengah_matang
  2: matang
```

### 2. Export ke ONNX

```bash
yolo export model=runs/detect/train/weights/best.pt format=onnx opset=12 imgsz=640 simplify=True
```

### 3. Copy ke project

```bash
mv best.onnx public/models/best.onnx
```

Reload app — badge akan berubah dari "Mode Demo" ke "Model: best.onnx".

## Struktur Project

```
src/
├── routes/             # File-based routing (TanStack)
│   ├── __root.tsx      # Layout, navbar, theme, toaster
│   ├── index.tsx       # Landing page
│   ├── detect.tsx      # Live webcam detection
│   ├── upload.tsx      # Upload image/video
│   ├── history.tsx     # Riwayat + export
│   ├── dashboard.tsx   # Statistik
│   ├── info.tsx        # Panduan kematangan
│   └── settings.tsx    # Pengaturan
├── components/
│   ├── layout/         # Navbar, Footer, ThemeToggle
│   ├── detection/      # WebcamDetector, UploadDetector
│   └── ui/             # shadcn/ui
├── lib/
│   ├── yolo/
│   │   ├── session.ts      # ONNX session loader (lazy)
│   │   ├── preprocess.ts   # Letterbox + NCHW normalize
│   │   ├── postprocess.ts  # Decode + NMS + scale-back
│   │   ├── draw.ts         # Canvas overlay
│   │   └── types.ts        # ClassId, BBox, Detection
│   ├── export.ts       # Export JSON / PDF
│   └── theme.tsx       # Theme sync
├── stores/             # Zustand (settings, history)
└── styles.css          # Design tokens (oklch)
```

## Kustomisasi Warna

Edit `src/styles.css`. Token utama:

- `--primary` — hijau alami
- `--accent` — cokelat sawo
- `--background` — krem hangat (light) / hijau gelap (dark)
- `--ripe-unripe` / `--ripe-half` / `--ripe-ripe` — warna per kelas

## Performance

Target: ≥15 FPS pada laptop modern dengan model `yolo11n` ONNX.
Tips:

- Gunakan model `nano` (`yolo11n`), bukan `s/m/l`
- Pastikan `imgsz=640` saat export
- Tutup tab/aplikasi berat lain
- Browser modern (Chrome, Edge, Safari, Firefox)

## Lisensi

MIT — bebas digunakan untuk keperluan akademik dan komersial.
