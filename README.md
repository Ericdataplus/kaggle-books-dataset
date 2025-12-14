# Books Dataset Analysis Dashboard

🔗 **Live Demo:** [View Dashboard](https://ericdataplus.github.io/kaggle-books-dataset/)

A comprehensive data-driven exploration of **15,000+ books** across 149 categories, revealing patterns in publishing, ratings, and reader preferences.

![Dashboard Preview](graphs/10_summary_dashboard.png)

## 📊 Key Statistics

| Metric | Value |
|--------|-------|
| Total Books | 15,147 |
| Categories | 149 |
| Publishers | 2,001 |
| Languages | 37 |
| Avg Pages | 485 |
| Avg Rating | 4.05 ⭐ |

## 🔍 Key Findings

1. **AI/ML Explosion** — 247.8% growth in Machine Learning books from 2010s to 2020s
2. **Spanish Books Win** — Highest average rating at 4.22
3. **The Description Effect** — Books with descriptions are 5x more likely to have ratings
4. **No Length-Quality Link** — Page count has virtually no correlation with ratings
5. **Best Value Finds** — 90 books under $15 with 4.5+ ratings

## 📁 Project Structure

```
kaggle-books-dataset/
├── index.html              # Interactive Dashboard
├── graphs/                 # Static visualizations (7 PNGs)
├── gifs/                   # Animated visualizations (10 GIFs)
├── scripts/                # Python analysis scripts
└── google_books_dataset.csv
```

## 🖼️ Visualizations

### Static Charts
- Category Distribution
- Ratings Analysis
- Page Count Analysis
- Publisher Analysis
- Language Distribution
- Price Analysis
- Summary Dashboard

### Animated GIFs
- Scatter Plot Buildup
- Histogram Animation
- Language Bubbles
- Category Countdown
- Price Thermometer
- Stats Counter
- Publisher Bar Race
- Ratings Wheel
- Radar Chart

## 🛠️ Tech Stack

- **Python** - Data analysis
- **Pandas** - Data manipulation
- **Matplotlib/Seaborn** - Visualizations
- **HTML/CSS/JS** - Dashboard

## 📦 Data Source

Dataset from Kaggle: [Books Dataset - 15K Books Across 100 Categories](https://www.kaggle.com/datasets/mihikaajayjadhav/books-dataset-15k-books-across-100-categories)

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Ericdataplus/kaggle-books-dataset.git
cd kaggle-books-dataset

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install pandas matplotlib seaborn pillow

# Run analysis
python scripts/run_all.py      # Generate static charts
python scripts/run_all_gifs.py # Generate GIF animations

# Open dashboard
start index.html  # Windows
open index.html   # Mac
```

## 📄 License

MIT License - Feel free to use and modify!

---

Made with 📚 and Python | December 2024
