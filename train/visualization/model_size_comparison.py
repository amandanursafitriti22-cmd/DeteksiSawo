"""
Model Size Comparison Visualization
Generates bar chart untuk perbandingan ukuran PyTorch vs ONNX models
Output: model_size_comparison.png
"""

import matplotlib.pyplot as plt
import numpy as np

# Model sizes
models = ['PyTorch\n(.pt)', 'ONNX\n(Simplified)', 'ONNX\n(Quantized)']
sizes = [26.3, 13.1, 6.8]  # MB
colors = ['#FF6B6B', '#4ECDC4', '#95E1D3']

fig, ax = plt.subplots(figsize=(10, 7))

# Create bars
bars = ax.bar(models, sizes, color=colors, edgecolor='black', linewidth=2.5, alpha=0.85, width=0.6)

# Add value labels on bars
for i, (bar, size) in enumerate(zip(bars, sizes)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{size} MB',
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Add reduction percentage for ONNX models
    if i > 0:
        reduction = ((sizes[0] - size) / sizes[0]) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'-{reduction:.1f}%',
                ha='center', va='center', fontsize=11, color='white', 
                fontweight='bold', bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

# Styling
ax.set_ylabel('Ukuran Model (MB)', fontsize=12, fontweight='bold')
ax.set_title('Perbandingan Ukuran Model: PyTorch vs ONNX', fontsize=14, fontweight='bold', pad=20)
ax.set_ylim([0, 32])
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add data table below chart
table_data = [
    ['Model', 'Ukuran', 'Compression', 'Benefit'],
    ['PyTorch', '26.3 MB', '-', 'Original'],
    ['ONNX Simplified', '13.1 MB', '2.01x', '50.2% smaller'],
    ['ONNX Quantized', '6.8 MB', '3.87x', '74.1% smaller']
]

table = ax.table(cellText=table_data, cellLoc='center', loc='bottom',
                bbox=[0, -0.35, 1, 0.25], colWidths=[0.25, 0.25, 0.25, 0.25])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.8)

# Style header row
for i in range(4):
    table[(0, i)].set_facecolor('#404040')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Style data rows with alternating colors
for i in range(1, 4):
    for j in range(4):
        if i % 2 == 0:
            table[(i, j)].set_facecolor('#E8E8E8')
        else:
            table[(i, j)].set_facecolor('#F5F5F5')

plt.tight_layout()
plt.savefig('model_size_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: model_size_comparison.png")

# Print comparison data
print("\n" + "="*80)
print("Model Size Comparison Analysis")
print("="*80)

for i, (model, size) in enumerate(zip(models, sizes)):
    model_clean = model.replace('\n', ' ')
    print(f"{model_clean:<30} {size:>8.1f} MB", end='')
    
    if i == 0:
        print(f"  (Baseline)")
    else:
        reduction = ((sizes[0] - size) / sizes[0]) * 100
        ratio = sizes[0] / size
        print(f"  ({reduction:>5.1f}% reduction, {ratio:.2f}x compression)")

print("="*80)

# Download time estimation
print("\nEstimated Download Times (various internet speeds):")
print("-"*80)
speeds = [1, 5, 10, 50]  # Mbps
for model_size in [26.3, 13.1, 6.8]:
    print(f"\nModel Size: {model_size} MB")
    for speed in speeds:
        # Convert Mbps to MB/s
        transfer_rate = speed / 8
        time_seconds = model_size / transfer_rate
        time_minutes = time_seconds / 60
        
        if time_seconds < 60:
            print(f"  @{speed:>2} Mbps: {time_seconds:>6.1f} sec")
        else:
            print(f"  @{speed:>2} Mbps: {time_minutes:>6.2f} min")

print("="*80)

plt.show()
