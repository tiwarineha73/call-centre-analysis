-- ============================================================================
-- Call Centre Performance Analytics — SQL Queries
-- Author: Neha Tiwari
-- Database: call_centre  |  Table: calls
-- Purpose: Business-driven operational queries for call centre management
-- ============================================================================


-- ── Q1: Headline KPI Summary ─────────────────────────────────────────────────
SELECT
    COUNT(*)                                                        AS total_calls,
    ROUND(SUM(call_duration_in_minutes) / 60.0, 2)                 AS total_duration_hrs,
    ROUND(AVG(call_duration_in_minutes), 2)                         AS avg_duration_min,
    ROUND(100.0 * SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS sla_compliance_pct,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat_score,
    COUNT(csat_score)                                               AS calls_with_csat
FROM calls;


-- ── Q2: Call Volume and SLA by Channel ───────────────────────────────────────
SELECT
    channel,
    COUNT(*)                                                        AS total_calls,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1)              AS pct_of_total,
    SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)  AS within_sla,
    ROUND(100.0 * SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS sla_rate_pct,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat
FROM calls
GROUP BY channel
ORDER BY total_calls DESC;


-- ── Q3: Sentiment Breakdown ───────────────────────────────────────────────────
SELECT
    sentiment,
    COUNT(*)                                                        AS call_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2)              AS pct_of_total,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat_score,
    ROUND(AVG(call_duration_in_minutes), 2)                         AS avg_duration_min
FROM calls
GROUP BY sentiment
ORDER BY
    CASE sentiment
        WHEN 'Very Negative' THEN 1
        WHEN 'Negative'      THEN 2
        WHEN 'Neutral'       THEN 3
        WHEN 'Positive'      THEN 4
        WHEN 'Very Positive' THEN 5
    END;


-- ── Q4: Contact Reason Analysis ───────────────────────────────────────────────
SELECT
    reason,
    COUNT(*)                                                        AS call_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2)              AS pct_of_total,
    ROUND(AVG(call_duration_in_minutes), 2)                         AS avg_duration_min,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat,
    ROUND(100.0 * SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS sla_rate_pct
FROM calls
GROUP BY reason
ORDER BY call_count DESC;


-- ── Q5: Call Centre City Performance ─────────────────────────────────────────
-- Which centres are handling the most volume and how do they perform?
SELECT
    call_centres_city,
    COUNT(*)                                                        AS total_calls,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1)              AS share_pct,
    ROUND(AVG(call_duration_in_minutes), 2)                         AS avg_duration_min,
    ROUND(100.0 * SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS sla_rate_pct,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat
FROM calls
GROUP BY call_centres_city
ORDER BY total_calls DESC;


-- ── Q6: Peak Day Analysis ─────────────────────────────────────────────────────
SELECT
    DAYNAME(call_timestamp)                                         AS day_of_week,
    COUNT(*)                                                        AS total_calls,
    ROUND(AVG(call_duration_in_minutes), 2)                         AS avg_duration_min,
    ROUND(100.0 * SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS sla_rate_pct
FROM calls
GROUP BY DAYNAME(call_timestamp), DAYOFWEEK(call_timestamp)
ORDER BY DAYOFWEEK(call_timestamp);


-- ── Q7: SLA Breach Analysis — Which segments breach most? ────────────────────
SELECT
    channel,
    reason,
    sentiment,
    COUNT(*)                                                        AS breach_count,
    ROUND(AVG(call_duration_in_minutes), 2)                         AS avg_duration_min
FROM calls
WHERE response_time = 'Above SLA'
GROUP BY channel, reason, sentiment
ORDER BY breach_count DESC
LIMIT 15;


-- ── Q8: Top 10 States by Call Volume ─────────────────────────────────────────
SELECT
    state,
    COUNT(*)                                                        AS total_calls,
    ROUND(100.0 * SUM(CASE WHEN response_time = 'Within SLA' THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS sla_rate_pct,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat
FROM calls
GROUP BY state
ORDER BY total_calls DESC
LIMIT 10;


-- ── Q9: CSAT Score Buckets ────────────────────────────────────────────────────
-- How are satisfaction scores distributed across bands?
SELECT
    CASE
        WHEN csat_score BETWEEN 1 AND 3  THEN '1–3 (Poor)'
        WHEN csat_score BETWEEN 4 AND 6  THEN '4–6 (Average)'
        WHEN csat_score BETWEEN 7 AND 8  THEN '7–8 (Good)'
        WHEN csat_score BETWEEN 9 AND 10 THEN '9–10 (Excellent)'
    END                                                             AS csat_band,
    COUNT(*)                                                        AS call_count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2)              AS pct_of_scored_calls
FROM calls
WHERE csat_score IS NOT NULL
GROUP BY csat_band
ORDER BY MIN(csat_score);


-- ── Q10: Negative Sentiment Hotspots ─────────────────────────────────────────
-- Find call centre + channel combos with worst sentiment to prioritise fixes
SELECT
    call_centres_city,
    channel,
    COUNT(*)                                                        AS total_calls,
    SUM(CASE WHEN sentiment IN ('Negative','Very Negative') THEN 1 ELSE 0 END)
                                                                    AS negative_calls,
    ROUND(100.0 * SUM(CASE WHEN sentiment IN ('Negative','Very Negative') THEN 1 ELSE 0 END)
          / COUNT(*), 2)                                            AS negative_rate_pct,
    ROUND(AVG(csat_score), 2)                                       AS avg_csat
FROM calls
GROUP BY call_centres_city, channel
ORDER BY negative_rate_pct DESC;
