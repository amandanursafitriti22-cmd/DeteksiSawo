"""
Augmentation Examples Visualization
Menggunakan gambar asli dari folder Dataset
Output: augmentation_examples.png
"""

import matplotlib.pyplot as plt
from PIL import Image
import os

# ==================== PATH GAMBAR ====================
# Sesuaikan path jika perlu
base_path = r"F:\JOKI\BARUDAK NUSA PUTRA\BARUDAK TI\Amanda\Skripsi\Project-Sawo\train\visualization\Dataset"

# Nama file gambar
image_files = {
    "Original": "original.jpg",
    "Brightness Adjusted": "brightnes.jpg",
    "Horizontal Flip": "flip.jpg"
}

# ==================== LOAD GAMBAR ====================
images = {}
for label, filename in image_files.items():
    filepath = os.path.join(base_path, filename)
    if os.path.exists(filepath):
        images[label] = Image.open(filepath)
    else:
        print(f"⚠️ File tidak ditemukan: {filepath}")

# ==================== VISUALISASI ====================
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('Contoh Augmentasi Data - Buah Sawo\n(Menggunakan Gambar Asli)', 
             fontsize=16, fontweight='bold', y=0.98)

positions = list(images.keys())

for i, (label, img) in enumerate(images.items()):
    ax = axes[i]
    ax.imshow(img)
    ax.set_title(label, fontsize=13, fontweight='bold', pad=10)
    ax.axis('off')

plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.savefig('augmentation_examples.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: augmentation_examples.png")

# ==================== PRINT INFO ====================
print("\n" + "="*70)
print("Contoh Augmentasi Data SawoVision")
print("="*70)
print("Gambar yang digunakan:")
for label in images.keys():
    print(f"• {label}")
print("\nCatatan:")
print("- Gambar di atas menunjukkan contoh hasil augmentasi")
print("- Augmentasi dilakukan menggunakan Roboflow")
print("="*70)

plt.show()