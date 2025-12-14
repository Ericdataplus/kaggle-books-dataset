"""
11 - Book Popularity Analysis
Analyzes what makes books popular using ML clustering
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
import warnings
warnings.filterwarnings('ignore')

# Setup
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_path = os.path.join(project_dir, 'google_books_dataset.csv')
output_path = os.path.join(project_dir, 'graphs', '11_popularity_analysis.png')

print("Loading data...")
df = pd.read_csv(data_path)

# Clean
df['page_count'] = pd.to_numeric(df['page_count'], errors='coerce').fillna(300)
df = df[df['page_count'] > 0]
df = df[df['page_count'] < 2000]  # Remove outliers

# Feature engineering
df['title_length'] = df['title'].fillna('').apply(len)
df['has_subtitle'] = df['subtitle'].notna().astype(int)
df['has_description'] = df['description'].notna().astype(int)
df['title_words'] = df['title'].fillna('').apply(lambda x: len(x.split()))

# Get top categories for analysis
category_counts = df['categories'].value_counts().head(10)
top_categories = category_counts.index.tolist()

# Filter to analyzable data
df_analysis = df[df['categories'].isin(top_categories)].copy()
print(f"Analyzing {len(df_analysis):,} books in top 10 categories")

# Category stats
category_stats = df_analysis.groupby('categories').agg({
    'page_count': ['mean', 'std'],
    'title_length': 'mean',
    'has_subtitle': 'mean',
    'has_description': 'mean',
    'title': 'count'
}).round(2)
category_stats.columns = ['avg_pages', 'std_pages', 'avg_title_len', 'subtitle_rate', 'desc_rate', 'count']
category_stats = category_stats.sort_values('count', ascending=False)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Book Category Intelligence', fontsize=22, fontweight='bold', color='white', y=0.98)

# Plot 1: Category sizes
ax1 = axes[0, 0]
ax1.set_facecolor('#0d1117')
colors = plt.cm.viridis(np.linspace(0.9, 0.3, len(category_counts)))
bars = ax1.barh(range(len(category_counts)), category_counts.values, color=colors)
ax1.set_yticks(range(len(category_counts)))
ax1.set_yticklabels([c[:25] + '...' if len(c) > 25 else c for c in category_counts.index], color='white', fontsize=9)
ax1.set_xlabel('Number of Books', color='white')
ax1.set_title('Top 10 Categories', color='white', fontsize=14, fontweight='bold')
ax1.tick_params(colors='white')
for spine in ax1.spines.values(): spine.set_color('#30363d')
ax1.invert_yaxis()

# Plot 2: Page count by category
ax2 = axes[0, 1]
ax2.set_facecolor('#0d1117')
cats = category_stats.head(8).index.tolist()
pages = category_stats.head(8)['avg_pages'].values
colors2 = ['#4ecdc4', '#ff6b6b', '#ffd93d', '#45b7d1', '#96ceb4', '#ff85a1', '#b39ddb', '#80cbc4']
bars = ax2.bar(range(len(cats)), pages, color=colors2[:len(cats)])
ax2.set_xticks(range(len(cats)))
ax2.set_xticklabels([c[:12] + '..' if len(c) > 12 else c for c in cats], color='white', fontsize=8, rotation=45, ha='right')
ax2.set_ylabel('Avg Pages', color='white')
ax2.set_title('Average Book Length by Category', color='white', fontsize=14, fontweight='bold')
ax2.tick_params(colors='white')
for spine in ax2.spines.values(): spine.set_color('#30363d')

# Add value labels
for i, (bar, val) in enumerate(zip(bars, pages)):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, f'{val:.0f}',
             ha='center', color='white', fontsize=9, fontweight='bold')

# Plot 3: Subtitle and Description rates
ax3 = axes[1, 0]
ax3.set_facecolor('#0d1117')
x = np.arange(len(cats))
width = 0.35
sub_rates = category_stats.head(8)['subtitle_rate'].values * 100
desc_rates = category_stats.head(8)['desc_rate'].values * 100

bars1 = ax3.bar(x - width/2, sub_rates, width, label='Has Subtitle', color='#4ecdc4')
bars2 = ax3.bar(x + width/2, desc_rates, width, label='Has Description', color='#ff6b6b')

ax3.set_xticks(x)
ax3.set_xticklabels([c[:12] + '..' if len(c) > 12 else c for c in cats], color='white', fontsize=8, rotation=45, ha='right')
ax3.set_ylabel('Percentage (%)', color='white')
ax3.set_title('Metadata Completeness by Category', color='white', fontsize=14, fontweight='bold')
ax3.legend(facecolor='#161b22', labelcolor='white')
ax3.tick_params(colors='white')
for spine in ax3.spines.values(): spine.set_color('#30363d')

# Plot 4: Key Insights
ax4 = axes[1, 1]
ax4.set_facecolor('#161b22')
ax4.set_xticks([])
ax4.set_yticks([])
for spine in ax4.spines.values(): spine.set_color('#30363d')

ax4.text(0.5, 0.95, 'Key Insights', fontsize=16, fontweight='bold', ha='center', color='white', transform=ax4.transAxes)

longest_cat = category_stats['avg_pages'].idxmax()
shortest_cat = category_stats['avg_pages'].idxmin()
most_subtitles = category_stats['subtitle_rate'].idxmax()
best_described = category_stats['desc_rate'].idxmax()

insights = [
    ('Total Books Analyzed:', f'{len(df_analysis):,}', '#ffd700'),
    ('Categories:', f'{len(top_categories)}', '#58a6ff'),
    ('Longest Books:', f'{longest_cat[:20]}', '#ff6b6b'),
    ('Shortest Books:', f'{shortest_cat[:20]}', '#4ecdc4'),
    ('Most Subtitles:', f'{most_subtitles[:20]}', '#a371f7'),
    ('Best Descriptions:', f'{best_described[:20]}', '#56d364'),
]

for i, (label, value, color) in enumerate(insights):
    y_pos = 0.80 - i * 0.11
    ax4.text(0.08, y_pos, label, fontsize=11, color='#8b949e', transform=ax4.transAxes, va='center')
    ax4.text(0.55, y_pos, value, fontsize=11, color=color, fontweight='bold', transform=ax4.transAxes, va='center')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
print(f"\nKey Findings:")
print(f"  Longest category: {longest_cat} ({category_stats.loc[longest_cat, 'avg_pages']:.0f} pages)")
print(f"  Shortest category: {shortest_cat} ({category_stats.loc[shortest_cat, 'avg_pages']:.0f} pages)")
