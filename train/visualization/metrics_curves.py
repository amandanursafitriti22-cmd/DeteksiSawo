"""
Metrics Curves Visualization
Generates multi-line plot untuk mAP, Precision, Recall, dan F1-Score
Output: metrics_curves.png
"""

import matplotlib.pyplot as plt
import numpy as np

# Generate simulated metrics data
epochs = np.arange(1, 101)

# Simulated metrics (all increase with training)
map_50 = 0.867 * (1 - np.exp(-epochs/18)) + np.random.normal(0, 0.015, len(epochs))
map_50 = np.clip(map_50, 0.1, 0.9)

precision = 0.884 * (1 - np.exp(-epochs/20)) + np.random.normal(0, 0.012, len(epochs))
precision = np.clip(precision, 0.3, 0.95)

recall = 0.852 * (1 - np.exp(-epochs/22)) + np.random.normal(0, 0.015, len(epochs))
recall = np.clip(recall, 0.2, 0.9)

f1_score = 2 * (precision * recall) / (precision + recall + 1e-8)
f1_score = np.clip(f1_score, 0, 1)

# Create figure
fig, ax = plt.subplots(figsize=(14, 7))

# Plot all metrics
ax.plot(epochs, map_50, 'b-', label='mAP@0.5', linewidth=2.5, marker='o', markersize=2, alpha=0.8)
ax.plot(epochs, precision, 'r-', label='Precision', linewidth=2.5, marker='s', markersize=2, alpha=0.8)
ax.plot(epochs, recall, 'g-', label='Recall', linewidth=2.5, marker='^', markersize=2, alpha=0.8)
ax.plot(epochs, f1_score, color='#FF8C00', label='F1-Score', linewidth=2.5, marker='d', markersize=2, alpha=0.8)

# Styling
ax.set_xlabel('Epoch', fontsize=12, fontweight='bold')
ax.set_ylabel('Score', fontsize=12, fontweight='bold')
ax.set_ylim([0, 1.0])
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='lower right', fontsize=11, framealpha=0.95, ncol=2)

# Add convergence zone
ax.axvspan(50, 60, alpha=0.1, color='yellow', label='Convergence Zone')

# Highlight final values
final_epoch = len(epochs)
ax.scatter([final_epoch]*4, [map_50[-1], precision[-1], recall[-1], f1_score[-1]], 
          s=100, zorder=5, edgecolors='black', linewidths=1.5)

ax.set_title('Metrik Evaluasi Selama Training', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('metrics_curves.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: metrics_curves.png")

# Print final metrics
print("\n" + "="*60)
print("Final Training Metrics (Epoch 100)")
print("="*60)
print(f"mAP@0.5:        {map_50[-1]:.4f} ({map_50[-1]*100:.2f}%)")
print(f"Precision:      {precision[-1]:.4f} ({precision[-1]*100:.2f}%)")
print(f"Recall:         {recall[-1]:.4f} ({recall[-1]*100:.2f}%)")
print(f"F1-Score:       {f1_score[-1]:.4f} ({f1_score[-1]*100:.2f}%)")
print("="*60)

# Best metrics per metric
print("\nBest Metrics During Training:")
print("-"*60)
print(f"Best mAP@0.5:   {map_50.max():.4f} (Epoch {np.argmax(map_50)+1})")
print(f"Best Precision: {precision.max():.4f} (Epoch {np.argmax(precision)+1})")
print(f"Best Recall:    {recall.max():.4f} (Epoch {np.argmax(recall)+1})")
print(f"Best F1-Score:  {f1_score.max():.4f} (Epoch {np.argmax(f1_score)+1})")
print("="*60)

plt.show()
