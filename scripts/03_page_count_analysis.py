"""
Page Count Analysis Visualization
Creates charts analyzing book lengths across categories
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Filter valid page counts (non-zero, reasonable range)
df_pages = df[(df['page_count'] > 0) & (df['page_count'] < 2000)].copy()

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Page Count Distribution
ax1 = axes[0, 0]
ax1.hist(df_pages['page_count'], bins=50, color='#9b59b6', edgecolor='white', alpha=0.8)
ax1.axvline(df_pages['page_count'].mean(), color='#e74c3c', linestyle='--', linewidth=2, 
            label=f'Mean: {df_pages["page_count"].mean():.0f}')
ax1.axvline(df_pages['page_count'].median(), color='#2ecc71', linestyle='--', linewidth=2,
            label=f'Median: {df_pages["page_count"].median():.0f}')
ax1.set_xlabel('Page Count', fontsize=11)
ax1.set_ylabel('Number of Books', fontsize=11)
ax1.set_title('📖 Page Count Distribution', fontsize=13, fontweight='bold')
ax1.legend()

# 2. Average Page Count by Category (Top 15)
ax2 = axes[0, 1]
category_pages = df_pages.groupby('search_category')['page_count'].mean().sort_values(ascending=True).tail(15)
colors = sns.color_palette("magma", len(category_pages))
bars = ax2.barh(range(len(category_pages)), category_pages.values, color=colors)
ax2.set_yticks(range(len(category_pages)))
ax2.set_yticklabels(category_pages.index, fontsize=9)
ax2.set_xlabel('Average Page Count', fontsize=11)
ax2.set_title('📚 Longest Books by Category\n(Average Pages)', fontsize=13, fontweight='bold')

for bar, val in zip(bars, category_pages.values):
    ax2.text(val + 5, bar.get_y() + bar.get_height()/2, f'{val:.0f}', 
            va='center', fontsize=9)

# 3. Shortest Books by Category
ax3 = axes[1, 0]
category_pages_short = df_pages.groupby('search_category')['page_count'].mean().sort_values().head(15)
colors = sns.color_palette("cool", len(category_pages_short))
bars = ax3.barh(range(len(category_pages_short)), category_pages_short.values, color=colors)
ax3.set_yticks(range(len(category_pages_short)))
ax3.set_yticklabels(category_pages_short.index, fontsize=9)
ax3.set_xlabel('Average Page Count', fontsize=11)
ax3.set_title('📄 Shortest Books by Category\n(Average Pages)', fontsize=13, fontweight='bold')

for bar, val in zip(bars, category_pages_short.values):
    ax3.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val:.0f}', 
            va='center', fontsize=9)

# 4. Page Count Box Plot by Top Categories
ax4 = axes[1, 1]
top_cats = df_pages['search_category'].value_counts().head(8).index
df_box = df_pages[df_pages['search_category'].isin(top_cats)]

# Create box plot
box_data = [df_box[df_box['search_category'] == cat]['page_count'].values for cat in top_cats]
bp = ax4.boxplot(box_data, labels=[cat[:15] + '...' if len(cat) > 15 else cat for cat in top_cats],
                 patch_artist=True)

# Color the boxes
colors = sns.color_palette("Set2", len(top_cats))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax4.set_xlabel('Category', fontsize=11)
ax4.set_ylabel('Page Count', fontsize=11)
ax4.set_title('📊 Page Count Distribution by Category', fontsize=13, fontweight='bold')
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/03_page_count_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/03_page_count_analysis.png")
plt.close()
