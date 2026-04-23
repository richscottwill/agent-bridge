# high_stakes_log DuckDB Table (Grok proposal)

Create a DuckDB table so the agent can query past flagged outputs and learn patterns.

Schema (proposed):
```sql
CREATE TABLE high_stakes_log (
    created_at TIMESTAMP,
    task_type VARCHAR,       -- projection / test_readout / wbr / pacing
    confidence_pct INTEGER,  -- 0-100
    human_review_flagged BOOLEAN,
    human_reviewed BOOLEAN,
    outcome VARCHAR,         -- hit / miss / pending
    output_ref VARCHAR,      -- path to artifact
    notes TEXT
);
```
