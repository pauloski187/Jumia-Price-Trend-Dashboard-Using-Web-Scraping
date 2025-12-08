# Jumia Price Trend Dashboard Using Web Scraping

This repository provides a scaffolded project structure for analyzing Jumia product price trends, training simple models, and exposing predictions via a FastAPI backend with a React frontend.

Project layout:

```
churn_prediction/
│
├── data/
│   ├── raw/                     # Raw customer data
│   ├── processed/               # Cleaned data
│   └── features/                # Engineered features
│
├── notebooks/
│   ├── 01_eda.ipynb            # Exploratory analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_modeling.ipynb
│
├── src/
│   ├── data/
│   │   ├── data_loader.py
│   │   └── feature_engineering.py
│   │
│   ├── models/
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   │
│   └── utils/
│       ├── preprocessing.py
│       └── visualization.py
│
├── app/                         # FastAPI
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routes.py
│
├── frontend/                    # React dashboard (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   ├── CustomerList.jsx
│   │   │   ├── RiskScore.jsx
│   │   │   └── Analytics.jsx
│   │   └── App.jsx
│   └── package.json
│
├── tests/
├── requirements.txt
└── README.md
```

Key file naming per request:
- Raw data file: `data/raw/jumia product.csv`
- Processed data file: `data/processed/jumia_product_processed.csv`

Setup
1) Python environment
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2) Run backend (FastAPI)
```
uvicorn app.main:app --reload
```
Visit: http://127.0.0.1:8000/health

3) Frontend (Vite + React)
```
cd frontend
npm install
npm run start
```

Notes
- Notebooks are provided in a lightweight, cell‑marker format for compatibility with this environment.
- The code modules are minimal placeholders to get you started; extend them as needed.
