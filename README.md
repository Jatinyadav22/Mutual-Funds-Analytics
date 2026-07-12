# 📈 Bluestock Mutual Fund Analytics

> End-to-end mutual fund analytics platform covering 40 schemes across 10 AMCs — built as part of the Bluestock Fintech Data Analytics Internship 2025.

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-3.0.2-green?logo=pandas)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-6.8.0-purple?logo=plotly)](https://plotly.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit)](https://streamlit.io)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow?logo=powerbi)](https://powerbi.microsoft.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?logo=sqlite)](https://sqlite.org)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Results](#-key-results)
- [Project Structure](#-project-structure)
- [Datasets](#-datasets)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Deliverables](#-deliverables)
- [Bonus Features](#-bonus-features)
- [Tech Stack](#-tech-stack)
- [Key Insights](#-key-insights)
- [Author](#-author)

---

## 🎯 Project Overview

This project builds a complete mutual fund analytics platform for Bluestock Fintech covering:

| Layer | What was built |
|---|---|
| **Data Engineering** | ETL pipeline ingesting 10 datasets + live NAV API fetch |
| **Database** | SQLite star schema with 8 tables and 10 analytical queries |
| **EDA** | 15+ charts covering NAV trends, AUM, SIP, demographics |
| **Performance Analytics** | Sharpe, Sortino, Alpha, Beta, CAGR, VaR, CVaR, Drawdown |
| **Dashboard** | 4-page interactive Power BI dashboard + Streamlit web app |
| **Advanced Analytics** | Fund recommender, cohort analysis, SIP continuity, HHI |
| **Quantitative Finance** | Monte Carlo simulation + Markowitz efficient frontier |

---

## 📊 Key Results

```
📦 Data Coverage
   Schemes      : 40 across 10 AMCs
   NAV Records  : 46,000 (Jan 2022 – May 2026)
   Transactions : 32,778 investor records
   Date Range   : 4.4 years

💰 Industry Highlights
   Peak SIP Inflow   : ₹31,002 Cr (Dec 2025) — all-time high
   Largest AMC       : SBI Mutual Fund at ₹12.5 Lakh Crore AUM
   Folio Growth      : 13.26 Cr → 26.12 Cr (doubled in 4 years)
   SIP Dominance     : 60.2% of all transactions

📈 Performance Metrics
   Avg Sharpe Ratio  : 1.362 across all 40 funds
   Avg Alpha         : +1.254% annualised vs NIFTY100
   Avg Beta          : 0.873 (slightly defensive)
   Avg Max Drawdown  : -19.20%

🏆 Markowitz Optimisation
   Max Sharpe Portfolio Sharpe : 2.668
   vs Equal Weight Sharpe      : 2.514 (+6% improvement)
   Optimal return at           : 26.70% with 7.57% volatility
```

---

## 📁 Project Structure

```
Mutual-Funds-Analytics/
│
├── 📂 data/
│   ├── raw/                        # Original CSVs + live NAV fetches
│   └── processed/                  # Cleaned, type-corrected CSVs
│
├── 📂 notebooks/
│   ├── EDA_Analysis.ipynb          # 15+ charts, 10 EDA insights
│   ├── Performance_Analytics.ipynb # Sharpe, Sortino, Alpha, VaR, Scorecard
│   └── Advanced_Analytics.ipynb   # VaR/CVaR, Rolling Sharpe, Cohorts, HHI
│
├── 📂 sql/
│   ├── schema.sql                  # CREATE TABLE statements (star schema)
│   └── queries.sql                 # 10 analytical SQL queries
│
├── 📂 dashboard/
│   ├── bluestock_mf_dashboard.pbix # Power BI dashboard (4 pages)
│   ├── Dashboard.pdf               # Exported PDF
│   └── page*.png                   # Page screenshots
│
├── 📂 reports/
│   ├── data_dictionary.md          # Column definitions for all 10 datasets
│   ├── data_quality_day1.txt       # AMFI code validation results
│   ├── cleaning_report_day2.txt    # Data cleaning summary
│   └── chart_*.png                 # All exported chart PNGs
│
├── 📂 logs/
│   └── etl_scheduler.log           # Auto-generated ETL run logs
│
├── 🐍 data_ingestion.py            # D1: Load + inspect all 10 CSVs
├── 🐍 live_nav_fetch.py            # D1: Fetch live NAV from mfapi.in
├── 🐍 data_cleaning.py             # D2: Clean 3 key datasets + copy rest
├── 🐍 db_loader.py                 # D2: Load all data into SQLite
├── 🐍 recommender.py               # D6: CLI fund recommender by risk
├── 🐍 etl_scheduler.py             # B1: Auto ETL every weekday 8 PM
├── 🐍 app.py                       # B2: Streamlit web app (4 pages)
├── 🐍 monte_carlo.py               # B3: GBM NAV simulation (5yr)
├── 🐍 markowitz.py                 # B4: Efficient frontier optimisation
│
├── 📄 fund_scorecard.csv           # 40 funds ranked 0-100
├── 📄 alpha_beta.csv               # Alpha, Beta, R² for all 40 funds
├── 📄 var_cvar_report.csv          # VaR (95%) and CVaR for all 40 funds
├── 📄 monte_carlo_results.csv      # P5/P50/P95 NAV projections (5yr)
├── 📄 markowitz_results.csv        # Optimal portfolio weights
├── 📄 requirements.txt             # Pinned Python dependencies
├── 📄 Final_Report.docx            # Complete project report
├── 📄 Presentation.pptx            # 11-slide presentation
└── 📄 .gitignore                   # Excludes *.db, *.pbix, raw CSVs
```

---

## 📂 Datasets

| # | File | Records | Description |
|---|---|---|---|
| 01 | `fund_master.csv` | 40 | Scheme metadata, categories, risk grades |
| 02 | `nav_history.csv` | 46,000 | Daily NAV — forward-filled for weekends |
| 03 | `aum_by_fund_house.csv` | 90 | Quarterly AUM per AMC |
| 04 | `monthly_sip_inflows.csv` | 48 | Industry SIP inflow trend |
| 05 | `category_inflows.csv` | 144 | Net inflow by fund category per month |
| 06 | `industry_folio_count.csv` | 21 | Quarterly total folios |
| 07 | `scheme_performance.csv` | 40 | Sharpe, Alpha, Beta, Drawdown metrics |
| 08 | `investor_transactions.csv` | 32,778 | SIP/Lumpsum/Redemption records |
| 09 | `portfolio_holdings.csv` | 322 | Stock-level equity fund holdings |
| 10 | `benchmark_indices.csv` | 8,050 | NIFTY50, NIFTY100, Midcap150 daily |

> **Note:** Raw CSVs are excluded from GitHub via `.gitignore`. Place them in `data/raw/` before running.

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Jatinyadav22/Mutual-Funds-Analytics.git
cd Mutual-Funds-Analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Place raw CSVs
Copy all 10 CSV files into `data/raw/` and rename them:
```
data/raw/01_fund_master.csv
data/raw/02_nav_history.csv
... (and so on)
```

---

## 🚀 How to Run

Run scripts in this exact order:

### Step 1 — Data Ingestion (Day 1)
```bash
python data_ingestion.py      # Load + inspect all 10 CSVs
python live_nav_fetch.py      # Fetch live NAV from mfapi.in
```

### Step 2 — Data Cleaning + Database (Day 2)
```bash
python data_cleaning.py       # Clean datasets
python db_loader.py           # Load into SQLite star schema
```

### Step 3 — EDA Notebook (Day 3)
```bash
jupyter notebook notebooks/EDA_Analysis.ipynb
# Run All Cells
```

### Step 4 — Performance Analytics (Day 4)
```bash
jupyter notebook notebooks/Performance_Analytics.ipynb
# Run All Cells — generates fund_scorecard.csv and alpha_beta.csv
```

### Step 5 — Advanced Analytics (Day 6)
```bash
jupyter notebook notebooks/Advanced_Analytics.ipynb
# Run All Cells — generates var_cvar_report.csv
```

### Step 6 — Streamlit Web App (B2)
```bash
pip install streamlit
streamlit run app.py
# Opens at http://localhost:8501
```

### Step 7 — Monte Carlo Simulation (B3)
```bash
python monte_carlo.py
# Generates monte_carlo_results.csv + 2 PNG charts
```

### Step 8 — Markowitz Optimisation (B4)
```bash
python markowitz.py
# Generates markowitz_results.csv + 3 PNG charts
```

### Step 9 — ETL Scheduler (B1)
```bash
pip install schedule
python etl_scheduler.py --run-now        # Test immediately
python etl_scheduler.py                  # Start scheduler (8 PM weekdays)
python etl_scheduler.py --setup-windows  # Register Windows Task
```

### Step 10 — Fund Recommender
```bash
python recommender.py
# Enter: Low / Moderate / High
```

---

## 📦 Deliverables

| ID | Deliverable | File | Weight |
|---|---|---|---|
| D1 | ETL Pipeline | `data_ingestion.py`, `live_nav_fetch.py`, `data_cleaning.py` | 15% |
| D2 | SQLite Database | `schema.sql`, `queries.sql`, `db_loader.py` | 10% |
| D3 | EDA Notebook | `notebooks/EDA_Analysis.ipynb` | 15% |
| D4 | Performance Metrics | `notebooks/Performance_Analytics.ipynb`, `fund_scorecard.csv`, `alpha_beta.csv` | 15% |
| D5 | Power BI Dashboard | `dashboard/bluestock_mf_dashboard.pbix` | 20% |
| D6 | Advanced Analytics | `notebooks/Advanced_Analytics.ipynb`, `var_cvar_report.csv`, `recommender.py` | 10% |
| D7 | Final Report + Slides | `Final_Report.docx`, `Presentation.pptx` | 15% |

---

## 🎁 Bonus Features

| ID | Feature | File | Description |
|---|---|---|---|
| B1 | Scheduled ETL | `etl_scheduler.py` | Auto NAV fetch every weekday at 8 PM |
| B2 | Streamlit Web App | `app.py` | 4-page interactive dashboard in browser |
| B3 | Monte Carlo | `monte_carlo.py` | GBM NAV simulation — 5yr projections |
| B4 | Markowitz | `markowitz.py` | Efficient frontier portfolio optimisation |

---

## 🛠️ Tech Stack

```
Language        Python 3.10
Data            Pandas 3.0.2 | NumPy 2.4.4
Visualisation   Matplotlib 3.10 | Seaborn 0.13 | Plotly 6.8
Web App         Streamlit
Database        SQLite + SQLAlchemy 2.0.51
Statistics      SciPy 1.17.1 (OLS regression, optimization)
Scheduling      schedule library
Dashboard       Microsoft Power BI Desktop
Notebooks       Jupyter Lab
Version Control Git + GitHub
API             mfapi.in (live NAV)
```

---

## 💡 Key Insights

1. **SIP inflows grew 3x** from ₹10,000 Cr (Jan 2022) to ₹31,002 Cr (Dec 2025)
2. **SBI MF dominates** at ₹12.5L Cr AUM — nearly 2x nearest competitor
3. **Positive avg alpha of +1.254%** — most funds outperform NIFTY100
4. **Direct plans cost 1%+ less** annually than Regular plans
5. **Folio count doubled** from 13.26 Cr to 26.12 Cr in 4 years
6. **26–35 age group** dominates SIP participation (~38%)
7. **T30 cities** contribute 78% of SIP volume — B30 is untapped
8. **Markowitz optimisation** improves Sharpe by 6% over equal weight
9. **All equity funds** show >98% probability of profit over 5 years
10. **Banking sector** has highest allocation (~28%) across equity funds

---

## 👤 Author

**Jatin Yadav**
- Roll No: 230916
- University: BML Munjal University
- Program: B.Tech Computer Science
- Internship: Bluestock Fintech — Data Analytics | Summer 2025
- GitHub: [@Jatinyadav22](https://github.com/Jatinyadav22)

---

## 📄 License

This project was built as part of an internship assignment for Bluestock Fintech.
All data used is for educational purposes only.

---

*Built with ❤️ for Bluestock Fintech | Summer 2025*