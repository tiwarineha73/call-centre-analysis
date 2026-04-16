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

st.title("📊 Call Centre Analytics Dashboard")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("Call_Center_Data.csv")

# 🔥 FIX COLUMN NAMES (important)
df.columns = df.columns.map(str).str.strip()

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filters")

# Safe column names
city_col = "City" if "City" in df.columns else df.columns[0]
channel_col = "Channel" if "Channel" in df.columns else df.columns[1]

city = st.sidebar.selectbox("Select City", df[city_col].dropna().unique())
channel = st.sidebar.selectbox("Select Channel", df[channel_col].dropna().unique())

# Apply filters
filtered_df = df[(df[city_col] == city) & (df[channel_col] == channel)]

# ------------------ DATA INFO ------------------
st.write(f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ------------------ KPI SECTION ------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

# Total Calls
col1.metric("Total Calls", len(filtered_df))

# Unique Cities
if "City" in df.columns:
    col2.metric("Unique Cities", filtered_df["City"].nunique())
else:
    col2.metric("Unique Cities", 0)

# Channels
if "Channel" in df.columns:
    col3.metric("Channels", filtered_df["Channel"].nunique())
else:
    col3.metric("Channels", 0)

# ------------------ ADVANCED KPIs ------------------
st.subheader("📈 Performance Metrics")

col4, col5 = st.columns(2)

# ✅ CSAT FIX
csat_col = None
for col in df.columns:
    if "csat" in col.lower():
        csat_col = col
        break

if csat_col:
    avg_csat = round(filtered_df[csat_col].mean(), 2)
    col4.metric("⭐ Avg CSAT Score", avg_csat)
else:
    col4.metric("⭐ Avg CSAT Score", "N/A")

# ✅ SLA FIX (from Response Time)
if "Response Time" in df.columns:
    sla = round((filtered_df["Response Time"].astype(str).str.contains("Within")).mean() * 100, 2)
    col5.metric("⏱ SLA Compliance (%)", f"{sla}%")
else:
    col5.metric("⏱ SLA Compliance (%)", "N/A")

# ------------------ DATA PREVIEW ------------------
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df)

# ------------------ VISUALS ------------------
st.subheader("📊 Calls by City")

if "City" in df.columns:
    city_counts = filtered_df["City"].value_counts()
    st.bar_chart(city_counts)

# ------------------ EXTRA INSIGHTS ------------------
st.subheader("🧠 Insights")

if csat_col:
    if avg_csat >= 7:
        st.success("✅ Customer satisfaction is good")
    else:
        st.warning("⚠️ Customer satisfaction needs improvement")

if "Response Time" in df.columns:
    if sla >= 80:
        st.success("✅ SLA performance is strong")
    else:
        st.error("❌ SLA performance is poor")

st.write("👉 Friday and weekday trends usually show higher call volume.")
