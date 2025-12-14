"""
Run All GIF Scripts
Executes all GIF visualization scripts
"""
import subprocess
import os
import sys

scripts = [
    "gif_01_scatter_buildup.py",
    "gif_02_histogram_buildup.py",
    "gif_03_language_bubbles.py",
    "gif_04_category_countdown.py",
    "gif_05_price_thermometer.py",
    "gif_06_stats_counter.py",
    "gif_07_radar_chart.py",
]

print("=" * 60)
print("🎬 GIF ANIMATION GENERATOR")
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
    if result.stderr and 'error' in result.stderr.lower():
        print(f"⚠️  {result.stderr.strip()}")
    
    if result.returncode != 0:
        print(f"❌ Error in {script}")
    else:
        print(f"✅ {script} completed")

print("\n" + "=" * 60)
print("🎉 ALL GIF ANIMATIONS COMPLETE!")
print("=" * 60)
print("\n📁 Check the 'gifs' folder for all animations:")
print("   - 01_scatter_buildup.gif    (Scatter plot animation)")
print("   - 02_histogram_buildup.gif  (Page count histogram)")
print("   - 03_language_bubbles.gif   (Language bubble chart)")
print("   - 04_category_countdown.gif (Top 10 categories)")
print("   - 05_price_thermometer.gif  (Price visualization)")
print("   - 06_stats_counter.gif      (Statistics counter)")
print("   - 07_radar_chart.gif        (Category metrics radar)")
