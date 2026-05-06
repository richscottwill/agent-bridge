---
title: "Adi Sync"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0196 | duck_id: meeting-adi-sync -->

# Adi Sync

## Metadata
- Cadence: Weekly (Monday)
- Attendees: Richard Williams, Aditya Satish Thakur (L5)
- Hedy Topic: Adi sync (ID: q5GzKGvlAxeTHppLeI1e)
- Hedy Sessions: 5
- Outlook Series: Richard/Adi sync

## Context
Richard mentors Adi on pacing, ICCP management, campaign optimization, and analytical frameworks. Adi is the newest team member (L5), manages JP and supports CA/EU LP work. Adi has grown significantly — now understands 70-80% of team discussions and is actively contributing. Richard is at his most articulate and strategic in these conversations. This is where Richard's expertise shines — he should document teaching moments as reusable frameworks.

Key dynamic: Peer-level but mentoring relationship. Adi is receptive, asks good follow-up questions, and is building independence. Richard should continue pushing Adi toward structured thinking and documentation habits.

## Latest Session
### 2026-04-22 — Automation + AI Workflow Sync (43 min)
Source: hedy:ZWN2w2OmaUCKWK5nD7so
- **OCI transition discussion**: Data sensitivity during CPC → ROAS transition. Every market differs; Adi leveraging Stacey's US file as template.
- **AI Max questions**: Stacey assigned Adi to compile team questions for Google call early May. Adi creating shared Quip temp doc.
- **BAU/AVT audience exclusion**: Richard walked Adi through identifying 9 AVT audiences via Google Ads filter + pivot table. Goal: AVT includes, BAU excludes these 9.
- **Kiro directory + AI workflow**: Richard demo'd weekly forecasting dashboard — upload weekly callout to IDE → hook injects data → AI regenerates projections with reinforcement-style weighting. Separate analyst agents per region (US/CA/EU5/JP) → writer agent (≤120 words) → critic rubric.
- Richard quote on AI capability: "whatever you can imagine, you should just ask your Kira like, hey, can we do this?"
- Agreed: Richard sends Kiro directory link + temporary web link to Adi for read/write testing.
- Action items: Adi — compile AI Max questions in temp doc (Tuesday). Richard — send Kiro directory (today). Adi — test Kiro connection (next sync).

## Previous Session
### 2025-11-19 — 1:1 Onboarding Catch-Up (47 min)
Source: hedy:UlQUG8kl9BA5Ws23hCzM

