# Risk Log — Leadership Demo Week of 2026-05-04

Technical / narrative / scheduling failure modes and mitigations.

Last updated: 2026-04-21

---

## Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| SharePoint MCP auth fails during demo | High (broken now) | Low | Demo is local-served. No SharePoint dependency during demo. |
| Agent Activity Feed is empty / stale | Low | Medium | Pre-seeded demo JSON. Refresh 24h before with real ops data if DevSpaces-to-Windows sync works. Fallback: demo data stays. |
| Internet hiccup in conference room / Zoom | Medium | Low | Dashboard fully served from localhost. No cloud calls during demo. |
| MotherDuck slow / times out | N/A | N/A | Dashboard reads static JSON, not live DuckDB. Any DB calls happen at refresh time, not demo time. |
| Browser crash mid-demo | Low | High | Second browser window pre-loaded with all tabs. Laptop lid closed on backup. |
| "Contribute" form doesn't trigger 4-stage UI | Low | Medium | It's client-side JS — no network dependency. If broken, open screenshot folder and narrate. |
| Sankey doesn't render (canvas issue on conference display) | Low | Medium | Fallback: screenshot of the Sankey as a static image. |
| Provenance bars don't inject (script load order) | Low | Low | Refresh tab. If still broken, they'd just be hidden — demo still works, lose the "every card has a producer" beat. |
| Dashboard server dies | Low | High | Kill + restart: `python3 ~/shared/dashboards/serve.py`. Takes <5 seconds. |
| OneDrive sync conflicts | Low | Low | Not in demo path. Only relevant after demo for file sharing. |

## Narrative Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| "Isn't this what [X] does?" (X = Kiro/Q/Asana AI/Copilot) | High | Medium | Tight 1-sentence answer: *"Kiro is the environment I build in. Q/Copilot are one-shot assistants. What's different is the orchestration — multi-agent, multi-surface, with provenance and quality gates."* |
| "Can my team have this?" | High | Low | Crisp yes + 3-step answer: Kiro env / shared context repo pattern / agent specs. Have a one-pager ready. |
| "What's the maintenance cost?" | High | Medium | ~1h/week calibration. Karpathy agent handles most drift. *Don't under-claim — L8+ will spot it.* |
| Security / PII probe | Medium | High | preToolUse hooks block external email, calendar invites, unauthorized writes. Every Asana write audited. Read-only Slack. Be ready to show a specific guard. |
| "How do you know the agents are right?" | Medium | Medium | Two mechanisms: (1) quality gates (8.0+ or blocked), (2) calibration — predictions scored vs actuals, system learns when it's over/under confident. |
| Q&A goes to fundraising / budget discussion too early | Medium | Medium | Bridge: *"Happy to go deep on resourcing. Let me first finish showing what's built, then we can talk about scale."* |
| I freeze / lose thread | Low | High | Script key transitions (see `demo-script.md`). Rehearse 3x. 30-second reset talking point: *"Let me restart from where this matters..."* |
| Tech leader says "the agents are just GPT calls — this is a prompt wrapper" | Medium | High | *"Prompts are the easy part. The hard parts are the context schema — 12 organs, 55 tables — and the quality gates. An agent without context and without gates is a chatbot. An agent with both is infrastructure."* |

## Scheduling Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Demo moves up unexpectedly | Medium | High | Builds 1-3 alone are demo-able in 10 min. 4-5 are polish. Already shippable today. |
| Demo slot shrinks to 10 min | Medium | Medium | 10-min version: cold open (1m) + provenance tour (3m) + Sankey (2m) + Activity Feed (2m) + close (2m). Skip Contribute. |
| Demo slot expands to 30 min | Low | Low | Ready-to-pull deep-dives: full wiki pipeline walkthrough, full Karpathy experiment loop, full safety-guard walkthrough. |
| Demo reschedules into summer | Low | Low | System keeps running. All prep stays valid. Only demo-script and screenshot fallbacks need a date update. |

---

## Pre-Demo 24h Checklist

**Tech readiness**
- [ ] Dashboard renders correctly at 125% zoom on presentation resolution
- [ ] All 4 demo tabs load fresh without errors (Command Center, Agent Activity, System Flow, Contribute)
- [ ] Provenance bars visible on every registered section
- [ ] Sankey renders on first visit to System Flow tab
- [ ] "Contribute" form shows 4-stage confirmation on submit
- [ ] Agent Activity Feed shows ≥10 rows with realistic timestamps
- [ ] Dashboard server stable for 30+ min without restart
- [ ] localhost URL works on both laptop and Zoom screen-share

**Backup readiness**
- [ ] Screenshot folder captured for all 4 demo tabs (8-12 screenshots)
- [ ] Screenshots opened in a second window, pre-positioned
- [ ] Second browser instance pre-loaded with all tabs
- [ ] Second laptop/device on standby with same dashboard
- [ ] Offline mode tested: kill wifi, does demo still work? (Answer: yes, fully)

**Content readiness**
- [ ] Demo script memorized, not read
- [ ] 5 Q&A answers rehearsed under 60 seconds each
- [ ] Bridge-back phrases ready
- [ ] One-pager printed (color) + PDF saved for post-demo email
- [ ] Pre-typed contribute signal copy-ready

**Logistics**
- [ ] Calendar invite confirms room + Zoom link
- [ ] Screen share tested on Zoom with someone the day before
- [ ] Laptop power cable + adapter for conference room display
- [ ] Notifications OFF (Slack, email, calendar alerts)
- [ ] Browser tabs closed except the demo one

**Final 5 min before**
- [ ] Full-screen dashboard
- [ ] Zoom 125%
- [ ] Refresh each tab to get fresh data
- [ ] Second monitor showing screenshot folder (for quick fallback)
- [ ] Deep breath

---

## After-Demo

- [ ] Send one-pager PDF to every attendee by end of day
- [ ] Asana follow-up task: log feedback in session-log, wait 48h before reaching out for 1:1s
- [ ] Karpathy experiment: which demo segment got the strongest reaction? Write that down for v2
