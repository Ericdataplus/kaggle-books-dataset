"""
Run All Visualization Scripts
Executes all visualization scripts in order
"""
import subprocess
import os
import sys

scripts = [
    "01_category_distribution.py",
    "02_ratings_analysis.py",
    "03_page_count_analysis.py",
    "04_publisher_analysis.py",
    "05_language_analysis.py",
    "06_price_analysis.py",
    "07_animated_category_growth.py",
    "08_animated_ratings_wheel.py",
    "09_animated_publisher_race.py",
    "10_summary_dashboard.py",
]

print("=" * 60)
print("📊 BOOKS DATASET VISUALIZATION GENERATOR")
print("=" * 60)
print()

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

for i, script in enumerate(scripts, 1):
    print(f"\n[{i}/{len(scripts)}] Running {script}...")
    print("-" * 40)
    
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"⚠️  {result.stderr.strip()}")
    
    if result.returncode != 0:
        print(f"❌ Error in {script}")
    else:
        print(f"✅ {script} completed")

print("\n" + "=" * 60)
print("🎉 ALL VISUALIZATIONS COMPLETE!")
print("=" * 60)
print("\n📁 Check the 'graphs' folder for all outputs:")
print("   - 6 static PNG charts")
print("   - 3 animated GIFs")
print("   - 1 comprehensive dashboard")
