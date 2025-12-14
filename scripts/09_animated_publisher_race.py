"""
Animated Publisher Bar Race GIF
Creates a bar chart race animation of top publishers
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get top 12 publishers
df_pub = df[df['publisher'].notna()]
top_publishers = df_pub['publisher'].value_counts().head(12)
publishers = top_publishers.index.tolist()
final_values = top_publishers.values

# Create frames - bars grow at different rates for racing effect
n_frames = 80
frames_data = []

# Random growth rates for racing effect
np.random.seed(42)
growth_patterns = []
for i in range(len(publishers)):
    # Each publisher has slightly different growth curve
    noise = np.random.randn(n_frames) * 0.05
    pattern = np.cumsum(np.ones(n_frames) + noise)
    pattern = pattern / pattern[-1]  # Normalize to 0-1
    growth_patterns.append(pattern)

for i in range(n_frames + 1):
    if i == 0:
        current_values = np.zeros(len(publishers))
    elif i == n_frames:
        current_values = final_values.astype(float)
    else:
        current_values = []
        for j, fv in enumerate(final_values):
            idx = min(i, len(growth_patterns[j]) - 1)
            current_values.append(fv * growth_patterns[j][idx])
        current_values = np.array(current_values)
    frames_data.append(current_values)

# Create figure
fig, ax = plt.subplots(figsize=(12, 8))

# Color palette
colors = plt.cm.tab20(np.linspace(0, 1, len(publishers)))

def animate(frame):
    ax.clear()
    
    values = frames_data[frame]
    
    # Sort by current value for racing effect
    sorted_indices = np.argsort(values)[::-1]
    sorted_pubs = [publishers[i] for i in sorted_indices]
    sorted_vals = values[sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]
    
    # Create bars
    y_pos = range(len(sorted_pubs))
    bars = ax.barh(y_pos, sorted_vals, color=sorted_colors, edgecolor='white', linewidth=0.5)
    
    # Customize
    ax.set_yticks(y_pos)
    ax.set_yticklabels([p[:25] + '...' if len(p) > 25 else p for p in sorted_pubs], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Books', fontsize=12, fontweight='bold')
    ax.set_title('🏢 Publisher Bar Race - Top 12 Publishers', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, max(final_values) * 1.15)
    
    # Add value labels
    for bar, val in zip(bars, sorted_vals):
        if val > 5:
            ax.text(val + 2, bar.get_y() + bar.get_height()/2, f'{int(val)}', 
                   va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    return bars

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames + 1, interval=60, blit=False)

# Save as GIF
os.makedirs('../graphs', exist_ok=True)
print("🎬 Generating publisher bar race GIF...")
anim.save('../graphs/09_publisher_race.gif', writer='pillow', fps=15, dpi=100)
print("✅ Saved: graphs/09_publisher_race.gif")
plt.close()
