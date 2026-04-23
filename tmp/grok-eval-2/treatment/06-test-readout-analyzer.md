# Treatment: Test Readout Analyzer — MX Polaris Gen4 Ad Copy Test (W16 close)

*Steering active: `performance-marketing-guide.md` (manual) + simulated invocation of the proposed Test Readout Analyzer tool (`shared/tmp/grok-eval-2/proposed/06-test-readout-analyzer.md`).*

This treatment does two things:
1. Simulates invoking the Test Readout Analyzer tool — what gets handed in, what comes back.
2. Integrates that structured output into the final readout Richard would actually use.

---

## Part 1 — Simulated Tool Invocation

### What the agent hands the tool

```json
{
  "test_id": "MX-PS-AdCopy-Polaris-Gen4-W13-W16",
  "market": "MX",
  "channel": "Paid Search",
  "test_type": "ad_copy_ab",
  "design": {
    "hypothesis": "Gen4 copy emphasizing 'Business Pricing Exclusive' lifts CVR vs Gen3 control",
    "split": "50/50",
    "window_weeks": ["W13", "W14", "W15", "W16"],
    "mde_pct": 5,
    "power": 0.80,
    "alpha": 0.05,
    "primary_metric": "registrations",
    "secondary_metrics": ["CVR", "CPA"]
  },
  "arms": {
    "control_gen3": {
      "regs": 548,
      "spend_usd": 24600,
      "cvr": 0.036,
      "cpa_usd": 45
    },
    "treatment_gen4": {
      "regs": 612,
      "spend_usd": 24800,
      "cvr": 0.041,
      "cpa_usd": 40
    }
  },
  "qualitative_flags": [
    {
      "source": "Yun-Kang",
      "week": "W15",
      "flag": "creative fatigue concern on Gen4"
    }
  ],
  "data_gaps": [
    "weekly CTR by arm not provided",
    "weekly CVR by arm not provided",
    "impression share / auction pressure by week not provided"
  ]
}
```

### What the tool returns (structured)

```json
{
  "incrementality": {
    "regs_lift_pct": 11.7,
    "cvr_lift_pct": 13.9,
    "cpa_delta_pct": -9.7,
    "implied_clicks_control": 15222,
    "implied_clicks_treatment": 14927,
    "z_stat_cvr": 2.25,
    "p_value_cvr_two_sided": 0.024,
    "significant_at_95": true,
    "observed_effect_vs_mde": "observed ~12% regs lift is >2x the 5% MDE the test was powered for",
    "counterfactual_note": "Pure 50/50 concurrent split — no cutover counterfactual needed. Incrementality read is direct."
  },
  "confidence": {
    "sign": "high — p=0.024, z=2.25, effect direction consistent on regs, CVR, and CPA",
    "magnitude": "medium — point estimate ~12% regs lift, but 95% CI on CVR lift spans roughly +2% to +26%; true effect could be meaningfully smaller than headline",
    "generalizability": "medium-low — single market (MX), single product angle ('Business Pricing Exclusive'), 4-week window; MX has unique seasonality and CPC dynamics that may not port to US/EU5/JP/CA",
    "overall_numeric": 0.70,
    "overall_qualitative": "Result is real. Size of the real effect is less certain than the headline suggests."
  },
  "recommended_action": {
    "decision": "SCALE (with guardrails)",
    "preconditions": [
      "Promote Gen4 to 100% in MX starting W17",
      "Hold a 10% Gen3 holdout for 2 weeks to confirm lift persists post-ramp",
      "Instrument weekly CTR/CVR/CPA-by-week pull so fatigue can be detected early",
      "Do NOT generalize to US/EU5/JP/CA without a market-specific retest — 'Business Pricing Exclusive' messaging legality and resonance varies by market"
    ],
    "retest_trigger": "If 10% holdout shows <5% lift over 2 weeks post-ramp, revert and investigate fatigue hypothesis."
  },
  "creative_fatigue_signal": {
    "status": "UNRESOLVED — cannot rule in or rule out with data provided",
    "evidence_required": "Week-over-week CTR and CVR by arm (W13, W14, W15, W16). Fatigue would show as declining CTR and/or CVR on Gen4 across the window with Gen3 flat or rising.",
    "what_was_provided": "Only aggregate 4-week totals. Aggregates can mask a W13-W14 spike followed by W15-W16 decay — which is exactly the fatigue pattern Yun-Kang raised.",
    "interpretation_risk": "If fatigue is real and we scale on the aggregate, we are scaling a decaying asset. The aggregate lift would overstate the go-forward lift.",
    "required_next_step": "Pull weekly CTR/CVR/CPA-by-arm before scaling. This is a blocker, not a nice-to-have."
  },
  "five_levels_tie": "L2 evidence (WW Testing methodology). The readout itself — structured, quantified, with a fatigue check — is also the artifact L1 needs.",
  "human_review_flag": true,
  "human_review_reason": "Spend on scale decision is ~$100K/month at MX Polaris run-rate; exceeds the $50K high-stakes threshold in soul.md principle #7."
}
```

---

## Part 2 — Integrated Readout for Richard

### MX Polaris Gen4 Ad Copy Test — W13–W16 Readout

