"""
Animated Ratings Pie Chart GIF
Creates a spinning pie chart of rating distribution
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get rating distribution
df_rated = df[df['average_rating'].notna()].copy()
rating_bins = [0, 1, 2, 3, 4, 5]
df_rated['rating_bin'] = pd.cut(df_rated['average_rating'], bins=rating_bins, 
                                 labels=['⭐ 0-1', '⭐⭐ 1-2', '⭐⭐⭐ 2-3', '⭐⭐⭐⭐ 3-4', '⭐⭐⭐⭐⭐ 4-5'])
rating_counts = df_rated['rating_bin'].value_counts().sort_index()

# Colors
colors = ['#e74c3c', '#e67e22', '#f1c40f', '#2ecc71', '#27ae60']

# Create figure
fig, ax = plt.subplots(figsize=(10, 10))

n_frames = 72  # Full rotation in 72 frames (5 degrees per frame)

def animate(frame):
    ax.clear()
    
    start_angle = frame * 5  # Rotate 5 degrees per frame
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        rating_counts.values, 
        labels=rating_counts.index,
        autopct='%1.1f%%',
        colors=colors,
        startangle=start_angle,
        explode=[0.02] * len(rating_counts),
        shadow=True,
        textprops={'fontsize': 11}
    )
    
    for autotext in autotexts:
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    # Add center circle for donut effect
    centre_circle = plt.Circle((0, 0), 0.4, fc='white', ec='gray', linewidth=2)
    ax.add_artist(centre_circle)
    
    # Center text
    ax.text(0, 0, f'{len(df_rated):,}\nBooks\nRated', ha='center', va='center',
           fontsize=14, fontweight='bold', color='#2c3e50')
    
    ax.set_title('⭐ Rating Distribution', fontsize=16, fontweight='bold', pad=20)
    
    return wedges

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=50, blit=False)

# Save as GIF
os.makedirs('../graphs', exist_ok=True)
print("🎬 Generating animated ratings wheel GIF...")
anim.save('../graphs/08_ratings_wheel.gif', writer='pillow', fps=20, dpi=100)
print("✅ Saved: graphs/08_ratings_wheel.gif")
plt.close()
