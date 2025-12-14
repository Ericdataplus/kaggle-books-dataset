"""
Publisher Analysis Visualization
Creates charts analyzing top publishers and their books
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Filter books with publisher info
df_pub = df[df['publisher'].notna()].copy()

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Top 15 Publishers by Book Count
ax1 = axes[0, 0]
top_publishers = df_pub['publisher'].value_counts().head(15)
colors = sns.color_palette("Blues_r", len(top_publishers))
bars = ax1.barh(range(len(top_publishers)), top_publishers.values, color=colors)
ax1.set_yticks(range(len(top_publishers)))
ax1.set_yticklabels(top_publishers.index, fontsize=9)
ax1.invert_yaxis()
ax1.set_xlabel('Number of Books', fontsize=11)
ax1.set_title('🏢 Top 15 Publishers by Book Count', fontsize=13, fontweight='bold')

for bar, val in zip(bars, top_publishers.values):
    ax1.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}', 
            va='center', fontsize=9, fontweight='bold')

# 2. Average Page Count by Top Publishers
ax2 = axes[0, 1]
top_10_pubs = top_publishers.index[:10]
pub_pages = df_pub[df_pub['publisher'].isin(top_10_pubs)].groupby('publisher')['page_count'].mean()
pub_pages = pub_pages.reindex(top_10_pubs)

colors = sns.color_palette("Oranges_r", len(pub_pages))
bars = ax2.bar(range(len(pub_pages)), pub_pages.values, color=colors)
ax2.set_xticks(range(len(pub_pages)))
ax2.set_xticklabels([p[:20] + '...' if len(p) > 20 else p for p in pub_pages.index], 
                    rotation=45, ha='right', fontsize=8)
ax2.set_ylabel('Average Page Count', fontsize=11)
ax2.set_title('📖 Average Book Length by Publisher', fontsize=13, fontweight='bold')

# 3. Publisher Market Share (Pie Chart)
ax3 = axes[1, 0]
top_5 = top_publishers.head(5)
other = top_publishers.iloc[5:].sum()
pie_data = pd.concat([top_5, pd.Series({'Others': other})])

colors = sns.color_palette("Set2", len(pie_data))
wedges, texts, autotexts = ax3.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%',
                                    colors=colors, startangle=90, pctdistance=0.85)
ax3.set_title('📊 Publisher Market Share\n(Top 5 + Others)', fontsize=13, fontweight='bold')

# Make percentage text bold
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(9)

# 4. Categories Covered by Top Publishers
ax4 = axes[1, 1]
top_5_pubs = top_publishers.index[:5]
pub_category_data = []
for pub in top_5_pubs:
    pub_df = df_pub[df_pub['publisher'] == pub]
    unique_cats = pub_df['search_category'].nunique()
    pub_category_data.append({'publisher': pub, 'categories': unique_cats})

pub_cat_df = pd.DataFrame(pub_category_data)
colors = sns.color_palette("Greens_r", len(pub_cat_df))
bars = ax4.bar(range(len(pub_cat_df)), pub_cat_df['categories'], color=colors)
ax4.set_xticks(range(len(pub_cat_df)))
ax4.set_xticklabels([p[:20] + '...' if len(p) > 20 else p for p in pub_cat_df['publisher']], 
                    rotation=45, ha='right', fontsize=9)
ax4.set_ylabel('Number of Categories', fontsize=11)
ax4.set_title('🎯 Category Diversity by Top Publishers', fontsize=13, fontweight='bold')

for bar, val in zip(bars, pub_cat_df['categories']):
    ax4.text(bar.get_x() + bar.get_width()/2, val + 0.5, f'{val}', 
            ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/04_publisher_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/04_publisher_analysis.png")
plt.close()
