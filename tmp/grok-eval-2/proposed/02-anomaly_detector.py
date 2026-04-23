# tools/anomaly_detector.py
def detect_anomalies(days_back=7):
    query = f"""
    SELECT metric, value, date,
           LAG(value) OVER (PARTITION BY metric ORDER BY date) as prev_value
    FROM ps
    WHERE date >= CURRENT_DATE - {days_back}
    """
    # Agent should run this and flag anything with >25% day-over-day change
    # Then append to daily output under "Data Snapshot"
    return "Run DuckDB query above and flag anomalies >25% change"
