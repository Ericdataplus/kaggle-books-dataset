"""
Animated Stats Counter
Counts up key statistics with animated numbers
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Stats to animate
stats = {
    '📚 Total Books': len(df),
    '📂 Categories': df['search_category'].nunique(),
    '🌍 Languages': df['language'].nunique(),
    '🏢 Publishers': df['publisher'].nunique(),
    '📖 Avg Pages': int(df['page_count'].mean()),
    '⭐ Rated Books': df['average_rating'].notna().sum(),
}

# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

n_frames = 100

def ease_out_expo(t):
    return 1 if t == 1 else 1 - pow(2, -10 * t)

def animate(frame):
    ax.clear()
    
    progress = frame / 60  # First 60 frames for counting
    progress = min(progress, 1)
    eased = ease_out_expo(progress)
    
    y_positions = np.linspace(0.85, 0.15, len(stats))
    
    for i, (label, final_value) in enumerate(stats.items()):
        y = y_positions[i]
        
        current_value = int(final_value * eased)
        
        # Label on left
        ax.text(0.1, y, label, fontsize=16, fontweight='bold', 
               va='center', transform=ax.transAxes)
        
        # Value on right with animation effect
        if progress < 1:
            # Spinning effect during counting
            display_val = f'{current_value:,}'
        else:
            display_val = f'{final_value:,}'
        
        # Color based on value magnitude
        if final_value > 10000:
            color = '#e74c3c'
        elif final_value > 1000:
            color = '#f39c12'
        elif final_value > 100:
            color = '#3498db'
        else:
            color = '#27ae60'
        
        ax.text(0.9, y, display_val, fontsize=24, fontweight='bold',
               va='center', ha='right', transform=ax.transAxes, color=color)
        
        # Progress bar under each stat
        bar_y = y - 0.04
        bar_width = 0.7 * eased
        ax.add_patch(plt.Rectangle((0.1, bar_y), bar_width, 0.015, 
                                    transform=ax.transAxes, facecolor=color, alpha=0.3))
    
    # Title
    ax.text(0.5, 0.95, '📊 BOOKS DATASET STATISTICS', fontsize=20, fontweight='bold',
           ha='center', va='top', transform=ax.transAxes)
    
    # Progress indicator
    if progress < 1:
        ax.text(0.5, 0.03, f'Loading... {int(progress * 100)}%', fontsize=12,
               ha='center', va='bottom', transform=ax.transAxes, color='gray', style='italic')
    else:
        ax.text(0.5, 0.03, '✅ Complete!', fontsize=14,
               ha='center', va='bottom', transform=ax.transAxes, color='#27ae60', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=40, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating stats counter GIF...")
anim.save('../gifs/06_stats_counter.gif', writer='pillow', fps=25, dpi=100)
print("✅ Saved: gifs/06_stats_counter.gif")
plt.close()
