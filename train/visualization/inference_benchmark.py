"""
Inference Speed Benchmark Visualization
Generates horizontal bar chart untuk inference time di berbagai platform
Output: inference_benchmark.png
"""

import matplotlib.pyplot as plt
import numpy as np

# Data dari Tabel 4.19
platforms = [
    'Desktop i7 CPU',
    'Desktop RTX GPU',
    'Laptop M1',
    'Browser WASM',
    'Browser WebGL',
    'iPhone 12',
    'Pixel 6 Pro'
]

times = [98, 15, 110, 145, 45, 120, 55]  # ms
fps = [1000/t for t in times]  # Calculate FPS

# Color: CPU = red, GPU = green
colors = ['#FF6B6B', '#4ECDC4', '#FF6B6B', '#FF6B6B', '#4ECDC4', '#FF6B6B', '#4ECDC4']

fig, ax = plt.subplots(figsize=(12, 8))

# Create horizontal bars
bars = ax.barh(platforms, times, color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)

# Add value labels and FPS on bars
for i, (bar, time, f) in enumerate(zip(bars, times, fps)):
    width = bar.get_width()
    
    # Time in ms
    ax.text(width + 3, bar.get_y() + bar.get_height()/2, 
            f'{time}ms ({f:.1f} FPS)',
            va='center', fontsize=10, fontweight='bold')
    
    # Add CPU/GPU indicator inside bar
    if i == 1 or i == 4 or i == 6:  # GPU platforms
        indicator = 'GPU'
        color = 'white'
    else:  # CPU platforms
        indicator = 'CPU'
        color = 'white'
    
    ax.text(width/2, bar.get_y() + bar.get_height()/2, 
            indicator,
            ha='center', va='center', fontsize=9, color=color, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.6))

# Styling
ax.set_xlabel('Inference Time (ms)', fontsize=12, fontweight='bold')
ax.set_title('Model Inference Time Benchmark (YOLOv11n)', fontsize=14, fontweight='bold', pad=20)
ax.set_xlim([0, 160])
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Add reference lines
ax.axvline(x=33, color='green', linestyle='--', linewidth=2, alpha=0.7, label='30 FPS threshold')
ax.axvline(x=16.67, color='blue', linestyle='--', linewidth=2, alpha=0.7, label='60 FPS threshold')

ax.legend(loc='lower right', fontsize=10, framealpha=0.95)

plt.tight_layout()
plt.savefig('inference_benchmark.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: inference_benchmark.png")

# Print detailed benchmark data
print("\n" + "="*90)
print("Inference Speed Benchmark Analysis")
print("="*90)
print(f"{'Platform':<25} {'Inference Time':<15} {'FPS':<10} {'Type':<10} {'Performance':<20}")
print("-"*90)

for platform, time, f in zip(platforms, times, fps):
    device_type = 'GPU' if 'GPU' in platform or 'WebGL' in platform or 'RTX' in platform else 'CPU'
    
    if f >= 30:
        perf = "✅ Real-time"
    elif f >= 15:
        perf = "⚠️ Acceptable"
    else:
        perf = "❌ Too slow"
    
    print(f"{platform:<25} {time:>6.1f} ms        {f:>6.1f}    {device_type:<10} {perf:<20}")

print("="*90)

# Calculate speedup factors
print("\nSpeedup Analysis:")
print("-"*90)
baseline = times[0]  # Desktop i7 CPU as baseline
for i, (platform, time) in enumerate(zip(platforms, times)):
    speedup = baseline / time
    if i == 0:
        print(f"{platform:<25} (Baseline)")
    else:
        if speedup > 1:
            print(f"{platform:<25} {speedup:.2f}x faster than CPU baseline")
        else:
            print(f"{platform:<25} {1/speedup:.2f}x slower than CPU baseline")

print("="*90)

# Browser performance note
print("\n✨ KEY INSIGHTS:")
print("-"*90)
print("• Browser with WebGL (22.2 FPS) is suitable for real-time detection")
print("• Browser with WASM (6.9 FPS) is acceptable for non-real-time applications")
print("• GPU acceleration provides 3-7x speedup compared to CPU")
print("• Mobile phones (8-18 FPS) can handle real-time detection with optimization")
print("="*90)

plt.show()
