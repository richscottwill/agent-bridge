# Dashboard vs R&O Reconciliation — Should We Build a Tool?

**Short answer: No. Not yet. Probably not ever in the form you're picturing.**

This is the device.md test, straight up: "Does this remove a recurring decision?" The answer right now is we don't even know what the decision is, because we haven't figured out the delta. Building a reconciliation tool before you understand the delta means automating our confusion.

## What we actually know

- MX Jan–Mar dashboard (ps.v_monthly): $56K + $68K + $96K = **$220K**
- April R&O for same period: **~$427K**
- Delta: 1.94x. FX alone (5.9% MXN→USD change 4/1) explains ~6%, not 94%.
- We have two live hypotheses and zero confirmed: (a) R&O includes gross-of-fees/taxes/chargebacks that the dashboard strips out, (b) MX team made off-platform manual adjustments that never hit the ad platform feed.
- Neither is a bug we can patch. They're accounting-basis differences, and we don't know the rule yet.

## Run it through device.md

**The test:** "Does this require Richard's judgment to produce a correct output?"

Today: **yes, heavily.** Every month someone has to decide what "correct" means when the two numbers disagree. Is net-of-fees the truth? Is the R&O gross number the truth? Which one does Brandon care about for pacing? Which one goes into OP2? That's not automation — that's policy.

Until we've answered that once, manually, a tool just hardcodes the wrong answer faster.

**Routine as liberation** — principle #1 from soul.md — cuts the other way here too. Routines eliminate decision fatigue on *stable* decisions. This decision isn't stable yet. You can't routinize what you haven't defined.

**Subtraction before addition** (principle #3): The right move is to subtract the ambiguity, not add a tool on top of it.

## Is it even repetitive enough?

Reconciliation frequency = monthly, maybe quarterly. Not daily, not weekly. At monthly cadence with a ~15-minute check, that's ~3 hrs/year. A tool that reliably handles this would take 2–3 days to build and test, plus maintenance. Break-even is years, not months — and the failure mode (silently reconciling on a wrong rule) is way worse than the manual friction.

Compare to forecast pipeline, which you actually built: weekly cadence, multiple markets, deterministic rules, clear correct answer. That earned its place. R&O reconciliation doesn't.

## The simpler alternative

Three steps, in order. Don't skip ahead.

**1. Ask Yun/York for the R&O definition (30-min ask, once).**
What's in the $427K that isn't in the $220K? Get the line items. Specifically: fees, agency margin, tax, chargebacks, manual invoice adjustments, anything off-platform. This is a one-email answer and it unblocks everything else.

**2. Document the reconciliation rule as a steering/ops doc.**
Once you know the delta composition, write it down in one place — probably `shared/wiki/agent-created/operations/` or similar. "Dashboard MX spend reconciles to R&O via: +X% fees, +$Y/mo agency, +manual adjustments." Future Richard and future Yun read one doc, not rebuild the logic every month.

**3. Only *then* consider a SQL view.**
If the rule turns out to be a clean formula (e.g., "R&O = dashboard × 1.15 + manual invoices"), add a `ps.v_monthly_ro_basis` view in DuckDB. One-day build. That's not a tool — that's a column. It's the right scope for this problem.

If the rule turns out to be messy/manual (chargebacks land in random months, MX team sometimes journals stuff), you don't automate it. You just check monthly with the documented rule and move on.

## What this means for the Lorena email

You already paused the Lorena budget email over this. Good call. The $1.1M ceiling is suspect if the gross/net basis is wrong — by 10–30% potentially. The hard block isn't "build a tool," it's "get Yun to confirm the basis before the email goes out." That's 30 minutes of Yun's time, not 2 days of your time.

## Five Levels check

- This would be a **Level 3** tool (Team Automation). But the Level 3 bar in soul.md is "tools teammates actually adopt." A reconciliation tool only Richard uses doesn't clear that bar. If you build here, build what Yun and Lorena would use — which means it has to encode *their* reconciliation rule, not yours.
- Spending Level 3 energy on this now pulls from Level 1 (weekly artifacts, which you're struggling on). Don't trade an active-struggling priority for a queued one.

## Recommendation

Ship Yun an email today asking for the R&O composition. Paste the $220K vs $427K math, ask for the line-item breakdown. Once you have it, write a 200-word ops doc. Revisit the tooling question in 90 days if reconciliation is still friction. My bet: it won't be, because the doc will make the rule cheap to apply.

Don't build the tool. Build the understanding first.
