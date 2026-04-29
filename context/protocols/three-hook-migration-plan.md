<!-- DOC-0414 | duck_id: protocol-three-hook-migration -->
# Three-Hook Architecture — Migration Plan

*Splits morning ingestion into three specialized hooks: AM Brief (narrow/daily), Broad Sweep (weekly), Topic Sentry (daily/topic-driven). Supersedes monolithic am-backend-parallel scan responsibilities.*

**Created:** 2026-04-28, in response to the ABMX-launch-email miss (Cristobal Jimenez 2026-04-24 — ABMX reg funnel 38%→73% launch announcement never surfaced in any AM digest because classification rules filter by sender only, not by topic or distro).

---

## Architecture at a glance

| Hook | Cadence | Scope | Output | Runtime target |
|------|---------|-------|--------|----------------|
| **AM Brief** | daily, ~7am PT | narrow priority: calendar, unread Brandon/Kate/Todd email, Asana today + overdue, Slack mentions | `~/shared/context/active/daily-brief-latest.md` | <5 min |
| **Topic Sentry** | daily, after AM Brief | topic-watchlist-driven, 24h window across all channels | `~/shared/context/active/topic-sentry.md` | <2 min |
| **Broad Sweep** | weekly | exhaustive: all distros, all channels, full bodies, Loop diffs, SharePoint drift | `~/shared/context/active/broad-sweep-YYYY-WNN.md` | ~10–15 min |

### How they compose

```
~7am: AM Brief fires → ingests narrow (current AM-Backend minus some steps) → writes daily-brief-latest.md
~7:05am: Topic Sentry fires → reads DuckDB written by AM Brief → writes topic-sentry.md
Weekly (Richard-scheduled): Broad Sweep fires → full ingestion pass → writes broad-sweep-YYYY-WNN.md
```

All three write to the same DuckDB tables (`signals.emails`, `signals.slack_messages`, `signals.hedy_meetings`, `docs.loop_pages`, `main.calendar_events`). Dedup happens on existing natural keys (conversation_id, ts, session_id, page_url). Running any of them on the same data is idempotent.

---

## What AM Brief keeps vs drops

### Keeps (the daily essentials) **Phase 5 (reduced)** — write `daily-brief-latest.md`, push to SharePoint **Phase 2.5F** — current.md refresh (quick surgical update only) **Phase 0** — Schema verification (10s) - **SharePoint drift check** → Broad Sweep weekly - Orchestrator B2 Activity Monitor (unchanged — activity on today's tasks) - **Full channel list Slack scan** (all 50+ channels) → Broad Sweep weekly - Subagent A Slack — filter to channels whose section has `"am_brief"` in its `scan_in` array per `~/shared/data/state/slack-channel-registry.json` v3.1+. By default: `WW Testing`, `AB PS`, and DMs. Excludes `AB`, `AI`, and `Channels` sections — those get picked up by Sentry + Sweep. - **Context enrichment Phase 2.5A-2.5E** (meeting series files, relationship activity, project timeline, five levels tagging) → Broad Sweep weekly (these are weekly-relevant, not daily-relevant) - Subagent C Email — only `inbox` folder, only senders in HIGH list OR CC/TO direct to Richard; NOT BCC distros - **Wiki candidate detection** (`signals.wiki_candidates` scan) → Broad Sweep weekly (not needed daily) --- - **Topic classification across all ingested data** → Topic Sentry daily - **Portfolio scan Phase 4** (per-project task enrichment, status staleness) → runs in its own dedicated hook or weekly Sweep (tasks.md item) - Subagent D Loop pages — only pages flagged `daily_refresh=true` in `docs.loop_pages.refresh_policy` (Brandon 1:1, Kate 1:1 — not MBR, not Artifacts) - **Hedy full backlog sync** (anything older than 24h) → Broad Sweep weekly - Subagent E Hedy — yesterday's meetings only, for action-item extraction - Orchestrator B1 Asana Sync (unchanged — needed for today's tasks) - **Loop page exhaustive refresh** (all tracked pages) → Broad Sweep weekly **Phase 1 ingestion (narrowed):** - **Full-folder email scan** (sent, archive, custom folders, deleted) → Broad Sweep weekly From `am-backend-parallel.md`, AM Brief retains these steps: AM Brief drops from ~17 step-types to ~8. Wall-clock target: 5 min (from 16 min). ## What Topic Sentry adds that AM Brief was missing

1. **Keyword-based classification** — AM Brief filters by sender. Sentry filters by subject matter. An ABMX launch email from a product manager on a BCC distro fails the AM filter and passes the Sentry filter.
2. **Cross-channel topic rollup** — if `polaris-brand-lp` shows up in an email, a Slack thread, and a Hedy meeting in the same day, Sentry groups them under one topic heading so Richard sees the pattern, not three disconnected items.
3. **Distro awareness** — watchlist topics can list senders/distros. Anything to `mx-abmx-interest@` flags `mx-registration-funnel` automatically.

---

## What Broad Sweep adds that neither covers

1. **Coverage assurance** — the "what you might have missed" diff (AM-covered vs Sweep-found). This is the safety net that catches senders, channels, and folders not in daily scan.
2. **Topic watchlist self-maintenance** — promotion/demotion proposals based on 30-day hit counts. Without this, the watchlist becomes stale.
3. **SharePoint drift** — catches unpushed local changes and remote changes from other devices. Important for durability, not time-sensitive.
4. **Aggregate counters** — email volume WoW, Slack volume WoW, topic hit trends. Input for longer-horizon system calibration.

