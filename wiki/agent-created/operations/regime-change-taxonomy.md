# Regime Change Taxonomy

**Purpose:** When something changes in a market, decide how to record it in `ps.regime_changes`.

## Three categories

Every regime change falls into exactly one of these:

### 1. Structural baseline
Infrastructure, LP, attribution model, or campaign architecture that **defines the current operating state**. Persists until replaced.

- **Examples:** OCI launch (100% complete), Polaris LP migration, attribution model change, major campaign restructure, PAM paused indefinitely.
- **Fields:** `is_structural_baseline = true`, `half_life_weeks = NULL`, `precedent_source = 'structural_persistent'`, `end_date = NULL` (unless replaced).
- **When to add:** When the underlying infrastructure changes. "AU is now on Polaris LP" — that's a baseline.
- **When to retire:** Set `end_date` on the old baseline when a new one replaces it. Don't deactivate — the history matters.

### 2. Active impact regime
A time-bound event that **currently modifies forecasts**. Has a numeric impact and a decay curve.

- **Examples:** Promo launch causing CPC spike, Semana Santa (during the window), OCI dial-up in progress (before it's complete), one-off pause.
- **Fields:** `is_structural_baseline = false`, `expected_impact_pct` set, `half_life_weeks` set, `precedent_source` set, `end_date` set if known.
- **When to add:** When the event starts and is expected to affect actuals.
- **When it exits:** When `end_date` passes OR impact decays below 5% — becomes "recent past" automatically via the view.

### 3. Historical noise (filter out)
One-off change_log entries that don't define state and don't modify forecasts.

- **Examples:** "PBDD promo sitelink launched without weblab, caused 404 errors for 2h", "New MCS promo page launched", monthly bid strategy summary notes.
- **Action:** If `detect_regime_changes.py` auto-inserted it, set `active = false`. Don't delete — preserves the log.

## Decay model

**The hard part.** Impact doesn't disappear at `end_date` — it decays. Two signals determine how fast:

### `half_life_weeks`

Weeks until impact reaches 50% of original. Guides the Bayesian projector's prior weighting.

| Event type | Typical half_life_weeks |
|---|---|
| Novel promo, first-time event | 1-2 |
| One-off pause or outage | 1 |
| Recurring seasonal (Semana Santa) | 1 (binary — in window or out) |
| OCI dial-up in transition | 4-8 |
| Attribution-level impact | 8-12 |
| Structural baseline | NULL (no decay) |

### `precedent_source`

How confident we are about the impact estimate.

| Value | Meaning | CI implication |
|---|---|---|
| `structural_persistent` | Baseline infrastructure — no CI needed, persistent | N/A |
| `yoy_same_event` | Same event happened last year at same time (Semana Santa, Prime Day) | Narrow CI based on prior occurrence |
| `yoy_analog` | Similar event, different market or different week | Moderate CI |
| `none_novel` | First time seeing this — guessing from theory | Wide CI, short half-life default |

**Why precedent matters:** A recurring event we've seen three times has a much tighter expected range than a novel campaign. The projector should weight these differently. `precedent_source` makes that explicit.

### What this means for callouts

When writing a callout, the three categories map to different narrative moves:

- **Structural baselines** — the "what setup are we working with" context. Usually implicit in the narrative (readers know AU is on Polaris now).
- **Active impact regimes** — called out explicitly in the "what changed" section. Decay info tells you whether to expect continued impact.
- **Recent past** — useful for YoY framing ("Semana Santa W14 suppressed MX by 35%, so W15 recovery is partially a base effect").

## Adding a new regime change

```sql
INSERT INTO ps.regime_changes (
    id, market, change_date, change_type, metric_affected,
    expected_impact_pct, confidence, description, source,
    is_structural_baseline, half_life_weeks, precedent_source,
    end_date, active
) VALUES (
    gen_random_uuid()::VARCHAR, 'MX', '2026-04-20', 'promo_launch', 'registrations',
    0.10, 0.5, 'Prime Day MX kickoff promo', 'manual-agent',
    false, 2, 'yoy_analog',
    '2026-05-05', true
);
```

Then run the regenerator to propagate to the steering file:

```bash
python3 ~/shared/tools/prediction/regenerate_market_constraints.py
```

## Retiring a baseline

When a new baseline replaces an old one (e.g., MX moves off Polaris INTL to something new):

```sql
-- Old baseline gets an end_date (stays active=true for historical context)
UPDATE ps.regime_changes 
SET end_date = CURRENT_DATE
WHERE id = '<old-baseline-uuid>' AND is_structural_baseline = true;

-- Insert the new baseline
INSERT INTO ps.regime_changes (...) VALUES (..., is_structural_baseline = true, ...);
```

The view will only surface the current baseline (no `end_date` or `end_date >= CURRENT_DATE`) — the retired one becomes part of history but stops appearing in agent context.
