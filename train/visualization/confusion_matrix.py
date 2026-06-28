"""
Confusion Matrix Heatmap Visualization
Generates heatmap untuk normalized confusion matrix
Output: confusion_matrix_heatmap.png
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Confusion matrix (normalized percentage)
cm_normalized = np.array([
    [93.3, 6.7, 0.0],
    [0.0, 80.0, 20.0],
    [6.7, 6.7, 86.7]
])

# Raw counts for annotation
cm_raw = np.array([
    [14, 1, 0],
    [0, 16, 4],
    [1, 1, 13]
])

class_names = ['Mentah', 'Setengah Matang', 'Matang']

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Create heatmap
sns.heatmap(cm_normalized, annot=False, fmt='.1f', cmap='YlOrRd', 
            xticklabels=class_names, yticklabels=class_names,
            cbar_kws={'label': 'Percentage (%)'}, 
            vmin=0, vmax=100, square=True, linewidths=2, linecolor='black',
            ax=ax)

# Add percentage annotations
for i in range(len(class_names)):
    for j in range(len(class_names)):
        percentage = cm_normalized[i, j]
        count = cm_raw[i, j]
        
        # Color for text: white for dark cells, black for light cells
        text_color = 'white' if percentage > 50 else 'black'
        
        # Add both percentage and count
        text = ax.text(j + 0.5, i + 0.65, f'{percentage:.1f}%',
                      ha="center", va="center", color=text_color, 
                      fontsize=12, fontweight='bold')
        
        text = ax.text(j + 0.5, i + 0.35, f'(n={count})',
                      ha="center", va="center", color=text_color, 
                      fontsize=9, style='italic')

ax.set_ylabel('Actual Class', fontsize=12, fontweight='bold')
ax.set_xlabel('Predicted Class', fontsize=12, fontweight='bold')
ax.set_title('Confusion Matrix - Test Set (Normalized %)', fontsize=14, fontweight='bold', pad=20)

# Rotate labels
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
plt.setp(ax.get_yticklabels(), rotation=0)

plt.tight_layout()
plt.savefig('confusion_matrix_heatmap.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: confusion_matrix_heatmap.png")

# Calculate and print metrics
print("\n" + "="*60)
print("Confusion Matrix Analysis")
print("="*60)

total = cm_raw.sum()
correct = np.diag(cm_raw).sum()
accuracy = correct / total

print(f"\nOverall Accuracy: {accuracy*100:.2f}% ({correct}/{total})")

print("\nPer-Class Metrics:")
print("-"*60)
print(f"{'Class':<20} {'Precision':<15} {'Recall':<15} {'F1-Score':<15}")
print("-"*60)

for i, class_name in enumerate(class_names):
    # Precision: TP / (TP + FP)
    tp = cm_raw[i, i]
    fp = cm_raw[:, i].sum() - tp
    fn = cm_raw[i, :].sum() - tp
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"{class_name:<20} {precision*100:>6.2f}%        {recall*100:>6.2f}%        {f1*100:>6.2f}%")

print("="*60)

plt.show()
