"""
Ratings Analysis Visualization
Creates charts for rating distribution and ratings by category
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Filter books with ratings
df_rated = df[df['average_rating'].notna()].copy()

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Rating Distribution Histogram
ax1 = axes[0, 0]
colors = ['#e74c3c' if x < 3 else '#f39c12' if x < 4 else '#2ecc71' for x in np.arange(1, 5.5, 0.5)]
ax1.hist(df_rated['average_rating'], bins=20, color='#3498db', edgecolor='white', alpha=0.8)
ax1.axvline(df_rated['average_rating'].mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: {df_rated["average_rating"].mean():.2f}')
ax1.axvline(df_rated['average_rating'].median(), color='#2ecc71', linestyle='--', linewidth=2, label=f'Median: {df_rated["average_rating"].median():.2f}')
ax1.set_xlabel('Average Rating', fontsize=11)
ax1.set_ylabel('Number of Books', fontsize=11)
ax1.set_title('⭐ Rating Distribution', fontsize=13, fontweight='bold')
ax1.legend()

# 2. Top 10 Categories by Average Rating
ax2 = axes[0, 1]
category_ratings = df_rated.groupby('search_category').agg({
    'average_rating': 'mean',
    'book_id': 'count'
}).rename(columns={'book_id': 'count'})
category_ratings = category_ratings[category_ratings['count'] >= 5].sort_values('average_rating', ascending=True).tail(15)

colors = sns.color_palette("RdYlGn", len(category_ratings))
bars = ax2.barh(range(len(category_ratings)), category_ratings['average_rating'], color=colors)
ax2.set_yticks(range(len(category_ratings)))
ax2.set_yticklabels(category_ratings.index, fontsize=9)
ax2.set_xlabel('Average Rating', fontsize=11)
ax2.set_title('🏆 Top 15 Categories by Rating\n(min 5 books)', fontsize=13, fontweight='bold')
ax2.set_xlim(3.5, 5)

# Add value labels
for bar, val in zip(bars, category_ratings['average_rating']):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2, f'{val:.2f}', 
            va='center', fontsize=9)

# 3. Ratings Count vs Average Rating Scatter
ax3 = axes[1, 0]
df_scatter = df_rated[df_rated['ratings_count'] > 0]
scatter = ax3.scatter(df_scatter['ratings_count'], df_scatter['average_rating'], 
                      alpha=0.6, c=df_scatter['average_rating'], cmap='RdYlGn',
                      s=50, edgecolors='white', linewidth=0.5)
ax3.set_xlabel('Number of Ratings', fontsize=11)
ax3.set_ylabel('Average Rating', fontsize=11)
ax3.set_title('📊 Ratings Count vs Average Rating', fontsize=13, fontweight='bold')
plt.colorbar(scatter, ax=ax3, label='Rating')

# 4. Rating Distribution by Language (top 5 languages)
ax4 = axes[1, 1]
top_langs = df_rated['language'].value_counts().head(5).index
df_lang = df_rated[df_rated['language'].isin(top_langs)]
lang_colors = sns.color_palette("husl", 5)
df_lang.boxplot(column='average_rating', by='language', ax=ax4, patch_artist=True)
ax4.set_xlabel('Language', fontsize=11)
ax4.set_ylabel('Average Rating', fontsize=11)
ax4.set_title('🌍 Rating Distribution by Language', fontsize=13, fontweight='bold')
plt.suptitle('')  # Remove automatic title

plt.tight_layout()
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/02_ratings_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/02_ratings_analysis.png")
plt.close()
