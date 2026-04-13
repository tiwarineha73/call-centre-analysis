# Call Centre Performance Analytics

**Operational Analysis of 32,941 Customer Calls — SLA, Sentiment & Channel Efficiency**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green?logo=pandas)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## Project Overview

Call centres are a critical customer touchpoint — and also one of the most expensive to operate. When SLA compliance drops, sentiment turns negative, or call volume concentrates in one channel, it signals systemic problems that cost both money and customer loyalty.

This project analyses **32,941 call records** from October 2020 across 4 cities, 4 channels, and 3 contact reasons — delivering operational insights for call centre management and customer experience leadership.

---

## Business Problem Statement

> *"The operations team needs to understand why 24.7% of calls are breaching SLA, why over half of customers express negative sentiment, and how call volume is distributed across channels and cities — so leadership can make informed staffing, routing, and self-service investment decisions."*

---

## Objectives

- Measure SLA compliance across channels, cities, and contact reasons
- Analyse customer sentiment patterns and identify negative experience hotspots
- Assess CSAT score distribution and flag data collection gaps
- Understand call volume trends by day, channel, and geography
- Deliver actionable recommendations for operational improvement

---

## Dataset Description

| Attribute         | Detail                                               |
|-------------------|------------------------------------------------------|
| **Source**        | Call Centre Operations Dataset                      |
| **Records**       | 32,941 call records                                  |
| **Time Period**   | October 1–31, 2020                                   |
| **Features**      | 12 columns                                           |
| **CSAT Coverage** | 37.3% (12,271 of 32,941 calls have scores)          |
| **Format**        | CSV                                                  |

**Key Features:**

- `Call Timestamp` — date of call
- `Channel` — Call-Center, Chatbot, Email, Web
- `Reason` — Billing Question, Payments, Service Outage
- `Response Time` — Within SLA / Above SLA
- `Sentiment` — Very Negative → Very Positive (5 levels)
- `Csat Score` — 1–10 (where available)
- `Call Duration In Minutes` — length of each call
- `Call-Centres City` — Los Angeles, Baltimore, Chicago, Denver
- `State` — US state of the customer

---

## Tools & Technologies

| Category         | Tools Used                          |
|------------------|-------------------------------------|
| Language         | Python 3.10+                        |
| Data Processing  | Pandas, NumPy                       |
| Visualization    | Matplotlib, Seaborn                 |
| Dashboard        | Power BI                            |
| SQL Analysis     | MySQL / Standard SQL                |
| Version Control  | Git, GitHub                         |
| Environment      | Jupyter Notebook / VS Code          |

---

## Project Workflow

```
Raw CSV (32,941 records)
        │
        ▼
Data Cleaning & Feature Engineering
(date parsing, SLA flag, sentiment scoring, day-of-week)
        │
        ▼
Exploratory Data Analysis
(volume, SLA rates, sentiment, CSAT, geography)
        │
        ▼
Python Visualizations (9 charts)
        │
        ▼
SQL Business Queries (10 queries)
        │
        ▼
Power BI Dashboard
        │
        ▼
Insights & Recommendations
```

---

## Key Insights

| # | Finding | Severity |
|---|---------|----------|
| 1 | **SLA compliance: 75.26%** — at minimum threshold, no buffer | 🔴 Critical |
| 2 | **51.9% of calls are Negative or Very Negative** sentiment | 🔴 Critical |
| 3 | **71.2% of calls are billing-related** — self-service gap evident | 🔴 Critical |
| 4 | **CSAT data is 62.7% missing** — metric is unreliable for decisions | 🟡 High |
| 5 | **Los Angeles handles 41.7% of all calls** — Denver underutilised at 8.4% | 🟡 High |
| 6 | **Friday peaks at 5,570 calls** — 29.6% higher than Sunday | 🟡 Medium |
| 7 | All 4 channels perform identically on SLA (74.9–75.6%) — systemic issue | 🟡 High |

---

## Visualizations Generated

| File | Description |
|------|-------------|
| `01_calls_by_day.png` | Call volume by day of week |
| `02_calls_by_channel.png` | Channel distribution pie chart |
| `03_sla_by_channel.png` | SLA compliance rate by channel |
| `04_sentiment_distribution.png` | Customer sentiment breakdown |
| `05_calls_by_reason.png` | Call volume by contact reason |
| `06_csat_distribution.png` | CSAT score histogram |
| `07_calls_by_city.png` | Volume by call centre location |
| `08_sentiment_vs_sla_heatmap.png` | Sentiment vs SLA cross-analysis |
| `09_daily_call_trend.png` | Daily call volume trend line |

---

## Recommendations

1. **Fix Billing Self-Service Immediately**
   71.2% of calls are billing questions. A better FAQ, chatbot billing flow, or improved billing portal could deflect 30–40% of volume — freeing agents for complex issues.

2. **Address Systemic SLA Breach (Not Channel-Level)**
   All 4 channels hover at ~75% SLA. This is a workforce planning problem, not a routing problem. Increase headcount or extend operating hours.

3. **Redistribute Load from LA to Denver**
   Los Angeles handles 5× more calls than Denver. Load balancing via routing rules would reduce LA burnout and utilise Denver's spare capacity.

4. **Fix CSAT Data Collection**
   Only 37.3% of calls have a score. This makes CSAT meaningless as a KPI. Implement mandatory post-call scoring or trigger automated SMS surveys.

5. **Staff Up Thursday–Friday**
   Friday (5,570) and Thursday (5,481) are peak days. Scheduling optimisation with Thu–Fri heavy shifts would directly improve SLA on peak load days.

---

## Project Structure

```
call-centre-analytics/
│
├── data/
│   └── Call_Center_Data.csv             # Raw dataset (32,941 rows)
│
├── notebooks/
│   └── call_centre_analysis.py          # Full Python analysis script
│
├── src/
│   └── call_centre_queries.sql          # 10 business SQL queries
│
├── outputs/
│   ├── 01_calls_by_day.png
│   ├── 02_calls_by_channel.png
│   ├── 03_sla_by_channel.png
│   ├── 04_sentiment_distribution.png
│   ├── 05_calls_by_reason.png
│   ├── 06_csat_distribution.png
│   ├── 07_calls_by_city.png
│   ├── 08_sentiment_vs_sla_heatmap.png
│   └── 09_daily_call_trend.png
│
├── docs/
│   └── Call_Centre_Dashboard_PowerBI.pdf  # Power BI dashboard
│
├── README.md
└── requirements.txt
```

---

## How to Run

**Step 1 — Clone the repository**
```bash
git clone https://github.com/tiwarineha73/call-centre-analytics.git
cd call-centre-analytics
```

**Step 2 — Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Run the analysis**
```bash
cd notebooks
python call_centre_analysis.py
```

**Step 5 — View outputs**
All 9 charts will be saved to the `/outputs/` folder automatically.

---

## Author

**Neha Tiwari**
Data Analyst | Python • SQL • Power BI • Machine Learning

- GitHub: [github.com/tiwarineha73](https://github.com/tiwarineha73)
- LinkedIn: [linkedin.com/in/neha-tiwari](https://linkedin.com/in/neha-tiwari)
- Email: tiwari.neha3111@gmail.com

---

*This project is part of an end-to-end data analytics portfolio built on real datasets.*
