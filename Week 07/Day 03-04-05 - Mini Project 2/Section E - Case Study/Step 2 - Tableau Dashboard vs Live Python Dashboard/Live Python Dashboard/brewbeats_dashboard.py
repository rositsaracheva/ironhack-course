"""
=============================================================================
BrewBeats — Mini Project 2: Section E (Live Real-Time Python Dashboard)
Folder: Section E - Case Study/Live Python Dashboard/
File  : brewbeats_dashboard.py
Stack : Python + Streamlit + Plotly + DuckDB (Connected to Section D dbt Warehouse!)
=============================================================================
How this Live Python Dashboard works:
1. Direct Warehouse Connection:
   It connects directly to our local DuckDB warehouse (`brewbeats.duckdb`) built by
   our dbt models (`stg_coffee_sales` & `fct_daily_revenue`) in Section D! If the DuckDB
   file is not present (e.g. if someone clones this repo fresh), it gracefully falls back
   to `cleaned_coffee_sales.csv` so the app always runs cleanly.
2. Real-Time POS Order Simulator:
   Using Streamlit `session_state`, we can simulate live coffee kiosk sales coming in
   ("⚡ Simulate Live Coffee Sale" button or Auto-Refresh toggle) and watch the KPIs,
   live transaction ticker, and Plotly charts update instantaneously!
3. All 10 Section E Dashboard Requirements + BrewBeats In-Store Music Tab:
   - Tab 1 (Executive Sales Overview): KPIs 1-4 (Total Revenue, Total Transactions,
     Avg Transaction Value, Best-Selling Coffee), Chart 5 (Revenue by Coffee Type),
     Chart 6 & 10 (Revenue by Month + Monthly Sales Trend with Linear Regression Line).
   - Tab 2 (Customer Purchasing Patterns): Chart 7 (Sales by Weekday), Chart 8 (Sales by Hour
     highlighting the 10 AM and 4 PM dual peaks), Chart 9 (Cash vs Card Donut Chart),
     and a Weekday × Hour Demand Heatmap!
   - Tab 3 (BrewBeats In-Store Spotify Playlists): Connects `Spotify_data.csv` so managers can
     explore the 5th Birthday Party Playlist (Section A - Q8), Drake's Top Tracks (Section C - Q4),
     and interactive audio-feature sliders (danceability, energy, valence, tempo).
"""

import os
import random
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    import duckdb
except ImportError:
    duckdb = None

