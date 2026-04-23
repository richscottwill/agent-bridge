# Should we build a tool to auto-reconcile dashboard vs R&O spend?

**Short answer: No. Not yet. Build a one-time investigation first. If the gap turns out to be a recurring, structural mismatch — then wrap it in a lightweight reconciliation view, not a new tool.**

---

## The question behind the question

You framed this as "should we build a tool." The steering file and device.md both say: check device.md first, ask whether it's repetitive enough to justify building, subtract before you add. So the honest answer is: you're conflating two different problems.

1. **One-time diagnostic problem:** $220K (dashboard) vs $427K (R&O) for MX Jan-Mar. 1.94x. That's not FX. That's a definitional or scope mismatch. You don't know what the delta is yet.
2. **Recurring reconciliation problem:** Every month, R&O and the dashboard diverge, someone has to explain why, and the explanation consumes analyst time.

You only have evidence for #1 right now. You're being asked by April Yun to explain one number. Building a tool for #2 before you understand #1 is premature — you'd be automating a reconciliation whose business logic you haven't derived yet.

## Why not build (right now)

Against the How I Build principles:

- **Subtraction before addition (P3):** You already have `ps.v_monthly`, `ps.dashboard_uploads` (lineage on every WW dashboard ingest), and presumably a R&O extract somewhere in finance's world. Before adding a reconciliation tool, figure out whether one of those already answers the question, or whether a SQL view over them does.
- **Structural over cosmetic (P2):** A one-off reconciliation script is cosmetic — it solves today's conversation with April. A structural fix is defining, once, what "MX paid search spend" means in each system and documenting the reconciliation rule (accrual timing? gross vs net of vendor rebates? includes PA/DSP? includes non-PS acquisition channels that share an account?). That doc is worth more than the tool.
- **Reduce decisions, not options (P6):** A tool that spits out "dashboard says X, R&O says Y, delta = Z" doesn't reduce any decision — someone still has to explain the delta. The decision is "what's in scope." Automate that only after you've defined it.
- **Repetitive enough?** Once a month, at WBR/MBR prep, maybe 15 minutes of analyst time. Not zero, not high enough to justify a new tool in device.md yet. Tool Factory backlog already has higher-leverage candidates (staleness detector, callout templates, campaign link generator) that are closer to ready.

## What to build instead (cheap, now)

**Step 1 — One-time investigation (2-3 hours, Richard or delegate):**
- Pull the R&O extract for MX Jan-Mar. Get it at the account/campaign/channel level if possible, not just market total.
- Join against `ps.accounts` + `ps.account_metrics` (or the raw account-level rows feeding `ps.v_monthly`). Identify which accounts/channels are in R&O but not in the dashboard, or vice versa.
- Candidate hypotheses to confirm/rule out:
  - R&O includes **Paid App + DSP + programmatic** — dashboard is PS-only
  - R&O includes **non-AB spend** sharing the same MCC / invoice entity
  - **Timing:** R&O is accrual-based (invoice month), dashboard is click/impression date
  - **Vendor rebates / Google credits** netted in one but not the other
  - **Cross-market attribution:** MX-billed accounts serving impressions in LATAM neighbors, or vice versa
  - **Agency fees / mgmt fees** included in R&O, not in dashboard
- Output: a one-page written reconciliation with each driver quantified (e.g., "$X is DSP, $Y is timing, $Z is agency fees, $W unexplained").

**Step 2 — Document the definition (30 minutes, once):**
- Add a section to `ps-performance-schema.md` or a new doc: "What `ps.v_monthly.cost` includes vs excludes, and how it relates to R&O." Keep it plain text. This is the structural fix.

**Step 3 — Only if step 1 reveals a recurring, non-one-time structural gap:**
- Add a view — not a tool — something like `ps.v_monthly_reconciled` that joins R&O extract (if you can get it in a stable form) to `ps.v_monthly` and exposes the defined drivers as columns. A view is subtraction-friendly: no new script, no hook, no maintenance burden. It lives in the existing analytics DB.
- Only if the view proves genuinely repetitive (monthly+, multiple consumers) do you wrap it in a tool. By that point you'll know the business logic cold and the tool becomes a formality.

## Simpler alternatives you should consider first

- **Ask finance for their definition, in writing.** 10 minutes of April's or Yun-Kang's or finance's time saves you building anything. If the answer is "R&O is all acquisition spend including DSP and agency fees," you're done — no tool needed, just update the callout language.
- **Add a standing line to WBR/MBR prep:** "Dashboard cost = PS channel only, excludes DSP/fees. R&O will be higher." One sentence. Zero build. Eliminates the recurring confusion without automation.
- **Delegate to Lorena** (she's already in the MX flow and actively owns keyword sourcing) to own the monthly tie-out. This is exactly the kind of recurring, low-judgment task the delegation protocol is built for.

## What would change my mind

Build the tool if, after step 1, you find:
- The gap is ≥3 independent drivers (not just "DSP + fees")
- The reconciliation is needed **weekly or more**, not monthly
- Multiple consumers (Brandon, Yun-Kang, April, finance) ask the same question independently
- The dashboard source data itself is wrong (not a scope mismatch) and needs repair upstream

Those conditions together justify the build cost. Right now you have none of them confirmed.

## Five Levels connection

This is Level 3 (Team Automation) work *if* you build. Level 3's bar is "one tool adopted" — and device.md flags that bar explicitly: tools teammates adopt first. A reconciliation tool that only you use, to answer one-off questions from April, doesn't clear that bar. The Paid Search Audit auto-ingest and the staleness detector are closer to teammates-will-use-this territory.

However, **the investigation itself** is L2 work (Drive WW Testing — every test/number has written status) because it produces a durable written definition of what dashboard cost is. That's the part worth doing this week.

## Recommendation

1. Do step 1 (investigation) yourself this week or delegate to Lorena — budget 2-3 hours. Use it as the substantive reply to Yun-Kang that's already drafted but vague on the R&O piece.
2. Do step 2 (definition doc) in the same session.
3. Put "reconciliation view" in the Tool Factory backlog as *unprioritized*, conditional on step 1 findings. Do not build it pre-emptively.
4. Revisit only if the gap recurs structurally in the May numbers.

---

*Applied principles: P3 (subtraction — investigate before adding), P2 (structural — definition doc > tool), P6 (reduce decisions — scope clarity is the decision to reduce). Checked against device.md Tool Factory: no existing candidate covers this, but existing backlog items (staleness detector, campaign link generator) are closer to ready and higher-leverage for Level 3.*

*Human Review Required: before committing any build, confirm with Brandon or finance that R&O scope is actually different from dashboard scope — this whole memo assumes it is, which is the most likely explanation but not verified.*
