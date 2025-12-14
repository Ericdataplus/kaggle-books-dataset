"""
Animated Scatter Plot - Page Count vs Rating
Shows books appearing one by one with color-coded ratings
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Filter books with ratings and valid page counts
df_scatter = df[(df['average_rating'].notna()) & 
                (df['page_count'] > 0) & 
                (df['page_count'] < 1500)].copy()

# Sample for animation (too many points would be slow)
df_sample = df_scatter.sample(n=min(200, len(df_scatter)), random_state=42)
df_sample = df_sample.sort_values('average_rating')

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

n_frames = len(df_sample) + 30  # Extra frames at end

# Pre-calculate all points
pages = df_sample['page_count'].values
ratings = df_sample['average_rating'].values
colors = ratings  # Color by rating

def animate(frame):
    ax.clear()
    
    # Number of points to show
    n_points = min(frame, len(df_sample))
    
    if n_points > 0:
        scatter = ax.scatter(pages[:n_points], ratings[:n_points], 
                            c=colors[:n_points], cmap='RdYlGn',
                            s=80, alpha=0.7, edgecolors='white', linewidth=0.5,
                            vmin=1, vmax=5)
        
        if frame == n_frames - 1:  # Add colorbar on last frame
            plt.colorbar(scatter, ax=ax, label='Rating')
    
    ax.set_xlim(0, 1500)
    ax.set_ylim(0.5, 5.5)
    ax.set_xlabel('Page Count', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Rating', fontsize=12, fontweight='bold')
    ax.set_title(f'📊 Books: Page Count vs Rating\n({n_points} books shown)', 
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add statistics
    if n_points > 0:
        avg_pages = pages[:n_points].mean()
        avg_rating = ratings[:n_points].mean()
        ax.text(0.02, 0.98, f'Avg Pages: {avg_pages:.0f}\nAvg Rating: {avg_rating:.2f}', 
               transform=ax.transAxes, fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=50, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating scatter animation GIF...")
anim.save('../gifs/01_scatter_buildup.gif', writer='pillow', fps=25, dpi=100)
print("✅ Saved: gifs/01_scatter_buildup.gif")
plt.close()