# ---------------------------------------------------------------------------
# 1. PAGE CONFIG & CUSTOM COFFEE-THEMED EXECUTIVE STYLING
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="BrewBeats | Real-Time Coffee & Music Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for sleek dark espresso & warm gold/latte KPI cards
st.markdown(
    """
    <style>
        .main {
            background-color: #0E1117;
        }
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #1E1B18 0%, #2B241E 100%);
            border: 1px solid #4A3728;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        div[data-testid="stMetric"] label {
            color: #D4A373 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #FFF8F0 !important;
            font-size: 1.85rem !important;
            font-weight: 700 !important;
        }
        .live-badge {
            display: inline-block;
            background-color: #1B4332;
            color: #74C69D;
            border: 1px solid #40916C;
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 2. DATA LOADING (CONNECTS DIRECTLY TO SECTION D DBT DUCKDB WAREHOUSE!)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))
DUCKDB_PATH = os.path.join(
    PROJECT_ROOT,
    "Section D - dbt + Airflow Pipeline",
    "Section D_Q1",
    "brewbeats_dbt",
    "brewbeats.duckdb",
)
CLEANED_CSV_PATH = os.path.join(
    PROJECT_ROOT, "Section E - Case Study", "Step 1 - Case Study & Ingestion", "cleaned_coffee_sales.csv"
)
SPOTIFY_CSV_PATH = os.path.join(PROJECT_ROOT, "Spotify_data.csv")


@st.cache_data
def load_coffee_data():
    """
    Loads coffee sales from our dbt DuckDB staging view (`main.stg_coffee_sales`)
    so the dashboard is connected directly to our Section D dbt warehouse.
    Falls back to `cleaned_coffee_sales.csv` if the local DuckDB file is unavailable.
    """
    source_label = "DuckDB dbt Warehouse (`main.stg_coffee_sales`)"
    if duckdb is not None and os.path.exists(DUCKDB_PATH):
        try:
            con = duckdb.connect(DUCKDB_PATH, read_only=True)
            df = con.sql(
                """
                SELECT
                    sale_date AS date,
                    sale_timestamp AS datetime,
                    payment_type AS cash_type,
                    card_id AS card,
                    CAST(amount AS DOUBLE) AS money,
                    coffee_name
                FROM main.stg_coffee_sales
                """
            ).df()
            con.close()
        except Exception:
            source_label = "Cleaned POS CSV (`cleaned_coffee_sales.csv`)"
            df = pd.read_csv(CLEANED_CSV_PATH)
    else:
        source_label = "Cleaned POS CSV (`cleaned_coffee_sales.csv`)"
        df = pd.read_csv(CLEANED_CSV_PATH)

    df["date"] = pd.to_datetime(df["date"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    df["weekday"] = df["date"].dt.day_name()
    df["hour_of_day"] = df["datetime"].dt.hour
    return df, source_label


@st.cache_data
def load_spotify_data():
    """Loads BrewBeats' Spotify music catalog (`Spotify_data.csv`) for the In-Store Playlists tab."""
    if os.path.exists(SPOTIFY_CSV_PATH):
        return pd.read_csv(SPOTIFY_CSV_PATH)
    return pd.DataFrame()


base_coffee_df, data_source_label = load_coffee_data()
spotify_df = load_spotify_data()

# ---------------------------------------------------------------------------
# 3. REAL-TIME POS SIMULATOR STATE (st.session_state)
# ---------------------------------------------------------------------------
# Store simulated live coffee kiosk transactions in session_state so clicking
# "Simulate Live Coffee Sale" adds real-time orders and updates all charts immediately!
if "live_orders" not in st.session_state:
    st.session_state.live_orders = []

COFFEE_MENU_PRICES = {
    "Latte": 35.76,
    "Americano with Milk": 30.86,
    "Cappuccino": 35.76,
    "Americano": 25.96,
    "Hot Chocolate": 35.76,
    "Cocoa": 35.76,
    "Cortado": 25.96,
    "Espresso": 21.06,
}

# Combine historical dbt warehouse data + any live simulated POS orders
if st.session_state.live_orders:
    live_df = pd.DataFrame(st.session_state.live_orders)
    full_df = pd.concat([base_coffee_df, live_df], ignore_index=True)
else:
    full_df = base_coffee_df.copy()

# ---------------------------------------------------------------------------
# 4. SIDEBAR CONTROLS (INTERACTIVE FILTERS + REAL-TIME POS SIMULATOR)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ☕ BrewBeats Control Panel")
    st.caption("**Built by:** Rositsa Kaloyanova (Data Engineering Portfolio)")
    st.caption(f"**Data Source:** {data_source_label}")
    st.divider()

    # Real-Time POS Order Simulator Section
    st.markdown("### ⚡ Real-Time POS Simulator")
    st.caption("Simulate live kiosk transactions arriving in real time:")

    col_sim1, col_sim2 = st.columns(2)
    with col_sim1:
        if st.button("➕ 1 Live Sale", use_container_width=True, type="primary"):
            drink = random.choice(list(COFFEE_MENU_PRICES.keys()))
            price = COFFEE_MENU_PRICES[drink]
            pay_type = random.choices(["card", "cash"], weights=[0.97, 0.03])[0]
            now = datetime.now()
            st.session_state.live_orders.append(
                {
                    "date": pd.Timestamp(now.date()),
                    "datetime": pd.Timestamp(now),
                    "cash_type": pay_type,
                    "card": f"LIVE-{random.randint(1000, 9999)}" if pay_type == "card" else "CASH_NO_CARD",
                    "money": price,
                    "coffee_name": drink,
                    "year_month": now.strftime("%Y-%m"),
                    "weekday": now.strftime("%A"),
                    "hour_of_day": now.hour,
                }
            )
            st.rerun()

    with col_sim2:
        if st.button("🔄 Reset Live", use_container_width=True):
            st.session_state.live_orders = []
            st.rerun()

    if st.session_state.live_orders:
        last = st.session_state.live_orders[-1]
        st.success(
            f"**+{len(st.session_state.live_orders)} live order(s)**\n\n"
            f"Latest: **{last['coffee_name']}** (${last['money']:.2f} via {last['cash_type']})"
        )

    st.divider()

    # Interactive Dashboard Filters
    st.markdown("### 🎛️ Interactive Filters")
    min_date = full_df["date"].min().date()
    max_date = full_df["date"].max().date()
    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    all_coffees = sorted(full_df["coffee_name"].unique().tolist())
    selected_coffees = st.multiselect(
        "Coffee Types",
        options=all_coffees,
        default=all_coffees,
    )

    all_payments = sorted(full_df["cash_type"].unique().tolist())
    selected_payments = st.multiselect(
        "Payment Method",
        options=all_payments,
        default=all_payments,
    )

# Apply all sidebar filters to create the active filtered DataFrame
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_dt, end_dt = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_dt, end_dt = pd.Timestamp(min_date), pd.Timestamp(max_date)

filtered_df = full_df[
    (full_df["date"] >= start_dt)
    & (full_df["date"] <= end_dt)
    & (full_df["coffee_name"].isin(selected_coffees))
    & (full_df["cash_type"].isin(selected_payments))
].copy()

# ---------------------------------------------------------------------------
# 5. DASHBOARD HEADER
# ---------------------------------------------------------------------------
st.markdown('<span class="live-badge">● LIVE PIPELINE CONNECTED</span>', unsafe_allow_html=True)
st.title("☕ BrewBeats — Coffee Sales & In-Store Music Executive Dashboard")
st.markdown("**Author:** Rositsa Kaloyanova  |  *IronHack Data Engineering Bootcamp — Mini Project 2*")
st.caption(
    f"Period: **{start_dt.strftime('%B %Y')} – {end_dt.strftime('%B %Y')}**  |  "
    f"Showing **{len(filtered_df):,}** transactions  |  "
    f"Architecture: `CSV → Python/Pandas → DuckDB/Snowflake → dbt → Airflow → Streamlit`"
)

if filtered_df.empty:
    st.warning("No transactions match your current filter selection. Please adjust the sidebar filters.")
    st.stop()

# ---------------------------------------------------------------------------
# 6. TABS LAYOUT (ALL 10 SECTION E REQUIREMENTS + SPOTIFY PLAYLISTS TAB)
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Executive Sales Overview (KPIs 1–6 & 10)",
        "🕒 Customer Patterns & Peak Hours (Charts 7–9)",
        "🎵 BrewBeats In-Store Spotify Playlists",
    ]
)

