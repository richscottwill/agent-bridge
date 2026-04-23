# Creative Fatigue Scanner (Grok proposal)

Simple rule: flag ads with declining CTR over 14+ days. Protects performance.

Pattern:
- Pull ad-level CTR daily
- Flag any ad with CTR trend down ≥14 days
- Surface in daily brief under "Data Snapshot" or as a new alert