- First 1:1 catch-up post-Richard's paternity leave. Casey (Richard's son) ~6 months old, visiting SF family for Thanksgiving.
- Adi's 3-month self-assessment: progress solid, Stacey's guidance working, challenge is connecting dots across ambiguous context — "this is basically all Amazon is about."
- **Canada Polaris URL swap work** (Adi's main project): Stacey-led, Alex-tracked, verified ref markers consistent across new pages. Adi flagged specific pattern: some new Polaris pages had ref-markers that overrode the CPS ref-marker on navigation links — caught and fixed via authoring toggle. (Documents this as reusable learning — same pattern likely recurs on future Polaris migrations in other markets.)
- **Quip folder structure walk-through** (Brandon had asked Richard to cover this):
  - AB Channel Marketing folder structure: public outbound-marketing (team-wide visibility) + internal outbound-marketing (just our 12-person team).
  - Green color-coding = account files; sorted by North America / EU / JP / ABIX.
  - onboarding/planning/review/OP folders for mechanism files (MBR/QBR/WBR callouts in `review`; mid-year + end-of-year planning in `OP`).
  - Testing files organized separately.
- **Documentation-style divergence flagged**: Brandon's style = one massive living doc with all topics (easy cross-search for her); Richard's style = one doc per project. Both consistent = both work. Adi to align with either but preserve consistency.
- **AI tool exploration**: Cedric being deprecated, QuickSight + Amazon Q merger is the direction. Richard recommends Amazon Q for SQL-heavy work (natural-language table discovery, query refactoring against accessible tables only). Party Rock for experimentation; Mentor cited as better-than-Q for general assistance.
- Adi following latest Gemini 3.0 / Claude / ChatGPT 5.1 releases; Richard open to learning from Adi's comparisons.
- Richard on future sessions (quoted): "the way that you're talking about things, I think the thing that you're getting at is like structurally things could be better. And so we just want to like over time just be doing things a little, making things a little bit better over time, little by little by little, and it just compounds."
- Adi requested future walkthrough on Richard's analytical framework for weekly callouts (how to balance analytical rigor with narrative clarity — Stacey-style verbose vs Brandon-style executive-summary distinction).
- Decisions: Adi to upload Canada Polaris project file to shared Quip. Future 1:1s to segment into 15-min general + 15-min specific-topic.
- Action items:
  - Adi: upload Canada Polaris file to shared Quip folder — today
  - Richard: share callout analysis framework with Adi — upcoming 1:1
  - Adi: continue Amazon Q + Party Rock exploration
  - Adi: comment/flag any Quip documentation improvements as he spots them
  - Future: dedicated session on UK Mac awareness recategorization thought process (Adi's curiosity, Richard's teaching material)

## Previous Session
### 2026-04-01 — OCI and Polaris Campaign Updates (32 min)
Source: hedy:1m61COhiskwFSEocPNKP
Detail backfill deferred — pull from Hedy on demand when needed.

## Previous Session
### 2026-01-14 — Pacing Projection Methodology + Japan Spend Gap (31 min)
Source: hedy:OxCaybhv3LECBG1i3O9x

- Mentoring session on pacing methodology + Japan (JP) campaign spend gap. Adi's self-assessment (quoted): "prior if I only followed like 20-30% of the conversations going on in the initial weeks, now I am at the 70-80%."
- **ICCP vs budget tension framing**: Richard (quoted) "you ideally you want to spend like all of your budget, but then if ICCP is off, then that's not going good for Brandon's level. So if you have a certain budget that you have to be able to spend and you're not able to spend it because ICCP is too high, then you would have to find some way creatively to sort of make your account more efficient or more effective."
- Adi's compressed reframe of the formula: underpacing on ICCP → more non-brand regs to bring ICCP % up; overpacing on ICCP → more brand regs to bring it down. Richard confirmed and added: brand regs weigh heavier in the ICCP equation regardless of CPA parity — so brand is the more efficient lever.
- **Pacing projection methodology**: Adi tested a weighted formula (last 8-week same-day avg + YoY same-day + holiday-adjusted) — projection accuracy poor. Richard's diagnosis (quoted): "because we have this ICCP and we have our business end of things influence how much we spend that could make it look different from real seasonality."
- Richard's fix: use brand-core as seasonality proxy instead of total spend — brand is less manipulated YoY, so brand curves are more trustworthy as normalcy baseline. Applies to Canada + Japan in Adi's portfolio.
- Aggregate at weekly/monthly level, not daily — daily noise too high.
- **JP spend gap**: Core brand campaign (YB) stuck at ~¥55K/day vs ¥95K/day needed; ~¥40K/day gap. Impression share at 76% = headroom available. Richard's advice: enable search partners (normally avoided) to close the gap — same setting already enabled on brand-core, so flipping YB would just be making it consistent.
- Rest of JP brand: minimal levers available for more spend. Non-brand the fallback. Adi wanted to wait until 1/20 to launch non-brand; Richard's guidance (quoted): "launch the campaign today or tomorrow with like a very small budget... it would be so insignificant that it wouldn't affect your performance" — start ¥500-1000/day now rather than later scale.
- Richard's YoY seasonal insight for JP: first-half-of-month vs second-half is the high-signal comparison — post-holiday ramp concentrates in back half. Richard (quoted): "I think right now the better thing that you could do is like the first two weeks versus the rest of the month because we're already done with the first two weeks."
- Richard noted pattern recognition is mutual — team still learning Adi's communication style, Adi learning team's pacing language. Both directions of adjustment needed.
- Action items:
  - Adi: enable all-search-results on YB brand campaign (consistency fix) — today
  - Adi: launch non-brand JP campaign at ¥500-1000/day floor — today/tomorrow
  - Adi: pull JP first-half vs second-half January 2025 spend to set W3-W5 expectations
  - Adi: document past ICCP-period manual adjustments to build reference log
  - Richard: share UK Mac awareness framework with Adi when needed

## Previous Session
### 2026-01-28 — Japan Pacing + Non-Brand Testing Strategy (39 min)
Source: hedy:xKf9phe4DP431VPNT1fS

- Mentoring session covering two topics: JP pacing calibration post-Stacey-absence, and Japan non-brand test framing.
- **Pacing**: Adi running JP at 107% this week. Worried about exceeding 100% vs under-delivering. Richard's calibration rule (quoted): "97% would be acceptable... on like the individual line level... if it's over 96% but then you don't want it to be over 100% unless you actually have the budget to go over." Adi's approach: built daily drop-off tracker to see whether changes are bending the spend curve as expected (quoted): "yesterday it spent 7.41 versus 9.31" — direct daily comparison after mid-week changes.
- **Japan non-brand testing strategy**: Adi inheriting the workstream. Richard's framing on why JP non-brand has stalled for years (quoted): "the non-brand CPA that's normal to me is like a thousand dollar CPA and that's kind of like the turnoff for running non-brand in Japan... the Japan team they have like a tight grip on us being able to bid on like ASINs, so the way that we had approached it in the past is like we just bid on like the business modifiers like wholesale bulk."
- Richard's ideal approach (quoted): "the ideal way to go about it is allocate your budget every single month to maximize brand. And then there's always going to be some leftover amount. And then that would be the non-brand. And if you do that, you should never have an issue with ICCP because even though the CPA is so high for non-brand, the vast majority of spend is going to go to brand anyway."
- Reframe of the ask (quoted): "get away from like a hard focus on CPA and get more towards this is going to be like a process that we work through to improve the CPA." Don't anchor leadership on the $1000 CPA number — anchor on learning cadence.
- Adi's Q1 window reasoning: MHLW event is pulling enough brand demand that JP will hit OP2 easily in Q1 — creates room for 5% non-brand budget allocation for learning without risking OP2 targets.
- Stacey's standing instruction (per Adi): "if you are able to get brand to spend the entirety of the budget do that, don't use non-brand only as a last resort." Adi to revisit when Stacey returns.
- Richard on market-specific context discipline: Mexico (Mercado Libre) + AU (tradies, paper in Sydney) + US (green/Uline competitive context) all show non-brand is solvable with the right vertical framing — JP shouldn't be treated as structurally different.
- Category-targeting method (reusable framework): Richard pulled ASIN-level Hubble query on business-customer orders + revenue over 12 months, aggregated by category — that's how UK/EU non-brand categories (grocery, electronics/PC) were identified. Adi to adapt for JP. Richard also demo'd internal SQL-focused LLM tool for accelerating table discovery.
- Richard's guidance on validation: don't ship category selection from data alone — cross-check with market-specific owner (Minami for JP, Moro for US, etc.) because they catch the local-context things pure data misses.
- Decisions: JP non-brand to continue as Adi-owned workstream with Stacey reconciliation when she returns. Pacing rule of thumb codified at ~97%. Adi's daily drop-off tracker adopted as personal tool.
- Action items:
  - Adi: finalize JP non-brand testing plan + align with Brandon — this week
  - Adi: draft 5%-budget non-brand experiment framing for Stacey's return
  - Adi: reach Minami for JP category validation
  - Richard: share JP non-brand context + UK Mac framework reference when needed

## Previous Session
### 2026-03-25 — AI Ad-Copy Workflow for JP (43 min)
- Adi presented structured AI workflow for generating JP non-brand ad creatives
- Workflow: copy existing ad creative into AI tool → analysis on right panel → actionable creative options on left → compare with D-Pel translations
- Key constraint: JP headlines limited to ~15 characters (tighter than English)
- Adi included both D-Pel and AI translations due to observed discrepancies between English source and D-Pel output
- P1/P2 tables summarize existing creatives; P3 generates new keyword/headline ideas from analysis
- Richard praised scalability, suggested expanding via knowledge bases (account data + LP text + historical performance like CA monthly returns)
- Richard: "I actually really like the structure that you have here because it's easy to work with. I feel like we could scale this up."
- Discussed iterative testing approach — keep variations close to original so performance drivers are identifiable
- Adi: "As a second assistant, it plays a good role. I had in mind with this where we are still the human decision-makers."
- Discussed difficulty of undocumented processes for pre-Oct 2025 projects — Adi: "a lot of things are just something that we know or have in our head and not necessarily documented"
- Richard: "I have a lot of opinions that I don't really talk about with everyone. I think Brandon is probably the one I talk most about that stuff too."
- Richard on AI timeline: "6 to 12 months, that's when stuff is actually going to get more useful. 12 to 18 months is when it's like probably going to hit people like, oh, if I'm not doing this, then I'm behind."
- Adi reflected on annual review — better understanding now vs. first months
- Decisions: AI ad copy for JP NB testing with human oversight; D-Pel + AI side-by-side during testing; 15-char compliance as pre-launch validation; knowledge base expansion for scaling
- Action items:
  - Adi: refine workflow, document JP translation rules in Quip, build D-Pel vs AI decision matrix, add spend guardrail (97% pacing target), create Loop knowledge repo for undocumented workflows
  - Richard: schedule 15-min "process-snap" sync to map undocumented hand-offs for post-Oct 2025 projects

## Running Themes
- AI tool integration into campaign workflows (JP focus, scaling to other markets)
- JP pacing management (107% → targeting 97% before Stacey's return)
- Knowledge capture and documentation gaps (pre-Oct 2025 projects)
- Adi's growth trajectory: analytical confidence, operational independence
- Richard as mentor: teaching pacing, ICCP, analytical frameworks — this is where Richard's expertise shines most clearly
- Richard's self-awareness: "I have a lot of opinions that I don't really talk about" — visibility gap extends even to peer conversations

## Open Items
- [ ] Adi: finalize AI ad-copy workflow with translation rules in Quip
- [ ] Adi: D-Pel vs AI decision matrix for JP
- [ ] Adi: spend guardrail (97% cap) in JP pacing model
- [ ] Richard: schedule process-snap sync (15 min)
- [ ] Adi: create Loop knowledge repo for undocumented workflows
- [ ] Future: expand AI workflow to UK Mac framework and other markets
