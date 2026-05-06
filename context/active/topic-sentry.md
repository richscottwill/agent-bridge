# Topic Sentry — 2026-05-06

_Scan window: Hedy live 24h (2026-05-05 11:00 → 2026-05-06 11:00 PT) · DuckDB last-good-ingest 24h (2026-05-03 14:30 → 2026-05-04 14:30 UTC) · 48–72h ingestion gap explicitly called out below._
_Watchlist: 16 active topics (5 P1, 6 P2, 3 P3, 2 monitoring). Hits: 17 sources across 10 topics._

**Five Levels coverage (by hit count):** L1: 0 · L2: 9 · L3: 2 · L4: 1 · L5: 0 · operational: 5

⚠️ **L1 quiet 7+ days** — Sharpen Yourself radar has no dedicated watchlist topic; structural coverage gap (consistent with 5/5 sentry).
⚠️ **L4 quiet — 1 hit in 7 days** — AI Max surfaced only in `ab-paid-search-global` Quip reference; zero AEO / AI Overviews / Zero-Click chatter. Kate/Todd-originated L4 signal non-existent this window.
⚠️ **L5 quiet** — expected, future level.

⚠️ **Source freshness:**
- `signals.emails`: last ingest 2026-05-04 14:43 UTC (~48h ago, ops.data_freshness `is_stale=FALSE` flag misleading — cadence lagged)
- `signals.slack_messages`: last ingest 2026-05-04 14:41 UTC (~48h ago)
- `docs.loop_pages`: last ingest 2026-05-03 13:18 UTC (~72h ago, 0 pages modified in last 7 days — nothing new in MBR/QBR Loop)
- `signals.hedy_meetings`: **intentionally not in DuckDB per directive.** Sentry reads Hedy live via MCP (`GetSessionDetails`). Four sessions covered this run.

What this means: **24h DuckDB window reflects 5/3 afternoon → 5/4 afternoon UTC, not today.** The last 48h of Slack/email is missing. Strongest live signal is Hedy coverage of 5/5 — richer than what DuckDB would have captured anyway.

---

## P1 — must surface

### polaris-brand-lp (5 hits)
_Why: Active cross-market dependency. Brandon committed Richard to Google Experiment path before 5/5 AU handoff. Italy P0 ref tag regression proved rollout process is load-bearing._

