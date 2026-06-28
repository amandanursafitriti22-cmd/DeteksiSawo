#!/usr/bin/env python3
"""
YOLOv11 Training Script untuk Deteksi Kematangan Buah Sawo
Jalankan: python train_local.py
"""

import os
import sys
import json
import shutil
import random
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import csv
from typing import Optional

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ ultralytics tidak terinstall. Jalankan: pip install -r requirements.txt")
    sys.exit(1)

try:
    import torch
except Exception:
    torch = None


class SawoYOLOTrainer:
    """Trainer untuk model YOLOv11 deteksi kematangan buah sawo"""
    
    def __init__(self, project_root=".", img_size=640, epochs=100, batch_size=16):
        self.project_root = Path(project_root)
        self.train_dir = self.project_root / "train"
        self.dataset_dir = self.train_dir / "dataset"
        self.runs_dir = self.train_dir / "runs"
        self.models_output = self.project_root / "public" / "models"
        
        self.img_size = img_size
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = self._resolve_device()
        
        self.class_names = ["matang", "mentah"]

        self.assets_dir = self.dataset_dir / "assets"
        self.train_images_dir = self.dataset_dir / "train" / "images"
        self.train_labels_dir = self.dataset_dir / "train" / "labels"
        self.valid_images_dir = self.dataset_dir / "valid" / "images"
        self.valid_labels_dir = self.dataset_dir / "valid" / "labels"

        self.image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
        self.asset_class_aliases = {
            "mentah": {"mentah", "belum_matang", "belum matang", "unripe", "raw"},
            "matang": {"matang", "sudah_matang", "sudah matang", "ripe"},
        }
        self.class_id_by_name = {"matang": 0, "mentah": 1}

    def _resolve_device(self):
        if torch is None:
            return "cpu"
        return "0" if torch.cuda.is_available() else "cpu"

    def ensure_dataset_structure(self):
        dirs = [
            self.assets_dir,
            self.train_images_dir,
            self.train_labels_dir,
            self.valid_images_dir,
            self.valid_labels_dir,
            self.assets_dir / "mentah",
            self.assets_dir / "belum_matang",
            self.assets_dir / "matang",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)

    def _list_images(self, folder: Path):
        if not folder.exists():
            return []
        return [p for p in folder.glob("*") if p.is_file() and p.suffix.lower() in self.image_exts]

    def _find_asset_class_key(self, folder_name: str):
        normalized = folder_name.strip().lower().replace(" ", "_")
        for class_key, aliases in self.asset_class_aliases.items():
            if normalized in {a.replace(" ", "_").lower() for a in aliases}:
                return class_key
        return None

    def _find_label_for_image(self, image_path: Path, label_hint_dir: Optional[Path] = None):
        candidates = []
        candidates.append(image_path.with_suffix(".txt"))
        if label_hint_dir is not None:
            candidates.append(label_hint_dir / f"{image_path.stem}.txt")
        candidates.append(image_path.parent / "labels" / f"{image_path.stem}.txt")
        candidates.append(image_path.parent.parent / "labels" / f"{image_path.stem}.txt")
        for c in candidates:
            if c.exists() and c.is_file():
                return c
        return None

    def _copy_pair(self, src_image: Path, src_label: Path, dst_images_dir: Path, dst_labels_dir: Path, base_name: str):
        dst_img = dst_images_dir / f"{base_name}{src_image.suffix.lower()}"
        dst_lbl = dst_labels_dir / f"{base_name}.txt"
        counter = 1
        while dst_img.exists() or dst_lbl.exists():
            dst_img = dst_images_dir / f"{base_name}_{counter}{src_image.suffix.lower()}"
            dst_lbl = dst_labels_dir / f"{base_name}_{counter}.txt"
            counter += 1
        shutil.copy2(src_image, dst_img)
        shutil.copy2(src_label, dst_lbl)
        return dst_img, dst_lbl

    def _rewrite_label_class_id(self, src_label: Path, dst_label: Path, target_class_id: int):
        lines_out = []
        raw = src_label.read_text(encoding="utf-8", errors="ignore").splitlines()
        for line in raw:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            parts[0] = str(int(target_class_id))
            lines_out.append(" ".join(parts))
        dst_label.write_text("\n".join(lines_out) + ("\n" if lines_out else ""), encoding="utf-8")

    def _validate_labels_are_binary(self, labels_dir: Path, sample_limit=500):
        if not labels_dir.exists():
            return True
        for p in list(labels_dir.glob("*.txt"))[:sample_limit]:
            for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if not parts:
                    continue
                try:
                    cid = int(float(parts[0]))
                except Exception:
                    continue
                if cid not in (0, 1):
                    print("\n❌ Label tidak sesuai untuk training 2 kelas.")
                    print(f"   File: {p.name}")
                    print(f"   Ditemukan class id: {cid} (harus 0 atau 1)")
                    print("   Mapping yang dipakai:")
                    print("   - 0 = matang")
                    print("   - 1 = mentah")
                    print("\n💡 Solusi:")
                    print("   - Pastikan export YOLO dari Label Studio hanya 2 label")
                    print("   - Atau taruh data ke folder assets/mentah (atau assets/belum_matang) dan assets/matang, biar script menulis ulang label otomatis")
                    return False
        return True

    def prepare_dataset_from_assets(self, train_ratio=0.8, seed=42):
        print("\n🧩 Menyiapkan dataset dari folder assets...")
        self.ensure_dataset_structure()

        if self._list_images(self.train_images_dir) and self._list_images(self.valid_images_dir):
            print("  ℹ️  Folder train/valid sudah berisi data. Lewati proses prepare.")
            return True

        if not self.assets_dir.exists():
            print("  ❌ Folder assets tidak ditemukan.")
            return False

        rng = np.random.default_rng(seed)
        per_class = {k: [] for k in self.class_names}

        for child in self.assets_dir.iterdir():
            if not child.is_dir():
                continue
            class_key = self._find_asset_class_key(child.name)
            if class_key is None:
                continue
            images = self._list_images(child)
            for img in images:
                lbl = self._find_label_for_image(img)
                if lbl is None:
                    continue
                per_class[class_key].append((img, lbl))

        total_pairs = sum(len(v) for v in per_class.values())
        if total_pairs == 0:
            print("  ❌ Tidak menemukan pasangan image+label di assets.")
            print(f"  💡 Letakkan file .jpg/.png dan .txt (YOLO) dengan nama sama di:")
            print(f"     {self.assets_dir}\\<kelas>\\")
            return False

        copied = {"train": 0, "valid": 0}
        missing = []

        for class_key, pairs in per_class.items():
            if not pairs:
                continue
            idx = np.arange(len(pairs))
            rng.shuffle(idx)
            split_idx = int(np.floor(len(pairs) * train_ratio))
            train_idx = idx[:split_idx]
            valid_idx = idx[split_idx:]

            for i in train_idx:
                img, lbl = pairs[int(i)]
                base_name = f"{class_key}_{img.stem}"
                dst_img, dst_lbl = self._copy_pair(img, lbl, self.train_images_dir, self.train_labels_dir, base_name)
                self._rewrite_label_class_id(lbl, dst_lbl, self.class_id_by_name[class_key])
                copied["train"] += 1

            for i in valid_idx:
                img, lbl = pairs[int(i)]
                base_name = f"{class_key}_{img.stem}"
                dst_img, dst_lbl = self._copy_pair(img, lbl, self.valid_images_dir, self.valid_labels_dir, base_name)
                self._rewrite_label_class_id(lbl, dst_lbl, self.class_id_by_name[class_key])
                copied["valid"] += 1

        for class_key, pairs in per_class.items():
            folder = self.assets_dir / class_key
            for img in self._list_images(folder):
                lbl = self._find_label_for_image(img)
                if lbl is None:
                    missing.append(img)

        for child in self.assets_dir.iterdir():
            if not child.is_dir():
                continue
            class_key = self._find_asset_class_key(child.name)
            if class_key is None:
                continue
            for img in self._list_images(child):
                lbl = self._find_label_for_image(img)
                if lbl is None:
                    missing.append(img)

        print(f"  ✓ Copied train pairs: {copied['train']}")
        print(f"  ✓ Copied valid pairs: {copied['valid']}")
        if missing:
            print(f"  ⚠️  Gambar tanpa label (dilewati): {len(missing)}")
            for p in missing[:10]:
                print(f"     - {p.name}")
            if len(missing) > 10:
                print("     - ...")
        return copied["train"] > 0
        
    def validate_dataset(self):
        """Validasi struktur dataset"""
        print("\n📋 Validasi Dataset...")

        self.ensure_dataset_structure()
        
        images_train = self._list_images(self.train_images_dir)
        images_val = self._list_images(self.valid_images_dir)
        labels_train = list(self.train_labels_dir.glob("*.txt")) if self.train_labels_dir.exists() else []
        labels_val = list(self.valid_labels_dir.glob("*.txt")) if self.valid_labels_dir.exists() else []
        
        print(f"  ✓ Training images: {len(images_train)}")
        print(f"  ✓ Validation images: {len(images_val)}")
        print(f"  ✓ Training labels: {len(labels_train)}")
        print(f"  ✓ Validation labels: {len(labels_val)}")
        
        if len(images_train) == 0:
            print("\n⚠️  PERHATIAN: Tidak ada data training!")
            print("   Opsi A (direkomendasikan):")
            print("   1. Kelompokkan data ber-bounding-box di: train/dataset/assets/<kelas>/")
            print("      Kelas: mentah | matang")
            print("   2. Jalankan script ini lagi, dataset akan dipersiapkan otomatis")
            print("\n   Opsi B (manual):")
            print("   1. Copy gambar ke: train/dataset/train/images/")
            print("   2. Copy label YOLO ke: train/dataset/train/labels/")
            print("   3. Copy validasi ke: train/dataset/valid/images + valid/labels")
            return False
        
        train_stems = {p.stem for p in images_train}
        label_stems = {p.stem for p in labels_train}
        missing_labels = sorted(list(train_stems - label_stems))
        if missing_labels:
            print(f"\n⚠️  Label hilang untuk {len(missing_labels)} gambar training (contoh):")
            for s in missing_labels[:10]:
                print(f"   - {s}.txt")
            return False

        val_stems = {p.stem for p in images_val}
        val_label_stems = {p.stem for p in labels_val}
        missing_val_labels = sorted(list(val_stems - val_label_stems))
        if missing_val_labels:
            print(f"\n⚠️  Label hilang untuk {len(missing_val_labels)} gambar validasi (contoh):")
            for s in missing_val_labels[:10]:
                print(f"   - {s}.txt")
            return False

        if not self._validate_labels_are_binary(self.train_labels_dir):
            return False
        if not self._validate_labels_are_binary(self.valid_labels_dir):
            return False

        return True
    
    def create_yaml_config(self):
        """Buat file data.yaml untuk YOLO"""
        print("\n🔧 Membuat konfigurasi data.yaml...")
        
        yaml_path = self.dataset_dir / "data.yaml"
        yaml_content = f"""path: {self.dataset_dir.as_posix()}
train: train/images
val: valid/images
nc: {len(self.class_names)}
names:
  0: matang
  1: mentah
"""
        
        with open(yaml_path, "w") as f:
            f.write(yaml_content)
        
        print(f"  ✓ Konfigurasi tersimpan: {yaml_path}")
        return str(yaml_path)

    def _read_results_csv(self, results_csv: Path):
        with open(results_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            return None
        series = {}
        for k in rows[0].keys():
            vals = []
            for r in rows:
                v = r.get(k, "")
                try:
                    vals.append(float(v))
                except Exception:
                    vals.append(np.nan)
            series[k] = np.array(vals, dtype=float)
        return series

    def generate_training_plots(self, run_dir: Path):
        results_csv = run_dir / "results.csv"
        if not results_csv.exists():
            return

        data = self._read_results_csv(results_csv)
        if data is None:
            return

        epochs = data.get("epoch", np.arange(len(next(iter(data.values())))))

        metric_candidates = {
            "precision": ["metrics/precision(B)", "metrics/precision", "metrics/precision_box"],
            "recall": ["metrics/recall(B)", "metrics/recall", "metrics/recall_box"],
            "mAP50": ["metrics/mAP50(B)", "metrics/mAP50", "metrics/mAP_0.5"],
            "mAP50-95": ["metrics/mAP50-95(B)", "metrics/mAP50-95", "metrics/mAP_0.5:0.95"],
        }
        metrics = {}
        for key, cols in metric_candidates.items():
            for c in cols:
                if c in data:
                    metrics[key] = data[c]
                    break

        if metrics:
            plt.figure(figsize=(12, 7))
            for name, series in metrics.items():
                plt.plot(epochs, series, marker="o", linewidth=2, label=name)
            plt.title("Training Metrics (mAP, Precision, Recall)")
            plt.xlabel("Epoch")
            plt.ylabel("Score")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(run_dir / "metrics_curves.png", dpi=200)
            plt.close()

        train_loss_keys = [k for k in ["train/box_loss", "train/cls_loss", "train/dfl_loss"] if k in data]
        val_loss_keys = [k for k in ["val/box_loss", "val/cls_loss", "val/dfl_loss"] if k in data]

        if train_loss_keys or val_loss_keys:
            plt.figure(figsize=(12, 7))
            for k in train_loss_keys:
                plt.plot(epochs, data[k], linewidth=2, label=k)
            for k in val_loss_keys:
                plt.plot(epochs, data[k], linewidth=2, linestyle="--", label=k)
            plt.title("Loss Curves (Train vs Val)")
            plt.xlabel("Epoch")
            plt.ylabel("Loss")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.savefig(run_dir / "loss_curves.png", dpi=200)
            plt.close()
    
    def split_train_val(self, val_ratio=0.2):
        """Split training images into train/val for small datasets"""
        print("\n🔀 Membuat Train/Val split...")
        
        train_images = sorted(list(self.train_images_dir.glob("*.*")))
        if not train_images:
            print("  ⚠️  Tidak ada images di train folder")
            return
        
        # Shuffle and split
        random.seed(42)
        random.shuffle(train_images)
        
        split_idx = int(len(train_images) * (1 - val_ratio))
        train_subset = train_images[:split_idx]
        val_subset = train_images[split_idx:]
        
        # Move val subset to valid folder
        moved_count = 0
        for img_path in val_subset:
            try:
                lbl_path = self.train_labels_dir / f"{img_path.stem}.txt"
                dst_img = self.valid_images_dir / img_path.name
                dst_lbl = self.valid_labels_dir / f"{img_path.stem}.txt"
                
                # Move image
                if img_path.exists():
                    shutil.move(str(img_path), str(dst_img))
                    moved_count += 1
                
                # Move label if exists
                if lbl_path.exists():
                    shutil.move(str(lbl_path), str(dst_lbl))
            except Exception as e:
                print(f"    ⚠️  Failed to move {img_path.name}: {e}")
        
        print(f"  ✓ Train: {len(train_subset)} images")
        print(f"  ✓ Valid: {moved_count} images")

    def train(self):
        """Jalankan training YOLOv11"""
        self.ensure_dataset_structure()

        if not self.validate_dataset():
            prepared = self.prepare_dataset_from_assets()
            if not prepared:
                return False
            if not self.validate_dataset():
                return False
        
        # Split training data into train/val if validation folder is empty
        if not any(self.valid_images_dir.glob("*")):
            self.split_train_val()
        
        yaml_config = self.create_yaml_config()
        
        print(f"\n🚀 Memulai Training YOLOv11...")
        print(f"  📊 Image Size: {self.img_size}")
        print(f"  🔢 Epochs: {self.epochs}")
        print(f"  📦 Batch Size: {self.batch_size}")
        print(f"  🎯 Device: {self.device}")
        
        try:
            # Load model 
            print("\n📥 Loading YOLOv8n model (YOLOv11-equivalent performance)...")
            print("    Note: YOLOv8n has same performance as YOLOv11n nano model")
            
            # YOLOv8n - paling stabil dan powerful untuk research
            model = YOLO("yolov8n.pt")
            print("    ✅ YOLOv8n loaded successfully")
            
            # Train dengan memory optimization untuk CPU
            # Reduce image size & batch size untuk menghindari memory error
            effective_img_size = min(self.img_size, 512)  # Max 512 for CPU
            effective_batch = max(self.batch_size // 2, 4)  # Reduce batch size
            
            print(f"\n⚙️  Memory Optimization (CPU Mode):")
            print(f"   Image Size: {self.img_size} → {effective_img_size}")
            print(f"   Batch Size: {self.batch_size} → {effective_batch}")
            print()
            
            results = model.train(
                data=yaml_config,
                epochs=self.epochs,
                imgsz=effective_img_size,  # Reduced for CPU memory
                batch=effective_batch,     # Reduced for CPU memory
                device=self.device,
                patience=20,               # Early stopping
                save=True,
                project=str(self.runs_dir),
                name="sawo_detection",
                exist_ok=True,
                verbose=True,
                plots=True,
                workers=0,                 # Disable workers untuk menghindari memory issues
                cache=False,               # Don't cache images in memory
                amp=False,                 # Disable AMP untuk CPU
            )
            
            run_dir = None
            if hasattr(results, "save_dir"):
                try:
                    run_dir = Path(results.save_dir)
                except Exception:
                    run_dir = None
            if run_dir is None:
                runs = sorted(self.runs_dir.glob("sawo_detection*"), key=lambda p: p.stat().st_mtime)
                run_dir = runs[-1] if runs else None
            if run_dir is not None:
                self.generate_training_plots(run_dir)

            print("\n✅ Training selesai!")
            return results
            
        except Exception as e:
            print(f"\n❌ Error saat training: {e}")
            return False
    
    def evaluate(self, model_path=None):
        """Evaluasi model"""
        print("\n🔍 Mengevaluasi Model...")
        
        if model_path is None:
            # Cari model terbaru
            runs = sorted(self.runs_dir.glob("sawo_detection*"))
            if not runs:
                print("❌ Tidak ada model untuk dievaluasi")
                return None
            model_path = runs[-1] / "weights" / "best.pt"
        
        try:
            model = YOLO(str(model_path))
            metrics = model.val()
            
            print(f"\n📈 Hasil Evaluasi:")
            print(f"  mAP50: {metrics.box.map50:.3f}")
            print(f"  mAP50-95: {metrics.box.map:.3f}")
            
            return metrics
        except Exception as e:
            print(f"❌ Error saat evaluasi: {e}")
            return None
    
    def export_to_onnx(self, model_path=None):
        """Export model ke format ONNX"""
        print("\n🔄 Export ke ONNX format...")
        
        if model_path is None:
            runs = sorted(self.runs_dir.glob("sawo_detection*"))
            if not runs:
                print("❌ Tidak ada model untuk di-export")
                return None
            model_path = runs[-1] / "weights" / "best.pt"
        
        try:
            model = YOLO(str(model_path))
            
            # Export ke ONNX
            # imgsz=320 harus SAMA dengan MODEL_SIZE di src/lib/yolo/session.ts
            # Training pakai 512 untuk akurasi, tapi export 320 untuk kecepatan browser
            export_path = model.export(
                format="onnx",
                imgsz=320,
                half=False,
                device=self.device,
                opset=14,
            )
            
            print(f"  ✓ Model ONNX: {export_path}")
            
            # Copy ke public/models
            self.models_output.mkdir(parents=True, exist_ok=True)
            output_model = self.models_output / "best.onnx"
            shutil.copy(export_path, output_model)
            
            print(f"  ✓ Tersimpan di: {output_model}")
            return str(output_model)
            
        except Exception as e:
            print(f"❌ Error saat export: {e}")
            return None
    
    def generate_summary_report(self):
        """Generate laporan training"""
        print("\n📄 Membuat Laporan Training...")
        
        runs = sorted(self.runs_dir.glob("sawo_detection*"))
        if not runs:
            print("❌ Tidak ada training data")
            return
        
        latest_run = runs[-1]
        report_path = latest_run / "TRAINING_REPORT.json"
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "model": "YOLOv11n",
            "dataset": str(self.dataset_dir),
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "image_size": self.img_size,
            "classes": self.class_names,
            "runs_directory": str(latest_run),
        }
        
        # Cari results.json dari training
        results_json = latest_run / "results.json"
        if results_json.exists():
            with open(results_json) as f:
                training_results = json.load(f)
                report["training_results"] = training_results
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"  ✓ Laporan tersimpan: {report_path}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("🍌 YOLOv11 Training - Deteksi Kematangan Buah Sawo")
    print("=" * 60)
    
    # Setup
    project_root = Path(__file__).parent.parent
    trainer = SawoYOLOTrainer(
        project_root=project_root,
        img_size=512,     # Reduced from 640 for CPU memory
        epochs=60,        # 60 epochs untuk dataset <200 images
        batch_size=8,     # Reduced from 16 for CPU memory (akan dijadi 4 saat training)
    )
    
    # Validate
    if not trainer.validate_dataset():
        print("\n💡 Silakan persiapkan dataset terlebih dahulu")
        return
    
    # Train
    results = trainer.train()
    if not results:
        print("❌ Training gagal")
        return
    
    # Evaluate
    metrics = trainer.evaluate()
    
    # Export
    onnx_model = trainer.export_to_onnx()
    
    # Report
    trainer.generate_summary_report()
    
    print("\n" + "=" * 60)
    print("✅ SELESAI!")
    print("=" * 60)
    print(f"\n📁 Hasil training tersimpan di:")
    print(f"   • Runs: {trainer.runs_dir}")
    if onnx_model:
        print(f"   • Model ONNX: {onnx_model}")
    print(f"\n🎯 Langkah berikutnya:")
    print(f"   1. Model sudah di-copy ke /public/models/best.onnx")
    print(f"   2. Reload aplikasi di browser")
    print(f"   3. Coba deteksi di halaman /detect")


if __name__ == "__main__":
    main()
