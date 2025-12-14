"""
Animated Category Bar Chart Race GIF
Creates an animated GIF showing categories accumulating books
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get top 15 categories
category_counts = df['search_category'].value_counts().head(15)
categories = category_counts.index.tolist()
final_values = category_counts.values

# Create frames for animation
n_frames = 60
frames_data = []

for i in range(n_frames + 1):
    progress = i / n_frames
    # Use easing function for smooth growth
    eased_progress = 1 - (1 - progress) ** 3  # Ease out cubic
    current_values = (final_values * eased_progress).astype(int)
    frames_data.append(current_values)

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Color palette
colors = plt.cm.viridis(np.linspace(0, 0.9, len(categories)))

def animate(frame):
    ax.clear()
    
    values = frames_data[frame]
    
    # Create bars
    bars = ax.barh(range(len(categories)), values, color=colors, edgecolor='white', linewidth=0.5)
    
    # Customize
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Books', fontsize=12, fontweight='bold')
    ax.set_title('📚 Books Dataset - Category Distribution', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, max(final_values) * 1.15)
    
    # Add value labels
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}', 
                   va='center', fontsize=9, fontweight='bold')
    
    # Add frame counter
    ax.text(0.98, 0.02, f'Frame: {frame}/{n_frames}', 
           transform=ax.transAxes, ha='right', va='bottom',
           fontsize=9, color='gray', style='italic')
    
    plt.tight_layout()
    return bars

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames + 1, interval=50, blit=False)

# Save as GIF
os.makedirs('../graphs', exist_ok=True)
print("🎬 Generating animated GIF... (this may take a moment)")
anim.save('../graphs/07_category_growth.gif', writer='pillow', fps=20, dpi=100)
print("✅ Saved: graphs/07_category_growth.gif")
plt.close()
