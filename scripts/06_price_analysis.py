"""
Price Analysis Visualization
Creates charts analyzing book pricing
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

plt.style.use('seaborn-v0_8-darkgrid')

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Filter books with price info and reasonable prices
df_price = df[(df['list_price'].notna()) & (df['list_price'] > 0) & (df['list_price'] < 200)].copy()

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Price Distribution
ax1 = axes[0, 0]
ax1.hist(df_price['list_price'], bins=50, color='#27ae60', edgecolor='white', alpha=0.8)
ax1.axvline(df_price['list_price'].mean(), color='#e74c3c', linestyle='--', linewidth=2, 
            label=f'Mean: ${df_price["list_price"].mean():.2f}')
ax1.axvline(df_price['list_price'].median(), color='#3498db', linestyle='--', linewidth=2,
            label=f'Median: ${df_price["list_price"].median():.2f}')
ax1.set_xlabel('Price ($)', fontsize=11)
ax1.set_ylabel('Number of Books', fontsize=11)
ax1.set_title('💰 Price Distribution', fontsize=13, fontweight='bold')
ax1.legend()

# 2. Average Price by Category
ax2 = axes[0, 1]
category_prices = df_price.groupby('search_category').agg({
    'list_price': 'mean',
    'book_id': 'count'
}).rename(columns={'book_id': 'count'})
category_prices = category_prices[category_prices['count'] >= 5].sort_values('list_price', ascending=True).tail(15)

colors = sns.color_palette("YlOrRd", len(category_prices))
bars = ax2.barh(range(len(category_prices)), category_prices['list_price'], color=colors)
ax2.set_yticks(range(len(category_prices)))
ax2.set_yticklabels(category_prices.index, fontsize=9)
ax2.set_xlabel('Average Price ($)', fontsize=11)
ax2.set_title('💵 Most Expensive Categories\n(min 5 books with price)', fontsize=13, fontweight='bold')

for bar, val in zip(bars, category_prices['list_price']):
    ax2.text(val + 1, bar.get_y() + bar.get_height()/2, f'${val:.0f}', 
            va='center', fontsize=9)

# 3. Cheapest Categories
ax3 = axes[1, 0]
cheap_categories = df_price.groupby('search_category').agg({
    'list_price': 'mean',
    'book_id': 'count'
}).rename(columns={'book_id': 'count'})
cheap_categories = cheap_categories[cheap_categories['count'] >= 5].sort_values('list_price').head(15)

colors = sns.color_palette("YlGn", len(cheap_categories))
bars = ax3.barh(range(len(cheap_categories)), cheap_categories['list_price'], color=colors)
ax3.set_yticks(range(len(cheap_categories)))
ax3.set_yticklabels(cheap_categories.index, fontsize=9)
ax3.set_xlabel('Average Price ($)', fontsize=11)
ax3.set_title('🏷️ Most Affordable Categories\n(min 5 books with price)', fontsize=13, fontweight='bold')

for bar, val in zip(bars, cheap_categories['list_price']):
    ax3.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'${val:.0f}', 
            va='center', fontsize=9)

# 4. Price vs Page Count Scatter
ax4 = axes[1, 1]
df_scatter = df_price[(df_price['page_count'] > 0) & (df_price['page_count'] < 1500)]
scatter = ax4.scatter(df_scatter['page_count'], df_scatter['list_price'], 
                      alpha=0.5, c=df_scatter['list_price'], cmap='viridis',
                      s=30, edgecolors='white', linewidth=0.3)
ax4.set_xlabel('Page Count', fontsize=11)
ax4.set_ylabel('Price ($)', fontsize=11)
ax4.set_title('📊 Price vs Page Count', fontsize=13, fontweight='bold')
plt.colorbar(scatter, ax=ax4, label='Price ($)')

# Add trend line
z = np.polyfit(df_scatter['page_count'].dropna(), df_scatter['list_price'].dropna(), 1)
p = np.poly1d(z)
x_line = np.linspace(df_scatter['page_count'].min(), df_scatter['page_count'].max(), 100)
ax4.plot(x_line, p(x_line), 'r--', linewidth=2, alpha=0.7, label='Trend')
ax4.legend()

plt.tight_layout()
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/06_price_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/06_price_analysis.png")
plt.close()
