"""
Deep Data Analysis - Finding Impressive Insights
Exploring the books dataset for compelling findings
"""
import pandas as pd
import numpy as np
from collections import Counter
import sys

# Redirect to file
sys.stdout = open('deep_insights.txt', 'w', encoding='utf-8')

# Load data
df = pd.read_csv('google_books_dataset.csv')

print("=" * 80)
print("📊 DEEP DATA ANALYSIS - IMPRESSIVE INSIGHTS")
print("=" * 80)

# =============================================================================
# 1. AUTHOR ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("👤 AUTHOR ANALYSIS")
print("=" * 80)

# Most prolific authors
df_authors = df[df['authors'].notna()].copy()
all_authors = []
for authors in df_authors['authors'].dropna():
    # Split by comma if multiple authors
    for author in str(authors).split(','):
        all_authors.append(author.strip())

author_counts = Counter(all_authors)
print("\n📚 TOP 15 MOST PROLIFIC AUTHORS:")
for author, count in author_counts.most_common(15):
    print(f"   {author}: {count} books")

# Authors with highest average ratings
author_ratings = df_authors[df_authors['average_rating'].notna()].groupby('authors').agg({
    'average_rating': 'mean',
    'book_id': 'count'
}).rename(columns={'book_id': 'book_count'})
author_ratings = author_ratings[author_ratings['book_count'] >= 3].sort_values('average_rating', ascending=False)

print("\n⭐ TOP 10 HIGHEST-RATED AUTHORS (min 3 books):")
for idx, (author, row) in enumerate(author_ratings.head(10).iterrows()):
    print(f"   {author[:40]}: {row['average_rating']:.2f} avg rating ({int(row['book_count'])} books)")

# =============================================================================
# 2. PUBLICATION TRENDS
# =============================================================================
print("\n" + "=" * 80)
print("📅 PUBLICATION TRENDS")
print("=" * 80)

df_dated = df[df['published_date'].notna()].copy()
# Extract year from published_date
df_dated['year'] = df_dated['published_date'].str.extract(r'(\d{4})').astype(float)
df_dated = df_dated[df_dated['year'].notna() & (df_dated['year'] >= 1900) & (df_dated['year'] <= 2025)]

