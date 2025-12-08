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
