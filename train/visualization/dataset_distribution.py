"""
Dataset Distribution Visualization
Hanya 2 kelas: Mentah dan Matang
Augmentasi dilakukan di Roboflow
Total gambar setelah augmentasi: 1.150
"""

import matplotlib.pyplot as plt
import numpy as np

# ==================== DATA YANG BENAR ====================
classes = ['Mentah', 'Matang']

# Original sebelum augmentasi
original_samples = [240, 240]          # Total original = 480

# Final setelah augmentasi di Roboflow (TOTAL per split)
training_samples = [503, 503]          # Training total = 1006
validation_samples = [48, 48]          # Validasi total = 96
test_samples = [24, 24]                # Test total = 48

colors = ['#FF6B6B', '#4ECDC4']

# ==================== VISUALISASI ====================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Pie Chart - Original
wedges, texts, autotexts = ax1.pie(
    original_samples, 
    labels=classes, 
    autopct='%1.1f%%',
    colors=colors,
    explode=(0.05, 0.05),
    startangle=90,
    textprops={'fontsize': 13, 'weight': 'bold'}
)

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(12)
    autotext.set_weight('bold')

ax1.set_title('Distribusi Kelas Dataset Original\n(Sebelum Augmentasi)', 
              fontsize=14, fontweight='bold', pad=15)

# Bar Chart - Final (Setelah Augmentasi Roboflow)
x = np.arange(len(classes))
width = 0.25

bars1 = ax2.bar(x - width, training_samples, width, label='Training (Augmented)', 
                color='#27AE60', edgecolor='black', linewidth=1.8)
bars2 = ax2.bar(x, validation_samples, width, label='Validasi', 
                color='#3498DB', edgecolor='black', linewidth=1.8)
bars3 = ax2.bar(x + width, test_samples, width, label='Test', 
                color='#9B59B6', edgecolor='black', linewidth=1.8)

# Value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 15,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_ylabel('Jumlah Gambar', fontsize=12, fontweight='bold')
ax2.set_xlabel('Kelas Kematangan', fontsize=12, fontweight='bold')
ax2.set_title('Distribusi Dataset Final\n(Setelah Augmentasi di Roboflow)', 
              fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(classes, fontsize=12)
ax2.legend(loc='upper right', fontsize=11)
ax2.set_ylim([0, 1200])
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# ==================== TOTAL ANNOTATION ====================
total_original = sum(original_samples)
total_final = sum(training_samples) + sum(validation_samples) + sum(test_samples)

fig.text(0.5, 0.02, 
         f'Total Original: {total_original} gambar   →   Total Setelah Augmentasi (Roboflow): {total_final} gambar',
         ha='center', fontsize=12.5, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#E8F6F3', edgecolor='#1ABC9C', linewidth=2.5))

plt.tight_layout(rect=[0, 0.07, 1, 1])
plt.savefig('dataset_distribution.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: dataset_distribution.png")

# ==================== PRINT SUMMARY ====================
print("\n" + "="*75)
print("DATASET DISTRIBUTION SUMMARY")
print("Augmentasi dilakukan di Roboflow")
print("="*75)
print(f"{'Class':<18} {'Original':<12} {'Training*':<12} {'Validasi':<10} {'Test':<8}")
print("-"*75)
for i, cls in enumerate(classes):
    print(f"{cls:<18} {original_samples[i]:<12} {training_samples[i]:<12} {validation_samples[i]:<10} {test_samples[i]:<8}")
print("-"*75)
print(f"{'TOTAL':<18} {sum(original_samples):<12} {sum(training_samples):<12} {sum(validation_samples):<10} {sum(test_samples):<8}")
print("="*75)
print(f"* Training set telah di-augmentasi menggunakan Roboflow")
print(f"Total gambar setelah augmentasi: {total_final}")
print("="*75)

plt.show()