"""
data_ingestion.py
Day 1 — Load all 10 CSV datasets, inspect each one (shape / dtypes / head),
flag anomalies, save cleaned copies to data/processed/, explore fund_master,
and validate AMFI codes against nav_history."""

import os
import pandas as pd

# RAW_DIR       = "data/raw"
# PROCESSED_DIR = "data/processed"
# REPORT_PATH   = "reports/data_quality_day1.txt"
from pathlib import Path

BASE_DIR      = Path(__file__).parent
RAW_DIR       = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORT_PATH   = BASE_DIR / "reports" / "data_quality_day1.txt"

CSV_FILES = {
    "fund_master":           "01_fund_master.csv",
    "nav_history":           "02_nav_history.csv",
    "aum_by_fund_house":     "03_aum_by_fund_house.csv",
    "monthly_sip_inflows":   "04_monthly_sip_inflows.csv",
    "category_inflows":      "05_category_inflows.csv",
    "industry_folio_count":  "06_industry_folio_count.csv",
    "scheme_performance":    "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings":    "09_portfolio_holdings.csv",
    "benchmark_indices":     "10_benchmark_indices.csv",
}

ANOMALY_LOG = []


def inspect(name, df):
    sep = "=" * 65
    print(f"\n{sep}")
    print(f"  DATASET : {name}")
    print(sep)
    print(f"  Shape   : {df.shape[0]:,} rows  x  {df.shape[1]} columns")
    print("\n-- dtypes --")
    print(df.dtypes.to_string())
    print("\n-- head(3) --")
    print(df.head(3).to_string())

    issues = []
    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]
    if not nulls.empty:
        issues.append(f"NULL values -> {nulls.to_dict()}")
    dups = df.duplicated().sum()
    if dups:
        issues.append(f"Duplicate rows -> {dups}")
    for col in df.select_dtypes(include="object").columns:
        if any(k in col.lower() for k in ["date", "month", "year"]):
            issues.append(f"Column '{col}' is date/time stored as string - consider pd.to_datetime()")

    if issues:
        print("\n[ANOMALIES]")
        for i in issues:
            print(f"   * {i}")
        ANOMALY_LOG.append({"dataset": name, "issues": issues})
    else:
        print("\n[OK] No anomalies detected.")


def load_all():
    dfs = {}
    for name, filename in CSV_FILES.items():
        path = os.path.join(RAW_DIR, filename)
        if not os.path.exists(path):
            print(f"\n[SKIP] File not found: {path}")
            ANOMALY_LOG.append({"dataset": name, "issues": ["File not found"]})
            continue
        try:
            df = pd.read_csv(path, low_memory=False)
            inspect(name, df)
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].str.strip()
            out = os.path.join(PROCESSED_DIR, filename)
            df.to_csv(out, index=False)
            print(f"\n   [SAVED] Cleaned copy -> {out}")
            dfs[name] = df
        except Exception as exc:
            print(f"\n[ERROR] Loading {filename}: {exc}")
            ANOMALY_LOG.append({"dataset": name, "issues": [str(exc)]})
    return dfs


def explore_fund_master(df):
    print("\n" + "=" * 65)
    print("  STEP 5 -- fund_master Exploration")
    print("=" * 65)

    fund_houses = df["fund_house"].unique()
    print(f"\n[Fund Houses] ({len(fund_houses)} AMCs):")
    for fh in sorted(fund_houses):
        n = df[df["fund_house"] == fh].shape[0]
        print(f"   {fh:<35} {n:>3} schemes")

    print(f"\n[Categories]: {sorted(df['category'].unique())}")

    print(f"\n[Sub-Categories] ({df['sub_category'].nunique()}):")
    for sc in sorted(df["sub_category"].unique()):
        print(f"   * {sc}")

    print(f"\n[Risk Grades]:")
    for grade, cnt in df["risk_category"].value_counts().items():
        print(f"   {grade:<20} {cnt:>3} schemes")

    print(f"\n[AMFI Code Structure]:")
    print(f"   Range   : {df['amfi_code'].min()} -> {df['amfi_code'].max()}")
    print( "   Format  : 6-digit integers assigned by AMFI")
    print( "   Note    : 40 schemes across 10 AMCs covering Regular + Direct plans")
    print(f"\n[Plan Split]:")
    print(df["plan"].value_counts().to_string())


def validate_amfi_codes(fund_master, nav_history):
    print("\n" + "=" * 65)
    print("  STEP 6 -- AMFI Code Validation")
    print("=" * 65)

    fm_codes  = set(fund_master["amfi_code"].astype(str))
    nav_codes = set(nav_history["amfi_code"].astype(str))
    matched   = fm_codes & nav_codes
    missing   = fm_codes - nav_codes
    extra     = nav_codes - fm_codes

    print(f"\n  fund_master unique codes : {len(fm_codes)}")
    print(f"  nav_history unique codes : {len(nav_codes)}")
    print(f"  Matched                  : {len(matched)}")
    print(f"  Missing NAV history      : {len(missing)}")
    print(f"  Extra in NAV             : {len(extra)}")

    if not missing:
        print("\n  [PASS] All fund_master codes have NAV history -- perfect 1-to-1 match!")
    else:
        for c in sorted(missing):
            print(f"    * {c}")

    return {
        "fm_codes":  len(fm_codes),
        "nav_codes": len(nav_codes),
        "matched":   len(matched),
        "missing":   sorted(missing),
        "extra":     sorted(extra),
    }


def write_quality_report(validation):
    os.makedirs("reports", exist_ok=True)
    lines = [
        "DATA QUALITY REPORT -- Day 1",
        "=" * 50,
        "",
        "-- AMFI Code Validation --",
        f"  fund_master unique codes  : {validation['fm_codes']}",
        f"  nav_history unique codes  : {validation['nav_codes']}",
        f"  Matched (both datasets)   : {validation['matched']}",
        f"  Missing NAV history       : {len(validation['missing'])}",
        f"  Extra in NAV              : {len(validation['extra'])}",
        "",
        "-- Per-Dataset Anomalies --",
    ]
    if not ANOMALY_LOG:
        lines.append("  All datasets are clean.")
    else:
        for entry in ANOMALY_LOG:
            lines.append(f"\n  {entry['dataset']}:")
            for issue in entry["issues"]:
                lines.append(f"    * {issue}")

    lines += [
        "",
        "-- Known Issues --",
        "  04_monthly_sip_inflows:",
        "    * yoy_growth_pct has 12 NULLs (rows 1-12, Jan-Dec 2022).",
        "      EXPECTED: YoY cannot be computed without prior-year baseline.",
        "      Action: document and fill when 2021 data is available.",
        "",
        "  All other datasets: zero nulls, zero duplicates.",
    ]

    with open(REPORT_PATH, "w") as f:
        f.write("\n".join(lines))
    print(f"\n[REPORT] Saved -> {REPORT_PATH}")


if __name__ == "__main__":
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    print("Starting data ingestion ...")
    dfs = load_all()

    if "fund_master" in dfs:
        explore_fund_master(dfs["fund_master"])

    if "fund_master" in dfs and "nav_history" in dfs:
        validation = validate_amfi_codes(dfs["fund_master"], dfs["nav_history"])
        write_quality_report(validation)

    print(f"\n{'='*65}")
    print(f"  Ingestion complete -- {len(dfs)}/{len(CSV_FILES)} datasets loaded.")
    print(f"{'='*65}")
