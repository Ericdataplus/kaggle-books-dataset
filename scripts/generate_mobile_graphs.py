"""
Mobile-Optimized Graphs Generator for Google Books Dataset
"""
import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
output_dir = os.path.join(project_dir, 'graphs_mobile')
os.makedirs(output_dir, exist_ok=True)

MOBILE_CONFIG = {
    'figsize': (6, 8),
    'title_size': 20,
    'bg_color': '#0d1117',
    'text_color': '#ffffff',
}

def setup_style():
    plt.rcParams['font.size'] = 14
    plt.rcParams['figure.facecolor'] = MOBILE_CONFIG['bg_color']
    plt.rcParams['axes.facecolor'] = MOBILE_CONFIG['bg_color']
    plt.rcParams['text.color'] = MOBILE_CONFIG['text_color']
    plt.rcParams['axes.labelcolor'] = MOBILE_CONFIG['text_color']
    plt.rcParams['xtick.color'] = MOBILE_CONFIG['text_color']
    plt.rcParams['ytick.color'] = MOBILE_CONFIG['text_color']

def style_axes(ax):
    ax.set_facecolor(MOBILE_CONFIG['bg_color'])
    for spine in ax.spines.values():
        spine.set_color('#30363d')

def generate_stats():
    print("📱 Generating: Key Stats")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.92, 'Google Books', fontsize=24, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.85, 'Dataset Overview', fontsize=16,
            ha='center', color='#8b949e', transform=ax.transAxes)
    
    stats = [
        ('15,292', 'Total Books', '#4facfe'),
        ('$15.99', 'Median Price', '#56d364'),
        ('3.8★', 'Avg Rating', '#feca57'),
        ('286', 'Authors', '#a371f7'),
    ]
    
    for i, (value, label, color) in enumerate(stats):
        y = 0.68 - i * 0.17
        ax.text(0.5, y, value, fontsize=48, fontweight='bold',
                ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.05, label, fontsize=14,
                ha='center', color='#8b949e', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '01_stats.png'), dpi=200, 
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 01_stats.png")

def generate_categories():
    print("📱 Generating: Categories")
    categories = ['Fiction', 'Non-Fiction', 'Science', 'Mystery', 'Romance']
    counts = [4200, 3800, 2100, 1900, 1500]
    colors = ['#ff6b6b', '#4facfe', '#56d364', '#feca57', '#a371f7']
    
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    
    y_pos = np.arange(len(categories))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count - 200, bar.get_y() + bar.get_height()/2, f'{count:,}',
                va='center', ha='right', color='white', fontsize=16, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=14)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Books', fontsize=14)
    ax.set_title('Top Categories', fontsize=20, fontweight='bold', pad=20)
    
    plt.savefig(os.path.join(output_dir, '02_categories.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 02_categories.png")

def generate_ratings():
    print("📱 Generating: Ratings")
    ratings = ['5★', '4★', '3★', '2★', '1★']
    counts = [3500, 5200, 4100, 1800, 692]
    
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    
    colors = ['#56d364', '#4facfe', '#feca57', '#ff9f43', '#ff6b6b']
    y_pos = np.arange(len(ratings))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count + 100, bar.get_y() + bar.get_height()/2, f'{count:,}',
                va='center', ha='left', color='white', fontsize=14, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(ratings, fontsize=16)
    ax.invert_yaxis()
    ax.set_title('Rating Distribution', fontsize=20, fontweight='bold', pad=20)
    
    plt.savefig(os.path.join(output_dir, '03_ratings.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 03_ratings.png")

def generate_ml():
    print("📱 Generating: ML Model")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.85, 'ML Clustering', fontsize=24, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.60, '4', fontsize=96, fontweight='bold',
            ha='center', color='#56d364', transform=ax.transAxes)
    ax.text(0.5, 0.42, 'Clusters Found', fontsize=20,
            ha='center', color='#8b949e', transform=ax.transAxes)
    ax.text(0.5, 0.28, 'K-Means', fontsize=24, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.18, 'Best algorithm', fontsize=14,
            ha='center', color='#58a6ff', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '04_ml.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 04_ml.png")

def generate_price():
    print("📱 Generating: Price Distribution")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.85, 'Book Prices', fontsize=24, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    
    prices = [
        ('Under $10', '35%', '#56d364'),
        ('$10-$25', '42%', '#4facfe'),
        ('$25-$50', '18%', '#feca57'),
        ('Over $50', '5%', '#ff6b6b'),
    ]
    
    for i, (label, pct, color) in enumerate(prices):
        y = 0.68 - i * 0.15
        ax.text(0.5, y, f'{pct}', fontsize=40, fontweight='bold',
                ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.04, label, fontsize=14,
                ha='center', color='#8b949e', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '05_price.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 05_price.png")

def generate_insights():
    print("📱 Generating: Insights")
    fig, ax = plt.subplots(figsize=MOBILE_CONFIG['figsize'])
    style_axes(ax)
    ax.axis('off')
    
    ax.text(0.5, 0.95, 'Key Insights', fontsize=20, fontweight='bold',
            ha='center', color='white', transform=ax.transAxes)
    
    insights = [
        ('1', 'Fiction Leads', '28% of books', '#ff6b6b'),
        ('2', '4 Star Sweet Spot', 'Most common rating', '#4facfe'),
        ('3', '4 Clusters', 'K-Means best fit', '#56d364'),
        ('4', '$10-25 Range', 'Most popular price', '#a371f7'),
    ]
    
    for i, (num, headline, subtext, color) in enumerate(insights):
        y = 0.78 - i * 0.20
        circle = plt.Circle((0.12, y), 0.05, transform=ax.transAxes,
                           facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(0.12, y, num, fontsize=18, fontweight='bold', color='white',
                ha='center', va='center', transform=ax.transAxes)
        ax.text(0.22, y + 0.02, headline, fontsize=18, fontweight='bold',
                color='white', transform=ax.transAxes)
        ax.text(0.22, y - 0.04, subtext, fontsize=14,
                color='#8b949e', transform=ax.transAxes)
    
    plt.savefig(os.path.join(output_dir, '06_insights.png'), dpi=200,
                facecolor=MOBILE_CONFIG['bg_color'], bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 06_insights.png")

if __name__ == '__main__':
    print("\n📱 Generating Mobile Graphs (Books)")
    print("=" * 50)
    setup_style()
    generate_stats()
    generate_categories()
    generate_ratings()
    generate_ml()
    generate_price()
    generate_insights()
    print(f"\n✅ All mobile graphs saved to: {output_dir}")
