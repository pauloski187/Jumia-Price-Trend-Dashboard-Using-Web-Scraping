# Jumia Price Trend Dashboard Using Web Scraping

This repository provides a scaffolded project structure for analyzing Jumia product price trends, training simple models, and exposing predictions via a FastAPI backend with a React frontend.

Project layout:
Jumia-Price-Trend-Dashboard-Using-Web-Scraping/
│
├── data/
│ ├── raw/ # Raw product data
│ ├── processed/ # Cleaned data
│ └── features/ # Engineered features
│
├── notebooks/
│ ├── 01_eda.ipynb # Exploratory analysis
│ ├── 02_feature_engineering.ipynb
│ └── 03_modeling.ipynb
│
├── src/
│ ├── data/
│ │ ├── data_loader.py
│ │ └── feature_engineering.py
│ │
│ ├── models/
│ │ ├── train.py
│ │ ├── predict.py
│ │ └── evaluate.py
│ │
│ └── utils/
│ ├── preprocessing.py
│ └── visualization.py
│
├── app/ # FastAPI backend
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ └── routes.py
│
├── frontend/ # React dashboard (Vite)
│ ├── src/
│ │ ├── components/
│ │ │ ├── CustomerList.jsx
│ │ │ ├── RiskScore.jsx
│ │ │ └── Analytics.jsx
│ │ └── App.jsx
│ └── package.json
│
├── tests/
├── requirements.txt
└── README.md

Key file naming per request:
- Raw data file: `data/raw/jumia product.csv`
- Processed data file: `data/processed/jumia_product_processed.csv`

### Setup

#### 1) Python environment

### Data scraping and history management

This project maintains historical product data in both a CSV file and a SQLite database. The CSV path remains `data/raw/jumia_product.csv` (accessed from the scraper as `../../data/raw/jumia_product.csv`), and the database file is `jumia_data.db` stored alongside the scraper script.

There are two scripts relevant to scraping and data history:

- `src/data/migration_script.py` — one-time migration that imports all existing CSV history into the SQLite database while skipping duplicates and reporting per-date counts.
- `src/data/scraper.py` — the daily scraper that collects data for all 65 categories, appends to CSV, and inserts into the database with duplicate prevention and summaries.

#### One-time migration (CSV → SQLite)

Run this only once to sync your existing CSV history into the DB:

```
cd src/data
python migration_script.py
```

What it does:
- Creates the `products` table if it does not exist and a unique index on `(name, url, date_scraped)`.
- Streams the CSV in chunks, inserting rows with `INSERT OR IGNORE` to avoid duplicates.
- Prints progress and final verification: total rows in DB and a breakdown by `date_scraped`.

Requirements:
- CSV must exist at `data/raw/jumia_product.csv` relative to project root (the script resolves it relative to its own location).
- Column names are expected to match the current CSV headers (Title Case) or supported `snake_case` equivalents.

#### Daily scraping

To perform the daily scrape:

```
cd src/data
python scraper.py
```

Behavior:
- Preserves existing scraping logic for the 65 categories.
- Prevents accidental duplicate runs for the same date. If today’s data already exists in the database, you will be prompted:
  - `yes` — the script deletes only today’s data from both DB and CSV, then re-scrapes.
  - `no` — exits gracefully without scraping.
- Uses a unique index and `INSERT OR IGNORE` to prevent duplicate rows.
- Appends the new day’s data to CSV and inserts into SQLite.
- Shows a summary after completion:
  - Products scraped today
  - Total products in database
  - Breakdown of counts per `date_scraped`
  - Confirmation of CSV update

Notes:
- The scraper writes `jumia_data.db` next to `src/data/scraper.py` and `src/data/migration_script.py`.
- The CSV path is fixed to `data/raw/jumia_product.csv` from the project root.
- Logging is printed to stdout; adjust the logging level in the scripts if needed.
