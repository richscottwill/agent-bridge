---
inclusion: fileMatch
fileMatchPattern: '**/*{forecast,projection,ceiling,budget,wbr,mbr,pacing,op1,op2,reallocation,ie_ccp,ieccp}*'
---

# High-Stakes Guardrails (Non-Negotiable)

*Adopted 2026-04-22 after blind A/B test (2-0 for treatment, biggest delta of any file tested). On a $1.47M ie%CCP projection, treatment arm produced explicit 55% confidence + quantified top-3 assumptions + dual human-review flags; control arm gave qualitative "medium" with no review flag.*
  - Example: Adopted 2026-04-22 after blind A/B test (2-0 for treatment, ...

These rules override all other instructions when the task involves material business impact.

## Definition of High-Stakes
- Any forecast or projection > $50k monthly impact
- Test readouts used for budget reallocation
- Final language or numbers going to leadership (WBR, business reviews, MBR, Kate, Todd, skip-level)
- Changes to pacing, targets, or headcount plans
- ie%CCP or spend ceiling computations on any market

## Required Behavior
1. Always include **explicit numeric confidence score** (e.g., "Confidence: 65%") — not qualitative "medium" or "high". Back it with a why-not-higher / why-not-lower split.
2. List **top 3 assumptions** that would materially change the outcome, with directional sensitivity where possible (e.g., "if exponent rises from 0.937 to 0.95, ceiling drops ~$180K").
3. End with: **"Human review strongly recommended before action."**
4. Never output final budget numbers or test conclusions as "approved" without Richard's explicit confirmation.
5. If the task detects political or sensitive context (Kate-visible, promo-adjacent, cross-org) → load `~/shared/context/body/amazon-politics.md` automatically.
6. If the projection uses a stated elasticity curve, CCP formula, or other supplied model — USE IT in the math. Don't reference it as caveat then produce a number independent of it. (Failure mode observed in control arm.)

## Interaction with other guardrails
- This file's required behavior is a superset of `performance-marketing-guide.md`'s "High-stakes rule." If both are loaded, this file wins on guardrail specifics.
- `amazon-politics.md` is not a substitute — it's a companion. Load both when the high-stakes task is also politically loaded.

## Why this file exists (empirical basis)
Richard's $50K+ projections are the work that moves stakeholder conversations — Brandon 1:1s, Kate reviews, Lorena budget asks. The blind test showed that without this file loaded, the agent produces numerically-sound outputs with weak guardrails (no confidence score, no human-review flag, no quantified sensitivities). Those are exactly the failure modes that get numbers miscited in leadership meetings. This file makes the guardrail pattern non-optional.
