"""
Animated Histogram - Page Count Distribution Building Up
Shows histogram bars growing dynamically
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Filter valid page counts
df_pages = df[(df['page_count'] > 0) & (df['page_count'] < 1500)].copy()

# Create histogram data
n_bins = 30
hist_values, bin_edges = np.histogram(df_pages['page_count'], bins=n_bins)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
bin_width = bin_edges[1] - bin_edges[0]

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

n_frames = 60

# Color gradient
colors = plt.cm.viridis(np.linspace(0.2, 0.9, n_bins))

def animate(frame):
    ax.clear()
    
    progress = frame / n_frames
    eased = min(1.0, 1 - (1 - progress) ** 3)  # Ease out cubic, clamp to 1.0
    
    current_heights = hist_values * eased
    
    bars = ax.bar(bin_centers, current_heights, width=bin_width * 0.9, 
                  color=colors, edgecolor='white', linewidth=0.5)
    
    # Add mean and median lines
    mean_val = df_pages['page_count'].mean()
    median_val = df_pages['page_count'].median()
    
    ax.axvline(mean_val, color='#e74c3c', linestyle='--', linewidth=2.5, 
              label=f'Mean: {mean_val:.0f}', alpha=eased)
    ax.axvline(median_val, color='#2ecc71', linestyle='--', linewidth=2.5,
              label=f'Median: {median_val:.0f}', alpha=eased)
    
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, max(hist_values) * 1.15)
    ax.set_xlabel('Page Count', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Books', fontsize=12, fontweight='bold')
    ax.set_title('📖 Page Count Distribution\nBuilding Up...', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    
    # Progress bar
    ax.text(0.5, 0.95, f'{int(eased * 100)}%', transform=ax.transAxes,
           fontsize=20, fontweight='bold', ha='center', va='top', color='gray', alpha=0.5)
    
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames + 20, interval=50, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating histogram animation GIF...")
anim.save('../gifs/02_histogram_buildup.gif', writer='pillow', fps=20, dpi=100)
print("✅ Saved: gifs/02_histogram_buildup.gif")
plt.close()
