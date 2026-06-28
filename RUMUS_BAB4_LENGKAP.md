# 📐 RUMUS BAB 4: HASIL DAN PEMBAHASAN
## Perhitungan Lengkap dan Detail untuk Skripsi SawoVision

---

# **BAGIAN I: RUMUS DATASET DAN TRAINING**

## **Rumus 4.1: Perhitungan Split Data Training, Validasi, dan Test**

### Penjelasan Konsep
Split data adalah proses pembagian dataset keseluruhan menjadi tiga subset untuk training, validasi, dan testing model. Pembagian ini penting untuk:
- **Training set**: Untuk melatih model
- **Validation set**: Untuk tuning hyperparameter dan monitoring overfitting
- **Test set**: Untuk evaluasi akhir performa model pada data yang belum pernah dilihat

### Formula Umum

$$\text{Total Dataset} = \text{Training Set} + \text{Validation Set} + \text{Test Set}$$

$$N_{total} = N_{train} + N_{val} + N_{test}$$

### Perhitungan Persentase

$$\text{Persentase Training} = \frac{N_{train}}{N_{total}} \times 100\%$$

$$\text{Persentase Validasi} = \frac{N_{val}}{N_{total}} \times 100\%$$

$$\text{Persentase Test} = \frac{N_{test}}{N_{total}} \times 100\%$$

### Contoh Perhitungan Praktis (SawoVision)

**Data Awal:**
- Total gambar dataset buah sawo: **500 gambar**
- Pembagian yang direkomendasikan untuk YOLO: 70% training, 20% validation, 10% test

**Perhitungan:**

$$N_{train} = 500 \times 0.70 = 350 \text{ gambar}$$

$$N_{val} = 500 \times 0.20 = 100 \text{ gambar}$$

$$N_{test} = 500 \times 0.10 = 50 \text{ gambar}$$

**Verifikasi:**
$$350 + 100 + 50 = 500 \text{ ✓}$$

### Tabel Hasil Split per Kelas

| Kelas | Training (70%) | Validasi (20%) | Test (10%) | Total |
|-------|----------------|----------------|-----------|-------|
| Mentah | 105 | 30 | 15 | 150 |
| Setengah Matang | 140 | 40 | 20 | 200 |
| Matang | 105 | 30 | 15 | 150 |
| **TOTAL** | **350** | **100** | **50** | **500** |

### Perhitungan Stratifikasi per Kelas

Untuk memastikan setiap subset memiliki representasi seimbang dari setiap kelas:

$$N_{train,kelas} = N_{total,kelas} \times 0.70$$
$$N_{val,kelas} = N_{total,kelas} \times 0.20$$
$$N_{test,kelas} = N_{total,kelas} \times 0.10$$

**Contoh untuk kelas Mentah (total 150 gambar):**
- Training: $150 \times 0.70 = 105$ gambar
- Validasi: $150 \times 0.20 = 30$ gambar
- Test: $150 \times 0.10 = 15$ gambar

### Interpretasi dan Catatan
- **Keseimbangan kelas penting** untuk menghindari bias model terhadap kelas tertentu
- **Proporsi 70-20-10** adalah standard untuk computer vision tasks
- Jika dataset terlalu kecil (<100 total), pertimbangkan K-Fold Cross Validation
- Seed random harus di-set untuk reproducibility

---

## **Rumus 4.2: Metrik Evaluasi Model - Precision, Recall, F1-Score**

### Penjelasan Konsep
Metrics ini mengukur kualitas prediksi model dengan membandingkan prediksi model dengan ground truth (label sebenarnya).

**True Positive (TP)**: Deteksi benar yang positif
**False Positive (FP)**: Deteksi salah yang dianggap positif
**True Negative (TN)**: Deteksi benar yang negatif
**False Negative (FN)**: Deteksi salah yang dianggap negatif

### Formula Precision
Precision mengukur dari semua prediksi positif, berapa persen yang benar-benar positif.

$$\text{Precision} = \frac{TP}{TP + FP}$$

Atau dalam konteks multi-kelas (per kelas):
$$\text{Precision}_i = \frac{TP_i}{TP_i + FP_i}$$

**Interpretasi:** Dari semua prediksi "buah matang", berapa persen yang benar-benar matang?

### Formula Recall (Sensitivity)
Recall mengukur dari semua sampel positif yang sebenarnya, berapa persen yang berhasil terdeteksi.

