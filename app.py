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
st.title("📊 Call Centre Analytics Dashboard")
st.write("App is running successfully🚀")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")

OUTPUT_DIR = "../outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["font.family"] = "DejaVu Sans"

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────
df = pd.read_csv("Call_Center_Data.csv")
st.write (f"Dataset loaded:{df.shape[0]}rows x {df.shape[1]}columns")
st.subheader("Dataset Preview")
st.subheader("📊 Key Metrics")


st.subheader("Filtered Data")
st.dataframe(filtered_df)
st.sidebar.header("🔍 Filters")
st.subheader("📈 Calls by City")

city_counts = filtered_df["City"].value_counts()

st.bar_chart(city_counts)

city = st.sidebar.selectbox("Select City", df["City"].unique())
channel = st.sidebar.selectbox("Select Channel", df["Channel"].unique())

filtered_df = df[(df["City"] == city) & (df["Channel"] == channel)]
col1, col2, col3 = st.columns(3)

col1.metric("Total Calls", len(filtered_df))
col2.metric("Unique Cities", filtered_df["City"].nunique())
col3.metric("Channels", filtered_df["Channel"].nunique())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: DATA CLEANING & FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────

# 3.1 Parse date column
df["Call Timestamp"] = pd.to_datetime(df["Call Timestamp"], dayfirst=True)
df["DayOfWeek"]      = df["Call Timestamp"].dt.day_name()
df["WeekNumber"]     = df["Call Timestamp"].dt.isocalendar().week.astype(int)
df["Date"]           = df["Call Timestamp"].dt.date

# 3.2 Check duplicates
dupes = df.duplicated(subset="Id").sum()
print(f"Duplicate IDs: {dupes}")

# 3.3 Missing values
missing = df.isnull().sum()
print(f"\nMissing values:\n{missing[missing > 0]}")
# Csat Score: 20,670 nulls (~62.7%) — these are calls where score wasn't collected.
# We keep them for volume analysis but exclude from CSAT calculations.

# 3.4 Binary SLA flag
df["SLA_Met"] = (df["Response Time"] == "Within SLA").astype(int)

# 3.5 Sentiment score mapping (for trend analysis)
sentiment_map = {
    "Very Negative": 1,
    "Negative":      2,
    "Neutral":       3,
    "Positive":      4,
    "Very Positive": 5,
}
df["SentimentScore"] = df["Sentiment"].map(sentiment_map)

# 3.6 Ordered categories
day_order       = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
sentiment_order = ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]

print("\n✅ Data cleaning complete.")
print(f"Date range: {df['Call Timestamp'].min().date()} → {df['Call Timestamp'].max().date()}")
print(f"Final shape: {df.shape}")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: EDA — KEY METRICS
# ─────────────────────────────────────────────────────────────────────────────

total_calls     = len(df)
total_hrs       = df["Call Duration In Minutes"].sum() / 60
avg_duration    = df["Call Duration In Minutes"].mean()
sla_rate        = df["SLA_Met"].mean() * 100
avg_csat        = df["Csat Score"].mean()
csat_coverage   = df["Csat Score"].notna().mean() * 100

print(f"""
── HEADLINE KPIs ──────────────────────────────────
  Total Calls          : {total_calls:,}
  Total Duration (hrs) : {total_hrs:,.2f}
  Avg Call Duration    : {avg_duration:.2f} min
  SLA Compliance Rate  : {sla_rate:.2f}%
  Avg CSAT Score       : {avg_csat:.2f} / 10
  CSAT Coverage        : {csat_coverage:.1f}% of calls scored
───────────────────────────────────────────────────
""")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────────────────

# ── Chart 1: Call Volume by Day of Week ──────────────────────────────────────
day_counts = (
    df["DayOfWeek"]
    .value_counts()
    .reindex(day_order)
)
fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#2196F3" if d not in ["Saturday", "Sunday"] else "#90CAF9" for d in day_order]
bars = ax.bar(day_counts.index, day_counts.values, color=colors, edgecolor="white", width=0.6)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 40,
        f"{bar.get_height():,}",
        ha="center", fontsize=10, fontweight="bold"
    )
