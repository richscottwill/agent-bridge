# Slack Digest — 2026-05-06

**STATUS: STUB DIGEST — Slack MCP auth failure**

- **Ingestion window:** 2026-05-04 14:35 UTC → 2026-05-06 14:50 UTC (~48 hours of backlog NOT fetched)
- **Messages ingested this run:** 0 (MCP auth blocked)
- **Thread replies fetched this run:** 0 (MCP auth blocked)
- **Failure:** `Failed to read Midway cookie jar file. Run mwinit to generate the cookie jar. Reason: ENOENT /home/prichwil/.midway/cookie`
- **Remediation:** Run `mwinit` on Richard's workstation before next AM cycle. Slack MCP has now failed 2 consecutive runs (2026-05-06 00:00 UTC and 2026-05-06 14:50 UTC).
- **Fallback content below:** Top Signals and Unanswered sections are hydrated from existing DuckDB rows (last successful ingestion 2026-05-04 14:41 UTC). These are STALE by ~48 hours — treat anything time-sensitive as out of date.

## By Channel

No fresh channel content. Per-channel `last_read` timestamps in `slack-scan-state.json` have NOT been advanced — next successful run will pick up the full 48h backlog plus anything since.

For context on where Richard's unreplied items sat as of the last successful scan, see the Unanswered section below.

## Signals top 7d

*Source: `signals.signal_tracker` WHERE last_seen ≥ now - 7d AND is_active = TRUE. No reinforcement applied this run.*

1. **polaris-brand-lp** (strength 2.73, 4 mentions, Brandon Munday) — Dwayne can only set Polaris Weblab when control leads to MCS; AU/MX direct to reg start need alternate testing method (Google experiment). Richard owns the handoff.
2. **op1-forecast-flat-budget** (strength 2.07, 3 mentions, Brandon Munday, ab-outbound-marketing) — Budget flat YoY per Kate/Todd. Break out Small SMB for SSR Reg. Reforecast RoY 2026 using OP2 budget.
3. **au-cpa-cvr** (strength 2.36, 3 mentions, Brandon Munday, ab-paid-search-abix) — AU CPA/CVR thread tied to Polaris brand LP testing decision.
4. **au-transition** (strength 2.07, 2 mentions, Brandon Munday, ab-paid-search-abix) — AU Transition doc awaiting Richard's review. OLDEST unreplied Brandon ask (since 2026-04-24).
5. **op1-strategy** (strength 1.95, 5 mentions, cross-channel incl. hedy) — OP1 planning context spanning Slack + meeting transcripts.
6. **polaris-brand-lp** DM-level (strength 1.66, Brandon, dm-brandon) — same thread resurfacing in 1:1 DM.
7. **polaris-brand-lp** ab-paid-search-global (strength 1.66, Brandon) — same thread in public channel, team visibility.

## Unanswered (Richard has not replied)

*Source: `signals.slack_messages` WHERE richard_mentioned = TRUE AND no Richard reply in thread or newer Richard message in channel. Last 14d. STALE as of 2026-05-04 14:41 UTC — Richard may have replied since but we can't see it.*

1. **ab-paid-search-abix — Brandon Munday (since 2026-04-24, ~12 days old):** "ok @Richard I've got my feedback in the AU Transition doc. Can you look through?" — also asks for A.com LP test month + data point. **HIGHEST PRIORITY — oldest Brandon ask.**
2. **ab-outbound-marketing — Brandon Munday (2026-05-01):** OP1 owners — budget flat YoY, break out Small SMB, reforecast RoY 2026. Affects AU/MX forecast work.
3. **ab-paid-search-global — Brandon / Yun-Kang / Andrew (2026-05-01):** Brandon anointed Richard as single owner for MCS team follow-up. Yun-Kang + Andrew both pinging for status/summary on what changed after Richard's communication with MCS team.
4. **mpdm-rasanmol-prichwil-mpgupta — Mukesh Gupta (2026-05-03):** "How do we do this today? Where will we get this data from in scalable way. If we find that, we can ingest to GenBI for self-serve." — GenBI/data scalability question.
5. **dm-meganos — Megan Oshry (2026-04-30):** Adobe Analytics access request + query share for conversion data.
6. **dm-asana-bot — Vijeth Shetty (2026-05-03):** mentioned Richard in comment on "ps-brand pages updates WW".
7. **mpdm-kiro-demo-prep — Brandon Munday (2026-04-28):** Kiro demo prep — Richard needs to set up slides for his section. Sample decks: Orcha (Nikko) + OmniAI.
8. **mpdm-peteocam-ssserene-brandoxy-prichwil — Peter Ocampo (2026-04-26):** Requested Brandon + Richard be added to AB PD26 date disclosure for Paid App Marketing strategy visibility.
9. **dm-peteocam — Peter Ocampo (2026-04-26):** PAM plan for Prime Day — budget + YoY comparison + projected impressions/taps/installs.
10. **ab-paid-search-abix — Brandon Munday (2026-04-24):** Polaris Weblab AU/MX direct-to-reg-start issue; Richard to set up alternate measurement method.

## Notes

- Digest content below the top section is re-hydrated from DuckDB to keep AM-Frontend functional. Do not treat as a fresh scan.
- All 4 required writes that depend on new Slack data are SKIPPED this run:
  - `slack-digest.md` — WRITTEN (stub, this file)
  - `slack-scan-state.json` — UPDATED with error flag (last_scan_ts NOT advanced)
  - `signals.slack_messages` INSERT — SKIPPED (0 new messages)
  - `signals.signal_tracker` UPSERT — SKIPPED (no new data to reinforce)
- Run `mwinit` and retry to break the 2-failure streak.