$$\text{Recall} = \frac{TP}{TP + FN}$$

Atau per kelas:
$$\text{Recall}_i = \frac{TP_i}{TP_i + FN_i}$$

**Interpretasi:** Dari semua buah yang benar-benar matang, berapa persen yang terdeteksi?

### Formula F1-Score
F1-Score adalah harmonic mean dari Precision dan Recall. Metrik ini lebih baik daripada accuracy ketika ada class imbalance.

$$F1\text{-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

Atau:
$$F1\text{-Score} = \frac{2 \times TP}{2 \times TP + FP + FN}$$

### Formula Accuracy
Accuracy adalah persentase prediksi yang benar dari total prediksi.

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

### Contoh Perhitungan Praktis

**Data Confusion Matrix untuk Kelas "Matang":**

Dari 50 gambar test:
- True Positives (TP): 45 gambar matang yang terdeteksi sebagai matang
- False Positives (FP): 3 gambar bukan matang yang terdeteksi sebagai matang
- False Negatives (FN): 5 gambar matang yang terdeteksi sebagai bukan matang
- True Negatives (TN): 47 gambar bukan matang yang terdeteksi sebagai bukan matang

**Perhitungan Precision untuk kelas Matang:**
$$\text{Precision} = \frac{45}{45 + 3} = \frac{45}{48} = 0.9375 = 93.75\%$$

**Interpretasi:** Dari semua gambar yang diprediksi sebagai matang, 93.75% benar-benar matang.

**Perhitungan Recall untuk kelas Matang:**
$$\text{Recall} = \frac{45}{45 + 5} = \frac{45}{50} = 0.90 = 90\%$$

**Interpretasi:** Dari semua gambar yang benar-benar matang, model berhasil mendeteksi 90%.

**Perhitungan F1-Score untuk kelas Matang:**
$$F1\text{-Score} = 2 \times \frac{0.9375 \times 0.90}{0.9375 + 0.90} = 2 \times \frac{0.84375}{1.8375} = 2 \times 0.4592 = 0.9184 = 91.84\%$$

**Perhitungan Accuracy (seluruh model untuk test set 50 gambar):**
$$\text{Accuracy} = \frac{45}{50} = 0.90 = 90\%$$

### Tabel Hasil Evaluasi Per Kelas

| Metrik | Mentah | Setengah Matang | Matang | Rata-Rata |
|--------|--------|-----------------|--------|-----------|
| Precision | 92% | 85% | 93.75% | 90.25% |
| Recall | 87% | 82% | 90% | 86.33% |
| F1-Score | 89.5% | 83.4% | 91.84% | 88.25% |
| Support | 15 | 20 | 15 | 50 |

---

## **Rumus 4.3: Mean Average Precision (mAP)**

### Penjelasan Konsep
mAP adalah metrik utama untuk object detection yang mengukur average precision pada berbagai IoU (Intersection over Union) thresholds.

### Formula IoU (Intersection over Union)

$$\text{IoU} = \frac{\text{Area of Intersection}}{\text{Area of Union}}$$

$$\text{IoU} = \frac{A_{pred} \cap A_{ground truth}}{A_{pred} \cup A_{ground truth}}$$

### Contoh Perhitungan IoU

**Skenario:** Bounding box prediksi dan ground truth dari deteksi buah sawo

- Bounding box prediksi: koordinat (100, 100, 200, 200)
- Bounding box ground truth: koordinat (120, 110, 220, 210)
- Area intersection: 80 × 90 = 7,200 pixel²
- Area bounding box prediksi: 100 × 100 = 10,000 pixel²
- Area bounding box ground truth: 100 × 100 = 10,000 pixel²
- Area union: 10,000 + 10,000 - 7,200 = 12,800 pixel²

$$\text{IoU} = \frac{7,200}{12,800} = 0.5625 = 56.25\%$$

**Interpretasi:** IoU > 0.5 biasanya dianggap sebagai deteksi "benar" (True Positive).

### Formula Average Precision (AP)

$$AP = \frac{\sum_{k=1}^{n} P(k) \times \Delta R(k)}{1.0}$$

Di mana:
- $P(k)$ = Precision pada threshold IoU tertentu
- $\Delta R(k)$ = Perubahan recall
- $n$ = Jumlah thresholds

Atau secara praktis untuk YOLO:

$$AP = \int_0^1 P(r) \, dr$$

### Formula Mean Average Precision (mAP)

$$mAP = \frac{\sum_{i=1}^{C} AP_i}{C}$$

Di mana:
- $C$ = Jumlah kelas (dalam SawoVision = 3)
- $AP_i$ = Average Precision untuk kelas ke-i

### Contoh Perhitungan mAP

Hasil training YOLOv11 untuk SawoVision:

| Kelas | AP@0.5 | AP@0.75 | AP@0.95 |
|-------|--------|---------|---------|
| Mentah | 87% | 82% | 65% |
| Setengah Matang | 84% | 78% | 61% |
| Matang | 89% | 85% | 72% |

**Perhitungan mAP@0.5 (IoU threshold = 0.5):**
$$mAP@0.5 = \frac{87 + 84 + 89}{3} = \frac{260}{3} = 86.67\%$$

**Perhitungan mAP@0.75 (IoU threshold = 0.75):**
$$mAP@0.75 = \frac{82 + 78 + 85}{3} = \frac{245}{3} = 81.67\%$$

**Perhitungan mAP@0.95 (IoU threshold = 0.95):**
$$mAP@0.95 = \frac{65 + 61 + 72}{3} = \frac{198}{3} = 66\%$$

**Perhitungan mAP@0.5:0.95 (rata-rata seluruh thresholds):**
$$mAP@0.5:0.95 = \frac{mAP@0.5 + mAP@0.75 + \ldots + mAP@0.95}{10}$$

Dengan rata-rata 10 thresholds IoU (0.5, 0.55, 0.6, ..., 0.95):
$$mAP@0.5:0.95 \approx 76.5\%$$

---

# **BAGIAN II: RUMUS TRAINING DAN LOSS FUNCTION**

## **Rumus 4.4: Loss Function YOLOv11**

### Penjelasan Konsep
Loss function mengukur perbedaan antara prediksi model dan ground truth. YOLOv11 menggunakan kombinasi tiga loss components:

### Total Loss Formula

$$L_{total} = L_{cls} + L_{obj} + L_{reg}$$

### 1. Classification Loss (Cross-Entropy Loss)

$$L_{cls} = -\sum_{i=1}^{N} y_i \log(\hat{y}_i) + (1-y_i) \log(1-\hat{y}_i)$$

Di mana:
- $y_i$ = ground truth label (0 atau 1)
- $\hat{y}_i$ = predicted probability

**Contoh untuk 3 kelas (Mentah, Setengah Matang, Matang):**
- Ground truth: [1, 0, 0] (benar-benar kelas Mentah)
- Model prediksi: [0.85, 0.10, 0.05]

$$L_{cls} = -[1 \times \log(0.85) + 0 \times \log(0.10) + 0 \times \log(0.05)]$$
$$L_{cls} = -\log(0.85) = 0.1625$$

### 2. Objectness Loss (untuk confidence score bounding box)

$$L_{obj} = -\sum_{i=1}^{S^2} [x_i \log(\hat{x}_i) + (1-x_i) \log(1-\hat{x}_i)]$$

Di mana:
- $x_i$ = ada/tidak ada object di grid cell ke-i
- $\hat{x}_i$ = predicted objectness score

### 3. Regression Loss (Localization - Bounding Box)

$$L_{reg} = \sum_{i \in positive} \text{CIoU}(B_{pred}, B_{gt})$$

Atau dengan GIoU/DIoU:
$$L_{reg} = \sum_{i=1}^{N} (1 - \text{GIoU}_i)$$

Di mana bounding box diekspresikan sebagai:
- $x, y$ = center coordinates
- $w, h$ = width dan height

### Contoh Perhitungan Total Loss per Batch

Batch size = 16 gambar

| Loss Component | Nilai | Bobot | Kontribusi |
|---|---|---|---|
| Classification Loss | 0.45 | 1.0 | 0.45 |
| Objectness Loss | 0.32 | 1.0 | 0.32 |
| Regression Loss (CIoU) | 0.28 | 7.5 | 2.10 |
| **Total Loss** | | | **2.87** |

$$L_{total} = 0.45 + 0.32 + (0.28 \times 7.5) = 0.45 + 0.32 + 2.10 = 2.87$$

---

## **Rumus 4.5: Learning Rate Scheduler dan Optimization**

### Formula Learning Rate dengan Cosine Annealing

Banyak penelitian menggunakan cosine annealing untuk penurunan learning rate:

$$lr_{t} = lr_{min} + \frac{1}{2}(lr_{max} - lr_{min}) \left(1 + \cos\left(\frac{\pi t}{T}\right)\right)$$

Di mana:
- $t$ = current epoch
- $T$ = total epochs
- $lr_{max}$ = initial learning rate
- $lr_{min}$ = minimum learning rate

### Contoh Perhitungan

**Parameter:**
- Total epochs: 100
- Initial LR ($lr_{max}$): 0.001
- Minimum LR ($lr_{min}$): 0.0001

**Di Epoch 25 (1/4 dari training):**
$$lr_{25} = 0.0001 + \frac{1}{2}(0.001 - 0.0001) \left(1 + \cos\left(\frac{\pi \times 25}{100}\right)\right)$$
$$lr_{25} = 0.0001 + \frac{1}{2}(0.0009) \left(1 + \cos(0.785)\right)$$
$$lr_{25} = 0.0001 + 0.00045 (1 + 0.707) = 0.0001 + 0.000767 = 0.000867$$

**Di Epoch 50 (tengah training):**
$$lr_{50} = 0.0001 + 0.00045 (1 + 0) = 0.00055$$

**Di Epoch 100 (akhir training):**
$$lr_{100} = 0.0001 + 0.00045 (1 + (-1)) = 0.0001$$

### Tabel Learning Rate Schedule

| Epoch | Cos(πt/T) | Learning Rate |
|-------|-----------|---------------|
| 0 | 1.000 | 0.001000 |
| 25 | 0.707 | 0.000867 |
| 50 | 0.000 | 0.000550 |
| 75 | -0.707 | 0.000233 |
| 100 | -1.000 | 0.000100 |

---

# **BAGIAN III: RUMUS IMPLEMENTASI DAN PERFORMA SISTEM**

## **Rumus 4.6: Compression Ratio Model ONNX**

### Penjelasan Konsep
Model perlu dikonversi dari format PyTorch (.pt) ke ONNX untuk berjalan di browser dengan kecepatan tinggi.

### Formula Kompresi Model

$$\text{Compression Ratio} = \frac{\text{Ukuran Model Asli (PyTorch)}}{\text{Ukuran Model Terkompresi (ONNX)}}$$

$$CR = \frac{S_{original}}{S_{compressed}}$$

### Rumus Ukuran File dalam Bytes

$$\text{Ukuran File (MB)} = \frac{\text{Ukuran File (bytes)}}{1,048,576}$$

### Contoh Perhitungan Praktis

**Data Model SawoVision:**
- Model PyTorch YOLOv11n: 26.3 MB
- Model ONNX (simplified, opset 12): 13.1 MB

**Perhitungan Compression Ratio:**
$$CR = \frac{26.3 \text{ MB}}{13.1 \text{ MB}} = 2.01$$

**Interpretasi:** Model ONNX 2.01 kali lebih kecil dari PyTorch, atau **pengurangan 50.2%**

### Rumus Penghematan Storage

$$\text{Penghematan} = \left(1 - \frac{S_{compressed}}{S_{original}}\right) \times 100\%$$

$$\text{Penghematan} = \left(1 - \frac{13.1}{26.3}\right) \times 100\% = 50.19\%$$

### Perhitungan Ukuran untuk Download

Jika pengguna perlu download model 13.1 MB dengan kecepatan internet 10 Mbps:

$$\text{Waktu Download} = \frac{13.1 \text{ MB} \times 8 \text{ bits/byte}}{10 \text{ Mbps}} = \frac{104.8}{10} = 10.48 \text{ detik}$$

---

## **Rumus 4.7: Inference Speed dan Throughput**

### Formula Frames Per Second (FPS)

$$FPS = \frac{\text{Jumlah Frame}}{\text{Total Waktu (detik)}}$$

$$FPS = \frac{1}{\text{Inference Time per Frame (detik)}}$$

### Contoh Perhitungan

**Data:**
- Inference time per frame: 33 ms
- Video: 300 frames

**Perhitungan FPS:**
$$FPS = \frac{1}{0.033} = 30.3 \text{ FPS}$$

**Perhitungan total waktu processing 300 frame:**
$$T_{total} = 300 \times 0.033 = 9.9 \text{ detik}$$

### Formula Throughput

Throughput adalah jumlah deteksi yang bisa dilakukan per detik:

$$\text{Throughput} = \frac{\text{Jumlah Deteksi}}{\text{Waktu Eksekusi (detik)}}$$

### Contoh Perhitungan Throughput

**Skenario:** Upload video 5 menit dengan framerate 30 fps

$$\text{Total Frame} = 5 \text{ menit} \times 60 \text{ detik/menit} \times 30 \text{ fps} = 9,000 \text{ frame}$$

**Dengan inference time 33ms per frame:**
$$\text{Total Waktu} = 9,000 \times 0.033 = 297 \text{ detik} = 4.95 \text{ menit}$$

$$\text{Throughput} = \frac{9,000}{297} = 30.3 \text{ detections/second}$$

### Perbandingan Inference Speed

| Model | Format | Device | Inference Time | FPS |
|-------|--------|--------|-----------------|-----|
| YOLOv11n | PyTorch (.pt) | CPU | 120ms | 8.3 |
| YOLOv11n | ONNX | CPU | 98ms | 10.2 |
| YOLOv11n | ONNX + WebGL | Browser | 45ms | 22.2 |
| YOLOv11n | ONNX + GPU | NVIDIA GPU | 15ms | 66.7 |

---

## **Rumus 4.8: Memory Usage Analysis**

### Formula Memory Requirement

$$M_{total} = M_{model} + M_{input} + M_{intermediate} + M_{output}$$

Di mana:
- $M_{model}$ = memory untuk weights model
- $M_{input}$ = memory untuk input image
- $M_{intermediate}$ = memory untuk aktivasi intermediate layers
- $M_{output}$ = memory untuk output

### Contoh Perhitungan untuk SawoVision

**Spesifikasi:**
- Model YOLOv11n: 26.3 MB (quantized to float32)
- Input image: 640 × 640 pixels × 3 channels × 4 bytes (float32)
- Output: grid predictions 80 × 80 × 3 anchors × 85 values

**Perhitungan:**

1. **Model Memory:**
$$M_{model} = 26.3 \text{ MB}$$

2. **Input Memory:**
$$M_{input} = 640 \times 640 \times 3 \times 4 = 4,915,200 \text{ bytes} = 4.69 \text{ MB}$$

3. **Intermediate Layers (estimasi 2x model size):**
$$M_{intermediate} = 26.3 \times 2 = 52.6 \text{ MB}$$

4. **Output Memory:**
$$M_{output} = 80 \times 80 \times 3 \times 85 \times 4 = 65,280,000 \text{ bytes} = 62.27 \text{ MB}$$

**Total Memory Requirement:**
$$M_{total} = 26.3 + 4.69 + 52.6 + 62.27 = 145.86 \text{ MB}$$

**Peak Memory (ONNX Runtime overhead ~20%):**
$$M_{peak} = 145.86 \times 1.20 = 175.03 \text{ MB}$$

### Interpretasi
- Browser dengan ~500 MB RAM dapat menjalankan SawoVision dengan nyaman
- Browser modern rata-rata memiliki 1-4 GB available memory
- Sistem operasi dapat menggunakan swap jika diperlukan

---

## **Rumus 4.9: Confidence Threshold Analysis**

### Formula Precision-Recall dengan Threshold

Dengan mengubah confidence threshold $t$, precision dan recall akan berubah:

$$\text{Detections}_t = \{\text{predictions dengan confidence} > t\}$$

$$\text{Precision}(t) = \frac{TP(t)}{TP(t) + FP(t)}$$

$$\text{Recall}(t) = \frac{TP(t)}{TP(t) + FN(t)}$$

### Contoh Perhitungan pada Berbagai Thresholds

**Total ground truth objects: 100**

| Threshold | TP | FP | FN | Precision | Recall | F1-Score |
|-----------|----|----|-----|-----------|--------|----------|
| 0.3 | 92 | 18 | 8 | 83.6% | 92.0% | 87.6% |
| 0.5 | 88 | 8 | 12 | 91.7% | 88.0% | 89.8% |
| 0.7 | 82 | 3 | 18 | 96.5% | 82.0% | 88.6% |
| 0.9 | 70 | 1 | 30 | 98.6% | 70.0% | 81.9% |

**Perhitungan untuk threshold 0.5:**
$$\text{Precision}(0.5) = \frac{88}{88 + 8} = \frac{88}{96} = 0.9167 = 91.7\%$$

$$\text{Recall}(0.5) = \frac{88}{88 + 12} = \frac{88}{100} = 0.88 = 88\%$$

$$F1(0.5) = 2 \times \frac{0.917 \times 0.88}{0.917 + 0.88} = 2 \times \frac{0.8070}{1.797} = 0.898 = 89.8\%$$

### Optimal Threshold Selection

Threshold optimal dipilih berdasarkan use case:
- **High precision dibutuhkan** (minim false alarm): gunakan threshold tinggi (0.7-0.9)
- **High recall dibutuhkan** (jangan miss object): gunakan threshold rendah (0.3-0.5)
- **Balanced**: gunakan threshold 0.5 (default YOLO)

---

## **Rumus 4.10: Accuracy, Precision, Recall per Class**

### Multi-Class Metrics Calculation

Untuk SawoVision dengan 3 kelas:

$$\text{Macro-averaged Precision} = \frac{1}{n_{classes}} \sum_{i=1}^{n_{classes}} Precision_i$$

$$\text{Micro-averaged Precision} = \frac{\sum_{i} TP_i}{\sum_{i} (TP_i + FP_i)}$$

$$\text{Weighted-averaged Precision} = \sum_{i=1}^{n_{classes}} Precision_i \times \frac{Support_i}{Total\_Support}$$

### Contoh Perhitungan

**Confusion Matrix dari 50 test images:**

|  | Pred Mentah | Pred Setengah | Pred Matang |
|---|---|---|---|
| Act Mentah | 14 | 1 | 0 |
| Act Setengah | 1 | 16 | 3 |
| Act Matang | 0 | 2 | 13 |

**Perhitungan per-kelas:**

**Kelas Mentah:**
- TP = 14, FP = 1 + 0 = 1, FN = 1 + 0 = 1
- Precision = 14/(14+1) = 93.3%
- Recall = 14/(14+1) = 93.3%
- F1 = 93.3%

**Kelas Setengah Matang:**
- TP = 16, FP = 1 + 2 = 3, FN = 1 + 3 = 4
- Precision = 16/(16+3) = 84.2%
- Recall = 16/(16+4) = 80.0%
- F1 = 82.1%

**Kelas Matang:**
- TP = 13, FP = 0 + 3 = 3, FN = 0 + 2 = 2
- Precision = 13/(13+3) = 81.3%
- Recall = 13/(13+2) = 86.7%
- F1 = 83.9%

**Macro-averaged Precision:**
$$= \frac{93.3 + 84.2 + 81.3}{3} = 86.3\%$$

**Overall Accuracy:**
$$= \frac{14 + 16 + 13}{50} = \frac{43}{50} = 86\%$$

---

## **Rumus 4.11: Confusion Matrix Visualization**

### Normalized Confusion Matrix

Untuk visualisasi yang lebih baik, confusion matrix sering di-normalize:

$$CM_{norm}[i,j] = \frac{CM[i,j]}{\sum_{k} CM[i,k]} \times 100\%$$

Di mana rows merepresentasikan actual class dan columns merepresentasikan predicted class.

### Contoh Normalized Confusion Matrix

| Actual \ Predicted | Mentah | Setengah | Matang |
|---|---|---|---|
| Mentah | 93.3% | 6.7% | 0% |
| Setengah | 5% | 80% | 15% |
| Matang | 0% | 13.3% | 86.7% |

---

## **Rumus 4.12: Cross Validation Score**

Jika menggunakan k-fold cross validation (lebih akurat untuk dataset kecil):

$$\text{CV Score} = \frac{1}{k} \sum_{i=1}^{k} \text{Score}_i$$

$$\text{CV Std Dev} = \sqrt{\frac{1}{k} \sum_{i=1}^{k} (\text{Score}_i - \text{CV Score})^2}$$

### Contoh untuk 5-Fold CV

| Fold | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Rata-rata |
|---|---|---|---|---|---|---|
| mAP@0.5 | 85.2% | 86.1% | 84.8% | 87.3% | 85.6% | **85.8%** |
| Std Dev | | | | | | **1.04%** |

---

# **BAGIAN IV: RUMUS ANALISIS PERBANDINGAN**

## **Rumus 4.13: Improvement Percentage**

### Formula Persentase Peningkatan

$$\text{Improvement} = \frac{\text{Nilai Baru} - \text{Nilai Lama}}{\text{Nilai Lama}} \times 100\%$$

### Contoh: YOLOv8 vs YOLOv11

**Data:**
- YOLOv8n mAP@0.5: 80.5%
- YOLOv11n mAP@0.5: 86.7%

**Perhitungan:**
$$\text{Improvement} = \frac{86.7 - 80.5}{80.5} \times 100\% = \frac{6.2}{80.5} \times 100\% = 7.7\%$$

**Interpretasi:** YOLOv11 meningkat 7.7% dalam akurasi dibanding YOLOv8.

### Perbandingan Inference Speed

**Data:**
- YOLOv8n inference time: 50 ms
- YOLOv11n inference time: 33 ms

$$\text{Speedup} = \frac{50 \text{ ms}}{33 \text{ ms}} = 1.52x$$

$$\text{Improvement} = \frac{50 - 33}{50} \times 100\% = 34\%$$

**Interpretasi:** YOLOv11 34% lebih cepat dalam inference.

---

## **Rumus 4.14: Statistical Significance Testing**

Untuk memastikan improvement signifikan secara statistik (bukan hanya kebetulan):

### T-Test Formula

$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

Di mana:
- $\bar{x}_1, \bar{x}_2$ = mean dari dua sampel
- $s_1, s_2$ = standard deviation
- $n_1, n_2$ = ukuran sampel

### Contoh Significance Test

**YOLOv8 pada 10 runs CV:**
- Mean mAP: 80.5%, Std: 1.2%

**YOLOv11 pada 10 runs CV:**
- Mean mAP: 86.7%, Std: 1.1%

$$t = \frac{86.7 - 80.5}{\sqrt{\frac{1.2^2}{10} + \frac{1.1^2}{10}}} = \frac{6.2}{\sqrt{0.1584}} = \frac{6.2}{0.398} = 15.57$$

**Interpretasi:** Dengan t-score 15.57 dan df=18, p-value < 0.001, improvement sangat signifikan (highly significant).

---

# **RINGKASAN RUMUS UNTUK SKRIPSI**

## Table of Formulas Used in Chapter 4

| No. | Formula | Usage | Page* |
|-----|---------|-------|-------|
| 4.1 | Dataset Split | Pembagian training/val/test | 4.1.3 |
| 4.2 | Precision, Recall, F1 | Evaluasi model | 4.3.1 |
| 4.3 | mAP @0.5:0.95 | Metrik YOLO utama | 4.2.2 |
| 4.4 | Loss Function | Training dynamics | 4.2.1 |
| 4.5 | Learning Rate Scheduler | LR decay | 4.2.1 |
| 4.6 | Model Compression Ratio | ONNX conversion | 4.2.3 |
| 4.7 | FPS & Throughput | Inference speed | 4.5.1 |
| 4.8 | Memory Usage | System requirements | 4.5.2 |
| 4.9 | Confidence Threshold | Trade-off analysis | 4.5.3 |
| 4.10 | Multi-class Metrics | Per-class evaluation | 4.3.1 |
| 4.11 | Normalized CM | Visualization | 4.3.1 |
| 4.12 | Cross Validation Score | Model robustness | 4.2.2 |
| 4.13 | Improvement % | Performance comparison | 4.6.1 |
| 4.14 | T-Test Significance | Statistical validation | 4.6.1 |

---

## **CATATAN PENTING UNTUK PENULISAN SKRIPSI:**

1. **Konsistensi Notasi**: Gunakan notasi yang sama di seluruh bab (misalnya $TP$, $FP$ harus konsisten)

2. **Menjelaskan Simbol**: Sebelum menggunakan rumus, jelaskan setiap simbol yang digunakan

3. **Konteks Penelitian**: Selalu hubungkan rumus dengan konteks SawoVision (buah sawo, 3 kelas)

4. **Angka Konkret**: Gunakan hasil actual dari training project Anda, bukan hanya contoh

5. **Interpretasi**: Setelah rumus dan perhitungan, selalu berikan interpretasi hasil dalam konteks bisnis/praktis

6. **Referensi**: Cantumkan paper/referensi asli dari setiap rumus (misalnya YOLO paper, mAP definition dari COCO)

7. **Visualisasi**: Kombinasikan rumus dengan grafik dan tabel untuk clarity

---

**Dokumen ini siap digunakan untuk penulisan Bab 4 skripsi Anda! 📝✨**
