"""
Animated Top Categories Countdown
Reveals categories from #10 to #1 with dramatic effect
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get top 10 categories (reversed for countdown)
top_cats = df['search_category'].value_counts().head(10)
categories = top_cats.index.tolist()[::-1]  # Reverse for countdown
counts = top_cats.values[::-1]

# Create figure
fig, ax = plt.subplots(figsize=(14, 8))

n_per_category = 25  # Frames per category reveal
n_frames = n_per_category * 10 + 40  # Extra frames at end

# Colors
colors = plt.cm.plasma(np.linspace(0.1, 0.9, 10))[::-1]

def animate(frame):
    ax.clear()
    
    # How many categories to show
    n_to_show = min(frame // n_per_category + 1, 10)
    
    # Current category being revealed
    current_reveal = frame // n_per_category
    reveal_progress = (frame % n_per_category) / n_per_category
    
    # Build data to display
    display_cats = categories[:n_to_show]
    display_counts = []
    display_colors = []
    
    for i in range(n_to_show):
        if i < current_reveal or frame >= n_per_category * 10:
            # Fully revealed
            display_counts.append(counts[i])
            display_colors.append(colors[i])
        elif i == current_reveal:
            # Currently revealing
            eased = 1 - (1 - reveal_progress) ** 2
            display_counts.append(counts[i] * eased)
            display_colors.append(colors[i])
    
    # Draw bars
    if display_cats:
        y_pos = range(len(display_cats))
        bars = ax.barh(y_pos, display_counts, color=display_colors, 
                      edgecolor='white', linewidth=1.5, height=0.7)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(display_cats, fontsize=11, fontweight='bold')
        
        # Value labels
        for bar, val, original in zip(bars, display_counts, counts[:len(display_counts)]):
            if val > original * 0.5:
                ax.text(val + 1, bar.get_y() + bar.get_height()/2, 
                       f'{int(original)}', va='center', fontsize=11, fontweight='bold')
    
    # Rank numbers
    for i in range(n_to_show):
        rank = 10 - i
        ax.text(-5, i, f'#{rank}', ha='right', va='center', fontsize=14, 
               fontweight='bold', color=colors[i])
    
    ax.set_xlim(-10, max(counts) * 1.2)
    ax.set_ylim(-0.5, 9.5)
    ax.set_xlabel('Number of Books', fontsize=12, fontweight='bold')
    ax.set_title('🏆 TOP 10 BOOK CATEGORIES COUNTDOWN', fontsize=16, fontweight='bold', pad=20)
    
    # Frame indicator
    if frame < n_per_category * 10:
        current_rank = 10 - current_reveal
        ax.text(0.98, 0.98, f'Revealing #{current_rank}...', transform=ax.transAxes,
               ha='right', va='top', fontsize=12, color='gray', style='italic')
    else:
        ax.text(0.98, 0.98, '🎉 Complete!', transform=ax.transAxes,
               ha='right', va='top', fontsize=14, fontweight='bold', color='#27ae60')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=60, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating category countdown GIF...")
anim.save('../gifs/04_category_countdown.gif', writer='pillow', fps=20, dpi=100)
print("✅ Saved: gifs/04_category_countdown.gif")
plt.close()
