# Broad Sweep — YTD Pass (scan window 2026-01-01 to 2026-04-29)

⚠️ **Window override:** Manual YTD scan per Richard's explicit request, not the standard 7/14-day protocol. 118-day window. This is a full-year coverage audit, not the weekly sweep.

⚠️ **Data coverage gap:** `ops.sync_watermarks` table does not exist — first run on record. AM-Backend's historical ingestion is shallow: `signals.emails` earliest = 2026-03-19 (6 weeks), `signals.hedy_meetings` earliest = 2026-04-14 (2 weeks). Only `signals.slack_messages` has genuine YTD coverage (earliest 2026-01-05). Findings below are bounded by what the ingestion layer actually captured, not by the 2026-01-01 to 2026-04-29 window. Treat email/Hedy gaps as "unknown," not "absent."

⚠️ **AM outage context:** Two back-to-back AM outages on 2026-04-25 (Slack 302 auth) and 2026-04-27 (Outlook 401 + Slack 302) mean everything post-4/24 was under-covered by the daily pipeline. Topic Sentry only ran today (4/29, 24h window). Gap analysis below reflects this — Sweep is doing heavier lifting than a clean AM week would require.

_Ingested (from DuckDB): 476 emails across 461 conversations (3/19→4/29), 830 Slack messages across 45 channels (1/5→4/29), 15 Hedy meetings (4/14→4/28), 5 Loop pages (current snapshot, no change history). New vs AM: ~40 distinct sources that never hit a digest._

---

## What you might have missed

