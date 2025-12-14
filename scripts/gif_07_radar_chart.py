"""
Animated Radar/Spider Chart
Shows category metrics in animated radar format
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Select categories for radar
categories_for_radar = ['romance', 'science fiction', 'biography', 'mystery thriller', 
                        'machine learning AI', 'finance investing']

# Calculate metrics for each category
metrics = ['Books', 'Avg Pages', 'Has Rating', 'Has Price', 'Has Description']

radar_data = []
for cat in categories_for_radar:
    cat_df = df[df['search_category'] == cat]
    data = {
        'Books': len(cat_df) / 50,  # Normalized
        'Avg Pages': cat_df['page_count'].mean() / 600 if cat_df['page_count'].mean() > 0 else 0,
        'Has Rating': cat_df['average_rating'].notna().mean(),
        'Has Price': cat_df['list_price'].notna().mean(),
        'Has Description': cat_df['description'].notna().mean(),
    }
    radar_data.append(data)

# Create figure
fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))

n_frames = 80
angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # Complete the circle

colors = plt.cm.Set1(np.linspace(0, 1, len(categories_for_radar)))

def animate(frame):
    ax.clear()
    
    progress = min(frame / 40, 1)
    eased = 1 - (1 - progress) ** 3
    
    # Rotation effect
    rotation = frame * 0.02
    
    for i, (cat, data, color) in enumerate(zip(categories_for_radar, radar_data, colors)):
        values = list(data.values())
        values = [v * eased for v in values]  # Animate growth
        values += values[:1]  # Complete the circle
        
        # Offset each category slightly for visual interest
        offset_angles = [a + rotation for a in angles]
        
        ax.plot(offset_angles, values, 'o-', linewidth=2, color=color, label=cat, markersize=6)
        ax.fill(offset_angles, values, alpha=0.15, color=color)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 1.2)
    
    # Legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
    
    ax.set_title('🎯 Category Metrics Radar Chart', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=60, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating radar chart GIF...")
anim.save('../gifs/07_radar_chart.gif', writer='pillow', fps=15, dpi=100)
print("✅ Saved: gifs/07_radar_chart.gif")
plt.close()
