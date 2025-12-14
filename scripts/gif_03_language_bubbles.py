"""
Animated Language Globe - Pulsing circles representing languages
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get language counts
lang_counts = df['language'].value_counts().head(10)

# Language codes to full names
lang_names = {
    'en': 'English', 'es': 'Spanish', 'de': 'German', 'fr': 'French',
    'pt-BR': 'Portuguese', 'it': 'Italian', 'zh-CN': 'Chinese',
    'nl': 'Dutch', 'id': 'Indonesian', 'da': 'Danish'
}

# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

n_frames = 80

# Positions for bubbles (arranged in a circle)
n_langs = len(lang_counts)
angles = np.linspace(0, 2 * np.pi, n_langs, endpoint=False)
radius = 3
x_pos = radius * np.cos(angles)
y_pos = radius * np.sin(angles)

# Max size proportional to count
max_count = lang_counts.values[0]
base_sizes = (lang_counts.values / max_count) * 3000

# Colors
colors = plt.cm.Set2(np.linspace(0, 1, n_langs))

def animate(frame):
    ax.clear()
    
    # Pulsing effect
    pulse = 1 + 0.15 * np.sin(2 * np.pi * frame / 20)
    
    # Growing effect for first 30 frames
    if frame < 30:
        grow = frame / 30
    else:
        grow = 1
    
    sizes = base_sizes * pulse * grow
    
    # Draw bubbles
    for i, (x, y, size, color, lang) in enumerate(zip(x_pos, y_pos, sizes, colors, lang_counts.index)):
        # Main bubble
        circle = plt.Circle((x, y), np.sqrt(size) / 50, color=color, alpha=0.7, ec='white', linewidth=2)
        ax.add_patch(circle)
        
        # Glow effect
        glow = plt.Circle((x, y), np.sqrt(size) / 50 * 1.1, color=color, alpha=0.2)
        ax.add_patch(glow)
        
        # Label
        name = lang_names.get(lang, lang)
        ax.text(x, y, f'{name}\n{lang_counts[lang]:,}', ha='center', va='center',
               fontsize=9, fontweight='bold', color='white' if lang_counts[lang] > 100 else 'black')
    
    # Center text
    ax.text(0, 0, '📚\nBooks by\nLanguage', ha='center', va='center',
           fontsize=14, fontweight='bold', color='#2c3e50')
    
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('🌍 Language Distribution - Bubble Chart', fontsize=16, fontweight='bold', pad=20)
    
    # Add total
    ax.text(0.98, 0.02, f'Total: {len(df):,} books', transform=ax.transAxes,
           ha='right', va='bottom', fontsize=11, color='gray')
    
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=60, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating language bubble animation GIF...")
anim.save('../gifs/03_language_bubbles.gif', writer='pillow', fps=15, dpi=100)
print("✅ Saved: gifs/03_language_bubbles.gif")
plt.close()