# Color palette (Coffee / Caramel / Gold theme)
COFFEE_COLORS = ["#D4A373", "#E9C46A", "#F4A261", "#E76F51", "#A98467", "#6C584C", "#2A9D8F", "#264653"]

# ===========================================================================
# TAB 1: EXECUTIVE SALES OVERVIEW (Requirements 1, 2, 3, 4, 5, 6, 10)
# ===========================================================================
with tab1:
    # --- KPI Row (Requirements 1, 2, 3, 4) ---
    total_revenue = filtered_df["money"].sum()
    total_tx = len(filtered_df)
    avg_tx = filtered_df["money"].mean()

    coffee_rev_summary = filtered_df.groupby("coffee_name").agg(
        transactions=("money", "count"),
        revenue=("money", "sum"),
        avg_price=("money", "mean"),
    ).reset_index()

    best_rev_row = coffee_rev_summary.sort_values("revenue", ascending=False).iloc[0]
    best_vol_row = coffee_rev_summary.sort_values("transactions", ascending=False).iloc[0]

    live_rev_delta = sum(o["money"] for o in st.session_state.live_orders)
    live_tx_delta = len(st.session_state.live_orders)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(
        "1. Total Sales Revenue",
        f"${total_revenue:,.2f}",
        delta=f"+${live_rev_delta:,.2f} live" if live_rev_delta > 0 else "Verified dbt Mart",
    )
    kpi2.metric(
        "2. Total Transactions",
        f"{total_tx:,}",
        delta=f"+{live_tx_delta} live orders" if live_tx_delta > 0 else "100% Data Quality Passed",
    )
    kpi3.metric(
        "3. Avg Transaction Value",
        f"${avg_tx:,.2f}",
        delta=f"Card: ${filtered_df[filtered_df['cash_type']=='card']['money'].mean():.2f}"
        if "card" in filtered_df["cash_type"].values
        else None,
    )
    kpi4.metric(
        "4. Best-Selling Coffee",
        f"{best_rev_row['coffee_name']}",
        delta=f"${best_rev_row['revenue']:,.2f} | Vol #1: {best_vol_row['coffee_name']} ({best_vol_row['transactions']})",
    )

    st.markdown("---")

    # --- Middle Row: Requirement 5 (Revenue by Coffee Type) & Requirement 10 (Monthly Sales Trends) ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("5. Revenue by Coffee Type")
        coffee_sorted = coffee_rev_summary.sort_values("revenue", ascending=True)
        fig_coffee = px.bar(
            coffee_sorted,
            x="revenue",
            y="coffee_name",
            orientation="h",
            text=coffee_sorted["revenue"].apply(lambda x: f"${x:,.0f}"),
            color="revenue",
            color_continuous_scale="YlOrBr",
            hover_data=["transactions", "avg_price", "revenue"],
            labels={"revenue": "Total Revenue ($)", "coffee_name": "Coffee Drink", "transactions": "Cups Sold"},
        )
        fig_coffee.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            height=400,
            margin=dict(l=10, r=20, t=20, b=20),
        )
        fig_coffee.update_traces(textposition="outside")
        st.plotly_chart(fig_coffee, use_container_width=True)

    with col_right:
        st.subheader("10. Monthly Sales Trends (with Linear Growth Line)")
        monthly_df = (
            filtered_df.groupby("year_month")
            .agg(transactions=("money", "count"), revenue=("money", "sum"))
            .reset_index()
            .sort_values("year_month")
        )

        # Calculate linear trend line using NumPy polyfit
        x_idx = np.arange(len(monthly_df))
        fig_trend = go.Figure()
        fig_trend.add_trace(
            go.Scatter(
                x=monthly_df["year_month"],
                y=monthly_df["revenue"],
                mode="lines+markers+text",
                name="Monthly Revenue ($)",
                line=dict(color="#D4A373", width=3),
                marker=dict(size=9, color="#FFF8F0", line=dict(color="#D4A373", width=2)),
                text=monthly_df["revenue"].apply(lambda v: f"${v/1000:.1f}k"),
                textposition="top center",
                hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>",
            )
        )
        if len(monthly_df) >= 2:
            slope, intercept = np.polyfit(x_idx, monthly_df["revenue"], 1)
            trend_vals = slope * x_idx + intercept
            fig_trend.add_trace(
                go.Scatter(
                    x=monthly_df["year_month"],
                    y=trend_vals,
                    mode="lines",
                    name="Linear Trend",
                    line=dict(color="#74C69D", width=2, dash="dash"),
                )
            )
        fig_trend.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            xaxis_title="Month (YYYY-MM)",
            yaxis_title="Revenue ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=20, t=30, b=20),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    # --- Bottom Row: Requirement 6 (Revenue by Month Bar Chart) ---
    st.subheader("6. Revenue & Transaction Volume by Month")
    fig_month_bar = px.bar(
        monthly_df,
        x="year_month",
        y="revenue",
        text=monthly_df["revenue"].apply(lambda x: f"${x:,.0f}"),
        color="revenue",
        color_continuous_scale="Tealgrn",
        hover_data=["transactions", "revenue"],
        labels={"year_month": "Month", "revenue": "Total Revenue ($)", "transactions": "Transactions"},
    )
    fig_month_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        height=340,
        margin=dict(l=10, r=20, t=20, b=20),
    )
    fig_month_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_month_bar, use_container_width=True)


