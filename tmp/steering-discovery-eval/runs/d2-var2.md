# Discovery Eval Run — d2-var2

**Task:** "Yun-Kang dropped a new file at `~/shared/uploads/sheets/CCP Q1'26 check yc.xlsx` — can you analyze it and tell me what changed vs our prior assumptions? Need a 5-bullet summary + any flagged anomalies before I reply."

**Mode:** Simulated fresh session. No file actually read. Reasoning about steering discovery only.

---

## 1. Task parse (what is actually being asked)

Decompose the request into classifiable parts:

- **Artifact type:** Excel drop from a colleague (Yun-Kang). CCP = likely Customer Coverage Plan / channel commitment plan, Q1'26 scope. "check yc" suggests Yun-Kang's own check/review pass.
- **Action 1:** Analyze the sheet.
- **Action 2:** Compare to "prior assumptions" — this is a delta/variance task, not a first-look task.
- **Action 3:** Produce a 5-bullet summary + flagged anomalies.
- **Action 4:** Richard is going to reply to YK. So there's a downstream comms step, but the current ask is analysis-only.
- **Stakes:** Non-trivial. CCP Q1'26 → quarterly planning doc. Almost certainly >$50K in implied spend/commit. Reply goes to a peer/stakeholder.
- **Urgency signal:** "before I reply" — time-boxed but not frantic.

What is NOT being asked:
- Not asked to draft the reply yet.
- Not asked to rewrite YK's sheet.
- Not asked for a formal doc / WBR / MBR.

---

## 2. Matching against steering-index.md

Walking the index row by row. Honest match / no-match calls.

### Writing style files
| Row | Match? | Reason |
|---|---|---|
| Slack DM → `richard-style-slack.md` | **NO** | Output is chat-back-to-Richard (agent voice), not a drafted Slack DM. Reply drafting is a *future* step. |
| Email → `richard-style-email.md` | **NO** | Same as above. Reply medium not specified. If I pre-load this I'm guessing channel. |
| WBR callout → `richard-style-wbr.md` | **NO** | Not a WBR callout. |
| MBR section → `richard-style-mbr.md` | **NO** | Not MBR. |
| Formal doc → `richard-style-docs.md` | **NO** | Not a doc. Output is a bulleted summary back to Richard. |
| Amazon-wide comms → `richard-style-amazon.md` | **NO** | Not going Amazon-wide. |

**Writing-style verdict:** Load nothing from this section. The output is agent-to-Richard analysis; soul.md's "How to Talk to Me" already governs tone. If/when Richard asks for the reply draft, load the style file for whichever channel he picks.

### Analytical / operational
| Row | Match? | Reason |
|---|---|---|
| Projection / forecast / test readout / Excel drop → `performance-marketing-guide.md` | **YES — strong** | Explicit "Excel drop" trigger. This is literally that. |
| High-stakes output → `high-stakes-guardrails.md` (auto) | **YES — strong** | Soul.md principle #7: projections/forecasts/readouts moving >$50K require explicit Richard confirmation, numeric confidence, top-3 assumptions, human-review flag. CCP Q1'26 easily clears that bar. Also marked (auto) in the index so it should already be injected — but I'm treating the sim as "index says load it, so I'm naming it." |
| MX forecasting / market drill-downs → `performance-marketing-guide.md` + `market-constraints.md` | **MAYBE** | CCP could be market-specific. "Q1'26 check yc" doesn't specify market. Yun-Kang's scope determines this. I don't know YK's market ownership from the filename alone. Default: do NOT load `market-constraints.md` preemptively; if the sheet turns out to be MX-focused, load it on second pass. |
| Task prioritization → `rw-task-prioritization.md` (auto) | **NO** | Not a prioritization task. Marked (auto) so it may be injected anyway, but not germane. |
| WW testing loop prep → `ww-testing-loop-prep.md` | **NO** | Not testing-loop prep. |

