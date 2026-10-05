# E-commerce Sales & Customer Analytics Dashboard

End-to-end analytics project on 50,000+ e-commerce transactions. Cleans and models raw data, segments customers with RFM analysis, tracks cohort retention, and delivers business insights through charts and a FastAPI dashboard.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## Overview

This project walks through the full analytics lifecycle on a realistic e-commerce dataset:

1. **Generate** 50,000+ synthetic transactions across 2,000 customers
2. **Clean and model** into one analysis-ready table
3. **Compute KPIs** — revenue, AOV, repeat rate, unique customers
4. **Segment customers** with RFM analysis (Champions, Loyal, At Risk, Lost)
5. **Track cohort retention** month over month
6. **Generate charts** for monthly trend, category, country, and RFM
7. **Write business insights** in plain English
8. **Serve everything** via a FastAPI dashboard

## Problem Statement

E-commerce businesses generate huge volumes of transaction data but struggle to answer basic questions:

- Which customers drive the most revenue?
- Which are about to churn?
- Which product categories and countries are growing?
- Are repeat buyers increasing or decreasing?
- Where should retention budget be spent?

Raw data alone doesn't answer these. Structured analysis does.

## Solution

A reproducible analytics pipeline that:

- Cleans and models 50K+ transactions into one table
- Computes RFM scores for every customer (1-5 each dimension)
- Classifies customers into 5 actionable segments
- Tracks monthly cohort retention
- Produces KPIs and a written insights report
- Serves all results over HTTP for dashboards

## Architecture

Raw Transactions (50K+)
         |
         v
Data Cleaning (duplicates, nulls, invalid rows)
         |
         v
Model + Derived Columns (year, month, quarter, day)
         |
         v
+--------+--------+--------+
|                 |        |
Customer Summary  RFM      Cohort
(per customer)   (segments) (retention)
|                 |        |
+--------+--------+--------+
         |
         v
KPIs + Charts + Insights Report
         |
         v
FastAPI Dashboard Endpoints
         |
         v
Docker + GitHub Actions

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Data Processing | Pandas, NumPy |
| Statistics | SciPy, RFM analysis |
| Visualization | Matplotlib, Seaborn |
| API | FastAPI, Uvicorn, Pydantic |
| Testing | pytest, httpx |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Language | Python 3.11+ |

## Project Structure

ecommerce-analytics/
├── src/
│   ├── __init__.py
│   ├── data_generator.py      # Generate synthetic transactions
│   ├── clean_data.py          # Clean, model, RFM, cohorts
│   ├── analyze.py             # KPIs, trends, insights
│   └── report.py              # Charts + Markdown report
├── api/
│   ├── __init__.py
│   └── main.py                # FastAPI analytics endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py            # pytest tests
├── data/                       # Generated CSVs (git-ignored)
├── reports/                    # Charts + report.md (git-ignored)
├── .github/workflows/ci.yml
├── Dockerfile
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md

## Quick Start

### 1. Clone

git clone https://github.com/sumit966/ecommerce-analytics.git
cd ecommerce-analytics

### 2. Virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Generate synthetic transactions

python src/data_generator.py

Output:
[OK] Generated 50000 transactions -> data/transactions.csv

### 5. Clean and model data

python src/clean_data.py

Output:
[OK] Cleaned 50000 transactions
[OK] Customer summary: 2000 customers
[OK] RFM segments:
Champions       234
Loyal           512
Potential       678
At Risk         342
Lost            234

### 6. Compute KPIs and insights

python src/analyze.py

Output:
=== KPIs ===
total_revenue: ...
total_orders: ...
total_customers: ...
avg_order_value: ...
repeat_purchase_rate_pct: ...

=== Business Insights ===
1. Total revenue is $...
2. Average order value is $...
...

### 7. Generate charts + report

python src/report.py

Creates:
reports/
├── monthly_revenue.png
├── revenue_by_category.png
├── rfm_segments.png
├── revenue_by_country.png
└── report.md

### 8. Start the API

uvicorn api.main:app --reload

API runs at http://localhost:8000

### 9. Open Swagger UI

http://localhost:8000/docs

## API Usage

### GET /kpis

Response:
{
  "total_revenue": 4523456.78,
  "total_orders": 50000,
  "total_customers": 2000,
  "avg_order_value": 90.47,
  "repeat_purchase_rate_pct": 68.5
}

### GET /revenue/monthly

Response:
[
  {"month": "2024-01", "revenue": 402345.12, "orders": 4200},
  {"month": "2024-02", "revenue": 418234.55, "orders": 4350},
  ...
]

### GET /revenue/category

Response:
[
  {"category": "Electronics", "revenue": 1800000.0, "orders": 15000},
  {"category": "Clothing", "revenue": 1200000.0, "orders": 12500},
  ...
]

