# Discovery Log — d4-var2

**Task given:** "Draft my MBR section for May covering AU and MX performance. Brandon needs my input by Monday."

**Instruction:** Do not draft the MBR. Reason as a fresh agent about what would be loaded, log the discovery process.

---

## 1. Fresh-agent reasoning (what I see on session start)

Always-on steering context loaded at session start:
- `soul.md` — identity, voice, Five Levels, routing directory, data routing table
- `steering-index.md` — pointer table from task → manual-inclusion file
- Standard global rules — process-execution, file-creation-rules, devspaces-core, amazon-builder-production-safety, agentspaces-core

Nothing market-specific, nothing writing-style-specific, no MBR template content. That's all gated behind manual inclusion and has to be triggered by something in the request.

## 2. Parsing the request

Three signals in one sentence:
1. **"MBR section"** — output type. Monthly Business Review. Professional writing artifact going to Brandon → Kate → up the org. Not a chat reply, not a task description. This is the strongest signal.
2. **"May covering AU and MX performance"** — scope. Two markets I'm hands-on with. Performance data means regs, spend, CPA, forecasts vs OP2, MTD / monthly roll-ups.
3. **"Brandon needs my input by Monday"** — stakeholder and deadline. Brandon = L7 manager, 1:1 relationship. Monday = hard deadline, so today's date matters for pacing.

## 3. Routing check (soul.md instructs this before acting)

**Professional writing rule (soul.md):**
> Any task that produces or edits professional writing (callouts, WBR narratives, emails, docs, wiki articles, frameworks, POVs) must go through the appropriate writing agent or, at minimum, load the relevant style guide before producing text. Do not write or rewrite professional prose in the default agent voice.

MBR section is professional writing going to Brandon and the broader org. This rule triggers. No dedicated MBR subagent exists in the routing directory (only `rw-trainer` and `karpathy`) — so the fallback applies: **load the relevant style guide before producing text.**

**High-stakes check (soul.md principle 7):**
> Projections, forecasts, test readouts that move >$50K, or final business reviews always require explicit Richard confirmation. Load `high-stakes-guardrails.md`.

MBR is a monthly business review going up the chain. "Final business review" language applies. `high-stakes-guardrails.md` needs to load. Richard confirmation required before any numbers ship.

## 4. Steering-index lookup (what I'd pull from the manual-inclusion table)

From the simulated `steering-index.md`:

**Writing style — MBR section → `richard-style-mbr.md`**
- Primary match. MBR has its own style file. Load it.
- Core style file `richard-writing-style.md` is the parent/foundation — load that too (the indexed ones are specialized overlays, not replacements).

**Analytical — Projection / forecast / Excel drop → `performance-marketing-guide.md`**
- MBR performance sections are retrospective on May, not forward projection. Borderline. But any PS performance writeup that touches pacing, forecast-vs-actual, CPA movements, or attribution calls usually needs the performance marketing guide to avoid analytical sloppiness. Load it.

**Not loaded (and why):**
- `richard-style-wbr.md` — weekly, not monthly. Different cadence, different audience depth.
- `richard-style-amazon.md` — for Amazon-wide comms like DL posts, not targeted up-the-chain narratives.
- `richard-style-docs.md` — for formal documents (OP1, Testing Approach, POVs), not MBR sections.
- `callout-principles.md` — callouts are a WBR construct, not MBR.

## 5. Data sources I'd consult (from soul.md data routing table)

Before drafting, these would be queried — not asked of Richard:

| What | Source |
|---|---|
| AU + MX May monthly totals (regs, spend, CPA, eff-CPA) | DuckDB `ps.v_monthly WHERE market IN ('AU','MX') AND period_key='2026-May'` |
| May weekly breakdown for trend narrative | DuckDB `ps.v_weekly WHERE market IN ('AU','MX') AND period_key BETWEEN '2026-W18' AND '2026-W22'` |
| OP2 targets to compare against | DuckDB `ps.targets WHERE market IN ('AU','MX') AND period_key='2026-May'` |
| MX narrative context — the NB drop Yun-Kang flagged (file is open in editor: `2026-04-22-yun-kang-mx-nb-drop.md`) | That intake file + signal-tracker for recent MX discussion |
| AU + MX state files for current initiatives and open items | SharePoint `Kiro-Drive/state-files/AU*.md`, `MX*.md` |
| Prior MBR structure / what Brandon expects | SharePoint `Artifacts/reporting/` for MBR templates; `docs.loop_pages` if Brandon's MBR lives in Loop |
| Last month's MBR section to match voice and continuity | Same SharePoint Artifacts dir |
| Any active tests closing in May that belong in the narrative | `ps.forecasts`, test dashboard `ps-testing-dashboard.xlsx` |

## 6. Open questions I'd need Richard to answer before drafting

- **Target length / format.** MBR sections vary — is this a 1-pager, a narrative paragraph inside Brandon's doc, or a full market writeup per market? Last month's artifact would tell me.
- **Audience depth.** Brandon consolidates for Kate (L8). Is this the version Brandon sees raw, or the version that goes up? Changes the jargon budget.
- **What "input" means.** Full draft or bullets for Brandon to weave in? Ambiguous in the request.
- **Hard numbers confirmation (high-stakes guardrail).** Any CPA / reg / spend figure that goes in gets explicit Richard sign-off before sending.

## 7. Files loaded / would-load summary

**Loaded automatically (always-on):**
- soul.md
- steering-index.md
- process-execution.md, file-creation-rules.md, devspaces-core.md, amazon-builder-production-safety.md, agentspaces-core.md

**Would load via manual inclusion for this task:**
- `richard-writing-style.md` (core, foundational for any drafted prose)
- `richard-style-mbr.md` (specialized overlay per steering-index MBR row)
- `performance-marketing-guide.md` (analytical discipline for performance numbers)
- `high-stakes-guardrails.md` (soul.md principle 7 triggers on "business review")

**Would consult but not steering files:**
- `~/shared/context/body/body.md` — navigation map, if I need to find an organ
- `~/shared/context/body/amcc.md` — streak / hard thing check per instruction 3
- `~/shared/context/active/current.md` — live state
- `~/shared/context/intake/drafts/2026-04-22-yun-kang-mx-nb-drop.md` — already open in editor, directly relevant to MX
- Prior MBR sections in SharePoint Artifacts
- DuckDB `ps.*` views for May numbers
- Market state files in SharePoint Kiro-Drive

## 8. Honest self-assessment

- The two-step resolution (steering-index → specialized style file) works cleanly for MBR. No ambiguity about which writing style file to pull.
- The analytical row is less obvious — "MBR performance section" isn't literally "projection / forecast / Excel drop," but the retro numbers and forecast commentary that usually appear in an MBR justify loading `performance-marketing-guide.md`. A stricter read of the index might skip it. I'd load it because the cost is low and the downside of analytical sloppiness in an up-the-chain doc is high.
- No subagent exists for MBR drafting specifically. If one existed, routing rule would push to it. Absent that, I'd draft in-agent after loading the style files.
- Deadline pressure ("Monday") doesn't change the discovery steps. Skipping style-file loads to save time is the exact kind of shortcut that produces voice drift.
- Subtraction check (soul.md principle 3): I'm loading 4 manual-inclusion files. Each earns its place — core style, MBR overlay, analytical guide, high-stakes guardrail. No redundancy.

## 9. What I did NOT do (per instruction)

- Did not draft the MBR section.
- Did not query DuckDB.
- Did not read the style files.
- Did not read the MX NB drop intake file.
- Did not ask Richard clarifying questions yet — this log is the deliverable.