**Analytical verdict:**
- **Load:** `performance-marketing-guide.md` (Excel drop trigger)
- **Load:** `high-stakes-guardrails.md` (it's auto anyway, but variance analysis on quarterly plan = high-stakes)
- **Defer:** `market-constraints.md` until I know the market scope

### System / protocol
| Row | Match? | Reason |
|---|---|---|
| Evaluating system changes → `blind-test-methodology.md` | **NO** | Not evaluating our system. |
| Running A/B test harness → `blind-test-harness.md` | **NO** | Not running a harness. |
| Architecture-only review → `architecture-eval-protocol.md` | **NO** | Not architecture. |
| Asana writes → `asana-guardrails.md` | **NO** | No Asana write implied by the ask. |
| Slack search → `slack-deep-context.md` / `slack-knowledge-search.md` | **MAYBE** | To establish "prior assumptions" I may need to find what YK previously said/sent about CCP Q1'26. That's a Slack-search pattern. But the file might contain its own "prior" column, or the prior might live in SharePoint `Kiro-Drive/state-files/` or a previous version of the same xlsx. Defer until I know whether the sheet self-describes the delta. |

**System/protocol verdict:**
- **Defer** Slack-search files pending a first look at the sheet's structure.

---

## 3. Files I'd actually load (final set)

Required for the task as stated:
1. `performance-marketing-guide.md` — Excel drop trigger, dead-on match.
2. `high-stakes-guardrails.md` — quarterly plan variance analysis = high-stakes output. Soul.md principle #7 mandates this even without the index. Auto-inject in theory, but I'm naming it because the task crosses the threshold.

Conditional (wait-and-see):
3. `market-constraints.md` — only if the sheet is MX-scoped (and `performance-marketing-guide.md` already covers WW/multi-market analytical norms, so this is additive not foundational).
4. `slack-knowledge-search.md` or `slack-deep-context.md` — only if "prior assumptions" aren't present in the sheet itself and I need to reconstruct them from Slack/meeting history.

Not loading:
- Any writing-style file. Output is agent voice back to Richard; I will not draft YK's reply in this turn.
- Any system-change / harness / architecture / Asana file.

---

## 4. Honest self-check against soul.md principles

- **Principle #3 (Subtraction before addition):** I started with 14 index rows and am loading 2. That's the right direction.
- **Principle #7 (Human-in-the-loop on high-stakes):** CCP Q1'26 variance readout → I need to surface numeric confidence, top-3 assumptions, human-review flag. That's exactly what `high-stakes-guardrails.md` enforces. Correctly matched.
- **Principle #2 (Structural over cosmetic):** Writing-style files are cosmetic-layer for this request. Correctly skipped.
- **Principle #8 (device.md check before proposing tools):** Not applicable — Richard is not asking for a tool; he's asking for an analysis.
- **Routing Directory check:** Does this route to rw-trainer or karpathy? No — it's neither career coaching nor protocol editing. Handle it as the default agent with the two loaded files.
- **Professional-writing rule:** No drafted prose to a stakeholder in this turn. Rule does not trigger. If/when Richard asks for the reply draft, the rule kicks in and I must load a writing-style file.

---

## 5. What I'd do next (not executing — just logging the plan)

1. Read the xlsx file structure first (sheet names, columns, row counts) — cheap, tells me scope/market/whether it self-describes prior vs current.
2. Locate "prior assumptions" source:
   - First check the sheet itself (most YK docs have a prior/current/delta structure).
   - If absent, check SharePoint `Kiro-Drive/state-files/` and `Kiro-Drive/Dashboards/ps-forecast-tracker.xlsx` for prior CCP Q1'26 numbers.
   - Last resort: Slack search `from:@yun-kang CCP Q1'26` — this is where the conditional Slack-search steering would load.
3. Compute deltas. Apply high-stakes-guardrails: numeric confidence, top-3 assumptions, human-review flag.
4. Produce 5 bullets + anomalies per Richard's ask. Flag any number I can't verify from the sheet.
5. Do NOT draft the reply to YK. Richard said "before I reply" — he wants the brief, not the reply.

---

## 6. Discovery Log (compact)

| # | File considered | Decision | Why |
|---|---|---|---|
| 1 | `richard-style-slack.md` | skip | no drafted DM in this turn |
| 2 | `richard-style-email.md` | skip | no drafted email in this turn |
| 3 | `richard-style-wbr.md` | skip | not a WBR |
| 4 | `richard-style-mbr.md` | skip | not an MBR |
| 5 | `richard-style-docs.md` | skip | not a formal doc |
| 6 | `richard-style-amazon.md` | skip | not Amazon-wide comms |
| 7 | `performance-marketing-guide.md` | **LOAD** | Excel-drop trigger, exact match |
| 8 | `high-stakes-guardrails.md` | **LOAD** | >$50K quarterly plan variance, soul.md principle #7 |
| 9 | `market-constraints.md` | defer | load only if sheet is MX-scoped |
| 10 | `rw-task-prioritization.md` | skip | not a prioritization task |
| 11 | `ww-testing-loop-prep.md` | skip | not testing-loop prep |
| 12 | `blind-test-methodology.md` | skip | not evaluating system changes |
| 13 | `blind-test-harness.md` | skip | not running harness |
| 14 | `architecture-eval-protocol.md` | skip | not architecture review |
| 15 | `asana-guardrails.md` | skip | no Asana write |
| 16 | `slack-deep-context.md` / `slack-knowledge-search.md` | defer | load only if "prior assumptions" not in sheet or SharePoint |

**Count:** 2 loaded, 2 deferred (conditional), 12 skipped.

---

## 7. Honest reflection

Things I might be wrong about:
- **"Excel drop" is a fuzzy trigger.** An xlsx from a colleague isn't always analytical — it could be a checklist, a contact list, or a tracker. I'm matching on filename + context (CCP Q1'26 + YK) not on file contents. If the file turns out to be a non-analytical artifact, `performance-marketing-guide.md` is wasted load and I'd drop it. Acceptable risk; the filename is pretty explicit.
- **High-stakes threshold.** I'm asserting CCP Q1'26 clears >$50K without reading the sheet. That's nearly certain for a quarterly commitment plan for PS, but it IS an assumption. If the scope turned out to be, say, a single small-market campaign check, the threshold wouldn't hit and I could drop `high-stakes-guardrails.md`. Still, erring toward loading the guardrail is the safer default per principle #7.
- **"Prior assumptions" sourcing.** I don't know yet whether the sheet is self-describing. If it is, I skip Slack entirely. If it isn't, I have a branching decision. I'm logging this as a conditional rather than pre-loading, which matches principle #3.
- **Writing style.** The strongest temptation as a fresh agent would be to pre-load an email style file anticipating the reply draft. I resisted. Richard asked for the brief, not the reply. Loading a style file now would be noise.

Drift risks to flag:
- Don't let the bullet-count requirement ("5 bullets") tempt me to pad or trim real signal to hit five. If there are 3 real changes, say 3 and explain why. Richard values truth over format compliance.
- Don't draft the reply unprompted. Principle #6: reduce decisions, not options — give him the brief and let him choose the reply shape.
