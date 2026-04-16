# =============================================================================
# Call Centre Performance Analytics
# Author: Neha Tiwari
# Dataset: Call Centre Operations — October 2020 (32,941 records, 12 features)
# Goal: Analyse call volume, SLA compliance, customer sentiment, and CSAT
#       scores to identify operational inefficiencies and improvement areas.
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Call Centre Analytics",
    layout="wide",
    page_icon="📊"
)

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}
.title {
    font-size: 32px;
    font-weight: 700;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.markdown('<p class="title">📊 Call Centre Analytics Dashboard</p>', unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("Call_Center_Data.csv")

# Convert date
df["Call Timestamp"] = pd.to_datetime(df["Call Timestamp"], dayfirst=True)

st.caption(f"📂 Dataset: {df.shape[0]} rows × {df.shape[1]} columns")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

city = st.sidebar.selectbox("City", df["City"].unique())
channel = st.sidebar.selectbox("Channel", df["Channel"].unique())

# -------------------------------
# FILTERED DATA
# -------------------------------
filtered_df = df[(df["City"] == city) & (df["Channel"] == channel)]

# -------------------------------
# KPI METRICS
# -------------------------------
st.subheader("📊 Key Performance Indicators")
st.write(df.colums)
total_calls = len(filtered_df)
avg_csat = round(filtered_df["CSAT"].mean(), 2)
sla = round((filtered_df["SLA"] == "Yes").mean() * 100, 2)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Calls</h3>
        <h2>{total_calls}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Avg CSAT</h3>
        <h2>{avg_csat}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>SLA Compliance %</h3>
        <h2>{sla}%</h2>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# TIME TREND
# -------------------------------
st.subheader("📈 Call Volume Trend")

calls_trend = filtered_df.groupby(filtered_df["Call Timestamp"].dt.date).size()
st.line_chart(calls_trend)

# -------------------------------
# CHARTS SECTION
# -------------------------------
st.subheader("📊 Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Calls by City")
    st.bar_chart(filtered_df["City"].value_counts())

with col2:
    st.markdown("### Calls by Channel")
    st.bar_chart(filtered_df["Channel"].value_counts())

# -------------------------------
# CSAT DISTRIBUTION
# -------------------------------
st.subheader("⭐ CSAT Score Distribution")
st.bar_chart(filtered_df["CSAT Score"].value_counts())

# -------------------------------
# SLA DISTRIBUTION
# -------------------------------
st.subheader("⏱ SLA Compliance Breakdown")
st.bar_chart(filtered_df["SLA Compliance"].value_counts())

# -------------------------------
# DATA TABLE
# -------------------------------
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