### GET /revenue/country

Response:
[
  {"country": "USA", "revenue": 1600000.0, "orders": 17500},
  {"country": "UK", "revenue": 900000.0, "orders": 10000},
  ...
]

### GET /customers/top?n=10

Response:
[
  {"customer_id": "C00012", "country": "USA", "segment": "VIP",
   "total_orders": 45, "total_revenue": 12450.32, "avg_order_value": 276.67},
  ...
]

### GET /insights

Response:
{
  "insights": [
    "Total revenue is $4,523,456.78 from 50,000 orders by 2,000 unique customers.",
    "Average order value is $90.47; 68.5% of customers are repeat buyers.",
    "Top category is Electronics with $1,800,000 (39.8% of revenue).",
    "Top market is USA with $1,600,000 (35.4% of revenue).",
    "234 customers are in the 'Champions' RFM segment — they generate 42.3% of revenue.",
    "342 customers are 'At Risk' (high value, low recency) — target them with win-back campaigns."
  ]
}

### GET /rfm/segments

Response:
[
  {"rfm_segment": "Champions", "customers": 234, "avg_recency": 12.4, "avg_frequency": 32.1, "total_revenue": 1912000.45},
  {"rfm_segment": "Loyal", "customers": 512, "avg_recency": 45.2, "avg_frequency": 14.3, "total_revenue": 1245000.12},
  ...
]

### Other Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| / | GET | API info |
| /health | GET | Health check |
| /docs | GET | Swagger UI |
| /redoc | GET | Alternative docs |

## RFM Segmentation Logic

Each customer is scored 1-5 on:

- **Recency (R)** — days since last purchase (5 = most recent)
- **Frequency (F)** — total number of orders (5 = most frequent)
- **Monetary (M)** — total spend (5 = highest)

Sum of R+F+M (range 3-15) maps to segments:

| Score | Segment | Action |
|-------|---------|--------|
| 13-15 | Champions | Reward, ask for referrals |
| 10-12 | Loyal | Upsell premium products |
| 7-9 | Potential | Nurture with content |
| 5-6 | At Risk | Win-back campaigns |
| 3-4 | Lost | Re-engagement or let go |

## Cohort Retention

Retention matrix shows, for each signup cohort (month), what % of customers are still purchasing N months later:

cohort_index:  0     1     2     3     4     5
2024-01:    100%   42%   28%   22%   18%   15%
2024-02:    100%   45%   30%   24%   19%    -
2024-03:    100%   43%   29%   23%    -     -
...

Used for measuring product-market fit and lifetime value.

## Testing

pytest tests/ -v

Tests cover:
- Root endpoint responds
- Health check reports data status
- /kpis returns KPI dict
- /revenue/monthly returns list
- /insights returns list of strings

## Docker

Build:
docker build -t ecommerce-analytics .

Run:
docker run -p 8000:8000 ecommerce-analytics

The Dockerfile generates data, cleans it, and runs analysis automatically during build.

## CI/CD Pipeline

Every push to main triggers GitHub Actions:

1. Install Python 3.11 + dependencies
2. Generate synthetic transactions
3. Clean and model data
4. Compute KPIs
5. Run pytest test suite

See .github/workflows/ci.yml.

## Key Learnings

- RFM analysis turns raw transactions into 5 actionable customer segments
- Cohort retention beats aggregate retention — same overall rate hides different behavior per cohort
- Repeat purchase rate is the single best predictor of long-term revenue
- Champions generate disproportionate revenue — always measure segment-level concentration
- Charts must be readable by non-technical stakeholders — use business labels, not feature names
- FastAPI lets the same pipeline serve both ad-hoc analysis and production dashboards
- Cleaning raw data is 60% of the work — duplicates, nulls, and invalid rows distort every metric

## Future Improvements

- Power BI / Tableau dashboard consuming the FastAPI endpoints
- Predictive churn model (logistic regression + feature importance)
- Customer Lifetime Value (CLV) prediction
- Market basket analysis (frequent itemsets, Apriori)
- Real dataset integration (UCI Online Retail, Kaggle e-commerce)
- Scheduled daily refresh with Airflow
- Email digest with top insights to stakeholders
- Deploy to GCP Cloud Run

## License

MIT License - see LICENSE file.

## Author

Sumit Raj
- M.Tech Applied AI & ML @ VNIT Nagpur
- Ex-Software Engineer Intern @ Salesforce
- GitHub: https://github.com/sumit966
- LinkedIn: https://www.linkedin.com/in/er-sumit-raj-/
- Portfolio: https://sumit966-github-io.vercel.app
- Email: info.sr0909@gmail.com

If you found this project useful, please consider giving it a star!
