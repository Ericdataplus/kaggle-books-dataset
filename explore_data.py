import pandas as pd
import sys

# Redirect output to file
sys.stdout = open('analysis_output.txt', 'w', encoding='utf-8')

# Load the dataset
df = pd.read_csv('google_books_dataset.csv')

print("=" * 70)
print("BOOKS DATASET - COMPREHENSIVE OVERVIEW")
print("=" * 70)

print(f"\n📚 Total Books: {len(df):,}")
print(f"📊 Total Columns: {len(df.columns)}")

print("\n" + "-" * 70)
print("COLUMNS & DATA TYPES")
print("-" * 70)
for col in df.columns:
    dtype = df[col].dtype
    non_null = df[col].notna().sum()
    print(f"  {col:<20} | {str(dtype):<10} | {non_null:,} non-null values")

print("\n" + "-" * 70)
print("MISSING VALUES SUMMARY")
print("-" * 70)
for col in df.columns:
    missing = df[col].isna().sum()
    pct = (missing / len(df)) * 100
    if missing > 0:
        print(f"  {col:<20} | {missing:>6,} missing ({pct:.1f}%)")

print("\n" + "-" * 70)
print("NUMERICAL COLUMNS STATISTICS")
print("-" * 70)
numerical_cols = ['page_count', 'average_rating', 'ratings_count', 'list_price']
for col in numerical_cols:
    if col in df.columns:
        print(f"\n  {col}:")
        print(f"    Min: {df[col].min()}")
        print(f"    Max: {df[col].max()}")
        print(f"    Mean: {df[col].mean():.2f}")
        print(f"    Median: {df[col].median():.2f}")

print("\n" + "-" * 70)
print("CATEGORICAL INSIGHTS")
print("-" * 70)

print(f"\n  Unique Categories: {df['search_category'].nunique()}")
print(f"  Unique Languages: {df['language'].nunique()}")
print(f"  Unique Publishers: {df['publisher'].nunique():,}")

print("\n  TOP 15 CATEGORIES:")
for cat, count in df['search_category'].value_counts().head(15).items():
    print(f"    {cat}: {count}")

print("\n  TOP 10 LANGUAGES:")
for lang, count in df['language'].value_counts().head(10).items():
    print(f"    {lang}: {count}")

print("\n  TOP 10 PUBLISHERS:")
for pub, count in df['publisher'].value_counts().head(10).items():
    print(f"    {pub}: {count}")

print("\n" + "-" * 70)
print("RATINGS DISTRIBUTION")
print("-" * 70)
rating_bins = [0, 1, 2, 3, 4, 5]
df['rating_bin'] = pd.cut(df['average_rating'], bins=rating_bins, labels=['0-1', '1-2', '2-3', '3-4', '4-5'])
print(df['rating_bin'].value_counts().sort_index().to_string())

print("\n" + "-" * 70)
print("SAMPLE DATA (First 3 rows)")
print("-" * 70)
print(df[['title', 'authors', 'average_rating', 'page_count', 'search_category']].head(3).to_string())

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
