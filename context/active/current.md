# Active Context — Richard Williams

Last updated: 2026-04-02 (Thursday PT, autoresearch loop run 16)

## Role & Scope
- Amazon Business, Paid Acquisition / Paid Search
- Markets: AU (Australia), MX (Mexico), US (involved in events)
- Manages campaign optimization, keyword strategy, bid strategies, landing page coordination
- Handles Google Ads invoicing and PO management for AU and MX
- Covers MCS WBR callouts when Dwayne is out
- Works with Adobe analytics (AMO access, bi-weekly Adobe sync)

## Active Projects

### AU CPC Benchmark Response (3/19, Kate-visible)
- Lena Zak challenged AB AU $6 avg CPC vs Consumer $0.18-0.50
- Brandon built Loop doc reply — Richard contributed data 3/19
- Key points: B2B keywords higher CPC; AB AU launched June 2025; no Shopping Ads for AB; OCI May 2026 will help
- Status: Response sent. Monitor Kate/Nick reaction.
- 🆕 Brandon sync (3/23): Focus on outlier keyword analysis (top 20 by CPC/CPA), not broad removal. Lena's 3 priorities: (1) keyword CPC/CPA investigation, (2) keyword-to-product mapping, (3) Polaris migration. Brandon offered to join AU syncs. CPC caps are a "two-way door" until OCI.