**TL;DR:** Gen4 won on the headline (regs +11.7%, CVR +13.9%, CPA −$5) and the result is statistically significant (p=0.024). But Yun-Kang's W3 fatigue flag is unresolved in the data we have, and we don't have weekly trend by arm. Recommend **scale with a 10% Gen3 holdout for 2 weeks + pull the weekly-by-arm trend before full ramp.** Don't generalize to other markets yet.

---

**Context**
- Test: MX Polaris Gen4 vs Gen3 ad copy, 50/50 split, W13–W16.
- Design: powered to detect ≥5% incrementality at 80% power.
- Observed: ~12% regs lift — more than 2x the MDE.

**What moved**

| Metric | Gen3 control | Gen4 treatment | Delta |
|---|---|---|---|
| Regs | 548 | 612 | +11.7% |
| Spend | $24.6K | $24.8K | ~flat |
| CVR | 3.6% | 4.1% | +13.9% rel (+0.5pp abs) |
| CPA | $45 | $40 | −$5 (−9.7%) |

Two-proportion z-test on CVR: z=2.25, p=0.024. Significant at 95%.

**Why (as best we can tell)**
"Business Pricing Exclusive" framing likely clarifies the value prop at the moment of click intent. MX Polaris traffic skews toward SMB buyers who are price-sensitive and need the "business-only" signal to feel qualified. Consistent with the Gen3→Gen4 hypothesis.

**Confidence (per performance-marketing-guide.md)**
- **Sign:** High. Effect direction consistent across regs, CVR, CPA. p=0.024.
- **Magnitude:** Medium. Point estimate is ~12% regs lift, but the 95% CI on CVR lift is wide (~+2% to +26%). True lift could be at the low end of that range.
- **Generalizability:** Medium-low. Single market, single product, 4 weeks. Don't assume it ports to US/EU5/JP/CA — "Business Pricing Exclusive" legality, translation, and resonance are not constants.
- **Overall numeric confidence: 0.70.**

**Risks & unresolved items**

1. **Creative fatigue (Yun-Kang's W3 flag) is unresolved.** The aggregate 4-week numbers can hide a W13-W14 spike followed by W15-W16 decay — which is the exact fatigue pattern. We need weekly CTR/CVR-by-arm before we scale. Scaling a decaying asset on aggregate data is the failure mode here.
2. **CI is wide.** Significant ≠ large. If the true lift is closer to +2%, this is still a win but a much smaller one than the headline.
3. **Impression share / auction pressure by week** not provided. If Gen4 traffic shifted composition mid-test, the lift may be partly selection.

**Recommendation (with confidence + human review flag)**

**Scale Gen4 to 100% in MX — with guardrails.** (Confidence: 0.70)

Guardrails:
1. Hold a 10% Gen3 holdout for 2 weeks post-ramp to confirm the lift persists. If <5% lift in holdout, revert and investigate fatigue.
2. Pull weekly CTR/CVR/CPA-by-arm for W13–W16 **before** full ramp — this retroactively resolves the Yun-Kang fatigue flag and is a blocker, not a nice-to-have.
3. Do **not** port Gen4 copy to US/EU5/JP/CA without a market-specific retest. Flag to the WW team as "MX result — retest candidate, not a direct lift."
4. Add a weekly-trend panel to the test scorecard so the next creative test can read fatigue in-flight, not retroactively.

**🚩 Human review flag: YES.** Run-rate at scale is ~$100K/month on MX Polaris, which exceeds the $50K high-stakes threshold. Confirm scale decision with Brandon before W17 ramp.

**Tough-but-fair questions you might get**
- *"Did you confirm the W3 fatigue signal is a false alarm or are you scaling on aggregates that hide it?"* → Honest answer: we don't have the weekly-by-arm data yet. Pulling it before ramp.
- *"Why are you confident this is causal and not a composition shift?"* → 50/50 concurrent split, same audience, same placements; that controls for most composition risk. Impression-share-by-week would fully close this.
- *"Are you recommending this for US too?"* → No. Single-market, single-product read. US is a retest candidate, not a scale candidate.

**Five Levels tie**
L2 evidence (WW Testing). Structured readout with quantified confidence + fatigue check is itself the L1 weekly artifact.

---

## Principle check (from soul.md §"How I Build")

- **#2 Structural over cosmetic:** The tool forces a 4-part structure (incrementality / confidence / next action / fatigue) every time — structural.
- **#3 Subtraction before addition:** Tool replaces the ad-hoc "let me think about this test" pattern with one standardized flow. Net subtraction of cognitive overhead.
- **#7 Human-in-the-loop on high-stakes:** Tool sets `human_review_flag=true` automatically when scale-decision spend exceeds $50K/month. Working as intended.
- **#8 Check device.md before proposing tools:** Test readouts happen weekly across 6+ markets. Recurring friction, 3+ instances/week, clear teammate adoption path (Yun-Kang, Bella, the broader WW team). Passes the device.md bar.

## What would make this tool v2

- Accept weekly-by-arm data as a required input, not optional. The MX Gen4 gap wasn't a tool gap — it was an input-discipline gap. Make the tool reject submissions without weekly rows.
- Auto-compute 95% CI on CVR lift, not just point estimate.
- Auto-flag generalizability downgrades when `arms.market` is single-market.
- Auto-pull `ps.v_weekly` from DuckDB for the market + window so the analyst doesn't have to hand-enter aggregates.