ax.set_title("Call Volume by Day of Week — October 2020",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Day of Week", fontsize=11)
ax.set_ylabel("Number of Calls", fontsize=11)
ax.set_ylim(0, 6500)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_calls_by_day.png")
plt.close()
print("Chart 1 saved.")

# ── Chart 2: Call Volume by Channel ──────────────────────────────────────────
channel_counts = df["Channel"].value_counts()
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#1565C0", "#1976D2", "#42A5F5", "#90CAF9"]
wedges, texts, autotexts = ax.pie(
    channel_counts.values,
    labels=channel_counts.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=140,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")
ax.set_title("Call Distribution by Channel",
             fontsize=14, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_calls_by_channel.png")
plt.close()
print("Chart 2 saved.")

# ── Chart 3: SLA Compliance by Channel ──────────────────────────────────────
sla_channel = (
    df.groupby("Channel")["SLA_Met"]
    .mean()
    .mul(100)
    .round(1)
    .reset_index()
    .rename(columns={"SLA_Met": "SLA_Rate_%"})
    .sort_values("SLA_Rate_%", ascending=True)
)
fig, ax = plt.subplots(figsize=(8, 5))
palette = sns.color_palette("Blues_d", len(sla_channel))
bars = ax.barh(sla_channel["Channel"], sla_channel["SLA_Rate_%"],
               color=palette, edgecolor="white")
ax.axvline(x=75, color="#E53935", linestyle="--", linewidth=1.5, label="75% target line")
for bar in bars:
    ax.text(
        bar.get_width() - 3,
        bar.get_y() + bar.get_height() / 2,
        f"{bar.get_width():.1f}%",
        va="center", fontsize=11, fontweight="bold", color="white"
    )
ax.set_title("SLA Compliance Rate by Channel",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("SLA Compliance (%)", fontsize=11)
ax.set_xlim(0, 90)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_sla_by_channel.png")
plt.close()
print("Chart 3 saved.")

# ── Chart 4: Sentiment Distribution ─────────────────────────────────────────
sentiment_counts = df["Sentiment"].value_counts().reindex(sentiment_order)
fig, ax = plt.subplots(figsize=(9, 5))
colors = ["#B71C1C", "#E53935", "#FDD835", "#43A047", "#1B5E20"]
bars = ax.bar(sentiment_counts.index, sentiment_counts.values,
              color=colors, edgecolor="white", width=0.6)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 80,
        f"{bar.get_height():,}",
        ha="center", fontsize=10, fontweight="bold"
    )
ax.set_title("Customer Sentiment Distribution",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Sentiment Category", fontsize=11)
ax.set_ylabel("Number of Calls", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_sentiment_distribution.png")
plt.close()
print("Chart 4 saved.")

# ── Chart 5: Call Volume by Reason ──────────────────────────────────────────
reason_counts = df["Reason"].value_counts()
fig, ax = plt.subplots(figsize=(7, 5))
colors = ["#1565C0", "#42A5F5", "#90CAF9"]
bars = ax.bar(reason_counts.index, reason_counts.values,
              color=colors, edgecolor="white", width=0.5)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 100,
        f"{bar.get_height():,}",
        ha="center", fontsize=11, fontweight="bold"
    )
ax.set_title("Call Volume by Contact Reason",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Reason", fontsize=11)
ax.set_ylabel("Number of Calls", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_calls_by_reason.png")
plt.close()
print("Chart 5 saved.")

# ── Chart 6: CSAT Score Distribution ────────────────────────────────────────
csat_data = df["Csat Score"].dropna()
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(csat_data, bins=10, range=(1, 11), color="#1976D2",
        edgecolor="white", linewidth=1.2, rwidth=0.85)
ax.axvline(x=csat_data.mean(), color="#E53935", linestyle="--",
           linewidth=2, label=f"Mean CSAT: {csat_data.mean():.2f}")
ax.set_title("CSAT Score Distribution (Scored Calls Only)",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("CSAT Score (1–10)", fontsize=11)
ax.set_ylabel("Number of Calls", fontsize=11)
ax.legend(fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_csat_distribution.png")
plt.close()
print("Chart 6 saved.")

# ── Chart 7: Call Volume by Call Centre City ─────────────────────────────────
city_counts = df["Call-Centres City"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
palette = sns.color_palette("Blues_d", len(city_counts))
bars = ax.bar(city_counts.index, city_counts.values,
              color=palette, edgecolor="white", width=0.5)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 100,
        f"{bar.get_height():,}",
        ha="center", fontsize=11, fontweight="bold"
    )
ax.set_title("Call Volume by Call Centre Location",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Call Centre City", fontsize=11)
ax.set_ylabel("Number of Calls", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_calls_by_city.png")
plt.close()
print("Chart 7 saved.")

# ── Chart 8: Sentiment vs SLA — Heatmap ─────────────────────────────────────
pivot = pd.crosstab(
    df["Sentiment"].reindex(df.index),
    df["Response Time"]
)
pivot = pivot.reindex(sentiment_order)
pivot_pct = pivot.div(pivot.sum(axis=1), axis=0).mul(100).round(1)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    pivot_pct,
    annot=True,
    fmt=".1f",
    cmap="RdYlGn",
    ax=ax,
    linewidths=0.5,
    cbar_kws={"label": "% of calls in sentiment category"},
)
ax.set_title("Sentiment vs SLA Response Time (%)",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Response Time", fontsize=11)
ax.set_ylabel("Customer Sentiment", fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_sentiment_vs_sla_heatmap.png")
plt.close()
print("Chart 8 saved.")

# ── Chart 9: Weekly Call Volume Trend ───────────────────────────────────────
weekly = df.groupby("Date").size().reset_index(name="Calls")
weekly["Date"] = pd.to_datetime(weekly["Date"])
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(weekly["Date"], weekly["Calls"], color="#1565C0",
        linewidth=2, marker="o", markersize=4)
ax.fill_between(weekly["Date"], weekly["Calls"],
                alpha=0.15, color="#1565C0")
ax.set_title("Daily Call Volume Trend — October 2020",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Number of Calls", fontsize=11)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/09_daily_call_trend.png")
plt.close()
print("Chart 9 saved.")

print("\n✅ All 9 charts saved to /outputs/")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: KEY INSIGHTS SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("""
═══════════════════════════════════════════════════════════════
                     KEY BUSINESS INSIGHTS
═══════════════════════════════════════════════════════════════

1. SCALE: 32,941 calls handled in October 2020 across 4 cities,
   4 channels, totalling 13,742 hours of call time.

2. SLA COMPLIANCE AT RISK:
   - Overall SLA rate: 75.26% — just at the minimum threshold.
   - All channels are between 74.9%–75.6% — no channel is
     clearly outperforming. This suggests a systemic capacity
     issue, not a channel-specific one.

3. NEGATIVE SENTIMENT DOMINATES:
   - 51.9% of calls are Negative or Very Negative combined.
   - Only 21.6% are Positive or Very Positive.
   - This is a serious customer experience red flag.

4. BILLING QUESTIONS OVERWHELM THE SYSTEM:
   - 71.2% of all calls (23,462) are billing-related.
   - This volume suggests poor self-service options — customers
     can't resolve billing issues without calling in.

5. CSAT DATA IS UNRELIABLE:
   - Only 37.3% of calls have a CSAT score (12,271 of 32,941).
   - Mean CSAT of 5.55/10 is mediocre, but the 62.7% missing
     rate means this metric cannot be trusted for decisions.

6. LOS ANGELES HANDLES 41.7% OF ALL CALLS:
   - LA: 13,734 | Baltimore: 11,012 | Chicago: 5,419 | Denver: 2,776
   - Workload is heavily skewed — Denver is significantly underutilised.

7. FRIDAY IS THE PEAK DAY:
   - Friday: 5,570 calls vs Sunday: 4,296 (lowest).
   - Staffing should be weighted toward Thu–Fri.

═══════════════════════════════════════════════════════════════
""")