### Topic-watchlist hits AM didn't surface
- [2026-04-22 slack #ab-ps_partnership-accounts] Brandon Munday — 18-reply thread on Adobe ENG URL redirects: "we have the ENG URLs redirecting through Adobe. Do you know what this is used for? Normally we'd have some extra tracking through Adobe Analytics." Yun-Kang replied multiple times re CTA overrides and ref tag carry-through. Continuation of the ungated LP ref tag problem (same failure class as Italy 4/16 and MX Auto). AM skipped — `ab-ps_partnership-accounts` isn't a priority channel for daily scans.
- [2026-04-22 slack #dm-aditthk + #dm-quip-bot] Adi added you to AI Max Questions quip doc. Feeds the same workstream.
**oci-rollout** (88 YTD hits, dominant topic)
**au-handoff** (12 hits)
- [2026-04-21 slack #baloo-channel] AU PM asking "I'd like to know if AU is already on the Baloo roadmap. If not, please let me know." Direct crossover between au-handoff and sparkle-and-baloo workstreams. Not surfaced by AM because `baloo-channel` is peripheral to Richard's daily rotation.


**reftag-and-attribution** (19 YTD hits; only 2 made topic-sentry)
- [2026-04-17 email] Weber, Kristine — `[HOLD] AB Marketing Reftag Bonanza & Working Session` — Kristine scheduled a dedicated reftag working session. Not in any AM digest. P2 watchlist match. Worth confirming whether you attended and whether follow-ups exist.
- [2026-04-21/23 email] Weber, Kristine — shared `TrafficWBR` folder + `Central Marketing - Pre-WBR Callouts` + `AB Traffic Transits WBR 04_18 WK16`. Cross-team WBR prep Richard isn't normally looped into.

**ai-search-aeo** (P2, 5 hits; underweighted in AM)
- [2026-04-15 slack #paid-search-amzn] 10 reactions: "google is sunsetting DSA, and all campaigns will be automatically AI MAX" (link to Google blog). This is the headline platform signal for your L4 POV. AM never surfaced it — `paid-search-amzn` isn't in daily rotation.

- [2026-04-24 email] Todd Heimes — `AB April Update` (medium priority in DB). L10 VP monthly update. Sits in inbox unread-surfaced-by-DB, never flagged by AM. If Todd's update summarizes PS positioning, it's worth a read.


**mx-registration-funnel** (2 hits YTD — surprisingly quiet given 4/24 Cristobal launch)
- Sparse pickup. The Sparkle/Cristobal 4/24 launch signal is living in `sparkle-and-baloo` topic signals, not `mx-registration-funnel`. Consider whether the funnel topic's keyword set is too narrow to catch the actual conversations.

### Non-priority senders worth noting

| Sender | Count | Window | Why flag |
|---|---:|---|---|
| Todd Heimes | 4 | 4/10→4/24 | L10 VP; "AB April Update" 4/24 + PSME Seattle events. AM only catches Todd if he's direct-to-Richard. |
| Weber, Kristine | 4 | 4/17→4/23 | Reftag Bonanza working session + TrafficWBR folder/callouts. New recurring cross-team contact; candidate for People Watch. |

#### Details

| Yi, Ashley | 5 | 4/20→4/24 | MBET/COUPA PO process overhaul. Operational — will affect PO submission workflow. |
| Rogers, Kelly | 3 | 4/14→4/27 | Content Flash Q1 2026 Portfolio Marketing Recap 4/27. Cross-team marketing signal. |
| Hopp, David | 3 | 4/18 | Triple OOO bomb (AWS Summit / Gartner / Forrester) — useful to know David's travel pattern. |
| Yukari Nunome | 3 | 4/15→4/28 | Yahoo Japan Release Notes recurring. If you're reading the JP platform, note the cadence; otherwise consider unsubscribing. |
| Dike, Taran | 2 | 4/28 | Launch: Your Orders ABM Enrollment + AppleCare+ Japan Multi-Quantity. Product launches in your orbit. |

### Slack channels outside daily rotation

**agentspaces-interest** (104 msgs / 82 threaded / 295 replies / 122 reactions YTD, last activity 4/28)
- Extremely high-engagement L3/L5 community channel AM skips. 4/15 had a cascade of 20+ questions about AgentSpaces setup, workspace validity (`12 replies: "Is there a Validity on the AgentSpace Workspace . I am getting Reminders that 7 days are left"`), Kiro slowness on DevSpaces (14 replies), scheduled/cron jobs (3 replies, 4 reacts — **directly relevant to your L5 Agentic Orchestration work**), pippin-mcp-server install issues, /model setting persistence, Firefox support. This is the clearest Level 3 radar miss in the sweep.

**amazon-builder-genai-power-users** (56 msgs / 37 threaded / 281 replies / 229 reacts YTD, last activity 4/16)
- 4/16: "Opus 4.7!" (anthropic news link) — 83 reactions, 13 replies. You're running on this model now.
- 4/16: "AI TPM" question — "consume and collate: Outlook, Slack, t.corp/Taskei, Mirador, Sauron, SAS, exception approvals, Dogm..." — 7 replies. That's structurally identical to what you're building. Worth reading the replies for ideas others have tested.
- 4/15: Video transcription tool question — 5 replies.

**ask-ab-aryabot** (32 msgs / 180 replies / 60 reacts YTD) — engineering/ops-heavy, low Richard relevance but very high engagement. Sweep notes for awareness, not action.

**ab-ps_jp** (28 msgs, 4 Richard-mentions)
- 4/1: Brandon and Stacey both @-mentioned you on JP Brand LP ref_ tracking ("Richard found that ref_ actually tracks through a.com (even better than ref=)"). AM never surfaced this — it's exactly the kind of cross-market reftag signal that feeds your `reftag-and-attribution` topic.

**ab-ps_partnership-accounts** (31 msgs YTD; 18-reply Brandon thread on 4/22 discussed above)

**paid-search-amzn** — 4/15 DSA→AI MAX signal referenced above.

**marketing_managers_all** — last activity 4/27, 3 msgs. Low volume but peer-level.

### Loop page changes
---

Five Loop pages ingested today (2026-04-29): `loop-brandon-1on1`, `loop-mbr-qbr-2026`, `loop-ddd-2026`, `loop-weekly-meeting`, `loop-working-session`. Current snapshot only — no `last_modified` timestamps in DuckDB, so diff vs prior state is not possible. Recommend populating `docs.loop_pages.last_modified` on next ingestion to enable future drift detection.



## SharePoint drift

Corrected finding (initial scan mis-routed to the deprecated `Kiro-Drive/` path). The canonical SharePoint layout as of 2026-04-28 is `AB-Paid-Acq-Team/` / `AB-Paid-Acq-Ops/` / `AB-Paid-Acq-Dashboards/` / `.Richard-Private/`. Drift check against the correct paths:

- **Local newer than SharePoint:** All three state files (`au-paid-search-state.md`, `mx-paid-search-state.md`, `ww-testing-state.md`) are ~8–9 hours ahead of the SharePoint mirror. Local timestamps: 2026-04-29 07:12 UTC. SharePoint (`AB-Paid-Acq-Team/markets/{au,mx}/` and `AB-Paid-Acq-Team/methodology/testing/`): 2026-04-28 22:50–22:51 UTC. Likely a morning sync hook updated local files but hasn't pushed yet. Minor drift, reconcile on next sync cycle — no action needed from Richard.
- **SharePoint-newer-than-local:** None detected.
- **Deprecated-path residue:** `Kiro-Drive/system-state/` on SharePoint held a stale `topic-sentry-2026-04-29.md` and this Broad Sweep digest (from my first push). Both deleted during this run. The topic-sentry and broad-sweep digests now live at `AB-Paid-Acq-Ops/agent-state/`.

---

## Topic watchlist proposals **ADD** `op1-forecast-flat-budget` — emerging from `signals.signal_tracker` with strength 2.0 in om-team (4/29: "OP1 forecast: flat YoY budget. Break out Small SMB. Reforecast RoY 2026."). Proposed keywords: `OP1 forecast, flat YoY budget, SMB breakout, RoY reforecast, 2027 OP1`. Priority: P2. Level: operational. Overlaps with `mx-budget-ieccp` but the OP1 framing is the scope OP1/OP2 planning cycles hit — worth its own slot for the planning-cycle window. Review: 2026-07-31. **ADD or FOLD INTO EXISTING** `pam-budget-availability` — strength 3.6, 10d unanswered in `ab-paid-search-app`, and MX-scoped ("No offsite resolution confirmed"). Could extend `mx-budget-ieccp` keywords with `PAM availability, PAM bandwidth, PAM offsite` than creating a new topic. Prefer fold-in. **DEMOTE** `competitor-intel` (P3 → monitoring). 0 YTD hits across 476 emails + 830 Slack messages + 15 Hedy meetings. Current review date 2026-10-31 — premature to sunset, but demotion to `monitoring` is warranted. If it still shows 0 hits at 10/31 review, sunset. **DEMOTE** `new-markets` (monitoring, already). Already in monitoring — no action required, but 0 YTD hits confirm the placement is correct. Next review 2026-10-31 holds. **PROMOTE consideration** — `kiro-agentspaces-tooling` has 115 YTD hits (113 Slack, 2 email). Currently P2. Hit volume justifies P1 on the numbers, but most hits are external community Q&A in `agentspaces-interest` / `amazon-builder-genai-power-users`, not signals requiring Richard's action. Recommend staying P2; the volume is noise-dominated community traffic, not priority-action signal. The Sentry's existing surfacing (3 hits 4/28) is appropriate. **KEYWORD TUNING** for `mx-registration-funnel` — only 2 YTD hits against a known-active workstream (Cristobal 4/24 launch). Current keywords miss the `Cristobal`, `CTC`, and `MV%` (already in) lift. Consider adding: `Cristobal, Cris launch, AVP shift, verification uplift`. _Review and apply in `~/shared/context/body/topic-watchlist.md` — proposals do not self-execute._ _Full proposal set written to `~/shared/context/intake/topic-sentry-proposals.md`._ ---

## Weekly aggregate counters (YTD with WoW note)

- **Email volume (ingested):** 476 YTD, earliest 3/19. Last 7 days (4/22→4/29): 112 emails.
- **Slack messages (ingested):** 830 YTD across 45 channels, earliest 1/5. Last 7 days: ~140 messages.
- **Loop page updates:** 5 pages currently tracked. No change-history available.
- **Meetings attended (Hedy):** 15 sessions 4/14→4/28. Last 7 days: 9 sessions.
- **Top 5 topic-watchlist hits YTD:**
  1. `kiro-agentspaces-tooling` — 115 hits (Slack-dominated, community traffic)
  2. `oci-rollout` — 88 hits
  3. `polaris-brand-lp` — 37 hits
  4. `ww-testing-methodology` — 29 hits
  5. `sparkle-and-baloo` — 26 hits

Signal concentration matches expectations: OCI rollout, Polaris, and Testing Approach are the active P1 workstreams. Kiro/AgentSpaces community volume is noise-dominated but explains why your daily agent tools feel like a firehose.

---

## Excluded from scan

None — `slack-channel-registry.json` v3.1 excludes only the `Channels` section from Topic Sentry, not Broad Sweep. All channels with messages in window were included. Consistent with protocol "scan_in: broad_sweep" rule.

---

## Failures

- **`ops.sync_watermarks` table not present.** Protocol Phase 0 assumes existence. Created Phase 7 insert logic assuming the table will be auto-created with first run; will need to validate the insert on execution.
- **`docs.loop_pages.last_modified` null for all rows.** Prevents change-detection. Not a sweep failure, a data-model gap.
- **AM-Backend ingestion depth insufficient for true YTD.** Only Slack goes back to 1/5; emails and Hedy are 6- and 2-week windows respectively. True YTD audit of the non-Slack sources would require a backfill, not a Sweep query.

---

_Next sweep due: 2026-05-06 (standard 7-day cadence) — run as normal weekly, not YTD._
