# Discovery Log — d4-var3

**Scenario:** Draft MBR section for May covering AU and MX. Brandon needs input by Monday.
**Simulated steering active:** soul.md + Canonical Resources table (MBR row → `richard-style-mbr.md` + `richard-style-amazon.md`) + always-on steering-index.md with full directory.
**Instruction:** Don't draft. Log the discovery path honestly.

---

## 1. Fresh-agent read of the request

Parse: it's an MBR section, monthly cadence, two markets (AU + MX), and there's a deadline (Monday). Audience is Brandon — that's an L7, so this qualifies as a leadership-facing document per soul's professional-writing rule. Any drafting has to go through the MBR style guide, not the default agent voice.

Ambiguity I should flag before drafting (not now, but on the drafting turn):
- "May" while we're still in April. Either Richard means the May cycle covering April data (most likely given MBR timing), or he has a partial-May window, or he mis-spoke and means the April MBR. Real draft requires confirming.
- "my input" — is this Richard's subsection of a larger MBR deck Brandon is assembling, or the full write-up? That changes the word budget and scope.

I'm not asking these yet because the task instruction is to log discovery, not to draft.

## 2. Which steering do I actually need?

The Canonical Resources table for MBR points at two files. Both are listed as manual-inclusion steering, which is the right default — MBR writing should not be polluting every context window. The pairing is deliberate:

- `richard-style-mbr.md` — the per-market template, paragraph structure, checklist order, failure modes, worked examples. This is the narrow, task-specific one.
- `richard-style-amazon.md` — the leadership-writing-norms layer that sits on top of Richard's voice for L7+. MBR goes to Brandon (L7) and likely lives inside a broader doc that reaches higher, so the Amazon layer is non-optional here.

Per soul's professional-writing rule: "Any task that produces or edits professional writing (callouts, WBR narratives, emails, docs, wiki articles, frameworks, POVs) must go through the appropriate writing agent or, at minimum, load the relevant style guide before producing text." MBR is in that list. I load both style guides before any prose gets written.

## 3. Steering-index reality check

Simulated setup claims an always-on `steering-index.md` with the full directory. I searched the workspace: **no such file exists.** In a real fresh session I'd treat this as a planted assumption and check. Since the Canonical Resources row for MBR is what actually contains the pointer, and I can read both target files directly, the absence of steering-index isn't blocking — the pointer still resolves. But it is worth naming: if the index were the only way to find these files, I'd be stuck. The resilient path is Canonical Resources table → file path → direct read.

Both files exist at the paths implied and are readable. Confirmed:
- `.kiro/steering/richard-style-mbr.md` (manual inclusion, ~80 lines, template + checklist + worked examples)
- `.kiro/steering/richard-style-amazon.md` (manual inclusion, narrative standard, structure, confidence calibration table)

## 4. What I'd load next (not now — on the drafting turn)

Files:
1. `richard-writing-style.md` — core voice. Called out in soul as the base that Amazon layer sits on top of. Didn't verify existence this pass, but soul references it as a core style file. Load before either layer.
2. `richard-style-mbr.md` — primary template.
3. `richard-style-amazon.md` — leadership layer.

Data sources (per soul's Data & Context Routing table):
- `ps.v_monthly WHERE market IN ('AU','MX') AND period_key='2026-May'` (or April, depending on which month the MBR covers) — monthly registrations, spend, CPA.
- `ps.v_monthly` for YTD roll-up across both markets.
- `ps.targets WHERE market IN ('AU','MX') AND period_key='2026-May'` — OP2 targets for the vs-OP2 framing the template requires.
- `ps.v_weekly` for same markets, last 4–6 weeks, to find MoM levers (NB/Brand split, spend shift, CVR movement).
- SharePoint `Kiro-Drive/state-files/` — AU and MX market state files for narrative context (active initiatives, known misses, running themes) that numbers alone won't reveal.
- SharePoint `Dashboards/ps-pacing-dashboard.xlsx` — a sanity cross-check against DuckDB.
- SharePoint `Artifacts/reporting/` — last MBR cycle's published version to see what Brandon's expectations look like in practice and to avoid repeating the same framing.

Not needed unless the data reveals something:
- Hedy transcripts (only if a specific meeting decision affected a market's month).
- Slack signals (only if a launch/pause event needs attribution).

## 5. What I would NOT do

- Not draft prose before loading the style guides. The default agent voice is wrong for MBR.
- Not query for May data without first confirming with Richard which month is actually in scope — the "May MBR" could legitimately mean April data, partial-May, or the cycle name. Drafting on the wrong month wastes his Monday deadline.
- Not skip the OP2 targets lookup. The MBR template's first line literally depends on vs-OP2 framing. Without targets pulled, I can't follow the template.
- Not route to rw-trainer. This isn't coaching, 1:1 prep, or strategic artifact review — it's a recurring reporting artifact with a clear style guide. Soul's routing rules say "if unsure, handle it." This isn't unsure.
- Not freelance on structure. The MBR template prescribes paragraph order (monthly → YTD → explanation → MoM). Any deviation needs a reason.

## 6. Honest gaps

- I didn't verify `richard-writing-style.md` exists in this pass. Soul references it as the core layer. A real drafting turn should confirm.
- I didn't check whether `ps.v_monthly` has May data yet, or whether `ps.targets` has the right `period_key` format. The soul table gives me the shape of the query but the data freshness is unknown. `ops.data_freshness` would tell me.
- Simulated steering claims an always-on steering-index — it doesn't exist. If this were a real cold start and I'd been told the index was the source of truth, I'd have wasted a turn looking for it. Flagging as a steering-setup inconsistency.
- Didn't check Asana for any MBR-related task with scope notes from Brandon — that's the fastest way to resolve the "May vs April" ambiguity without pinging Richard.

## 7. Minimum confirmation needed before drafting

Two questions, batched:
1. Does "May MBR" mean the May cycle covering April data, or something else?
2. Is this your subsection of a larger MBR, or the full AU + MX write-up? (Affects word budget.)

If Asana has a task from Brandon with scope, both may already be answered without asking.

## 8. Principle check (soul's 8 principles)

- **Routine as liberation** — MBR is a monthly artifact with a fixed template. Load the template, follow the checklist. Don't reinvent.
- **Subtraction before addition** — I'm resisting the urge to load every style file in the system. MBR + Amazon layer + core voice. Three files, not ten.
- **Human-in-the-loop on high-stakes** — MBR goes to Brandon, who shares upward to Kate. Numeric confidence per paragraph, flag LOW confidence where volume is thin, no projections without Richard confirming. Matches MBR template's checklist item 6.
