---
title: "Blind Eval A: Workstreams 3, 4, 5 (v4)"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0499 | duck_id: wiki-review-ws3-ws4-ws5-v4-eval-a -->

# Blind Eval A: Workstreams 3, 4, 5 (v4)

Reviewer: wiki-critic | Date: 2026-04-05 | Appendix excluded from Economy scoring per instructions.

## Summary Table

| Dimension | WS3: Audiences | WS4: UX | WS5: Algorithmic Ads |
|-----------|---------------|---------|---------------------|
| Usefulness | 8 | 9 | 8 |
| Clarity | 9 | 9 | 8 |
| Accuracy | 8 | 8 | 8 |
| Dual-audience | 9 | 9 | 9 |
| Economy | 8 | 8 | 7 |
| **Average** | **8.4** | **8.6** | **8.0** |
| **Verdict** | **PUBLISH** | **PUBLISH** | **REVISE** |

---

## WS3: Audiences and Lifecycle — 8.4 — PUBLISH

Unchanged from v3 in substance. The three-phase narrative (suppress → expand match rate → build Engagement channel) remains clean. The "What did we learn" section from v3 has been folded into the Phase 3 closing sentence — tighter. Purpose statement in paragraph one does exactly what the Amazon template asks.

No dimension below 7. No economy violations. Ships.

**Suggestions (non-blocking):** Specify "$765K iOPS in CY2025" or "FY2025" for precision. Carried forward from v3 — still not blocking.

---

## WS4: User Experience — 8.6 — PUBLISH

Both v3 issues are fixed.

The Polaris section now keeps only impact data in the main body ("Early MCS Flash data shows +235 bps improvement in CTR...") and cites Appendix C for rollout logistics. AEM translations, Brandon's priority order, and per-market details live in the appendix where they belong. The main body Polaris paragraph is four sentences of narrative argument — tight.

The catch-all sentence is gone. Current customer redirects and email overlay weblabs each get their own sentence with stated impact ("eliminate wasted spend on existing customers across all markets" / "capture emails earlier in the funnel, reducing drop-off at registration start page"). The 2026 portfolio paragraph is still dense — five initiatives in one paragraph after Baloo's two paragraphs — but each initiative now earns its sentence with a verb and an expected outcome. That's adequate economy, not padding.

Economy moves from 7 to 8. No dimension below 7. Ships.

---

## WS5: Algorithmic Ads — 8.0 — REVISE

Two of three v3 issues are fixed. The BSE paragraph is trimmed — no more double-mention of Raven Smith or double-stated video CPC. Appendix C is now AI Max test parameters instead of the redundant Prime Day one-liner. The "Richard should confirm" internal note is gone, replaced with forward-looking language about the planned Q2 2026 test. Accuracy moves from 7 to 8.

The new problem is a verbatim duplication that wasn't in v3 (or was masked by the other issues). Economy stays at 7 because of it, and one dimension below 7 blocks PUBLISH.

**Economy (7):** The opening sentence of "What are the risks and open questions?" is word-for-word identical to the opening sentence of "How is the team managing AI Max risk?":

> "The team is developing the AI Max test design for a planned US test in Q2 2026, following the same measurement discipline used for OCI — clear baselines, phased rollout, incrementality benchmarks."

This sentence appears verbatim in both sections. The risks section then restates the cannibalization and budget inflation concerns already explained in the guardrails section, and re-mentions Hydra coordination. The two sections overlap by roughly 70%. This is a clear economy violation — two sections covering the same ground with the same words.

### Required changes

1. **Merge the risks section into the guardrails section or eliminate the duplication.** The "How is the team managing AI Max risk?" section already covers the test design approach, the two specific risks (cannibalization, budget inflation), and the Hydra coordination. The "What are the risks and open questions?" section restates all three and adds only two new pieces of information: (a) the guardrail design needs to detect issues within the first two weeks, and (b) Modern Search consolidation delays directly delay AI Max readiness. Fold those two points into the existing guardrails section and cut the risks section. Alternatively, keep the risks section but rewrite it to cover only the dependency chain (Modern Search → AI Max readiness, Hydra coordination timing) without restating the guardrail content. Either approach works — the current state of two sections saying the same thing does not.
