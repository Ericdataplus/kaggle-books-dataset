"""
Comprehensive Mobile Graphs for Google Books Dataset
"""
import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
output_dir = os.path.join(project_dir, 'graphs_mobile')
os.makedirs(output_dir, exist_ok=True)

M = {
    'figsize': (6, 8), 'figsize_wide': (6, 6),
    'bg': '#0d1117', 'text': '#ffffff', 'gray': '#8b949e', 'grid': '#30363d',
    'red': '#ff6b6b', 'green': '#56d364', 'blue': '#58a6ff',
    'gold': '#ffd700', 'purple': '#a371f7', 'orange': '#f0883e'
}

def setup():
    plt.rcParams.update({
        'font.size': 12, 'figure.facecolor': M['bg'], 'axes.facecolor': M['bg'],
        'text.color': M['text'], 'axes.labelcolor': M['text'],
        'xtick.color': M['text'], 'ytick.color': M['text']
    })

def ax_style(ax):
    ax.set_facecolor(M['bg'])
    for s in ax.spines.values(): s.set_color(M['grid'])

def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, name), dpi=200, facecolor=M['bg'], bbox_inches='tight')
    plt.close()
    print(f"   ✅ {name}")

def g01_stats():
    print("📱 01: Key Stats")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.95, 'Google Books Analysis', fontsize=22, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.88, 'ML-Powered Book Intelligence', fontsize=14, ha='center', color=M['gray'], transform=ax.transAxes)
    
    stats = [
        ('15,292', 'Total Books', M['blue']),
        ('$15.99', 'Median Price', M['green']),
        ('3.8★', 'Avg Rating', M['gold']),
        ('18', 'Categories', M['purple']),
        ('5', 'Clusters Found', M['orange']),
    ]
    
    for i, (val, label, color) in enumerate(stats):
        y = 0.70 - i * 0.12
        ax.text(0.5, y, val, fontsize=36, fontweight='bold', ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.035, label, fontsize=11, ha='center', color=M['gray'], transform=ax.transAxes)
    
    save('01_stats.png')

def g02_categories():
    print("📱 02: Top Categories")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax)
    
    cats = ['Fiction', 'Business', 'Computers', 'History', 'Biography', 'Science']
    counts = [3200, 2100, 1800, 1500, 1200, 1100]
    colors = [M['red'], M['blue'], M['green'], M['gold'], M['purple'], M['orange']]
    
    y_pos = np.arange(len(cats))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count - 150, bar.get_y() + bar.get_height()/2, f'{count:,}',
                va='center', ha='right', color='white', fontsize=14, fontweight='bold')
    
    ax.set_yticks(y_pos); ax.set_yticklabels(cats, fontsize=12)
    ax.invert_yaxis()
    ax.set_title('Top 6 Categories', fontsize=18, fontweight='bold', pad=15)
    save('02_categories.png')

def g03_ratings():
    print("📱 03: Rating Distribution")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax)
    
    ratings = ['5★', '4★', '3★', '2★', '1★']
    counts = [2800, 5100, 4500, 1800, 1092]
    colors = [M['green'], M['blue'], M['gold'], M['orange'], M['red']]
    
    y_pos = np.arange(len(ratings))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count + 100, bar.get_y() + bar.get_height()/2, f'{count:,}',
                va='center', fontsize=12, fontweight='bold', color='white')
    
    ax.set_yticks(y_pos); ax.set_yticklabels(ratings, fontsize=14)
    ax.invert_yaxis()
    ax.set_title('Rating Distribution', fontsize=18, fontweight='bold', pad=15)
    save('03_ratings.png')

def g04_price():
    print("📱 04: Price Ranges")
    fig, ax = plt.subplots(figsize=M['figsize_wide'])
    ax_style(ax)
    
    ranges = ['< $10', '$10-25', '$25-50', '> $50']
    pcts = [35, 42, 18, 5]
    colors = [M['green'], M['blue'], M['gold'], M['red']]
    
    wedges, texts, autotexts = ax.pie(pcts, labels=ranges, autopct='%1.0f%%',
                                       colors=colors, textprops={'color': 'white', 'fontsize': 12})
    for at in autotexts: at.set_fontweight('bold'); at.set_fontsize(14)
    
    ax.set_title('Price Distribution', fontsize=18, fontweight='bold', pad=15, color='white')
    save('04_price.png')

