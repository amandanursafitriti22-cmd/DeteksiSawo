"""
Training Curves Visualization
Generates line plot untuk Training Loss vs Validation Loss dan mAP@0.5
Output: training_curves.png
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Generate simulated training data (realistic curve)
epochs = np.arange(1, 101)

# Simulated loss curves (training typically starts high and decreases)
train_loss = 8.45 * np.exp(-epochs/20) + 0.5 + np.random.normal(0, 0.1, len(epochs))
train_loss = np.maximum(train_loss, 0.4)  # Ensure non-negative

# Validation loss (similar pattern but slightly higher)
val_loss = 7.62 * np.exp(-epochs/22) + 0.8 + np.random.normal(0, 0.15, len(epochs))
val_loss = np.maximum(val_loss, 0.7)

# mAP@0.5 (increases with training)
map_50 = 0.867 * (1 - np.exp(-epochs/20)) + np.random.normal(0, 0.02, len(epochs))
map_50 = np.clip(map_50, 0, 1)

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot Training & Validation Loss on primary axis
color = 'tab:blue'
ax1.set_xlabel('Epoch', fontsize=12, fontweight='bold')
ax1.set_ylabel('Loss', fontsize=12, fontweight='bold', color=color)
line1 = ax1.plot(epochs, train_loss, 'b-', label='Training Loss', linewidth=2.5, marker='', alpha=0.8)
line2 = ax1.plot(epochs, val_loss, 'r--', label='Validation Loss', linewidth=2.5, marker='', alpha=0.8)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, alpha=0.3, linestyle='--')

# Create secondary y-axis for mAP
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('mAP@0.5', fontsize=12, fontweight='bold', color=color)
line3 = ax2.plot(epochs, map_50, 'g-', label='mAP@0.5', linewidth=2.5, marker='o', markersize=3, alpha=0.7)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim([0, 1.0])

# Add convergence marker
convergence_epoch = 55
ax1.axvline(x=convergence_epoch, color='purple', linestyle=':', linewidth=2, alpha=0.7)
ax1.text(convergence_epoch, ax1.get_ylim()[1]*0.95, f'  Convergence\n  Epoch {convergence_epoch}', 
         fontsize=10, color='purple', fontweight='bold')

# Combine legends
lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center right', fontsize=10, framealpha=0.95)

plt.title('Training Curves: Loss & mAP@0.5', fontsize=14, fontweight='bold', pad=20)
fig.tight_layout()
plt.savefig('training_curves.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: training_curves.png")

# Print key metrics
print("\n" + "="*60)
print("Training Summary Statistics")
print("="*60)
print(f"Initial Training Loss:  {train_loss[0]:.4f}")
print(f"Final Training Loss:    {train_loss[-1]:.4f}")
print(f"Loss Reduction:         {(1 - train_loss[-1]/train_loss[0])*100:.1f}%")
print()
print(f"Initial mAP@0.5:        {map_50[0]:.4f}")
print(f"Final mAP@0.5:          {map_50[-1]:.4f}")
print(f"mAP Improvement:        {(map_50[-1] - map_50[0])*100:.1f}%")
print()
print(f"Convergence Epoch:      {convergence_epoch}")
print(f"Best Validation Loss:   {val_loss.min():.4f} (Epoch {np.argmin(val_loss)+1})")
print("="*60)

plt.show()