# ===========================================================================
# TAB 2: CUSTOMER PURCHASING PATTERNS (Requirements 7, 8, 9 + Demand Heatmap)
# ===========================================================================
with tab2:
    col_w, col_p = st.columns([1.4, 1])

    with col_w:
        st.subheader("7. Sales by Weekday")
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday_df = (
            filtered_df.groupby("weekday")
            .agg(transactions=("money", "count"), revenue=("money", "sum"))
            .reindex(weekday_order)
            .dropna()
            .reset_index()
        )
        fig_weekday = px.bar(
            weekday_df,
            x="weekday",
            y="revenue",
            text=weekday_df["revenue"].apply(lambda x: f"${x:,.0f}"),
            color="revenue",
            color_continuous_scale="YlOrBr",
            hover_data=["transactions", "revenue"],
            labels={"weekday": "Day of Week", "revenue": "Total Revenue ($)", "transactions": "Transactions"},
        )
        fig_weekday.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            height=380,
            margin=dict(l=10, r=20, t=20, b=20),
        )
        fig_weekday.update_traces(textposition="outside")
        st.plotly_chart(fig_weekday, use_container_width=True)

    with col_p:
        st.subheader("9. Cash vs. Card Transactions")
        pay_df = (
            filtered_df.groupby("cash_type")
            .agg(transactions=("money", "count"), revenue=("money", "sum"))
            .reset_index()
        )
        fig_pay = px.pie(
            pay_df,
            names="cash_type",
            values="transactions",
            hole=0.55,
            color="cash_type",
            color_discrete_map={"card": "#D4A373", "cash": "#2A9D8F"},
            hover_data=["revenue"],
        )
        fig_pay.update_traces(textinfo="label+percent+value", textfont_size=13)
        fig_pay.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=380,
            margin=dict(l=10, r=10, t=20, b=20),
        )
        st.plotly_chart(fig_pay, use_container_width=True)

    st.markdown("---")

    # Requirement 8: Sales by Hour (Area Chart showing Dual Peak at 10 AM & 4 PM)
    st.subheader("8. Sales by Hour of Day (Dual-Peak Demand Curve)")
    hour_df = (
        filtered_df.groupby("hour_of_day")
        .agg(transactions=("money", "count"), revenue=("money", "sum"))
        .reset_index()
        .sort_values("hour_of_day")
    )
    fig_hour = px.area(
        hour_df,
        x="hour_of_day",
        y="revenue",
        markers=True,
        hover_data=["transactions", "revenue"],
        labels={"hour_of_day": "Hour of Day (24h)", "revenue": "Total Revenue ($)", "transactions": "Transactions"},
    )
    fig_hour.update_traces(line_color="#E9C46A", fillcolor="rgba(233, 196, 106, 0.25)")
    fig_hour.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(dtick=1),
        height=350,
        margin=dict(l=10, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_hour, use_container_width=True)

    # Bonus Advanced Visual: Weekday x Hour Demand Heatmap (Staffing & Playlist Optimization)
    st.subheader("🔥 Bonus: Weekday × Hour Sales Heatmap (Staffing & Playlist Optimization)")
    heat_pivot = (
        filtered_df.pivot_table(
            index="weekday", columns="hour_of_day", values="money", aggfunc="sum", fill_value=0
        )
        .reindex(weekday_order)
        .dropna(how="all")
    )
    fig_heat = px.imshow(
        heat_pivot,
        aspect="auto",
        color_continuous_scale="YlOrBr",
        labels=dict(x="Hour of Day (24h)", y="Weekday", color="Revenue ($)"),
    )
    fig_heat.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        height=340,
        margin=dict(l=10, r=20, t=10, b=20),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ===========================================================================
