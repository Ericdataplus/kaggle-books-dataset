"""
Language Analysis Visualization
Creates charts analyzing book distribution by language
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')

# Load data
df = pd.read_csv('../google_books_dataset.csv')

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Language Distribution (excluding English for better visibility)
ax1 = axes[0, 0]
lang_counts = df['language'].value_counts()
non_english = lang_counts[lang_counts.index != 'en'].head(15)

colors = sns.color_palette("husl", len(non_english))
bars = ax1.barh(range(len(non_english)), non_english.values, color=colors)
ax1.set_yticks(range(len(non_english)))
ax1.set_yticklabels(non_english.index, fontsize=10)
ax1.invert_yaxis()
ax1.set_xlabel('Number of Books', fontsize=11)
ax1.set_title('🌍 Top Non-English Languages', fontsize=13, fontweight='bold')

for bar, val in zip(bars, non_english.values):
    ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val}', 
            va='center', fontsize=9, fontweight='bold')

# 2. English vs Non-English Pie Chart
ax2 = axes[0, 1]
english_count = lang_counts.get('en', 0)
non_english_count = len(df) - english_count

pie_data = pd.Series({'English': english_count, 'Non-English': non_english_count})
colors = ['#3498db', '#e74c3c']
explode = (0.02, 0.05)
wedges, texts, autotexts = ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%',
                                    colors=colors, startangle=90, explode=explode,
                                    shadow=True)
ax2.set_title('📚 English vs Non-English Books', fontsize=13, fontweight='bold')

for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)
    autotext.set_color('white')

# 3. Average Page Count by Language
ax3 = axes[1, 0]
top_langs = lang_counts.head(10).index
lang_pages = df[df['language'].isin(top_langs)].groupby('language')['page_count'].mean().sort_values(ascending=True)

colors = sns.color_palette("coolwarm", len(lang_pages))
bars = ax3.barh(range(len(lang_pages)), lang_pages.values, color=colors)
ax3.set_yticks(range(len(lang_pages)))
ax3.set_yticklabels(lang_pages.index, fontsize=10)
ax3.set_xlabel('Average Page Count', fontsize=11)
ax3.set_title('📖 Average Book Length by Language', fontsize=13, fontweight='bold')

for bar, val in zip(bars, lang_pages.values):
    ax3.text(val + 5, bar.get_y() + bar.get_height()/2, f'{val:.0f}', 
            va='center', fontsize=9)

# 4. Language Diversity by Category
ax4 = axes[1, 1]
# Find categories with most language diversity
cat_lang_diversity = df.groupby('search_category')['language'].nunique().sort_values(ascending=False).head(15)

colors = sns.color_palette("Spectral", len(cat_lang_diversity))
bars = ax4.barh(range(len(cat_lang_diversity)), cat_lang_diversity.values, color=colors)
ax4.set_yticks(range(len(cat_lang_diversity)))
ax4.set_yticklabels(cat_lang_diversity.index, fontsize=9)
ax4.invert_yaxis()
ax4.set_xlabel('Number of Languages', fontsize=11)
ax4.set_title('🌐 Most Multilingual Categories', fontsize=13, fontweight='bold')

for bar, val in zip(bars, cat_lang_diversity.values):
    ax4.text(val + 0.1, bar.get_y() + bar.get_height()/2, f'{val}', 
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/05_language_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/05_language_analysis.png")
plt.close()
