"""
Summary Dashboard
Creates a comprehensive single-image dashboard of the dataset
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Create figure with subplots
fig = plt.figure(figsize=(18, 14))
fig.suptitle('📚 Books Dataset - Comprehensive Dashboard', fontsize=20, fontweight='bold', y=0.98)

# Grid spec for custom layout
gs = fig.add_gridspec(3, 4, hspace=0.35, wspace=0.3)

# 1. Key Stats Box (top left)
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
stats_text = f"""
📊 KEY STATISTICS

Total Books: {len(df):,}
Categories: {df['search_category'].nunique()}
Languages: {df['language'].nunique()}
Publishers: {df['publisher'].nunique():,}

Avg Pages: {df['page_count'].mean():.0f}
Avg Rating: {df['average_rating'].mean():.2f}
Rated Books: {df['average_rating'].notna().sum():,}
"""
ax1.text(0.1, 0.9, stats_text, transform=ax1.transAxes, fontsize=11, 
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8, edgecolor='#3498db', linewidth=2))

# 2. Top 10 Categories (top middle)
ax2 = fig.add_subplot(gs[0, 1:3])
top_cats = df['search_category'].value_counts().head(10)
colors = sns.color_palette("viridis", len(top_cats))
bars = ax2.barh(range(len(top_cats)), top_cats.values, color=colors)
ax2.set_yticks(range(len(top_cats)))
ax2.set_yticklabels(top_cats.index, fontsize=9)
ax2.invert_yaxis()
ax2.set_xlabel('Books', fontsize=10)
ax2.set_title('🏆 Top 10 Categories', fontsize=12, fontweight='bold')
for bar, val in zip(bars, top_cats.values):
    ax2.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}', va='center', fontsize=8)

# 3. Language Pie (top right)
ax3 = fig.add_subplot(gs[0, 3])
lang_counts = df['language'].value_counts()
english = lang_counts.get('en', 0)
non_english = len(df) - english
pie_data = [english, non_english]
colors = ['#3498db', '#e74c3c']
ax3.pie(pie_data, labels=['English', 'Other'], autopct='%1.1f%%', colors=colors, startangle=90)
ax3.set_title('🌍 Language Split', fontsize=12, fontweight='bold')

# 4. Page Count Distribution (middle left)
ax4 = fig.add_subplot(gs[1, 0:2])
df_pages = df[(df['page_count'] > 0) & (df['page_count'] < 1500)]
ax4.hist(df_pages['page_count'], bins=40, color='#9b59b6', edgecolor='white', alpha=0.8)
ax4.axvline(df_pages['page_count'].mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: {df_pages["page_count"].mean():.0f}')
ax4.axvline(df_pages['page_count'].median(), color='#2ecc71', linestyle='--', linewidth=2, label=f'Median: {df_pages["page_count"].median():.0f}')
ax4.set_xlabel('Page Count', fontsize=10)
ax4.set_ylabel('Books', fontsize=10)
ax4.set_title('📖 Page Count Distribution', fontsize=12, fontweight='bold')
ax4.legend(fontsize=8)

# 5. Rating Distribution (middle right)
ax5 = fig.add_subplot(gs[1, 2:4])
df_rated = df[df['average_rating'].notna()]
ax5.hist(df_rated['average_rating'], bins=20, color='#f39c12', edgecolor='white', alpha=0.8)
ax5.axvline(df_rated['average_rating'].mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: {df_rated["average_rating"].mean():.2f}')
ax5.set_xlabel('Rating', fontsize=10)
ax5.set_ylabel('Books', fontsize=10)
ax5.set_title('⭐ Rating Distribution (857 rated books)', fontsize=12, fontweight='bold')
ax5.legend(fontsize=8)

# 6. Top Publishers (bottom left)
ax6 = fig.add_subplot(gs[2, 0:2])
df_pub = df[df['publisher'].notna()]
top_pubs = df_pub['publisher'].value_counts().head(8)
colors = sns.color_palette("Blues_r", len(top_pubs))
bars = ax6.bar(range(len(top_pubs)), top_pubs.values, color=colors)
ax6.set_xticks(range(len(top_pubs)))
ax6.set_xticklabels([p[:15] + '...' if len(p) > 15 else p for p in top_pubs.index], rotation=45, ha='right', fontsize=8)
ax6.set_ylabel('Books', fontsize=10)
ax6.set_title('🏢 Top 8 Publishers', fontsize=12, fontweight='bold')

# 7. Missing Data Summary (bottom right)
ax7 = fig.add_subplot(gs[2, 2:4])
missing_data = {
    'rating': (df['average_rating'].isna().sum() / len(df)) * 100,
    'price': (df['list_price'].isna().sum() / len(df)) * 100,
    'publisher': (df['publisher'].isna().sum() / len(df)) * 100,
    'description': (df['description'].isna().sum() / len(df)) * 100,
    'authors': (df['authors'].isna().sum() / len(df)) * 100,
    'isbn_13': (df['isbn_13'].isna().sum() / len(df)) * 100,
}
missing_df = pd.Series(missing_data).sort_values(ascending=True)
colors = ['#2ecc71' if v < 30 else '#f39c12' if v < 60 else '#e74c3c' for v in missing_df.values]
bars = ax7.barh(range(len(missing_df)), missing_df.values, color=colors)
ax7.set_yticks(range(len(missing_df)))
ax7.set_yticklabels(missing_df.index, fontsize=9)
ax7.set_xlabel('Missing (%)', fontsize=10)
ax7.set_title('⚠️ Missing Data Overview', fontsize=12, fontweight='bold')
ax7.set_xlim(0, 100)
for bar, val in zip(bars, missing_df.values):
    ax7.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=8)

plt.tight_layout(rect=[0, 0, 1, 0.96])
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/10_summary_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/10_summary_dashboard.png")
plt.close()