- [5/5 hedy weekly-sync] Richard — "Polaris brand LP testing: AMO updates not reflecting live due to caching issue in CS. Weblab is ready, just needs content push. Expected resolution in next few days, then QA pass, then dial-up." — full recap in session `qbgFqERRUQl6Eh2PcI8S`
- [5/5 hedy brandon-1on1] Brandon — "[AU handover is today] brand landing pages haven't rolled out for Mexico yet. You should have the opportunity to repeat these ongoing projects in every weekly update — like Andrew does. Would be a forcing mechanism to keep on top of it." — session `Qz26yMKVFzAWAiU99ZoD`
- [5/4 email 08:54] Matis Bodaghi — "[MCS-3004] A/B Testing & Personalization - WW PS Brand Polaris Redesign: let me know when the pages are ready for the weblab to be dialed up"
- [5/4 slack #ab-paid-search-abix] Brandon — "ok Richard I've got my feedback in the AU Transition doc. Can you look through? Yun-Kang if you get some time, take a look if there's anything missing. Add the month the A.com LP test took place and any data point you have on it." (richard_mentioned, relevance 100)
- [5/4 slack dm-asana-bot] Vijeth Shetty (via Asana mention) — "ps-brand pages updates WW: Symphony cannot serve distinct auth vs non-auth experiences; both versions now lead to registration flow. International markets..." (richard_mentioned)

### au-handoff (4 hits)
_Why: Handoff target was 5/5 (today). Every late-breaking AU signal decision-relevant until Megan is fully onboarded._

- [5/5 hedy] Lena/Richard/Megan — "AU Paid Search Handover and Performance Review" — 81 min handover covering: source-of-truth reporting (Hubble actual, GenBI directional only, Adobe Ad Cloud for impressions/clicks), ref tag structure at keyword level (not ad level), AU no-IECCP until year-one mark, Max Clicks bidding through Google (Adobe bidding experiment reverted), Baloo WW ex-US 2027 timing, FX rate workflow via AB Marketing Finance, Megan taking over R&O from next month. Follow-ups: Richard owes Megan Adobe Ad Cloud recurring exports + Adobe Analytics access via Dwayne's team. Session `j7nQYyfUFwwAbzM6LGZv` (no recap auto-generated — transcript only).
- [5/5 hedy weekly-sync] Brandon — "Kate's Offsite Mon–Fri next week. I'll be flying Monday and Friday, limited availability." — affects all handoff follow-up coordination
- [5/4 email 02:35] Lena Zak — "AB AU Paid Search - Broader handover" (empty preview but email exists — likely doc distribution to stakeholders)
- [5/4 slack #ab-paid-search-abix] Brandon — same AU Transition doc feedback thread as polaris-brand-lp

### ww-testing-methodology (1 hit)
_Why: Testing Approach doc is formalization of PS testing authority. Any leadership mention is strategic signal._

- [5/1 email/asana] Asana digest — "ABPS - WW Testing Projects / Create Intro Guide — Brandon changed the due date to Wednesday" — project-layer ping, not doc-level discussion

### oci-rollout (3 hits)
_Why: AU and MX still TBD; each quarter without AU OCI forgoes 18–24% reg uplift._

- [5/5 hedy weekly-sync] Stacey — "OCI only a week in for new markets, not concerned yet. CA OCI transitioned to 100% tracking per 4/29 msg."
- [5/5 hedy AU handover] Lena — "AU doesn't have IECCP until year-one mark. Data science extremely limited throughput — don't expect it on roadmap this year. Even after setup, Canada kept high IECCP threshold for multiple years as emerging market (standard is 50%)."
- [5/2, 4/30, 4/29, 4/28, 4/27 emails] Adobe Advertising Cloud Search — 5 automated "OCI Tracking Template has completed" reports (measurement-only, not strategic)

### mx-registration-funnel (0 hits)
_Why: MX reg funnel changes shift CPA math directly._

- No keyword-level hits in window. **But note:** 5/5 MX Hedy session surfaced registration-flow signal (M-Shop app share of regs 34% → 69% post-Sparkle) which would have hit here if keywords included "M-Shop" or "app registration." Worth tuning on next watchlist pass.

---

## P2 — worth knowing

### sparkle-and-baloo (3 hits)
- [5/5 hedy MX sync] Lorena/Richard — "Sparkle ended 4/30. Peaked week 15, decreased toward May. M-Shop app share of registrations went 34%→69% post-Sparkle. Testing paid social halo hypothesis on brand search. Richard pushing budget up to hit higher IECCP."
- [5/3 slack dm-brandon] Brandon — "I think justifying MCS tech is tough since everyone expects us to use Baloo long term...so it straps us solely to Brand experiences"
- [5/3 slack dm-brandon] Brandon — "I had done some playing with Baloo as well and put together this doc with some of the issues/suggestions I have" [BalooTesting.pptx — B2B/B2C experiences testing, sign-in]
- [4/30 email] Cansu Ozturk — "[BALOO-8] [BalooEarlyAccess][FeatureName][refmarker attribution persist]"
- [4/28 email] Richard self — "Budget follow-up (reply to Lorena): Forecast with SPARKLE increased expected budget from $577K to $1.2M roughly 2x"

### mx-budget-ieccp (3 hits)
- [5/5 hedy MX sync] Lorena — "R&O budget transition to AB Finance expected end of next week. Richard to update monthly breakout."
- [5/5 hedy brandon-1on1] Brandon — "PO management eats too much time. Not a value-add. OP1 request to automate PO/Google Ads data integration." Richard flagged interest.
- [5/4 slack dm-asana-bot] Asana — "Asana moved this task from 'WW' to 'NA' - Move LR Negative to NA MCC - catch any customers who may cross into CA"

### liveramp-enhanced-match (4 hits)
- [5/5 hedy weekly-sync] Richard — "Had a call with LiveRamp on enhanced match yesterday. F90 blocked at InfoSec TPS approval — no owner assigned per Joel. Media team estimates end-of-May but that's unreliable."
- [5/3 email] Remi Schader — "[EXTERNAL] Invitation: LiveRamp | Amazon Business @ Mon May 4"
- [5/3 email] Remi Schader — "[EXTERNAL] Canceled event with note: Amazon Business x LiveRamp — Monthly Status"
- [5/1 email] Brandon via Asana — "Legal SIM no longer on hold, asking for call with LR next week" (Enhanced Match Legal comment) — high priority

### f90-lifecycle-legal (5 hits)
- [5/5 hedy weekly-sync] Richard/Brandon — "F90 TPS approval stuck at InfoSec with no assigned reviewer. Joel confirmed end-of-May ETA is unreliable because no one is looking at it."
- [5/5 hedy brandon-1on1] Brandon — "F90 — you're supposed to reach out to LiveRamp. I ended up doing it. I sat in your queue for some time. That's where I want you to really spend time actioning on these."
- [5/1 email] Brandon via Asana — "Enhanced Match Legal SIM no longer on hold"
- [4/29 slack dm-brandon] Brandon — "Oh! Also they were wondering if we can create a filter for our F90 audience; like if there's a setting in LR that can use the reg date they're going to send"
- [4/29 slack dm-brandon] Brandon — "can you add the Legal approval in the F90 request within the Media Tech SIM? They just want to see that it's approved"

### reftag-and-attribution (3 hits)
- [5/5 hedy AU handover] Lena — "Ref tags are at the keyword level (not ad level) for AU. Changing structure breaks ABMA/WBR reporting. Create new ref tags for new keywords but follow established structure. Adobe Analytics owned by Dwayne's team — separate ticket for Megan's access."
- [4/27 email] Hedy AI — "Hedy Session Recap: AB Marketing RefTag Taxonomy Workshop"
- [4/27 email] Amazon Meetings Summary — "Workshop AB Marketing Reftag Bonanza & Working Session — Mon Apr 27 9-11AM PDT, 1h46m, comprehensive workshop to build robust [ref tag taxonomy]"

### ai-search-aeo (1 hit)
- [4/30 slack #ab-paid-search-global] J Slater — "Sharing the Quip link I've been maintaining to gather all of our questions related to AI Max that we wanted to discuss with the Google team — https://quip-amazon.com/LmwJABXtAAQu/AI-Max-Questions"
- Additional context from 5/5 weekly Hedy: team scheduling internal review of AI Max questions before Mike/Google call; initial AMX launch planned end-of-May

### kiro-agentspaces-tooling (7 hits — all infrastructure noise)
_Mostly AgentSpaces bug reports and tooling digest channel chatter, not strategic tooling-adoption signal. Keyword tuning opportunity: "kiro" is too broad._
- [5/4 slack agentspaces-interest] Jesse Alcaraz — Outlook MCP returning empty email data (known issue in AgentSpaces — directly relevant to this sentry's ingestion staleness)
- [5/3 slack agentspaces-interest] Weekly digest — AgentSpaces /clear doesn't clear context, known looping bug
- [5/3 slack cps-ai-win-share-learn] — "Built V1 with Kiro" customer-onboarding checklist tool
- [5/2 slack amazon-builder-genai-digest] James Hood — Kiro CLI Voice Mode Preview, agent-generated CR guides
- [5/2 slack agentspaces-interest] Manohar Swamynathan — AgentSpaces browser UI "failed to start" bug
- [5/1 slack agentspaces-interest] Kyle Franke — AgentSpaces restart / context persistence issue
- [5/1 slack agentspaces-interest] William Chong — stale message rendering bug
- [4/30 slack mpdm-kiro-demo-prep] Brandon — "Still working with David on Kiro demo time allocation. Setup a few slides for your section." (richard_mentioned)
- [4/28 email] Machine Learning University — "May 7 Tech Talk: Work Smarter with Kiro IDE"

---

## P3 — background radar

### genbi-adobe-attribution (2 hits)
- [5/5 hedy AU handover] Brandon/Richard — "GenBI has all the correct data but time-mismatch between cost and registration (infrastructure). For actual registrations, only Hubble. GenBI good for channel comparison at high level but breaks down when stitching platform-side with registration data."
- [5/4 slack mpdm] Mukesh — "Hey Richard, how do we do this today? Just wondering where we will get this data from in scalable way. If we find that, we can ingest this to GenBI for self serve analysis" (richard_mentioned)

### ad-copy-and-creative (0 hits)
- No hits in window. Modern Search / UK Phase 1 quiet.

### competitor-intel (0 hits)
- No hits in window.

---

## Monitoring

### new-markets (0 hits)
### org-changes (1 hit)
- [4/30 email] Todd Heimes — "PSME Seattle Summer Party" (high priority, Todd-direct)

---

## Footer

**Review dates:**
- None overdue as of 2026-05-06. Nearest: `au-handoff` review 2026-05-15 (9 days — **should sunset soon if Megan handoff sticks**), `polaris-brand-lp` review 2026-05-31.

**Watchlist tuning candidates:**
- `kiro-agentspaces-tooling` keyword "kiro" fires on bug reports in agentspaces-interest channel. 7 hits / 0 strategic. Consider narrowing to `"kiro power"`, `"kiro hook"`, `"agent adoption"`, `"prompt repository"`, `MCP Registry` — drop bare "kiro".
- `mx-registration-funnel` missed the M-Shop app surge (34%→69%) because keywords don't cover mobile app registration share. Add `"M-Shop"`, `"mobile app registration"`, `"app share of regs"` on next revision.
- **New topic candidate:** `op1-planning` — surfaced consistently in Hedy weekly (5/12 first draft, 5/20 final), Asana OP1 intake thread, dm-brandon OP1 Tech coordination. Combined 5+ hits this run across weekly-sync + 1:1 + Asana. Still not on watchlist as of 5/5 sentry — 2-day repeat = pattern. Recommend P2 add.

**Hedy coverage this run (live MCP — not DuckDB):**
- `qbgFqERRUQl6Eh2PcI8S` (5/5 weekly team sync, 66 min)
- `FKZWlEQGcW5S2tv3FCav` (5/5 MX Paid Search, 31 min)
- `Qz26yMKVFzAWAiU99ZoD` (5/5 Brandon 1:1, 34 min)
- `j7nQYyfUFwwAbzM6LGZv` (5/5 AU handover Lena→Megan, 81 min — no auto-recap, transcript-only)

**Next scan:** when AM-Backend relands fresh ingest (ops.data_freshness will update). If Outlook MCP 401 persists per the agentspaces-interest thread, Sentry stays Hedy-plus-stale-DuckDB until Jesse's fix lands.