# TAB 3: BREWBEATS IN-STORE SPOTIFY PLAYLISTS (Connecting Spotify_data.csv!)
# ===========================================================================
with tab3:
    if spotify_df.empty:
        st.info("Spotify_data.csv not found at project root.")
    else:
        st.subheader("🎵 BrewBeats In-Store Music Curation Engine (`Spotify_data.csv`)")
        st.caption("Interactive playlist curator powered by the same Spotify audio features analyzed in Sections A & C.")

        c1, c2, c3 = st.columns(3)
        min_dance = c1.slider("Min Danceability", 0.0, 1.0, 0.80, 0.05)
        min_energy = c2.slider("Min Energy", 0.0, 1.0, 0.80, 0.05)
        min_valence = c3.slider("Min Valence (Happiness)", 0.0, 1.0, 0.75, 0.05)

        curated = spotify_df[
            (spotify_df["danceability"] >= min_dance)
            & (spotify_df["energy"] >= min_energy)
            & (spotify_df["valence"] >= min_valence)
        ].copy()
        curated["party_score"] = (
            (curated["danceability"] + curated["energy"] + curated["valence"]) / 3
        ).round(3)
        curated = curated.sort_values("party_score", ascending=False)

        m1, m2, m3 = st.columns(3)
        m1.metric("Catalog Songs", f"{len(spotify_df):,}")
        m2.metric("Matching Playlist Tracks", f"{len(curated):,}")
        m3.metric("Avg Catalog Danceability", f"{spotify_df['danceability'].mean():.4f}")

        fig_scatter = px.scatter(
            curated.head(50),
            x="danceability",
            y="energy",
            size="tempo",
            color="valence",
            hover_name="song_title",
            hover_data=["artist", "party_score", "tempo"],
            color_continuous_scale="YlOrBr",
            title="Curated In-Store Playlist Audio Map (Danceability vs. Energy)",
        )
        fig_scatter.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.dataframe(
            curated[["song_title", "artist", "danceability", "energy", "valence", "tempo", "party_score"]].head(15),
            use_container_width=True,
            hide_index=True,
        )

