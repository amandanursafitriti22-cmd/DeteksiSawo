"""
Per-Class Metrics Comparison
Generates grouped bar chart untuk Precision, Recall, F1-Score, AP@0.5 per kelas
Output: per_class_metrics.png
"""

import matplotlib.pyplot as plt
import numpy as np

# Data dari Tabel 4.12
classes = ['Mentah', 'Setengah Matang', 'Matang']
precision = [93.3, 88.9, 76.5]
recall = [93.3, 80.0, 86.7]
f1_score = [93.3, 84.2, 81.3]
ap_50 = [91.2, 84.6, 79.8]

x = np.arange(len(classes))
width = 0.2

fig, ax = plt.subplots(figsize=(14, 7))

# Create bars
bars1 = ax.bar(x - 1.5*width, precision, width, label='Precision', 
               color='#FF6B6B', edgecolor='black', linewidth=1.5, alpha=0.85)
bars2 = ax.bar(x - 0.5*width, recall, width, label='Recall', 
               color='#4ECDC4', edgecolor='black', linewidth=1.5, alpha=0.85)
bars3 = ax.bar(x + 0.5*width, f1_score, width, label='F1-Score', 
               color='#95E1D3', edgecolor='black', linewidth=1.5, alpha=0.85)
bars4 = ax.bar(x + 1.5*width, ap_50, width, label='AP@0.5', 
               color='#FFD93D', edgecolor='black', linewidth=1.5, alpha=0.85)

# Add value labels on bars
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Styling
ax.set_ylabel('Score (%)', fontsize=12, fontweight='bold')
ax.set_xlabel('Kelas Kematangan', fontsize=12, fontweight='bold')
ax.set_title('Performa Model per Kelas', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(classes)
ax.legend(loc='upper right', fontsize=11, framealpha=0.95, ncol=2)
ax.set_ylim([70, 105])
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add horizontal line for overall average
overall_avg = np.mean([precision, recall, f1_score, ap_50])
ax.axhline(y=np.mean(precision), color='#FF6B6B', linestyle=':', alpha=0.5, linewidth=1)
ax.axhline(y=np.mean(recall), color='#4ECDC4', linestyle=':', alpha=0.5, linewidth=1)
ax.axhline(y=np.mean(f1_score), color='#95E1D3', linestyle=':', alpha=0.5, linewidth=1)
ax.axhline(y=np.mean(ap_50), color='#FFD93D', linestyle=':', alpha=0.5, linewidth=1)

plt.tight_layout()
plt.savefig('per_class_metrics.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: per_class_metrics.png")

# Print detailed metrics
print("\n" + "="*80)
print("Per-Class Metrics Summary")
print("="*80)
print(f"{'Class':<20} {'Precision':<15} {'Recall':<15} {'F1-Score':<15} {'AP@0.5':<15}")
print("-"*80)

for i, cls in enumerate(classes):
    print(f"{cls:<20} {precision[i]:>6.2f}%        {recall[i]:>6.2f}%        {f1_score[i]:>6.2f}%        {ap_50[i]:>6.2f}%")

print("-"*80)
print(f"{'Average':<20} {np.mean(precision):>6.2f}%        {np.mean(recall):>6.2f}%        {np.mean(f1_score):>6.2f}%        {np.mean(ap_50):>6.2f}%")
print("="*80)

# Best and worst per metric
print("\nBest & Worst per Metric:")
print("-"*80)
print(f"Precision:   Best: {classes[np.argmax(precision)]} ({max(precision):.2f}%) | Worst: {classes[np.argmin(precision)]} ({min(precision):.2f}%)")
print(f"Recall:      Best: {classes[np.argmax(recall)]} ({max(recall):.2f}%) | Worst: {classes[np.argmin(recall)]} ({min(recall):.2f}%)")
print(f"F1-Score:    Best: {classes[np.argmax(f1_score)]} ({max(f1_score):.2f}%) | Worst: {classes[np.argmin(f1_score)]} ({min(f1_score):.2f}%)")
print(f"AP@0.5:      Best: {classes[np.argmax(ap_50)]} ({max(ap_50):.2f}%) | Worst: {classes[np.argmin(ap_50)]} ({min(ap_50):.2f}%)")
print("="*80)

plt.show()
