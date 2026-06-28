"""
Class Examples Visualization
Generates 3x2 grid menunjukkan contoh gambar dari setiap kelas
Output: class_examples.png
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import random

# Set random seed
random.seed(42)
np.random.seed(42)

def create_synthetic_sawo(size=200, class_type='mentah', variation=1):
    """
    Generate synthetic sawo fruit images representing different ripeness levels
    
    Args:
        size: Image size
        class_type: 'mentah', 'setengah_matang', or 'matang'
        variation: 1 or 2 for different samples
    """
    img = Image.new('RGB', (size, size), color=(180, 180, 180))  # Background
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Define colors and characteristics per ripeness
    if class_type == 'mentah':
        fruit_colors = [
            (34, 139, 34, 255),      # Dark green - variation 1
            (46, 160, 67, 255),      # Lighter green - variation 2
        ]
        stem_color = (139, 69, 19, 255)
        highlight_alpha = 80
    elif class_type == 'setengah_matang':
        fruit_colors = [
            (184, 134, 11, 255),     # Dark goldenrod - variation 1
            (210, 180, 140, 255),    # Tan - variation 2
        ]
        stem_color = (139, 69, 19, 255)
        highlight_alpha = 100
    else:  # matang
        fruit_colors = [
            (139, 69, 19, 255),      # Dark brown - variation 1
            (101, 50, 15, 255),      # Darker brown - variation 2
        ]
        stem_color = (101, 50, 15, 255)
        highlight_alpha = 60
    
    fruit_color = fruit_colors[variation - 1]
    center_x, center_y = size // 2, size // 2
    radius = 70
    
    # Draw fruit (oval shape)
    draw.ellipse(
        [center_x - radius, center_y - radius + 15, 
         center_x + radius, center_y + radius + 15],
        fill=fruit_color,
        outline='black'
    )
    
    # Add stem
    stem_x1, stem_y1 = center_x - 5, center_y - radius + 10
    stem_x2, stem_y2 = center_x + 5, center_y - radius - 20
    draw.line([(stem_x1, stem_y1), (stem_x2, stem_y2)], fill=stem_color, width=4)
    
    # Add highlight (more prominent for unripe)
    if class_type == 'mentah':
        highlight_x = center_x - radius // 2.5
        highlight_y = center_y - radius // 3
        hl_size = 25
    else:
        highlight_x = center_x - radius // 3
        highlight_y = center_y - radius // 4
        hl_size = 20
    
    draw.ellipse(
        [highlight_x - hl_size, highlight_y - hl_size,
         highlight_x + hl_size, highlight_y + hl_size],
        fill=(255, 255, 255, highlight_alpha)
    )
    
    # Add some texture spots (more for ripe fruits)
    if class_type == 'matang':
        num_spots = 3
        for _ in range(num_spots):
            spot_x = center_x + random.randint(-40, 40)
            spot_y = center_y + random.randint(-20, 40)
            spot_radius = random.randint(3, 8)
            draw.ellipse(
                [spot_x - spot_radius, spot_y - spot_radius,
                 spot_x + spot_radius, spot_y + spot_radius],
                fill=(80, 40, 10, 150)
            )
    
    return np.array(img)

# Create 3x2 grid
fig, axes = plt.subplots(3, 2, figsize=(12, 14))
fig.suptitle('Contoh Gambar per Kelas Kematangan Buah Sawo', 
             fontsize=16, fontweight='bold', y=0.995)

classes_info = [
    ('mentah', 'Mentah (Unripe)', '🟢 Green color, firm texture, astringent taste'),
    ('setengah_matang', 'Setengah Matang (Half-ripe)', '🟡 Yellow-brown color, starting to soften'),
    ('matang', 'Matang (Ripe)', '🟤 Dark brown color, soft texture, sweet taste'),
]

# Generate and display images
for class_idx, (class_type, title, description) in enumerate(classes_info):
    for var_idx in range(2):
        ax = axes[class_idx, var_idx]
        
        # Generate synthetic image
        img = create_synthetic_sawo(size=300, class_type=class_type, variation=var_idx + 1)
        ax.imshow(img)
        
        # Add title
        if var_idx == 0:
            ax.set_title(f'{title}\n{description}', 
                        fontsize=11, fontweight='bold', pad=10, color='darkblue')
        else:
            ax.set_title(f'Contoh {var_idx + 1}', fontsize=10, fontweight='bold', pad=10)
        
        ax.axis('off')

plt.tight_layout(rect=[0, 0, 1, 0.98])
plt.savefig('class_examples.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Generated: class_examples.png")

# Print class characteristics
print("\n" + "="*80)
print("Karakteristik Kelas Kematangan Buah Sawo")
print("="*80)

characteristics = {
    'Mentah': {
        'Color': 'Hijau gelap (dark green)',
        'Texture': 'Keras (firm), tidak mudah ditekan',
        'Taste': 'Getir/sepet (astringent), tidak enak',
        'Touch': 'Kulit halus, tidak berkerut',
        'Smell': 'Aroma minimal',
        'Best For': 'Penyimpanan jangka panjang',
        'Ripeness %': '0-20%',
    },
    'Setengah Matang': {
        'Color': 'Kuning-cokelat (yellow-brown)',
        'Texture': 'Mulai lembut (slightly soft)',
        'Taste': 'Getir berkurang, mulai manis',
        'Touch': 'Kulit mulai berkerut',
        'Smell': 'Aroma mulai tercium',
        'Best For': 'Konsumsi dalam 2-3 hari',
        'Ripeness %': '40-70%',
    },
    'Matang': {
        'Color': 'Cokelat gelap (dark brown)',
        'Texture': 'Sangat lembut (very soft)',
        'Taste': 'Manis, lezat (sweet, delicious)',
        'Touch': 'Kulit berkerut, mudah ditekan',
        'Smell': 'Aroma kuat dan harum',
        'Best For': 'Konsumsi segera, tidak tahan lama',
        'Ripeness %': '90-100%',
    }
}

for class_name, chars in characteristics.items():
    print(f"\n{class_name}:")
    print("-" * 80)
    for char_name, char_value in chars.items():
        print(f"  {char_name:<15}: {char_value}")

print("\n" + "="*80)

plt.show()
