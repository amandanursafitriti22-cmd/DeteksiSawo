"""
YOLOv8 vs YOLOv11 Comparison Visualization
Generates grouped bar chart untuk perbandingan metrik YOLOv8n vs YOLOv11n
Output: yolov8_vs_v11.png
"""

import matplotlib.pyplot as plt
import numpy as np

# Data dari Tabel 4.23
models = ['YOLOv8n', 'YOLOv11n']
accuracy = [80.5, 86.7]  # mAP@0.5 %
inference_fps = [19.2, 22.2]  # FPS (Browser WebGL)
model_size = [28.5, 26.3]  # MB

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

colors_v8 = '#FF9500'
colors_v11 = '#4ECDC4'
colors = [colors_v8, colors_v11]

# ========== Subplot 1: Accuracy (mAP@0.5) ==========
bars1 = axes[0].bar(models, accuracy, color=colors, edgecolor='black', linewidth=2, alpha=0.85, width=0.6)
axes[0].set_ylabel('mAP@0.5 (%)', fontsize=12, fontweight='bold')
axes[0].set_title('Accuracy Comparison', fontsize=13, fontweight='bold', pad=15)
axes[0].set_ylim([75, 90])
axes[0].grid(axis='y', alpha=0.3, linestyle='--')

for i, (bar, val) in enumerate(zip(bars1, accuracy)):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{val:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    if i == 1:
        improvement = ((accuracy[1] - accuracy[0]) / accuracy[0]) * 100
        axes[0].text(bar.get_x() + bar.get_width()/2., height/2,
                    f'+{improvement:.1f}%',
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.8))

# ========== Subplot 2: Speed (FPS) ==========
bars2 = axes[1].bar(models, inference_fps, color=colors, edgecolor='black', linewidth=2, alpha=0.85, width=0.6)
axes[1].set_ylabel('FPS (Browser WebGL)', fontsize=12, fontweight='bold')
axes[1].set_title('Speed Comparison', fontsize=13, fontweight='bold', pad=15)
axes[1].set_ylim([15, 25])
axes[1].grid(axis='y', alpha=0.3, linestyle='--')

for i, (bar, val) in enumerate(zip(bars2, inference_fps)):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{val:.1f} FPS',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    if i == 1:
        improvement = ((inference_fps[1] - inference_fps[0]) / inference_fps[0]) * 100
        axes[1].text(bar.get_x() + bar.get_width()/2., height/2,
                    f'+{improvement:.1f}%',
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.8))

# ========== Subplot 3: Size (Model Size) ==========
bars3 = axes[2].bar(models, model_size, color=colors, edgecolor='black', linewidth=2, alpha=0.85, width=0.6)
axes[2].set_ylabel('Model Size (MB)', fontsize=12, fontweight='bold')
axes[2].set_title('Model Size Comparison', fontsize=13, fontweight='bold', pad=15)
axes[2].set_ylim([20, 32])
axes[2].grid(axis='y', alpha=0.3, linestyle='--')

for i, (bar, val) in enumerate(zip(bars3, model_size)):
    height = bar.get_height()
    axes[2].text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{val:.1f} MB',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    if i == 1:
        reduction = ((model_size[0] - model_size[1]) / model_size[0]) * 100
        axes[2].text(bar.get_x() + bar.get_width()/2., height/2,
                    f'-{reduction:.1f}%',
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='darkgreen', alpha=0.8))

# Main title
fig.suptitle('YOLOv8n vs YOLOv11n Comparison - SawoVision', 
             fontsize=15, fontweight='bold', y=1.00)

plt.tight_layout()
plt.savefig('yolov8_vs_v11.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: yolov8_vs_v11.png")

# Print detailed comparison
print("\n" + "="*80)
print("YOLOv8n vs YOLOv11n Detailed Comparison")
print("="*80)

metrics_v8 = {
    'mAP@0.5': 80.5,
    'mAP@0.5:0.95': 65.2,
    'Precision': 85.1,
    'Recall': 80.8,
    'F1-Score': 82.9,
    'Inference (CPU)': 120,
    'Inference (WebGL)': 45,
    'FPS (WebGL)': 19.2,
    'Model Size': 28.5,
    'Parameters': '3.16M',
}

metrics_v11 = {
    'mAP@0.5': 86.7,
    'mAP@0.5:0.95': 70.1,
    'Precision': 88.4,
    'Recall': 85.2,
    'F1-Score': 86.8,
    'Inference (CPU)': 98,
    'Inference (WebGL)': 45,
    'FPS (WebGL)': 22.2,
    'Model Size': 26.3,
    'Parameters': '2.67M',
}

print(f"{'Metric':<25} {'YOLOv8n':<20} {'YOLOv11n':<20} {'Improvement':<15}")
print("-"*80)

for metric in metrics_v8.keys():
    v8_val = metrics_v8[metric]
    v11_val = metrics_v11[metric]
    
    # Calculate improvement based on metric type
    if 'Inference' in metric or 'Size' in metric or 'Parameters' in metric:
        if isinstance(v8_val, str) or isinstance(v11_val, str):
            improvement = f"{v8_val} → {v11_val}"
        else:
            if v8_val > v11_val:  # For these metrics, lower is better
                improvement = f"-{((v8_val - v11_val) / v8_val * 100):.1f}% (faster/smaller)"
            else:
                improvement = f"+{((v11_val - v8_val) / v8_val * 100):.1f}%"
    else:
        if isinstance(v8_val, str) or isinstance(v11_val, str):
            improvement = f"{v8_val} → {v11_val}"
        else:
            improvement = f"+{((v11_val - v8_val) / v8_val * 100):.1f}%"
    
    if isinstance(v8_val, str):
        print(f"{metric:<25} {str(v8_val):<20} {str(v11_val):<20} {improvement:<15}")
    else:
        print(f"{metric:<25} {v8_val:<20} {v11_val:<20} {improvement:<15}")

print("="*80)

print("\n🏆 WINNER: YOLOv11n")
print("-"*80)
print("✅ Better accuracy: +7.7% in mAP@0.5")
print("✅ Better speed: +15.6% faster (22.2 FPS vs 19.2 FPS)")
print("✅ Smaller model: -7.7% (26.3 MB vs 28.5 MB)")
print("✅ Fewer parameters: -15.5% (2.67M vs 3.16M)")
print("\n→ YOLOv11n is the clear winner for SawoVision deployment!")
print("="*80)

plt.show()