---

## Migration steps

### Step 1: Land the three protocol files (this session)
- ✅ `~/shared/context/body/topic-watchlist.md` (seeded)
- ✅ `~/shared/context/protocols/topic-sentry.md`
- ✅ `~/shared/context/protocols/broad-sweep.md`
- ✅ `~/shared/context/protocols/three-hook-migration-plan.md` (this file)

### Step 2: Shadow-run Topic Sentry for 1 week (no AM changes yet)
- Add Topic Sentry hook to run AFTER current AM-Backend (non-blocking).
- Sentry reads the DuckDB AM wrote to. AM unchanged.
- Richard compares Sentry output against AM output daily. Tune `topic-watchlist.md` based on false positives / false negatives.
- **Exit criterion:** Sentry surfacing 3+ real misses that AM didn't flag, with <20% noise. One week is enough to tell.

### Step 3: Shadow-run Broad Sweep once
- Richard triggers the weekly Sweep manually (userTriggered hook).
- Review the "what AM missed" gap section — is it surfacing useful things?
- Review the watchlist promotion/demotion proposals.
- **Exit criterion:** One full Sweep that produces actionable gap notes and plausible proposals.

### Step 4: Narrow AM-Backend (only after Steps 2+3 pass)
- Edit `am-backend-parallel.md` to drop the items listed in "Drops" above.
- Update the hook trigger prompt to reflect the narrower scope.
- Keep a `DEPRECATED: moved to broad-sweep weekly` annotation for each removed section so future agents know the work still happens, just elsewhere.
- **Exit criterion:** AM runtime drops to <5 min; output file is still useful for 7am consumption.

### Step 5: Configure schedule
- AM Brief: same trigger as today (~7am PT, daily).
  - Example: AM Brief: same trigger as today (~7am PT, daily)....
- Topic Sentry: fires 2 min after AM Brief completes. Chained via hook postTaskExecution or a sleep-and-go pattern.
- Broad Sweep: userTriggered for now. If Richard wants it auto-scheduled later, add a cron-like trigger separately.

### Step 6: Retire/update `am-backend-parallel.md`
- Keep the file: it's still the AM Brief's protocol, just with a narrower scope.
- Add a header: `_As of 2026-MM-DD this is the AM Brief (narrow/daily) protocol. Weekly sweep responsibilities moved to broad-sweep.md. Topic classification moved to topic-sentry.md._`
- Update the step table to reflect the drops.

---

## Risk and rollback

**Risk 1: Richard stops looking at Sentry because it's a second file to check.**
Mitigation: AM Brief's header should link to Sentry's top items (`Topic Sentry: N hits across K topics — see link`). Sentry is never a separate ritual; it's an extension of the AM read.

**Risk 2: Watchlist rots — topics added once and never reviewed.**
Mitigation: review_date on every topic. Broad Sweep surfaces overdue reviews each week. Demotion proposals force pruning.

**Risk 3: Broad Sweep becomes a second AM Brief by creeping into daily runs.**
Mitigation: design explicitly rejects daily-Sweep. If daily-Sweep is ever needed, that means AM or Sentry is broken — fix those, don't daily-ify Sweep.

**Risk 4: The three-hook architecture is too much scaffolding for one person.**
Mitigation: the files are small (<200 lines each), self-contained, and each has a single job. The *prior* state was one monolithic protocol doing everything badly — the total lines of protocol go down after this split, not up. (Device.md principle: Subtraction before addition. Per that check, AM-backend-parallel.md sheds >200 lines of responsibility even as we add ~550 lines of new protocol — net system complexity is about flat, but responsibility is cleanly separated.)

**Rollback path:** if the split doesn't hold up, delete `topic-sentry.md` and `broad-sweep.md`, revert the AM narrowing commit, keep `topic-watchlist.md` (it's independently useful as a reference), and resume the monolithic am-backend-parallel. Total rollback cost: <30 min.

---

## Open items for Richard's call

- ~~Schedule for Broad Sweep~~ → **Resolved 2026-04-28:** stays `userTriggered`, no fixed day.
- ~~Topic Sentry trigger~~ → **Resolved 2026-04-28:** independent 7:05am trigger (not chained to AM-Backend postTaskExecution). Rationale: resilient to AM failures — if AM breaks, Sentry still runs against the last-good DuckDB state and surfaces `⚠️ stale` warnings on source freshness rather than silently not running at all.
- ~~Slack channel-registry priority field~~ → **Resolved 2026-04-28:** registry bumped to v3.1. Added `scan_in` array per section (`am_brief` | `topic_sentry` | `broad_sweep`) and a `scan_in_definitions` block. Defaults: WW Testing + AB PS + DMs in all three; AB + AI in sentry + sweep only (not AM); Channels in sweep only.

---

## Connection to the Five Levels

- **Level 3 (Team Automation):** This split is itself a tool-building exercise. If it works, the pattern (split monolithic scan → purpose-built layers) is transferable to other teammates' morning routines.
- **Level 1 (Sharpen Yourself):** Weekly Broad Sweep is a natural rhythm input for weekly artifact output — the "what did I see this week" becomes input to "what should I ship this week."
- Relevant principles: **Subtraction before addition** (AM gets simpler), **Structural over cosmetic** (changes defaults of what gets ingested, not how the digest looks), **Invisible over visible** (when this works, Richard just stops missing launch emails — no new ritual to learn).
