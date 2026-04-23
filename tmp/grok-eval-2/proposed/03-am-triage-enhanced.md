# AM Triage Enhanced Hook (Post April 22 Update)

**Steps**:

1. Run `tools/excel_ingest.py` (if new files exist)
2. Run anomaly detection
3. Load latest `current.md`, `rw-tracker.md`, `eyes.md`
4. Generate brief using this exact structure:

   **Priorities** (max 5, tied to Five Levels)
   **Leverage Move** (one highest-impact action)
   **Friction to Remove** (one thing to simplify/automate)
   **Data Snapshot** (key numbers + anomalies from ingest + detector)
   **Open Questions for Richard**

5. Apply `high-stakes-guardrails.md` if any forecast/budget numbers appear
6. Post brief to Slack (rsw-channel) + save to `current.md`
