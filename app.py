"""
app.py
======
B2 Bonus — Streamlit Web App
Alternative to Power BI Dashboard

4 Pages:
  1. Industry Overview
  2. Fund Performance
  3. Investor Analytics
  4. SIP & Market Trends

Run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0D1B2A; color: #E0E0E0; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0A1628;
        border-right: 2px solid #1565C0;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1A3C6E, #0D2137);
        border: 1px solid #00B4D8;
        border-radius: 10px;
        padding: 15px;
    }
    [data-testid="metric-container"] label {
        color: #00B4D8 !important;
        font-weight: bold;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
    }

    /* Headers */
    h1, h2, h3 { color: #00B4D8 !important; }

    /* Selectbox / multiselect */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: #0D2137;
        border: 1px solid #1565C0;
        color: #E0E0E0;
    }

    /* Divider */
    hr { border-color: #1565C0; }

    /* Dataframe */
    .stDataFrame { border: 1px solid #1565C0; border-radius: 8px; }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background-color: #0D2137;
        color: #00B4D8;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1565C0 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
PROC = Path("data/processed")

@st.cache_data
def load_data():
    fm   = pd.read_csv(PROC / "01_fund_master.csv")
    nav  = pd.read_csv(PROC / "02_nav_history.csv",  parse_dates=["date"])
    aum  = pd.read_csv(PROC / "03_aum_by_fund_house.csv", parse_dates=["date"])
    sip  = pd.read_csv(PROC / "04_monthly_sip_inflows.csv")
    cat  = pd.read_csv(PROC / "05_category_inflows.csv")
    fol  = pd.read_csv(PROC / "06_industry_folio_count.csv")
    perf = pd.read_csv(PROC / "07_scheme_performance.csv")
    txn  = pd.read_csv(PROC / "08_investor_transactions.csv",
                       parse_dates=["transaction_date"])
    ph   = pd.read_csv(PROC / "09_portfolio_holdings.csv")
    bi   = pd.read_csv(PROC / "10_benchmark_indices.csv", parse_dates=["date"])

    sip["month_dt"] = pd.to_datetime(sip["month"], infer_datetime_format=True, errors="coerce")
    cat["month_dt"] = pd.to_datetime(cat["month"], infer_datetime_format=True, errors="coerce")
    fol["month_dt"] = pd.to_datetime(fol["month"], infer_datetime_format=True, errors="coerce")

    nav = nav.merge(
        fm[["amfi_code","scheme_name","fund_house","sub_category","plan","risk_category"]],
        on="amfi_code", how="left"
    )
    perf = perf.merge(
        fm[["amfi_code","sub_category","risk_category","fund_manager"]].rename(
            columns={"sub_category":"sub_cat_fm","risk_category":"risk_cat_fm"}),
        on="amfi_code", how="left"
    )
    return fm, nav, aum, sip, cat, fol, perf, txn, ph, bi

fm, nav, aum, sip, cat, fol, perf, txn, ph, bi = load_data()

PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="#0D1B2A",
    plot_bgcolor="#0D2137",
    font=dict(color="#E0E0E0"),
)

# ─────────────────────────────────────────────────────────────
# SIDEBAR — NAVIGATION
# ─────────────────────────────────────────────────────────────
st.sidebar.image("https://via.placeholder.com/200x60/1565C0/FFFFFF?text=BLUESTOCK",
                 use_column_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["🏠 Industry Overview",
     "📈 Fund Performance",
     "👥 Investor Analytics",
     "💰 SIP & Market Trends"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info(
    "**Bluestock Mutual Fund Analytics**\n\n"
    "End-to-end analytics platform\n"
    "covering 40 schemes across 10 AMCs\n\n"
    "📅 Data: Jan 2022 – May 2026\n"
    "🏦 AMCs: 10 | Schemes: 40"
)


# ═════════════════════════════════════════════════════════════
# PAGE 1 — INDUSTRY OVERVIEW
# ═════════════════════════════════════════════════════════════
if page == "🏠 Industry Overview":
    st.title("🏠 Industry Overview")
    st.markdown("High-level snapshot of the Indian mutual fund industry (2022–2026)")
    st.markdown("---")

    # ── KPI Cards ────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)

    total_aum  = aum["aum_crore"].sum()
    latest_sip = sip["sip_inflow_crore"].max()
    latest_fol = fol["total_folios_crore"].max()
    num_schemes = fm["amfi_code"].nunique()
    num_amcs    = fm["fund_house"].nunique()

    k1.metric("💰 Total AUM",       f"₹{total_aum/1e5:.1f}L Cr")
    k2.metric("📥 Peak SIP Inflow", f"₹{latest_sip:,.0f} Cr")
    k3.metric("👤 Total Folios",    f"{latest_fol:.2f} Cr")
    k4.metric("📋 Schemes",          f"{num_schemes}")
    k5.metric("🏦 AMCs",             f"{num_amcs}")

    st.markdown("---")

    # ── AUM Trend ────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Industry AUM Trend (2022–2025)")
        aum_trend = aum.groupby("date")["aum_crore"].sum().reset_index()
        fig = px.area(aum_trend, x="date", y="aum_crore",
                      color_discrete_sequence=["#00B4D8"],
                      labels={"aum_crore": "AUM (₹ Crore)", "date": "Date"})
        fig.update_traces(fill="tozeroy", fillcolor="rgba(0,180,216,0.15)")
        fig.update_layout(**PLOTLY_THEME, height=380,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🏦 AUM by Fund House")
        aum_by_fh = aum.groupby("fund_house")["aum_crore"].mean()\
                        .sort_values(ascending=True).reset_index()
        aum_by_fh["short"] = aum_by_fh["fund_house"]\
            .str.replace(" Mutual Fund","",regex=False)\
            .str.replace(" MF","",regex=False)
        fig = px.bar(aum_by_fh, x="aum_crore", y="short",
                     orientation="h",
                     color="aum_crore",
                     color_continuous_scale="Blues",
                     labels={"aum_crore":"Avg AUM (₹ Cr)","short":"Fund House"})
        fig.update_layout(**PLOTLY_THEME, height=380,
                          showlegend=False, coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Folio Count + Category Split ─────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("👤 Folio Count Growth")
        fig = px.line(fol, x="month_dt", y="total_folios_crore",
                      color_discrete_sequence=["#9C27B0"],
                      labels={"total_folios_crore":"Folios (Crore)",
                               "month_dt":"Month"})
        fig.update_traces(line=dict(width=3))
        fig.add_hline(y=20, line_dash="dash", line_color="yellow",
                      annotation_text="20 Cr milestone")
        fig.update_layout(**PLOTLY_THEME, height=350,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("📂 Schemes by Sub-Category")
        sub_cat = fm["sub_category"].value_counts().reset_index()
        sub_cat.columns = ["sub_category","count"]
        fig = px.pie(sub_cat, values="count", names="sub_category",
                     color_discrete_sequence=px.colors.qualitative.Set3,
                     hole=0.4)
        fig.update_layout(**PLOTLY_THEME, height=350,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Fund Master Table ─────────────────────────────────────
    st.markdown("---")
    st.subheader("📋 Fund Master — All 40 Schemes")
    display_cols = ["scheme_name","fund_house","sub_category",
                    "plan","expense_ratio_pct","risk_category"]
    st.dataframe(
        fm[display_cols].rename(columns={
            "scheme_name":"Scheme Name",
            "fund_house":"Fund House",
            "sub_category":"Sub-Category",
            "plan":"Plan",
            "expense_ratio_pct":"Expense Ratio %",
            "risk_category":"Risk Category"
        }),
        use_container_width=True, height=400
    )


# ═════════════════════════════════════════════════════════════
# PAGE 2 — FUND PERFORMANCE
# ═════════════════════════════════════════════════════════════
elif page == "📈 Fund Performance":
    st.title("📈 Fund Performance")
    st.markdown("Risk-return analysis, NAV trends and fund scorecard")
    st.markdown("---")

    # ── Sidebar Filters ───────────────────────────────────────
    st.sidebar.markdown("### 🔍 Filters")
    sel_fh  = st.sidebar.multiselect(
        "Fund House", fm["fund_house"].unique().tolist(),
        default=fm["fund_house"].unique().tolist()
    )
    sel_cat = st.sidebar.multiselect(
        "Category", fm["sub_category"].unique().tolist(),
        default=fm["sub_category"].unique().tolist()
    )
    sel_plan = st.sidebar.multiselect(
        "Plan", ["Regular","Direct"], default=["Regular","Direct"]
    )

    # Filter perf
    perf_f = perf[
        (perf["fund_house"].isin(sel_fh)) &
        (perf["plan"].isin(sel_plan))
    ]
    fm_f = fm[
        (fm["fund_house"].isin(sel_fh)) &
        (fm["sub_category"].isin(sel_cat)) &
        (fm["plan"].isin(sel_plan))
    ]

    # ── Risk vs Return Scatter ────────────────────────────────
    st.subheader("🎯 Risk vs Return — All Funds")
    fig = px.scatter(
        perf_f, x="std_dev_ann_pct", y="return_3yr_pct",
        size="aum_crore", color="risk_grade",
        hover_name="scheme_name",
        hover_data={"sharpe_ratio":True,"expense_ratio_pct":True,
                    "alpha":True,"aum_crore":":.0f"},
        size_max=50,
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"std_dev_ann_pct":"Annualised Std Dev — Risk (%)",
                "return_3yr_pct":"3-Year Return (%)"},
    )
    fig.add_hline(y=perf_f["return_3yr_pct"].mean(),
                  line_dash="dash", line_color="yellow",
                  annotation_text="Avg 3yr Return")
    fig.add_vline(x=perf_f["std_dev_ann_pct"].mean(),
                  line_dash="dash", line_color="orange",
                  annotation_text="Avg Risk")
    fig.update_layout(**PLOTLY_THEME, height=480,
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    # ── NAV Trend ─────────────────────────────────────────────
    with col1:
        st.subheader("📉 NAV Trend")
        nav_codes = fm_f["amfi_code"].tolist()
        nav_f = nav[nav["amfi_code"].isin(nav_codes[:10])]

        sel_scheme = st.selectbox(
            "Select Fund",
            nav_f["scheme_name"].dropna().unique().tolist()
        )
        nav_single = nav_f[nav_f["scheme_name"] == sel_scheme]

        fig = px.line(nav_single, x="date", y="nav",
                      color_discrete_sequence=["#00B4D8"],
                      labels={"nav":"NAV (₹)","date":"Date"})
        fig.update_traces(line=dict(width=2))

        # Benchmark
        nifty = bi[bi["index_name"]=="NIFTY100"].set_index("date")["close_value"]
        nav_idx = nav_single.set_index("date")["nav"]
        if not nav_idx.empty and not nifty.empty:
            base = nav_idx.index.min()
            nav_norm  = (nav_idx / nav_idx.loc[nav_idx.index >= base].iloc[0]) * 100
            nifty_norm = (nifty / nifty.loc[nifty.index >= base].iloc[0]) * 100
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=nav_norm.index, y=nav_norm.values,
                name=sel_scheme[:20], line=dict(color="#00B4D8",width=2)))
            fig2.add_trace(go.Scatter(
                x=nifty_norm.index, y=nifty_norm.values,
                name="NIFTY100", line=dict(color="yellow",width=2,dash="dash")))
            fig2.update_layout(**PLOTLY_THEME, height=350,
                               yaxis_title="Indexed (Base=100)",
                               margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            fig.update_layout(**PLOTLY_THEME, height=350,
                              margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig, use_container_width=True)

    # ── Sharpe Ranking ────────────────────────────────────────
    with col2:
        st.subheader("⚡ Top 10 by Sharpe Ratio")
        top_sharpe = perf_f.nlargest(10,"sharpe_ratio")[
            ["scheme_name","sharpe_ratio","return_3yr_pct","risk_grade"]
        ].reset_index(drop=True)
        top_sharpe.index = top_sharpe.index + 1
        top_sharpe["scheme_name"] = top_sharpe["scheme_name"].str[:30]
        fig = px.bar(top_sharpe, x="sharpe_ratio", y="scheme_name",
                     orientation="h", color="risk_grade",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     labels={"sharpe_ratio":"Sharpe Ratio","scheme_name":""})
        fig.update_layout(**PLOTLY_THEME, height=350,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Fund Scorecard Table ──────────────────────────────────
    st.markdown("---")
    st.subheader("🏆 Fund Scorecard")
    scorecard_cols = [
        "scheme_name","fund_house","plan","return_1yr_pct",
        "return_3yr_pct","sharpe_ratio","alpha","beta",
        "expense_ratio_pct","max_drawdown_pct","aum_crore","risk_grade"
    ]
    st.dataframe(
        perf_f[scorecard_cols].sort_values("sharpe_ratio",ascending=False)
        .reset_index(drop=True).rename(columns={
            "scheme_name":"Scheme","fund_house":"Fund House",
            "plan":"Plan","return_1yr_pct":"1yr Return %",
            "return_3yr_pct":"3yr Return %","sharpe_ratio":"Sharpe",
            "alpha":"Alpha","beta":"Beta",
            "expense_ratio_pct":"Expense %",
            "max_drawdown_pct":"Max DD %",
            "aum_crore":"AUM Cr","risk_grade":"Risk"
        }),
        use_container_width=True, height=420
    )

    # ── Sector Holdings ───────────────────────────────────────
    st.markdown("---")
    st.subheader("🍩 Sector Allocation (Equity Funds)")
    equity_codes = fm[fm["category"]=="Equity"]["amfi_code"].tolist()
    ph_eq = ph[ph["amfi_code"].isin(equity_codes)]
    sector_wt = ph_eq.groupby("sector")["weight_pct"].sum()\
                     .sort_values(ascending=False).reset_index()
    fig = px.pie(sector_wt, values="weight_pct", names="sector",
                 hole=0.45,
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(**PLOTLY_THEME, height=400,
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════
# PAGE 3 — INVESTOR ANALYTICS
# ═════════════════════════════════════════════════════════════
elif page == "👥 Investor Analytics":
    st.title("👥 Investor Analytics")
    st.markdown("Demographics, geographic distribution and transaction patterns")
    st.markdown("---")

    # ── Sidebar Filters ───────────────────────────────────────
    st.sidebar.markdown("### 🔍 Filters")
    sel_state = st.sidebar.multiselect(
        "State", txn["state"].unique().tolist(),
        default=txn["state"].unique().tolist()
    )
    sel_age = st.sidebar.multiselect(
        "Age Group",
        sorted(txn["age_group"].unique().tolist()),
        default=sorted(txn["age_group"].unique().tolist())
    )
    sel_tier = st.sidebar.multiselect(
        "City Tier", ["T30","B30"], default=["T30","B30"]
    )
    sel_type = st.sidebar.multiselect(
        "Transaction Type",
        txn["transaction_type"].unique().tolist(),
        default=txn["transaction_type"].unique().tolist()
    )

    txn_f = txn[
        (txn["state"].isin(sel_state)) &
        (txn["age_group"].isin(sel_age)) &
        (txn["city_tier"].isin(sel_tier)) &
        (txn["transaction_type"].isin(sel_type))
    ]

    # ── KPI Cards ─────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Transactions", f"{len(txn_f):,}")
    k2.metric("Total Amount",       f"₹{txn_f['amount_inr'].sum()/1e7:.1f} Cr")
    k3.metric("Unique Investors",   f"{txn_f['investor_id'].nunique():,}")
    k4.metric("Avg Transaction",    f"₹{txn_f['amount_inr'].mean():,.0f}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    # ── Amount by State ───────────────────────────────────────
    with col1:
        st.subheader("🗺️ SIP Amount by State")
        state_amt = txn_f.groupby("state")["amount_inr"].sum()\
                         .sort_values(ascending=True).reset_index()
        state_amt["amount_cr"] = state_amt["amount_inr"] / 1e7
        fig = px.bar(state_amt, x="amount_cr", y="state",
                     orientation="h",
                     color="amount_cr",
                     color_continuous_scale="Blues",
                     labels={"amount_cr":"Amount (₹ Cr)","state":"State"})
        fig.update_layout(**PLOTLY_THEME, height=400,
                          showlegend=False, coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Transaction Type Donut ────────────────────────────────
    with col2:
        st.subheader("🍩 Transaction Type Split")
        type_amt = txn_f.groupby("transaction_type")["amount_inr"]\
                        .sum().reset_index()
        fig = px.pie(type_amt, values="amount_inr",
                     names="transaction_type", hole=0.45,
                     color_discrete_sequence=["#2196F3","#4CAF50","#E63946"])
        fig.update_layout(**PLOTLY_THEME, height=400,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)

    # ── Age Group vs Avg SIP ──────────────────────────────────
    with col3:
        st.subheader("👥 Avg SIP Amount by Age Group")
        age_order = ["18-25","26-35","36-45","46-55","56+"]
        sip_age = txn_f[txn_f["transaction_type"]=="SIP"]\
                       .groupby("age_group")["amount_inr"]\
                       .mean().reindex(age_order).reset_index()
        fig = px.bar(sip_age, x="age_group", y="amount_inr",
                     color="amount_inr",
                     color_continuous_scale="Blues",
                     labels={"amount_inr":"Avg SIP (₹)","age_group":"Age Group"})
        fig.update_layout(**PLOTLY_THEME, height=350,
                          coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Gender Split ──────────────────────────────────────────
    with col4:
        st.subheader("⚧ Gender Split")
        gen = txn_f["gender"].value_counts().reset_index()
        gen.columns = ["gender","count"]
        fig = px.pie(gen, values="count", names="gender",
                     hole=0.45,
                     color_discrete_sequence=["#4FC3F7","#F48FB1"])
        fig.update_layout(**PLOTLY_THEME, height=350,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Monthly Transaction Volume ────────────────────────────
    st.markdown("---")
    st.subheader("📅 Monthly Transaction Volume")
    txn_f2 = txn_f.copy()
    txn_f2["month"] = txn_f2["transaction_date"].dt.to_period("M").dt.to_timestamp()
    monthly = txn_f2.groupby(["month","transaction_type"])["amount_inr"]\
                    .sum().reset_index()
    monthly["amount_cr"] = monthly["amount_inr"] / 1e7
    fig = px.line(monthly, x="month", y="amount_cr",
                  color="transaction_type",
                  color_discrete_sequence=["#2196F3","#4CAF50","#E63946"],
                  markers=True,
                  labels={"amount_cr":"Amount (₹ Cr)","month":"Month",
                          "transaction_type":"Type"})
    fig.update_layout(**PLOTLY_THEME, height=380,
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # ── T30 vs B30 ────────────────────────────────────────────
    st.markdown("---")
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("🏙️ T30 vs B30 City Tier")
        tier = txn_f.groupby("city_tier")["amount_inr"].sum().reset_index()
        fig = px.pie(tier, values="amount_inr", names="city_tier",
                     hole=0.45,
                     color_discrete_sequence=["#2196F3","#FF9800"])
        fig.update_layout(**PLOTLY_THEME, height=350,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.subheader("💳 Payment Mode Distribution")
        pay = txn_f.groupby("payment_mode")["amount_inr"].sum()\
                   .sort_values(ascending=False).reset_index()
        pay["amount_cr"] = pay["amount_inr"] / 1e7
        fig = px.bar(pay, x="payment_mode", y="amount_cr",
                     color="payment_mode",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     labels={"amount_cr":"Amount (₹ Cr)","payment_mode":"Mode"})
        fig.update_layout(**PLOTLY_THEME, height=350,
                          showlegend=False,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════
# PAGE 4 — SIP & MARKET TRENDS
# ═════════════════════════════════════════════════════════════
elif page == "💰 SIP & Market Trends":
    st.title("💰 SIP & Market Trends")
    st.markdown("SIP inflow trends, category analysis and benchmark comparison")
    st.markdown("---")

    # ── Sidebar Filters ───────────────────────────────────────
    st.sidebar.markdown("### 🔍 Filters")
    sel_index = st.sidebar.selectbox(
        "Benchmark Index",
        bi["index_name"].unique().tolist(),
        index=0
    )
    sel_categories = st.sidebar.multiselect(
        "Fund Categories",
        cat["category"].unique().tolist(),
        default=cat["category"].unique().tolist()
    )

    # ── SIP Inflow Trend ──────────────────────────────────────
    st.subheader("📈 Monthly SIP Inflow (2022–2025)")
    ath_idx = sip["sip_inflow_crore"].idxmax()
    ath_x   = sip.loc[ath_idx,"month_dt"]
    ath_y   = sip.loc[ath_idx,"sip_inflow_crore"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sip["month_dt"], y=sip["sip_inflow_crore"],
        mode="lines+markers", name="SIP Inflow",
        line=dict(color="#2196F3",width=2.5),
        fill="tozeroy", fillcolor="rgba(33,150,243,0.12)"
    ))
    fig.add_annotation(
        x=ath_x, y=ath_y,
        text=f"<b>All-Time High<br>₹{ath_y:,.0f} Cr</b>",
        showarrow=True, arrowhead=2, arrowcolor="red",
        font=dict(color="red",size=12),
        bgcolor="rgba(255,255,200,0.9)",
        bordercolor="red", borderwidth=1.5,
        ax=0, ay=-55
    )
    fig.update_layout(**PLOTLY_THEME, height=380,
                      xaxis_title="Month",
                      yaxis_title="SIP Inflow (₹ Crore)",
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    # ── Benchmark Trend ───────────────────────────────────────
    with col1:
        st.subheader(f"📊 {sel_index} Index Trend")
        bi_sel = bi[bi["index_name"]==sel_index]
        fig = px.line(bi_sel, x="date", y="close_value",
                      color_discrete_sequence=["#FF9800"],
                      labels={"close_value":"Close Value","date":"Date"})
        fig.update_traces(line=dict(width=2))
        fig.update_layout(**PLOTLY_THEME, height=380,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── SIP Accounts ──────────────────────────────────────────
    with col2:
        st.subheader("👤 Active SIP Accounts Growth")
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=sip["month_dt"], y=sip["sip_inflow_crore"],
            name="SIP Inflow (₹ Cr)",
            marker_color="rgba(33,150,243,0.6)"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=sip["month_dt"], y=sip["active_sip_accounts_crore"],
            name="Active Accounts (Cr)",
            line=dict(color="#FF9800",width=2.5),
            mode="lines+markers"
        ), secondary_y=True)
        fig.update_layout(**PLOTLY_THEME, height=380,
                          margin=dict(l=0,r=0,t=20,b=0))
        fig.update_yaxes(title_text="SIP Inflow (₹ Cr)",
                         secondary_y=False)
        fig.update_yaxes(title_text="Active Accounts (Cr)",
                         secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    # ── Category Heatmap ──────────────────────────────────────
    st.markdown("---")
    st.subheader("🗺️ Category Inflow Heatmap")
    cat_f = cat[cat["category"].isin(sel_categories)].copy()
    cat_f = cat_f[cat_f["category"] != "Liquid"]
    cat_f["month_str"] = cat_f["month_dt"].dt.strftime("%b %Y")
    pivot = cat_f.pivot_table(
        index="category", columns="month_str",
        values="net_inflow_crore", aggfunc="sum"
    )
    col_order = [pd.Timestamp(m).strftime("%b %Y")
                 for m in sorted(cat_f["month_dt"].dropna().unique())]
    col_order = [c for c in col_order if c in pivot.columns]
    pivot = pivot[col_order]

    fig = px.imshow(
        pivot, color_continuous_scale="RdYlGn",
        aspect="auto",
        labels=dict(x="Month", y="Category", color="Net Inflow (₹ Cr)")
    )
    fig.update_layout(**PLOTLY_THEME, height=420,
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # ── Top 5 Categories ─────────────────────────────────────
    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🏆 Top 5 Categories by Net Inflow")
        top5_cat = cat_f.groupby("category")["net_inflow_crore"]\
                        .sum().nlargest(5).reset_index()
        fig = px.bar(top5_cat, x="net_inflow_crore", y="category",
                     orientation="h", color="net_inflow_crore",
                     color_continuous_scale="Greens",
                     labels={"net_inflow_crore":"Net Inflow (₹ Cr)",
                              "category":"Category"})
        fig.update_layout(**PLOTLY_THEME, height=350,
                          coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("📊 YoY SIP Growth")
        sip_yoy = sip.dropna(subset=["yoy_growth_pct"])
        fig = px.bar(sip_yoy, x="month_dt", y="yoy_growth_pct",
                     color="yoy_growth_pct",
                     color_continuous_scale="RdYlGn",
                     labels={"yoy_growth_pct":"YoY Growth (%)",
                              "month_dt":"Month"})
        fig.add_hline(y=0, line_color="white",
                      line_dash="dash", line_width=1)
        fig.update_layout(**PLOTLY_THEME, height=350,
                          coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # ── Fund Recommender ──────────────────────────────────────
    st.markdown("---")
    st.subheader("🤖 Quick Fund Recommender")
    risk_input = st.selectbox(
        "Select your Risk Appetite",
        ["Low","Moderate","High"]
    )
    risk_map = {
        "Low"     : ["Low"],
        "Moderate": ["Moderate","Moderately High"],
        "High"    : ["High","Very High"],
    }
    matching = risk_map[risk_input]
    perf_rec = perf.copy()
    perf_rec["risk_grade"] = perf_rec.get(
        "risk_grade", perf_rec.get("risk_grade","")
    )
    rec = perf_rec[perf_rec["risk_grade"].isin(matching)]\
              .nlargest(3,"sharpe_ratio")[[
                  "scheme_name","fund_house","plan",
                  "sharpe_ratio","return_3yr_pct",
                  "expense_ratio_pct","risk_grade"
              ]].reset_index(drop=True)
    rec.index = rec.index + 1
    if not rec.empty:
        st.success(f"Top 3 funds for **{risk_input}** risk appetite:")
        st.dataframe(rec.rename(columns={
            "scheme_name":"Fund Name",
            "fund_house":"AMC",
            "plan":"Plan",
            "sharpe_ratio":"Sharpe",
            "return_3yr_pct":"3yr Return %",
            "expense_ratio_pct":"Expense %",
            "risk_grade":"Risk Grade"
        }), use_container_width=True)
    else:
        st.warning("No funds found for this risk appetite.")

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#64748B; font-size:12px;'>"
    "Bluestock Mutual Fund Analytics | Jatin Yadav | BML Munjal University | 2025"
    "</div>",
    unsafe_allow_html=True
)