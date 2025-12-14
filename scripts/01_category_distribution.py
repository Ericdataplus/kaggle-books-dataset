"""
Category Distribution Visualization
Creates a horizontal bar chart showing the top 20 book categories
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

# Load data
df = pd.read_csv('../google_books_dataset.csv')

# Get top 20 categories
category_counts = df['search_category'].value_counts().head(20)

# Create figure
fig, ax = plt.subplots(figsize=(12, 10))

# Create horizontal bar chart
colors = sns.color_palette("viridis", len(category_counts))
bars = ax.barh(range(len(category_counts)), category_counts.values, color=colors)

# Customize
ax.set_yticks(range(len(category_counts)))
ax.set_yticklabels(category_counts.index, fontsize=11)
ax.invert_yaxis()  # Top category at the top
ax.set_xlabel('Number of Books', fontsize=12, fontweight='bold')
ax.set_title('📚 Top 20 Book Categories', fontsize=16, fontweight='bold', pad=20)

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, category_counts.values)):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}', 
            va='center', fontsize=10, fontweight='bold')

# Add total books annotation
ax.text(0.98, 0.02, f'Total Books: {len(df):,}', 
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=10, style='italic', color='gray')

plt.tight_layout()

# Save
os.makedirs('../graphs', exist_ok=True)
plt.savefig('../graphs/01_category_distribution.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✅ Saved: graphs/01_category_distribution.png")
plt.close()