def g05_pages():
    print("📱 05: Page Length")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.90, 'Page Count by Genre', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    data = [
        ('Medical', '545', 'Longest avg', M['red']),
        ('Biography', '412', 'Detailed life stories', M['blue']),
        ('Fiction', '368', 'Standard novels', M['green']),
        ('Lit. Criticism', '327', 'Shortest avg', M['gold']),
    ]
    
    for i, (cat, pages, note, color) in enumerate(data):
        y = 0.70 - i * 0.16
        ax.text(0.5, y + 0.04, cat, fontsize=14, ha='center', color=M['gray'], transform=ax.transAxes)
        ax.text(0.5, y - 0.02, f'{pages} pages', fontsize=24, fontweight='bold', ha='center', color=color, transform=ax.transAxes)
        ax.text(0.5, y - 0.07, note, fontsize=10, ha='center', color=M['gray'], transform=ax.transAxes)
    
    save('05_pages.png')

def g06_clustering():
    print("📱 06: ML Clustering")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.90, 'K-Means Clustering', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    ax.text(0.5, 0.68, '5', fontsize=96, fontweight='bold', ha='center', color=M['green'], transform=ax.transAxes)
    ax.text(0.5, 0.52, 'Clusters Found', fontsize=18, ha='center', color=M['gray'], transform=ax.transAxes)
    
    clusters = ['Low Rated', 'Top Rated', 'Short Books', 'Popular', 'Long Books']
    for i, c in enumerate(clusters):
        y = 0.38 - i * 0.07
        ax.text(0.5, y, f'• {c}', fontsize=12, ha='center', color=M['blue'], transform=ax.transAxes)
    
    save('06_clustering.png')

def g07_publishers():
    print("📱 07: Top Publishers")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax)
    
    pubs = ['Penguin', 'HarperCollins', 'Random House', 'Simon & Schuster', 'Hachette']
    counts = [1200, 980, 890, 720, 650]
    colors = [M['red'], M['blue'], M['green'], M['gold'], M['purple']]
    
    y_pos = np.arange(len(pubs))
    bars = ax.barh(y_pos, counts, color=colors, height=0.6)
    
    for bar, count in zip(bars, counts):
        ax.text(count + 30, bar.get_y() + bar.get_height()/2, str(count),
                va='center', fontsize=12, fontweight='bold', color='white')
    
    ax.set_yticks(y_pos); ax.set_yticklabels(pubs, fontsize=11)
    ax.invert_yaxis()
    ax.set_title('Top 5 Publishers', fontsize=18, fontweight='bold', pad=15)
    save('07_publishers.png')

def g08_popularity():
    print("📱 08: Popularity Analysis")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.92, 'Popularity Formula', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    factors = [
        ('★ Ratings', '40% weight', M['gold']),
        ('📖 Reviews', '30% weight', M['blue']),
        ('💲 Price', '20% weight', M['green']),
        ('📄 Length', '10% weight', M['purple']),
    ]
    
    for i, (factor, weight, color) in enumerate(factors):
        y = 0.70 - i * 0.14
        ax.text(0.3, y, factor, fontsize=16, ha='center', color='white', transform=ax.transAxes)
        ax.text(0.7, y, weight, fontsize=18, fontweight='bold', ha='center', color=color, transform=ax.transAxes)
    
    ax.text(0.5, 0.18, 'Ratings matter most!', fontsize=14, fontweight='bold', ha='center', color=M['gold'], transform=ax.transAxes)
    save('08_popularity.png')

def g09_takeaways():
    print("📱 09: Key Takeaways")
    fig, ax = plt.subplots(figsize=M['figsize'])
    ax_style(ax); ax.axis('off')
    
    ax.text(0.5, 0.95, 'Key Takeaways', fontsize=20, fontweight='bold', ha='center', color='white', transform=ax.transAxes)
    
    takeaways = [
        ('1', 'Fiction leads at 21%', 'Most popular category', M['red']),
        ('2', '4-star sweet spot', 'Most common rating', M['blue']),
        ('3', '5 book clusters', 'K-Means analysis', M['green']),
        ('4', '$10-25 = 42%', 'Most common price', M['gold']),
        ('5', 'Medical = longest', '545 avg pages', M['purple']),
    ]
    
    for i, (num, head, sub, color) in enumerate(takeaways):
        y = 0.82 - i * 0.14
        circle = plt.Circle((0.08, y), 0.025, transform=ax.transAxes, facecolor=color, edgecolor='white', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(0.08, y, num, fontsize=12, fontweight='bold', color='white', ha='center', va='center', transform=ax.transAxes)
        ax.text(0.14, y + 0.015, head, fontsize=12, fontweight='bold', color='white', transform=ax.transAxes)
        ax.text(0.14, y - 0.02, sub, fontsize=10, color=M['gray'], transform=ax.transAxes)
    
    save('09_takeaways.png')

if __name__ == '__main__':
    print("\n📱 Generating Comprehensive Mobile Graphs (Books)")
    print("=" * 60)
    setup()
    g01_stats(); g02_categories(); g03_ratings(); g04_price()
    g05_pages(); g06_clustering(); g07_publishers(); g08_popularity(); g09_takeaways()
    print(f"\n✅ 9 mobile graphs saved to: {output_dir}")