### Polaris Brand LP Rollout — WW (3/20, Brandon-driven)
- US: Stacey switched to Polaris on 3/24 ✅
- WW: Weblabs needed for AU, JP, EU (DE + FR per Andrew's recco). Brandon confirmed do-no-harm: minimal localization, follow US template.
- ✅ Weblab ticket SUBMITTED (3/21): "WW PS Brand Polaris Redesign" via Taskei. Weblab dial-up targeting April 6-7.
- ✅ Frank Volinsky (MCS-3004, 3/31): CANCELLED sync — Frank got requirements from Alex directly. "No other information is needed at this time." No action needed from Richard.
- ✅ Vijeth Shetty completed ps-brand XF + Template task (Asana 4/1). Alex confirmed: "all nav's look great!" Minimal-nav live for all GEOs. ASIN/Carousel component and EU5 page creation remaining.
- Alex (Asana 3/27): Added Richard to "Page Creation / Page Edit, ps-brand XF + Template" task. Alex checking in with Vijeth on status.
- Brandon's priority: AU > MX > DE > UK > JP > FR > IT > ES > CA > US-ES
- US-ES page: noindex/nofollow, Alex working with Yun
- Action: Create one-page Polaris rollout timeline with dates and owners (OVERDUE — was due last week).

### AU Paid Search Optimization
- MCS → Polaris: FULL SWITCH confirmed by Lena (3/13). Alexis sent mapping (3/17). Migration completing 3/24-25.
- W13: NB regs -9% WoW, CPA $132. Lena wants weekly CPA review.
- .co.uk URL issue RESOLVED (3/16).
- 🆕 Richard sent AU PS Weekly Update (4/1): Updated weekly performance doc with W13 decline analysis (traffic-driven + CVR drop) and keyword-level performance report. Alexis thanked him. Lena replied with follow-up questions: (1) can we get data with landing page URLs? (2) how many clicks redirect because customer is already logged in? (3) are we overstating CPAs due to repeat visitors? ACTION NEEDED: respond to Lena's questions.
- 🆕 Brandon (Slack 4/1 ABIX): "is there something you need from me for Lena's req? [I haven't looked at it yet, but LMK if so]" — Brandon offering support on Lena's follow-up. Richard confirmed alignment on WW streams strategy. ACTION: Reply to Brandon if help needed.
- Alexis (3/24): Two-campaign structure proposal (product-intent vs business-intent). Biweekly keyword review cadence agreed. MCS page replication from MX model discussed.
- Lena's 3 priorities (via Brandon 3/23): keyword CPC/CPA investigation, keyword-to-product mapping, Polaris migration.

### MX Paid Search
- Kingpin Goals overdue (was due 3/17). Blocked by Andes data.
- MX Auto page due 3/20 (waiting Vijeth footer). MX Beauty — Lorena added inputs for beauty LP (3/25).
- Lorena is now PRIMARY MX PS stakeholder (Carlos transitioned to CPS ~3/17).
- Carlos final PS sync (3/24): shared updated keywords, ad text, escalated ref tag fix. Handoff to Lorena effective.
- 🆕 Lorena needs Q2 expected spend for PO submission (3/25 email). Action required.

### Annual Review 2026
- 🆕 Annual Review shared with Richard (3/24). Overall: Meets High Bar. LP: Solid Strength.
- Brandon's #1 growth area: visibility — "maintaining consistent visibility across all workstreams," "lightweight mechanisms for timely communication," "structured stakeholder documentation."
- Peer feedback: communication/knowledge sharing (3+ peers), project management (2+ peers), Have Backbone (1 peer).
- Strengths: analytical depth, testing expertise, ownership, bias for action, mentoring.
- Persisting gaps (same as Forte 2025): communication, project management, strategic proactivity.

### Paid Acquisition Flash (3/27, Richard wrote sections)
- Richard wrote MX highlight (~100w), AU update (~50w), Bid Strategy Test status, Brand LP Tests status, Paid App status (blocked — needs Andrew).
- MX: NB CPA $267→$112 in H2 2025, sustained $117 YTD 2026 despite +16% CPC. Regs +14% vs H2, exceeding OP2 by 16%.
- AU: keyword audit, CPA optimization, Polaris migration monitoring.
- Bid Strategy: 6 consecutive weeks NB CPC decline (-21%), NB CPA $168→$117. No longer a test.
- Brand LP: US switched March, weblab submitted, dial-up April 6-7.
- Status: Sections written. Flash due 3/30.

### Agent Bridge (3/27, built and live)
- Google Sheets/Docs communication layer between Kiro and personal agent swarm.
- Toolkit: `~/shared/tools/bridge/bridge.py` + CLI.
- Message bus, context snapshots, agent registry, heartbeat monitoring.
- Apps Script automation deployed (bus poller, staleness checker, heartbeat monitor, request notifier).
- 10 Drive folders + 3 new docs (portable body, testing approach, agent protocols) created.
- Status: Live. Richard needs to paste Code.gs into Apps Script editor and run createTriggers().

### Data Layer & Tooling (3/28-3/31, built across sessions)
- Bayesian Prediction Engine: `~/shared/tools/prediction/` — NL question parsing, conjugate priors, posterior updates, credible intervals, auto-calibration, autonomy tracking. 9 modules, 10 test files. CLI: `python3 ~/shared/tools/prediction/predict.py`.
- PS Analytics Data Layer Overhaul: query.py expanded with `db_validate()`, `schema()`, `export_parquet()`, `check_freshness()`, `data_summary()`, agent state functions (`log_agent_action`, `log_agent_observation`, `query_prior_observations`). DuckDB MCP Server configured. 6 PBT test files. Migration scripts for changelog, competitors, OCI.
- WBR Callout Pipeline consolidated: 3 parameterized agents (market-analyst, callout-writer, callout-reviewer). Hook v2 with 6-phase process. W13 callouts produced for all 10 markets. Agent state wired to DuckDB.
- Attention Tracker: `~/shared/tools/attention-tracker/` — full application for local machine (browser monitor, window monitor, idle detector, classifier, event processor, session tracker, state machine, summary, daemon). 34 test files.
- Dashboard ingester ie%CCP bug fixed (was reading CPA instead of ie%CCP ratios).
- Change Log CSVs ingested to DuckDB (477 rows across EU5, MX/AU, NA/JP).
- 🆕 Andrew DM (4/1): Requesting ENG max budget calculation file (audience size × frequency). Brandon mentioned in Andrew's 1:1 — needs recalculation for OP1. ACTION: Share the file with Andrew.

### ABMA-11245: Quick Paid Search Integration (SIM ticket)
- Richard created 3/3. Requests Amazon Quick integration to read from multiple Google Ads MCCs for anomaly detection, budget/bid recommendations, and weekly investigations.
- rasanmol asked mpgupta to groom for sprint planning (3/9).
- Richard followed up 3/30: "Hey all, wondering if this ticket would be possible to action?"
- Status: Open, unassigned. Impact: 4.

### Microsoft Advertising
- 10x "account paused" emails (3/17). Needs triage.

### Paid Search ENG Budget & Coordination (from Slack ingestion)
- 🆕 Y26 OP2 PS ENG budget: $1,851,000 (up from $1M — includes Mauro's campaign $596K + Liveramp $255K). Yun updated finance OP2 file.
- Monthly budget split: for months without events, Kristine's team chooses between Business Essential or Saving Guide.
- Transit WBR early version shared by Kristine's team (2/26) — data hygiene issues being addressed with ABMA.
- ABMA attribution: pulling reftag prefix by ETL + Feature Registry. Ideally just Feature Registry, but both PS-ENG and PS-ACQ folders need monitoring.
- 1-click account switching launched (1/28) — Brandon flagged as opportunity for ENG ads to ensure customers land on AB shopping site.
- BFCM 2025 result: PS was top traffic driver (+105.3% YoY, +147K page hits). Team investigating whether B2C search campaigns contributed.
- Events doc for Todd/Shelley review: due EOW 2/27, review with Shelley 3/5.

### Flash Cadence & Team Dynamics (from Slack ingestion)
- 🆕 Brandon's management style in Slack: direct, deadline-driven, holds team accountable. Called out "very light" Flash inputs (3/23) — listed each person's gap by name. "PLEASE UPDATE THIS TODAY! I expect that moving forward everyone will adhere to timelines."
- Flash inputs consistently due EOD on designated day. Andrew (U0840CQJVUK) manages Flash logistics and reminders.
- Stacey (U02NX7TMMHB) is the most active OCI coordinator — manages tech team interface, data validation, campaign-level tracking changes.
- Yun (U06AQT6EZED) handles EU traffic/ENG, cross-team coordination, budget management. Very responsive in Slack.
- Adi (U09HN78BTL4) handles JP/CA dashboard updates, weekly WW dashboard. Joined team ~Sept 2025.
- Richard (U040ECP305S) handles AU/MX, ABIX, bid strategy, landing page testing, ref tag management. Lower Slack volume but high-signal messages.
- Prime Day marketing brief process introduced (event overview, historical performance, target audience, key messages, goals, KPIs).
- Translation SLA changing 3→4 days for content <500w when JP secondary support ends.
- Memorial Day round 2 assets due Monday 3/30, feedback due Tuesday 3/31.
- Marquee event tags restricted to official event emails only.
- Teams retain existing homepage hero placements for Prime Day.

### OCI APAC MCC Access Issues (3/25, Brandon-escalated)
- Brandon escalated to Google (Mike Babich) — team can't access APAC MCC (852-899-4580) for OCI.
- ab-paidsearch-oci-apac@ hit "too many failed attempts" loop on 2nd verification step.
- ab-paidsearch-oci-apac2@ created, but Google flagged account for deletion on signup.
- Brandon submitted appeal + Google support ticket (case 1-3869000041102).
- Brandon + Richard had call with Mike at 2pm PT 3/25. Mike escalating internally.
- 3/26 update: Google sent "access restored" notice but Brandon retested — still blocked. Mike filed internal escalation (case 6-7924000040915).
- 3/26 11pm: Mike sent 3 follow-up questions: (1) loop him into case 6-7924000040915 thread, (2) confirm if new user access resolved the issue, (3) status of appeal for first user. Brandon needs to respond.
- Impact: JP OCI launch being pushed back until access resolved.
- Richard added to ab-paidsearch-oci-apac2@ email list (3/25).
- 🆕 **OCI WW Launch milestone (Slack 3/31):** FR, IT, ES dialed up to 100%. JP already at 100%. CA on track for 04/07. Kiran Pantham celebrated first QBR goal of 2026. Brandon confirmed Day7 MCM steps. Mukesh Artham created MCM-147368188 for JP tracking template update. Brandon decided to wait on JP ref tag taxonomy update until after tech confirms OCI is working — will discuss with Deepika Thursday.
- 🆕 **JP OCI preflight (Slack 3/31):** Brandon initiating JP OCI enable. Adi confirmed JP Google account: all ref tags unique, no KW/adgroup overrides, search ads only. Stacey raised ref tag taxonomy update question — Brandon deferred to post-launch. Richard asked Stacey about planned changes to JP ref tags (thread active).
- 🆕 **MCM approvals received (Slack 4/1):** All approvals for MCM-147368188 (JP tracking template) received. Tech cleared to proceed with execution. Brandon confirmed Day7 steps look good.
- 🆕 **JP Brand LP Experiment (Slack 4/1-4/2):** Stacey confirmed ref_= carry-over works on a.com. Experiment targeting live 4/2 after CTA experience double-check. Brandon confirmed "sounds good." Stacey also asking (DM 4/1 11:38pm) about CA exclusion from Polaris 50/50 testing on 4/7 — Richard needs to reply with rationale (OCI data clean focus).
- 🆕 **FRITES 100% OCI confirmed (Slack 3/30):** Brandon confirmed FRITES updated to send 100% of traffic through OCI after click volume double-confirmation with tech (FR: 775, IT: 1,412, ES: 1,168 events on 3/24 UTC).
- 🆕 **DE data issue root cause (Slack 3/26):** Yun identified DE registration data loss 3/18-3/25 caused by Amazon-wide DUB→ZAZ/FRA infrastructure migration (Region_Flexibility project). DE maps to FRA (misconfigured), other EU4 maps to ZAZ (correct). Data after 3/25 should be fine. Brandon escalated in WBR — ABMA moved to Sev 2.5.
- 🆕 **EU3 OCI data exclusion (Slack 3/9):** Yun requested Andrew exclude EU3 data from AMO bidding from OCI test start through 3/9/26. Stacey to advise if more exclusion needed. DE 2/27 UTC full day also excluded.
- 🆕 **CCP decision (Slack 2/24):** Brandon confirmed: keep using dashboard CCPs for March (beneficial to team). ieCCP output CCPs will continue improving over time — that's why 3-month refresh cadence was chosen. Don't switch to Jan ieCCP actuals.

### Adobe OCI Rollout
- Discussion (3/19) with Suzane Huynh. AU OCI May 2026 timeline. Adobe Bi-Weekly TODAY (1pm PT).

### Baloo Early Access Cost Planning (3/26)
- Vijay Kumar (Tech) briefed Richard on early access rollout: 50 stakeholders get Tampermonkey script to enable Baloo weblabs.
- Two access paths: direct URL (shop.business.amazon.com) for routine testing, Google search for leadership demos only (5-6 clicks).
- Brandon's MBR concern: internal clicks inflate paid media costs (~$4.43 NB CPC).
- Decision: restrict Google search testing, provide direct URL instead.
- ✅ Richard shared 26 keywords + URLs + tracking params in Quip sheet (3/30) — commented on ABCA-371 Taskei ticket. Deliverable DONE.
- Baloo SIM ticket: ABCA-371 (Aarushi Jamwal assigned).
- Kate attended prior Baloo demo — positive reaction.
- Early access launched EOD Monday 3/30.
- Still need: follow up with Brandon on MBR click-cost guardrails.
- 🆕 **Baloo noindex blocker (Slack 3/31):** Meta tag noindex requirement (V2083026891) not implemented on Baloo pages. Not impacting SEO while behind VPN, but flagged as a launch blocker. 6 replies in thread — being actively discussed. Richard should monitor — this could delay Baloo public launch.
- 🆕 **Baloo ps_kw parameter (Slack 3/17):** Yun flagged that ps_kw is not being passed through when redirecting to Baloo subdomain (shop.business.amazon.com). Brandon confirmed: "yes, please apply some ps_kw, Richard. We can find some decent traffic kws that aren't high reg-drivers." Aarushi Jamwal from Baloo tech to reach out to Richard. 35-reply thread — active coordination between Brandon, Yun, Stacey, Richard.

### AU Paid Media CPA Challenge (Slack 4/1, ab-paid-search-abix)
- 🆕 Lena claiming $80 paid media CPA for AU — team skeptical. Yun found paid offsite showing 0 regs in Hubble.
- Paid Media launched 1/27 (YouTube, LinkedIn, PV Spotlight, Rokt, ADA). Results to be shared in Feb MBR.
- Brandon got insight from Paid Media team: they're using view-through conversions — NOT comparable with PS click-through attribution.
- Yun: "It's a bit crazy to me that she's comparing view through vs actual regs."
- Brandon: "while we don't have data proving that's what she's doing, it makes sense — otherwise she'd be pulling our budget."
- Richard confirmed: "It should still show up as registrations though, right?" — checking OP2 planning from Melissa.
- Lena already connected with Dwayne's team on redirect questions. Richard needs to sync with Dwayne before replying.
- Brandon talking to Dwayne in Friday 1:1 — AU should fold within current redirect plan, not get special treatment.

### R&O Flash Review (3/26, Deep Dive & Debate — Hedy captured)
- Flash content finalized: US Modern Search Structure highlight (renamed from "Portfolio Consolidation" — combines campaign + portfolio consolidation), CA moved to status update (tariff-driven, not team-influenced), AU moved from lowlight to announcements (repurpose Lena CPC content), WhatsApp simplified (remove description, add Amazon-wide scope).
- Brandon frustrated with late Flash submissions — called out team directly.
- DE tech issue: AME central team seeing registration problems, possibly linked to EAAAAA infrastructure project. Too early to include in Flash — wait 5 days for impact data.
- Video strategy: Andrew to specify "unlocking new placements" (YouTube) rather than just "reach."
- App resourcing: Peter advised too early — will message Kate to include in her 1:1 with Todd.
- Richard assigned: AU status update (repurpose Lena CPC content), UK/CA split decision, 10% growth metric clarification, DE tech investigation.

### Adi Sync — AI Ad-Copy Workflow (3/25, Hedy)
- Adi presented AI-powered workflow for JP non-brand ad creatives: input existing ads → AI generates variations → compare D-Pel vs AI translations → enforce 15-char JP limit.
- Richard praised structure, suggested scaling via knowledge bases (account data + LP text).
- Decisions: AI ad copy for JP NB testing with human oversight; D-Pel + AI side-by-side during testing; 15-char compliance as pre-launch validation.
- Action items (Adi): refine workflow, document JP translation rules in Quip, build D-Pel vs AI decision matrix, add spend guardrail (97% pacing target).
- Action items (Richard): schedule 15-min "process-snap" sync to map undocumented hand-offs for post-Oct 2025 projects.

### ATMS Direct Submission
- Continue using GlobalLink until 3/31. Switch to ATMS for project submissions starting 3/31.
- Training materials shared 3/24 (Kiyo Walker).

## Recurring Meetings
| Meeting | Cadence | Key Attendees |
|---------|---------|---------------|
| AB AU Paid Search Sync | Weekly | Alexis Eck, Lena Zak, Harsha Mudradi |
| MX Paid Search Sync | Biweekly | Lorena Alvarez Larrea, Yun-Kang Chu (Carlos transitioned to CPS) |
| Richard & Yun 1-1 | Regular | Yun-Kang Chu |
| Richard/Adi sync | Weekly (Mon) | Aditya Satish Thakur |
| Paid Acq: Deep Dive & Debate | Weekly (Thu) | Brandon Munday, team |
| ACQ Promo OHs | Weekly (Wed) | Saajan Chowhan |
| Pre-WBR Customer Engagement | Weekly | Dwayne Palmer, Kristine Weber, Kate Rundell |
| Bi-Weekly Google + AB Performance Sync | Biweekly | External Google reps |
| Amazon Business // Adobe Bi-Weekly Call | Biweekly | Jen Vitiello (Adobe) |
| Biweekly AB Onsite Events Stakeholder | Biweekly | Caroline Miller |
| Testing Approach & Year Ahead | Apr 16 | Kate Rundell, Brandon, team |

## Key People
| Name | Alias | Role/Context |
|------|-------|-------------|
| Alexis Eck | alexieck | AU POC, MCS page mapping |
| Lena Zak | lenazak | AU country leader. Challenged AU CPC (3/19). |
| Yun-Kang Chu | yunchu | MX, Adobe, Modern Search. Contributed Shopping data for CPC reply. |
| Brandon Munday | brandoxy | L7 manager. Building AU CPC Loop doc. Annual Review context. |
| Carlos Palmos | cpalmos | MX — transitioned to CPS acquisition (~3/17). Final PS sync 3/24. No longer PS stakeholder. |
| Lorena Alvarez Larrea | lorealea | MX Paid Search — NOW PRIMARY PS STAKEHOLDER (replaced Carlos ~3/17). Needs Q2 spend for PO. |
| Dwayne Palmer | dtpalmer | MCS/website, WBR coverage partner |
| Andrew Wirtz | — | Testing collaborator. Active in Loop doc (3/18). |
| Aditya Satish Thakur | — | Weekly sync. OOO 3/19-20. |
| Harjeet Heer | hkheer | Stepped away from AU day-to-day |
| Kate Rundell | kataxt | L8 Director. Visible on AU CPC thread. |
| Sharon Serene | ssserene | Prime Day 2026 Visibility Intake (3/17) |
| Frank Volinsky | — | MX market, page builds. MCS-3004 weblab scoping (3/27). |
| Suzane Huynh | — | Adobe, OCI Rollout Discussion (3/19) |
| Alex VanDerStuyf | afvans | AEM translations, Polaris Brand LP rollout. Submitted AU/MX/JP/CA translations (3/19, due 3/26). |
| York Chen | yorkchen | Back from paternity leave (ended 3/22). JP market. |
| Vijay Kumar | vkumarmp | Baloo Tech lead. Early access rollout. 1:1 with Richard 3/26. |
| Mike Babich | — | Google rep. OCI email creation issues escalation (3/25). APAC MCC access. Latest: 3/26 11pm — 3 follow-up questions for Brandon. |
| Caroline Miller | carolimy | Product Marketing Manager. Biweekly AB Onsite Events. |
| Jen Vitiello | — | Adobe rep. Adobe Bi-Weekly. Sent dinner + meeting invites 3/26. |
| Aarushi Jamwal | aarushij | Baloo Tech team. Assigned on ABCA-371 (Baloo Paid Search flow). |
| Mukesh Artham | arthamm | OCI Tech team. Created MCM-147368188 for JP tracking template. CIT dashboard validation. |
| Yashasvi Chowta | ychowta | OCI Tech team. EU3 dial-up approval coordination. Duplicate hvocijid parameter investigation. |
| Kiran Pantham | kpantham | OCI Tech PM. Celebrated QBR goal. APAC Google account setup coordination. |
| Ayush Aggarwal | aggaayus | OCI Tech lead. MCM approvals. JP issue options discussion. |
| Srinivas Adavi | saadavi | OCI Tech. Congratulated team on launch. |
| Praveen Chandolu | chandop | OCI Tech. Working with Brandon on new APAC account setup. |

## Pending Actions
- [ ] 🚨 Testing Approach doc for Kate — THE hard thing. Apr 16 meeting. Draft exists. Bridge doc created (sections outlined). Andrew active. 12 WORKDAYS AT ZERO.
- [ ] Respond to Lena's AU PS Weekly Update follow-up questions (landing page URLs, repeat visitor CPA overstating) — 1d, high-visibility. Brandon offering support in ABIX.
- [ ] Reply to Stacey DM — CA exclusion from Polaris 50/50 testing on 4/7 (reason: OCI data clean focus)
- [ ] Share ENG max budget calculation file with Andrew (DM 4/1) — Brandon mentioned in Andrew's 1:1 for OP1 recalculation
- [ ] Kudoboard for Kate Vives — was due 4/1, NOW OVERDUE
- [ ] Provide Lorena Q2 expected spend for MX PO submission (8d overdue — 3/25 request). Richard told Lorena he'd update (Slack 4/1).
- [ ] Reply to Lorena keyword data request (14d overdue — 3/19 request)
- [ ] Create one-page Polaris rollout timeline with dates and owners (OVERDUE — was due last week)
- [ ] Compile rolling 4-week keyword CPA dashboard for AU (due this week)
- [ ] Coordinate with MCS team on tracking/attribution post-migration (overdue)
- [ ] Follow up with Brandon on Baloo MBR click-cost guardrails
- [ ] Schedule 15-min "process-snap" sync to map undocumented hand-offs (from Adi sync 3/25)
- [ ] UK/CA combined vs separate decision for R&O report
- [ ] Clarify 10% growth metric definition — before next flash
- [ ] DE tech issue / EAAAAA investigation — within 5 days (from 3/26)
- [ ] AI Max test design (4d OVERDUE — was due 3/28)
- [ ] Bridge: paste Code.gs into Apps Script editor, run createTriggers()
- [ ] Admin: Flash topics (14d overdue), PAM US PO (31d overdue), PAM R&O (22d overdue)
- [ ] WW redirect — Adobe Ad Cloud reporting (13d overdue)
- [ ] OCI TT/suffix — FR to 25% (12d overdue)
- [ ] MX Auto page — Vijeth footer (12d overdue)
- [ ] MX/AU confirm budgets (7d overdue)
- [ ] Delegate MX invoicing — Carlos VOID, needs new owner (Lorena or Richard keeps it)
- [ ] Kingpin Goals MX — overdue, blocked by Andes
- [ ] Triage MS Advertising paused accounts (10x emails)
- [ ] Follow up with Brandon on specific "walk on water" promo criteria
- [ ] Proactively share AU CPC and Polaris outcomes with Lena and stakeholders
- [ ] Apple Ads: investigate system issue (campaigns overspent — 3/27 notice)
- [ ] ABMA-11245: follow up if no response to 3/30 comment
- [x] Polaris brand pages: Vijeth completed XF + Template, Alex confirmed navs working — 4/1
- [x] Baloo: keyword cost data + "don't use Google" blurb — DONE 3/30 (ABCA-371 comment, Quip sheet)
- [x] Flash sections written (MX highlight, AU update, Bid Strategy, Brand LP, Paid App) — 3/27
- [x] Agent Bridge built and live — 3/27
- [x] Onsite Events meeting attended — 3/27
- [x] Polaris weblab acknowledged by MCS team (Frank) — 3/27
- [x] W13 WBR callouts produced for all 10 markets — 3/30
- [x] ie%CCP ingester bug fixed — 3/30
- [x] Change Log CSVs ingested to DuckDB (477 rows) — 3/30
- [x] Bayesian Prediction Engine built — 3/30
- [x] Data layer overhaul (query.py, agent state, DuckDB MCP, PBT tests) — 3/30
- [x] Attention Tracker built — 3/30
- [x] Annual Review shared with Richard (3/24)
- [x] ATMS Training session attended (3/24)
- [x] System Snapshot (portable body sync) sent (3/24)
- [x] US Polaris switch — Stacey completed (3/24)

## Key Quip Documents
- MX Sync: https://quip-amazon.com/K9OYA9mXm7DU/AB-MX-Paid-Search-Sync
- Pre-WBR Callouts: https://quip-amazon.com/MMgBAzDrlVou

## Administrative
- Google Ads invoicing: AU (Feb invoice sent Mar 3), MX (Jan/Dec invoices)
- Google Ireland Ltd PO 5LN2R - 5489247319

## Long-Term Goals
See ~/shared/context/active/long-term-goals.md — five sequential levels:
1. Sharpen yourself (consistent artifact output)
2. Drive & communicate worldwide testing (OCI, WW redirects, email overlay, Baloo, etc.)
3. Give team leverage through automation (non-tech adoption)
4. Own the zero-click future (AEO, AI Overviews)
5. Full agentic orchestration of PS work
