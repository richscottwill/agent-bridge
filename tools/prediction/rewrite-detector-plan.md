# detect_regime_changes.py — Graceful Rewrite Plan

**Context:** The current detector auto-inserts too many change_log entries as "regime changes," polluting `ps.regime_changes` with historical noise (transient promo notes, monthly bid strategy summaries, one-off incidents). The market_constraints view works around this with filters, but the root cause is the detector.

**This plan is for a future focused session.** It's scoped to not destabilize anything we've just built.

## Current behavior (approximate)

`detect_regime_changes.py` scans `change_log` for entries matching pattern keywords (OCI, LP, PAM, pause, launch, etc.) and auto-inserts them into `ps.regime_changes` with default impact estimates. It runs in the WBR pipeline.

**Problem:** pattern matching doesn't distinguish between:
- "Launched new promo page" (transient)
- "OCI 100% dial-up complete" (structural baseline)
- "Promo sitelink 404s for 2h" (noise)

All three get inserted with the same treatment.

## Rewrite phases

### Phase 1 — Stop the bleeding (15 min)

Add an allow-list filter on top of existing pattern matching:

```python
STRUCTURAL_TYPES = {'oci_launch', 'lp_switch', 'attribution_change', 'pause', 'campaign_restructure'}
IMPACT_TYPES = {'promo_launch', 'seasonal_event', 'bid_strategy'}

def should_insert(entry):
    classified_type = classify(entry)
    if classified_type not in STRUCTURAL_TYPES | IMPACT_TYPES:
        return False
    # For impact types, require non-zero expected impact
    if classified_type in IMPACT_TYPES and abs(entry.impact_pct) < 0.05:
        return False
    return True
```

This stops new noise from being inserted. Doesn't clean existing noise (that's manual and already done).

### Phase 2 — Classify on insert (30-45 min)

Auto-fill `is_structural_baseline`, `half_life_weeks`, `precedent_source` on insert:

```python
CLASSIFIER = {
    'oci_launch': {
        'is_structural_baseline': True,  # once 100% complete
        'half_life_weeks': None,
        'precedent_source': 'structural_persistent',
    },
    'lp_switch': {
        'is_structural_baseline': True,
        'half_life_weeks': None,
        'precedent_source': 'structural_persistent',
    },
    'promo_launch': {
        'is_structural_baseline': False,
        'half_life_weeks': 2,
        'precedent_source': 'none_novel',
    },
    'seasonal_event': {
        'is_structural_baseline': False,
        'half_life_weeks': 1,
        'precedent_source': 'yoy_same_event',  # if we have prior occurrence
    },
    'pause': {
        'is_structural_baseline': True,  # if extended pause
        'half_life_weeks': None,
        'precedent_source': 'structural_persistent',
    },
}
```

OCI dial-ups are tricky — 25% is impact, 100% is structural. Needs a "dial-up complete" detector that looks for "100%" in the description.

### Phase 3 — Historical cleanup (15 min)

Build a one-shot script that:
1. Reads every active row
2. Applies the Phase 2 classifier
3. Updates is_structural_baseline, half_life_weeks, precedent_source
4. Flags ambiguous rows for human review (outputs a diff)

Richard reviews diff, applies with a single SQL transaction.

### Phase 4 — Validation (30 min)

Add a test against the current curated state (what we have today after manual curation). Any change to the classifier that would reclassify a currently-curated row fails the test. Forces intentional updates.

## Out of scope (future / maybe never)

- NLP classification of description text
- Slack-to-regime auto-insertion (currently manual)
- Impact magnitude estimation from text (currently uses hardcoded defaults)

## Risk

The main risk is reclassifying existing rows incorrectly and losing context. Phase 3 mitigates this with the human-in-the-loop diff review. Don't skip that step.

## Success criteria

After rewrite:
- New change_log entries get classified correctly 90%+ of the time without review
- Richard never sees `is_structural_baseline=false` on an OCI 100% entry
- The market_constraints view no longer needs heuristic filters — it just reads the `is_structural_baseline` flag

## When to do this

Recommended: after 2-3 WBR cycles with the current state, so we have real evidence of what the current detector is doing and whether Phase 1 filters are sufficient.
