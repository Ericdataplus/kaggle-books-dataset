"""
Animated Price Thermometer
Shows price range with animated fill
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
import os

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get price data
df_price = df[(df['list_price'].notna()) & (df['list_price'] > 0) & (df['list_price'] < 150)].copy()

# Price statistics
min_price = df_price['list_price'].min()
max_price = df_price['list_price'].max()
mean_price = df_price['list_price'].mean()
median_price = df_price['list_price'].median()

# Price ranges for "zones"
cheap = df_price[df_price['list_price'] < 20]['list_price'].count()
moderate = df_price[(df_price['list_price'] >= 20) & (df_price['list_price'] < 50)]['list_price'].count()
expensive = df_price[df_price['list_price'] >= 50]['list_price'].count()

# Create figure
fig, ax = plt.subplots(figsize=(10, 12))

n_frames = 80

def animate(frame):
    ax.clear()
    
    progress = min(frame / 50, 1)
    eased = 1 - (1 - progress) ** 3
    
    # Draw thermometer
    therm_x = 0.4
    therm_width = 0.2
    therm_height = 0.7
    therm_y = 0.15
    
    # Background
    bg = patches.FancyBboxPatch((therm_x, therm_y), therm_width, therm_height,
                                 boxstyle="round,pad=0.02", 
                                 facecolor='#ecf0f1', edgecolor='#2c3e50', linewidth=3)
    ax.add_patch(bg)
    
    # Bulb at bottom
    bulb = plt.Circle((therm_x + therm_width/2, therm_y + 0.02), 0.08,
                      color='#e74c3c', ec='#c0392b', linewidth=2)
    ax.add_patch(bulb)
    
    # Fill zones (animated)
    fill_height = therm_height * 0.85 * eased
    
    # Cheap zone (green)
    cheap_height = fill_height * (cheap / len(df_price))
    cheap_rect = patches.Rectangle((therm_x + 0.02, therm_y + 0.05), 
                                    therm_width - 0.04, cheap_height,
                                    facecolor='#2ecc71', alpha=0.8)
    ax.add_patch(cheap_rect)
    
    # Moderate zone (yellow)
    mod_height = fill_height * (moderate / len(df_price))
    mod_rect = patches.Rectangle((therm_x + 0.02, therm_y + 0.05 + cheap_height), 
                                  therm_width - 0.04, mod_height,
                                  facecolor='#f1c40f', alpha=0.8)
    ax.add_patch(mod_rect)
    
    # Expensive zone (red)
    exp_height = fill_height * (expensive / len(df_price))
    exp_rect = patches.Rectangle((therm_x + 0.02, therm_y + 0.05 + cheap_height + mod_height), 
                                  therm_width - 0.04, exp_height,
                                  facecolor='#e74c3c', alpha=0.8)
    ax.add_patch(exp_rect)
    
    # Scale marks
    for i, price in enumerate([0, 25, 50, 75, 100, 125, 150]):
        y = therm_y + 0.05 + (price / 150) * therm_height * 0.85
        ax.plot([therm_x - 0.02, therm_x], [y, y], color='#2c3e50', linewidth=2)
        ax.text(therm_x - 0.04, y, f'${price}', ha='right', va='center', fontsize=10)
    
    # Legend on right side
    legend_x = 0.7
    legend_y = 0.6
    
    # Cheap
    ax.add_patch(patches.Rectangle((legend_x, legend_y + 0.15), 0.03, 0.03, facecolor='#2ecc71'))
    ax.text(legend_x + 0.05, legend_y + 0.165, f'Under $20: {int(cheap * eased):,} books', fontsize=11, va='center')
    
    # Moderate
    ax.add_patch(patches.Rectangle((legend_x, legend_y + 0.08), 0.03, 0.03, facecolor='#f1c40f'))
    ax.text(legend_x + 0.05, legend_y + 0.095, f'$20-$50: {int(moderate * eased):,} books', fontsize=11, va='center')
    
    # Expensive
    ax.add_patch(patches.Rectangle((legend_x, legend_y + 0.01), 0.03, 0.03, facecolor='#e74c3c'))
    ax.text(legend_x + 0.05, legend_y + 0.025, f'Over $50: {int(expensive * eased):,} books', fontsize=11, va='center')
    
    # Statistics
    ax.text(0.5, 0.05, f'💰 Mean: ${mean_price:.2f}  |  Median: ${median_price:.2f}', 
           ha='center', fontsize=12, fontweight='bold', transform=ax.transAxes)
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('📊 Book Price Thermometer', fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()

# Create animation
anim = animation.FuncAnimation(fig, animate, frames=n_frames, interval=50, blit=False)

# Save
os.makedirs('../gifs', exist_ok=True)
print("🎬 Generating price thermometer GIF...")
anim.save('../gifs/05_price_thermometer.gif', writer='pillow', fps=20, dpi=100)
print("✅ Saved: gifs/05_price_thermometer.gif")
plt.close()
