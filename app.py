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
# CUSTOM CSS (UI IMPROVEMENT)
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
            box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
            text-align: center;
        }
        .title {
            font-size: 28px;
            font-weight: 700;
            color: #1f2937;
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

st.caption(f"📂 Dataset: {df.shape[0]} rows × {df.shape[1]} columns")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

city = st.sidebar.selectbox("Select City", df["City"].unique())
channel = st.sidebar.selectbox("Select Channel", df["Channel"].unique())

# -------------------------------
# FILTERED DATA
# -------------------------------
filtered_df = df[(df["City"] == city) & (df["Channel"] == channel)]

# -------------------------------
# METRICS (CARDS STYLE)
# -------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total Calls</h3>
            <h2>{len(filtered_df)}</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Unique Cities</h3>
            <h2>{filtered_df['City'].nunique()}</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Channels</h3>
            <h2>{filtered_df['Channel'].nunique()}</h2>
        </div>
    """, unsafe_allow_html=True)

# -------------------------------
# CHARTS SECTION
# -------------------------------
st.subheader("📈 Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Calls by City")
    city_counts = filtered_df["City"].value_counts()
    st.bar_chart(city_counts)

with col2:
    st.markdown("### Calls by Channel")
    channel_counts = filtered_df["Channel"].value_counts()
    st.bar_chart(channel_counts)

# -------------------------------
# DATA TABLE
# -------------------------------
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered_df, use_container_width=True)
