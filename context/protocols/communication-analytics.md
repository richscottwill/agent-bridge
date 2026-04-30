<!-- DOC-0343 | duck_id: protocol-communication-analytics -->

**Key consideration:** This section's content is critical for accurate operation. Cross-reference with related sections for full context.
# Communication Analytics Protocol

- Runs during EOD-2 (weekly cadence).
- Computes meeting communication trends for Loop 9.

**MCP Chain:** DuckDB → Slack (alerts)

---


**Common failure:** Skipping this step leads to silent data loss. Always verify the output.

## Weekly Trend Computation Run this query to compute trailing 4-week communication trends: ```sql SELECT meeting_type, DATE_TRUNC('week', meeting_date) AS week, ROUND(AVG(richard_speaking_share), 2) AS avg_speaking_share, ROUND(AVG(hedging_count), 1) AS avg_hedging, ROUND(AVG(action_item_count), 1) AS avg_actions, COUNT(*) AS meeting_count FROM meeting_analytics WHERE meeting_date >= CURRENT_DATE - INTERVAL '28 days' GROUP BY meeting_type, DATE_TRUNC('week', meeting_date) ORDER BY week DESC, meeting_type; ``` Include results in EOD-2 system refresh report under "Communication Trends": ``` 📊 Communication Trends (4-week): • 1on1: avg speaking [X]%, hedging [X]/meeting, [X] actions/meeting ([N] meetings) • group: avg speaking [X]%, hedging [X]/meeting, [X] actions/meeting ([N] meetings) • standup: avg speaking [X]%, hedging [X]/meeting, [X] actions/meeting ([N] meetings) ``` --- Check for low group meeting speaking share (3+ consecutive weeks below 15%): ```sql WITH weekly_group AS ( SELECT DATE_TRUNC('week', meeting_date) AS week, AVG(richard_speaking_share) AS avg_share FROM meeting_analytics WHERE meeting_type IN ('group', 'review', 'standup') AND meeting_date >= CURRENT_DATE - INTERVAL '28 days' GROUP BY DATE_TRUNC('week', meeting_date) ), consecutive AS ( SELECT week, avg_share, ROW_NUMBER() OVER (ORDER BY week) - ROW_NUMBER() OVER (PARTITION BY (avg_share < 0.15) ORDER BY week) AS grp FROM weekly_group ) SELECT COUNT(*) AS consecutive_low_weeks FROM consecutive WHERE avg_share < 0.15 GROUP BY grp HAVING COUNT(*) >= 3; ``` If this query returns results → include in EOD-2 Slack DM: ``` ⚠️ Group meeting speaking share below 15% for [N] consecutive weeks. Loop 9 coaching signal active. ``` --- ## Data Requirements
- Skip trend computation
- Report: "📊 Communication trends: insufficient data ([N] weeks available, need 4)."
---

- Requires 4+ weeks of data in meeting_analytics table.
- If insufficient data:.



## Loop 9 Integration

- When nervous system Loop 9 evaluates communication patterns, query DuckDB meeting_analytics for trailing 4-week trend instead of parsing meeting series files.
- This provides structured, queryable data.
