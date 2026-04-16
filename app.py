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

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Call Centre Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.big-title {
    font-size: 32px;
    font-weight: bold;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}
.metric {
    font-size: 28px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown('<div class="big-title">📊 Call Centre Analytics Dashboard</div>', unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
df = pd.read_csv("Call_Center_Data.csv")
df.columns = df.columns.map(str).str.strip()

# ------------------ SIDEBAR ------------------
st.sidebar.header("🔍 Filters")

city = st.sidebar.selectbox("Select City", df["City"].dropna().unique())
channel = st.sidebar.selectbox("Select Channel", df["Channel"].dropna().unique())

filtered_df = df[(df["City"] == city) & (df["Channel"] == channel)]

# ------------------ KPI CARDS ------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

# Detect CSAT column automatically
csat_col = None
for col in df.columns:
    if "csat" in col.lower():
        csat_col = col

# Metrics
total_calls = len(filtered_df)
unique_cities = filtered_df["City"].nunique()
channels = filtered_df["Channel"].nunique()
avg_csat = round(filtered_df[csat_col].mean(), 2) if csat_col else 0

# Cards UI
col1.markdown(f"<div class='card'><div>Total Calls</div><div class='metric'>{total_calls}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><div>Unique Cities</div><div class='metric'>{unique_cities}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><div>Channels</div><div class='metric'>{channels}</div></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='card'><div>Avg CSAT</div><div class='metric'>{avg_csat}</div></div>", unsafe_allow_html=True)

# ------------------ CHARTS ------------------
st.subheader("📊 Visual Insights")

col5, col6 = st.columns(2)

# Calls by City
city_counts = filtered_df["City"].value_counts()
col5.bar_chart(city_counts)

# Calls by Channel
channel_counts = filtered_df["Channel"].value_counts()
col6.bar_chart(channel_counts)

# ------------------ DATA TABLE ------------------
st.subheader("📋 Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# ------------------ INSIGHTS ------------------
st.subheader("🧠 Insights")

# CSAT insight
if avg_csat >= 7:
    st.success("✅ Customer satisfaction is good")
else:
    st.warning("⚠️ Customer satisfaction needs improvement")

# SLA insight
if "Response Time" in df.columns:
    sla = round((filtered_df["Response Time"].astype(str).str.contains("Within")).mean() * 100, 2)
    
    if sla >= 80:
        st.success("✅ SLA performance is strong")
    else:
        st.error("❌ SLA performance is poor")

st.info("📌 Fridays and weekdays usually have higher call volume.")
