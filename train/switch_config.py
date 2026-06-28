#!/usr/bin/env python3
"""
Utility untuk quick config switch untuk training dengan berbagai dataset sizes
Usage: python switch_config.py [small|medium|large|custom]
"""

import sys
from pathlib import Path

CONFIG_TEMPLATES = {
    "small": {
        "description": "36 images - Quick validation test",
        "epochs": 60,
        "batch_size": 16,
        "img_size": 640,
        "comment": "# Dataset kecil, training cepat untuk validation"
    },
    "medium": {
        "description": "200-500 images - Balanced training",
        "epochs": 50,
        "batch_size": 32,
        "img_size": 640,
        "comment": "# Dataset medium, balance kecepatan & akurasi"
    },
    "large": {
        "description": "1000+ images - Full training",
        "epochs": 40,
        "batch_size": 64,
        "img_size": 640,
        "comment": "# Dataset besar, focus akurasi"
    },
    "gpu": {
        "description": "GPU training (if available)",
        "epochs": 40,
        "batch_size": 128,
        "img_size": 640,
        "comment": "# GPU available, bigger batch & more intensive"
    }
}

def generate_config(config_name):
    """Generate trainer configuration"""
    if config_name not in CONFIG_TEMPLATES:
        print(f"❌ Unknown config: {config_name}")
        print(f"Available: {', '.join(CONFIG_TEMPLATES.keys())}")
        return None
    
    cfg = CONFIG_TEMPLATES[config_name]
    
    config_code = f'''    # Setup
    project_root = Path(__file__).parent.parent
    trainer = SawoYOLOTrainer(
        project_root=project_root,
        img_size={cfg['img_size']},  {cfg['comment']}
        epochs={cfg['epochs']},
        batch_size={cfg['batch_size']},
    )'''
    
    return config_code, cfg

def show_all_configs():
    """Display all available configurations"""
    print("\n" + "=" * 70)
    print("🎯 Available Training Configurations")
    print("=" * 70)
    for name, cfg in CONFIG_TEMPLATES.items():
        print(f"\n📌 {name.upper()}")
        print(f"   Description: {cfg['description']}")
        print(f"   Epochs: {cfg['epochs']}")
        print(f"   Batch Size: {cfg['batch_size']}")
        print(f"   Image Size: {cfg['img_size']}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_all_configs()
        print("\n✏️  To use a config, edit train_local.py line ~611 with:")
        print("\nExample for SMALL dataset:")
        result = generate_config("small")
        if result:
            code, _ = result
            print(code)
    else:
        config = sys.argv[1].lower()
        result = generate_config(config)
        if result:
            code, cfg = result
            print(f"\n✅ Config: {config}")
            print(f"   {cfg['description']}\n")
            print("Update train_local.py dengan:\n")
            print(code)
