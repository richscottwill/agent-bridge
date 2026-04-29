# MPE v1.1 Slim — Leadership Demo Script

*Target audience: Kate Rundell (L8 Director), Todd Heimes (L10 VP), Brandon Munday (L7)*
*Duration: 3 minutes. Hard cap: 5 minutes including Q&A.*
*Demo date: **2026-05-16 Friday**.*
*Venue: Richard's laptop, projection.html on localhost:8080.*

---

## Opening (15 seconds)

> "We re-architected the Paid Search Market Projection Engine. The old one couldn't reason about campaign lifts separately from spend. The new one does. I'll show you MX — the market where this first broke — and then the all-ten view."

---

## Scene 1 — MX hero (30 seconds)

Page loads with **MX Y2026 @ 100% ie%CCP target** preloaded.

> "**Hero number**: projected spend this year at MX target. Regs on the right.
> 
> This number comes from: the last 8 weeks of actuals tell us where Brand is NOW. A campaign lift stream projects how that level evolves through the year. And we solve NB spend to hit the 100% ie%CCP target finance committed to."

Point at the regime badge top-right: *"Sparkle still peaking at 30% confidence."*

> "The engine knows Sparkle's lift is only 7 weeks old — so its confidence is low and it decays forward based on the assumption we'll learn more week by week."

---

## Scene 2 — Scenario chips (45 seconds)

Click through chips in order: **Current plan (Mixed)** → **Frequentist** → **Bayesian** → **No lift**.

> "Four scenarios, all four mean something specific:
> 
> **Mixed** — what the engine believes. Recent actuals + fitted decay.
> 
> **Frequentist** — what the last 8 weeks alone would tell us. No assumed campaign lift.
> 
> **Bayesian** — what happens if Sparkle holds forever at the lift we authored. Full confidence, no decay.
> 
> **No lift** — strip Sparkle out of the anchor entirely. What would MX look like without the current campaigns.
> 
> Watch the hero move. ($1.31M → $1.56M → $1.79M → $2.48M range.) The spread tells us how much of the current projection is 'recent data' vs 'assumed future campaign impact.' That's been the question that kept getting asked in WBRs — and now it's a visible dial."

---

## Scene 3 — All 10 markets (30 seconds)

Click **All 10 markets** view.

> "Same engine, every market. Each mini-chart is that market's full-year trajectory. Click any one to drill in."

Click **Distance to target** view.

> "This is the one-glance view: green markets are pacing within ±5pp of their ie%CCP target, yellow ±5–15pp, red worse. AU and JP don't use ie%CCP so they're colored by spend vs OP2.
> 
> Today: MX red at +54% above OP2. That's the Sparkle scenario showing up as a real forecast. UK + FR + IT yellow, slightly behind OP2."

Point at the NA/EU5/WW rollup strip: *"Regional rollups — sum of children, not separately solved."*

---

## Scene 4 — Period selector + time scoping (15 seconds)

Back to **Single market**, click **Period** → **Q2**.

> "Any period. W17 alone, April, Q2, Y2026, or the next year. Numbers update to that scope. Chart highlights the selected period."

---

## Scene 5 — Share + Model View (15 seconds)

Click **Share**.

> "One-click PNG card. Paste straight into Slack."

Click **Parameters** disclosure.

> "Model View drawer — fit quality r², the active campaign lifts with their confidence, NB CPA elasticity, Locked-YTD position. Every number has an 'Explain this' link."

---

## Closing (15 seconds)

> "One architecture. Ten markets. Four scenarios per market. Period-scoped. Feedback bar appears after the third projection in a session — so Lorena, Brandon, you can tell the model when you disagree and that feeds forward to next quarter's fit.
> 
> Questions?"

---

## Likely questions — pre-canned answers

**Q: How is this different from the Bayesian thing we had before?**
A: Old one solved for a spend envelope and allocated Brand/NB via a fixed share. When Sparkle hit, the share didn't know how to model "Brand went up 80% independent of spend." This one projects Brand from recent actuals + campaign lift stream, and solves NB separately. Two independent levers, two independent market facts.

**Q: Why are the numbers so different from last month's projection?**
A: Anchor rework on 2026-04-26. The old anchor was a pre-regime mean averaged against stale data. The new anchor is the last 8 weeks of actuals. For campaign-heavy markets like MX that's a meaningful swing. MX Y2026 @ 75% moved from $800K–$1.2M to $1.0M–$1.5M — that's the Sparkle-era baseline showing up correctly.

**Q: How accurate is it?**
A: Phase 6.5.2 backtest: 12-week holdout across all 10 markets, 8 of 10 under 22% Brand MAPE. MX and JP fail the gate because their holdout windows include campaign step-changes that no baseline can anticipate without advance notice — those are flagged in the report.

**Q: What's next?**
A: Phase 6.5 (post-demo) wires in the qualitative priors catalog, the user feedback loop, and retires the old Bayesian projector from the WBR pipeline. v1.2 adds skeleton posteriors + BOCPD automatic regime detection; v1.3 adds cross-market hierarchical priors so data-sparse markets borrow from peers. See design-v1.1.md destination arc for sequencing.

**Q: Can I see the code?**
A: All in `shared/tools/prediction/` + `shared/dashboards/`. Quick reference at `shared/wiki/agent-created/operations/mpe-v1-1-slim-quick-reference.md`. CHANGELOG at `.kiro/specs/market-projection-engine/CHANGELOG.md`.

---

## Prep checklist — run morning of 2026-05-16

- [ ] Confirm http://localhost:8080/projection.html loads cleanly
- [ ] Regenerate projection-data.json: `python3 shared/dashboards/export-projection-data.py`
- [ ] Run acceptance hook: confirm 131/131 + 3/3 JS parity green
- [ ] Run backtest: confirm ≥8/10 markets under 22% Brand MAPE
- [ ] Clear localStorage (session state + saved projections) for clean default view
- [ ] Close all browser dev tools panels
- [ ] Chrome full-screen at 1440×900 (matches responsive desktop breakpoint)
- [ ] Demo rehearsal: run the above 5 scenes in exactly 3 minutes

---

*Script authored 2026-04-26. Maintained as MPE ships — update after demo to capture what actually worked vs what didn't.*