print("\n📈 BOOKS BY DECADE:")
df_dated['decade'] = (df_dated['year'] // 10 * 10).astype(int)
decade_counts = df_dated['decade'].value_counts().sort_index()
for decade, count in decade_counts.items():
    bar = '█' * (count // 100)
    print(f"   {int(decade)}s: {count:>4} books {bar}")

# Which categories have grown the most recently?
recent = df_dated[df_dated['year'] >= 2020]
older = df_dated[(df_dated['year'] >= 2010) & (df_dated['year'] < 2020)]

recent_cats = recent['search_category'].value_counts()
older_cats = older['search_category'].value_counts()

print("\n🚀 FASTEST GROWING CATEGORIES (2020s vs 2010s):")
growth_rates = {}
for cat in set(recent_cats.index) & set(older_cats.index):
    if older_cats[cat] > 10:  # Minimum base
        growth = (recent_cats[cat] - older_cats[cat]) / older_cats[cat] * 100
        growth_rates[cat] = growth

for cat, growth in sorted(growth_rates.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"   {cat}: {growth:+.1f}% growth")

# =============================================================================
# 3. PRICE VS QUALITY ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("💰 PRICE VS QUALITY ANALYSIS")
print("=" * 80)

df_price_rating = df[(df['list_price'].notna()) & (df['average_rating'].notna()) & 
                      (df['list_price'] > 0) & (df['list_price'] < 200)]

if len(df_price_rating) > 10:
    correlation = df_price_rating['list_price'].corr(df_price_rating['average_rating'])
    print(f"\n📊 Correlation between price and rating: {correlation:.3f}")
    
    # Expensive but highly rated
    expensive_good = df_price_rating[(df_price_rating['list_price'] > 50) & 
                                      (df_price_rating['average_rating'] >= 4.5)]
    print(f"\n💎 Premium gems (>$50, rating ≥4.5): {len(expensive_good)} books")
    
    # Cheap but highly rated (best value!)
    cheap_good = df_price_rating[(df_price_rating['list_price'] < 15) & 
                                  (df_price_rating['average_rating'] >= 4.5)]
    print(f"🏆 Best value (<$15, rating ≥4.5): {len(cheap_good)} books")

# =============================================================================
# 4. PAGE COUNT INSIGHTS
# =============================================================================
print("\n" + "=" * 80)
print("📖 PAGE COUNT INSIGHTS")
print("=" * 80)

df_pages = df[(df['page_count'] > 0) & (df['page_count'] < 5000)]

# Longest books
print("\n📚 TOP 10 LONGEST BOOKS:")
longest = df_pages.nlargest(10, 'page_count')[['title', 'authors', 'page_count', 'search_category']]
for _, row in longest.iterrows():
    title = str(row['title'])[:40] if pd.notna(row['title']) else 'Unknown'
    print(f"   {title}: {int(row['page_count'])} pages ({row['search_category']})")

# Average pages by category
print("\n📊 CATEGORIES WITH LONGEST AVERAGE BOOKS:")
cat_pages = df_pages.groupby('search_category')['page_count'].mean().sort_values(ascending=False)
for cat, pages in cat_pages.head(10).items():
    print(f"   {cat}: {pages:.0f} avg pages")

# Shortest books still being sold
short_books = df_pages[df_pages['page_count'] < 50]
print(f"\n📄 Books under 50 pages: {len(short_books)} ({len(short_books)/len(df_pages)*100:.1f}%)")

# =============================================================================
# 5. LANGUAGE DIVERSITY ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("🌍 LANGUAGE DIVERSITY")
print("=" * 80)

# Languages with highest average ratings
lang_ratings = df[df['average_rating'].notna()].groupby('language').agg({
    'average_rating': 'mean',
    'book_id': 'count'
}).rename(columns={'book_id': 'count'})
lang_ratings = lang_ratings[lang_ratings['count'] >= 5].sort_values('average_rating', ascending=False)

print("\n⭐ HIGHEST-RATED LANGUAGES (min 5 rated books):")
for lang, row in lang_ratings.head(10).iterrows():
    print(f"   {lang}: {row['average_rating']:.2f} avg rating ({int(row['count'])} books)")

# Non-English categories
non_english = df[df['language'] != 'en']
print(f"\n📚 Non-English books: {len(non_english)} ({len(non_english)/len(df)*100:.1f}%)")

non_eng_cats = non_english['search_category'].value_counts().head(10)
print("\n🌐 Top categories for non-English books:")
for cat, count in non_eng_cats.items():
    print(f"   {cat}: {count} books")

# =============================================================================
# 6. PUBLISHER SPECIALIZATION
# =============================================================================
print("\n" + "=" * 80)
print("🏢 PUBLISHER SPECIALIZATION")
print("=" * 80)

df_pub = df[df['publisher'].notna()]
top_publishers = df_pub['publisher'].value_counts().head(10).index

print("\n📊 WHAT DO TOP PUBLISHERS SPECIALIZE IN?")
for pub in top_publishers[:5]:
    pub_books = df_pub[df_pub['publisher'] == pub]
    top_cat = pub_books['search_category'].value_counts().head(3)
    pub_name = pub[:30] + '...' if len(pub) > 30 else pub
    print(f"\n   {pub_name}:")
    for cat, count in top_cat.items():
        pct = count / len(pub_books) * 100
        print(f"      └─ {cat}: {count} books ({pct:.0f}%)")

# =============================================================================
# 7. RATING PATTERNS
# =============================================================================
print("\n" + "=" * 80)
print("⭐ RATING PATTERNS")
print("=" * 80)

df_rated = df[df['average_rating'].notna()]

# Rating distribution
rating_dist = pd.cut(df_rated['average_rating'], bins=[0,1,2,3,4,5], labels=['1★','2★','3★','4★','5★'])
print("\n📊 RATING DISTRIBUTION:")
for rating, count in rating_dist.value_counts().sort_index().items():
    pct = count / len(df_rated) * 100
    bar = '█' * int(pct / 2)
    print(f"   {rating}: {count:>4} ({pct:>5.1f}%) {bar}")

# Do longer books get better ratings?
df_pages_rated = df[(df['page_count'] > 0) & (df['page_count'] < 2000) & (df['average_rating'].notna())]
if len(df_pages_rated) > 10:
    corr = df_pages_rated['page_count'].corr(df_pages_rated['average_rating'])
    print(f"\n📈 Correlation: Page Count vs Rating: {corr:.3f}")
    
    short = df_pages_rated[df_pages_rated['page_count'] < 200]['average_rating'].mean()
    long = df_pages_rated[df_pages_rated['page_count'] > 500]['average_rating'].mean()
    print(f"   Short books (<200 pages) avg rating: {short:.2f}")
    print(f"   Long books (>500 pages) avg rating: {long:.2f}")

# =============================================================================
# 8. ISBN ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("📘 ISBN & BUYABILITY ANALYSIS")
print("=" * 80)

has_isbn = df['isbn_13'].notna() | df['isbn_10'].notna()
print(f"\n📖 Books with ISBN: {has_isbn.sum()} ({has_isbn.mean()*100:.1f}%)")
print(f"🛒 Buyable books: {df['buyable'].sum()} ({df['buyable'].mean()*100:.1f}%)")

# Buyable by category
buyable_by_cat = df.groupby('search_category')['buyable'].mean().sort_values(ascending=False)
print("\n💳 MOST PURCHASABLE CATEGORIES:")
for cat, rate in buyable_by_cat.head(10).items():
    print(f"   {cat}: {rate*100:.1f}% buyable")

# =============================================================================
# 9. INTERESTING CORRELATIONS
# =============================================================================
print("\n" + "=" * 80)
print("🔍 INTERESTING FINDINGS")
print("=" * 80)

# Books with descriptions vs without
with_desc = df[df['description'].notna()]
without_desc = df[df['description'].isna()]
print(f"\n📝 Books with descriptions: {len(with_desc)} ({len(with_desc)/len(df)*100:.1f}%)")

if 'average_rating' in df.columns:
    rated_with_desc = with_desc['average_rating'].notna().mean() * 100
    rated_without_desc = without_desc['average_rating'].notna().mean() * 100
    print(f"   With description: {rated_with_desc:.1f}% have ratings")
    print(f"   Without description: {rated_without_desc:.1f}% have ratings")

# Subtitle analysis
has_subtitle = df['subtitle'].notna().sum()
print(f"\n📑 Books with subtitles: {has_subtitle} ({has_subtitle/len(df)*100:.1f}%)")

# Most common words in titles (simple analysis)
all_titles = ' '.join(df['title'].dropna().astype(str))
words = [w.lower() for w in all_titles.split() if len(w) > 4]
word_counts = Counter(words).most_common(15)
print("\n📰 MOST COMMON TITLE WORDS (>4 chars):")
for word, count in word_counts:
    print(f"   {word}: {count}")

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE")
print("=" * 80)
