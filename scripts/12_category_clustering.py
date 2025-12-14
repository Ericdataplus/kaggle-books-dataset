"""
12 - Category Clustering
Groups books by features using K-Means
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
output_path = os.path.join(project_dir, 'graphs', '12_category_clustering.png')

print("Loading data...")
df = pd.read_csv(data_path)

# Clean
df = df.dropna(subset=['average_rating', 'page_count'])
df = df[df['average_rating'] > 0]
df['page_count'] = pd.to_numeric(df['page_count'], errors='coerce').fillna(200)
df['ratings_count'] = pd.to_numeric(df['ratings_count'], errors='coerce').fillna(0)
df['title_length'] = df['title'].fillna('').apply(len)

features = ['average_rating', 'page_count', 'ratings_count', 'title_length']
X = df[features].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow
inertias = []
K_range = range(2, 8)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

n_clusters = 5
print(f"Clustering with {n_clusters} clusters...")
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['pca1'] = X_pca[:, 0]
df['pca2'] = X_pca[:, 1]

cluster_stats = df.groupby('Cluster').agg({
    'average_rating': 'mean',
    'page_count': 'mean',
    'ratings_count': 'mean',
    'title': 'count'
}).rename(columns={'title': 'count'})

# Name clusters
cluster_names = {}
sorted_by_rating = cluster_stats.sort_values('average_rating')
cluster_names[sorted_by_rating.index[0]] = 'Low Rated'
cluster_names[sorted_by_rating.index[-1]] = 'Top Rated'

sorted_by_pages = cluster_stats.sort_values('page_count')
remaining = [i for i in range(n_clusters) if i not in cluster_names]
if len(remaining) > 0:
    cluster_names[remaining[0]] = 'Short Books'
if len(remaining) > 1:
    cluster_names[remaining[1]] = 'Popular'
if len(remaining) > 2:
    cluster_names[remaining[2]] = 'Long Books'

df['Cluster_Name'] = df['Cluster'].map(cluster_names)

colors = ['#ff6b6b', '#4ecdc4', '#ffd93d', '#45b7d1', '#96ceb4']

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.patch.set_facecolor('#0d1117')
fig.suptitle('Book Category Clustering (K-Means)', fontsize=22, fontweight='bold', color='white', y=0.98)

# PCA scatter
ax1 = axes[0, 0]
ax1.set_facecolor('#0d1117')
for i, (cluster_id, name) in enumerate(cluster_names.items()):
    mask = df['Cluster'] == cluster_id
    ax1.scatter(df.loc[mask, 'pca1'], df.loc[mask, 'pca2'], 
                c=colors[i % len(colors)], s=15, alpha=0.5, label=name)
ax1.set_xlabel('PC1', color='white')
ax1.set_ylabel('PC2', color='white')
ax1.set_title('Book Clusters (PCA)', color='white', fontsize=14, fontweight='bold')
ax1.legend(facecolor='#161b22', labelcolor='white', fontsize=8)
ax1.tick_params(colors='white')
for spine in ax1.spines.values(): spine.set_color('#30363d')

# Pie
ax2 = axes[0, 1]
ax2.set_facecolor('#0d1117')
segment_counts = df['Cluster_Name'].value_counts()
valid_colors = colors[:len(segment_counts)]
ax2.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', 
        colors=valid_colors, textprops={'color': 'white', 'fontsize': 9})
ax2.set_title('Cluster Distribution', color='white', fontsize=14, fontweight='bold')

# Rating by cluster
ax3 = axes[1, 0]
ax3.set_facecolor('#0d1117')
cluster_order = list(cluster_names.values())
ratings = [cluster_stats.loc[k, 'average_rating'] for k in cluster_names.keys()]
bars = ax3.bar(cluster_order, ratings, color=colors[:len(cluster_order)])
ax3.set_ylabel('Avg Rating', color='white')
ax3.set_title('Average Rating by Cluster', color='white', fontsize=14, fontweight='bold')
ax3.tick_params(colors='white', labelsize=8)
ax3.set_xticklabels(cluster_order, rotation=15)
for spine in ax3.spines.values(): spine.set_color('#30363d')

# Elbow
ax4 = axes[1, 1]
ax4.set_facecolor('#0d1117')
ax4.plot(list(K_range), inertias, 'o-', color='#4ecdc4', linewidth=2, markersize=8)
ax4.axvline(x=n_clusters, color='#ff6b6b', linestyle='--', linewidth=2, label=f'K={n_clusters}')
ax4.set_xlabel('K', color='white')
ax4.set_ylabel('Inertia', color='white')
ax4.set_title('Elbow Method', color='white', fontsize=14, fontweight='bold')
ax4.legend(facecolor='#161b22', labelcolor='white')
ax4.tick_params(colors='white')
for spine in ax4.spines.values(): spine.set_color('#30363d')

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(output_path, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()

print(f"Saved: {output_path}")
