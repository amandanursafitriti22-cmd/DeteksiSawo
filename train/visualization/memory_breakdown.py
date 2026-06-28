"""
Memory Usage Breakdown Visualization
Generates pie chart untuk breakdown memory usage
Output: memory_breakdown.png
"""

import matplotlib.pyplot as plt
import numpy as np

# Memory breakdown (MB) dari Tabel 4.20
components = [
    'Model ONNX',
    'Input Buffer',
    'Output Buffer',
    'Intermediate Tensors',
    'ONNX Runtime Overhead',
    'Browser Overhead'
]

sizes = [13.1, 4.9, 62.3, 52.6, 67.6, 24.5]  # MB
colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FFD93D', '#F38181', '#AA96DA']
explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ========== Pie Chart ==========
wedges, texts, autotexts = ax1.pie(
    sizes,
    labels=components,
    autopct='%1.1f%%',
    colors=colors,
    explode=explode,
    startangle=90,
    textprops={'fontsize': 10, 'weight': 'bold'}
)

# Improve pie chart
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(9)
    autotext.set_weight('bold')

ax1.set_title('Memory Usage Breakdown (Peak: 225 MB)', fontsize=13, fontweight='bold', pad=20)

# ========== Bar Chart ==========
components_short = [c.replace(' ', '\n') for c in components]
bars = ax2.barh(components_short, sizes, color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)

# Add value labels
for i, (bar, size) in enumerate(zip(bars, sizes)):
    width = bar.get_width()
    percentage = (size / sum(sizes)) * 100
    ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
            f'{size:.1f} MB ({percentage:.1f}%)',
            va='center', fontsize=10, fontweight='bold')

ax2.set_xlabel('Memory (MB)', fontsize=12, fontweight='bold')
ax2.set_title('Memory Components Breakdown', fontsize=13, fontweight='bold', pad=20)
ax2.set_xlim([0, 80])
ax2.grid(axis='x', alpha=0.3, linestyle='--')

# Add total annotation
total = sum(sizes)
fig.text(0.5, 0.02, f'Total Peak Memory: {total:.1f} MB | Available Browser Memory: ~500-2000 MB | Utilization: 11-45%', 
         ha='center', fontsize=11, style='italic', weight='bold')

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('memory_breakdown.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: memory_breakdown.png")

# Print memory analysis
print("\n" + "="*80)
print("Memory Usage Analysis")
print("="*80)
print(f"{'Component':<30} {'Size (MB)':<15} {'Percentage':<15}")
print("-"*80)

for comp, size in zip(components, sizes):
    percentage = (size / total) * 100
    print(f"{comp:<30} {size:>8.1f}        {percentage:>6.1f}%")

print("-"*80)
print(f"{'TOTAL':<30} {total:>8.1f}        100.0%")
print("="*80)

# Device compatibility analysis
print("\nDevice Memory Compatibility:")
print("-"*80)
devices = [
    ('Laptop (4GB RAM)', 4000, 'Ample headroom'),
    ('Desktop (8GB RAM)', 8000, 'Excellent'),
    ('Tablet (2GB RAM)', 2000, 'Sufficient'),
    ('Smartphone (1GB RAM)', 1000, 'Tight but feasible'),
    ('Low-end Phone (512MB)', 512, 'Not recommended'),
]

for device, ram, note in devices:
    available = ram * 0.5  # Assume 50% available for browser
    if available > total * 1.5:
        status = '✅ OK'
    elif available > total * 1.2:
        status = '⚠️ Marginal'
    else:
        status = '❌ Risky'
    
    print(f"{device:<25} {ram} MB total ({available:.0f} MB available)  {status}  {note}")

print("="*80)

plt.show()
