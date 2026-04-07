<!-- DOC-0215 | duck_id: ops-landing-page-testing-playbook -->
---
title: Landing Page Testing Playbook
status: DRAFT
doc-type: execution
audience: amazon-internal
level: N/A
owner: Richard Williams
created: 2026-03-25
updated: 2026-03-25
update-trigger: new LP test results, Polaris migration milestones, category page launches
---

# Landing Page Testing Playbook

---

## Principles

1. Test before you migrate — phased rollout unless stakeholder overrides (AU was an exception)
2. Measure what matters — CVR and CPA, not just traffic
3. Category pages outperform general pages — Office +52%, Apparel +28%, Janitorial +21%
4. Polaris is the future — all new pages should be Polaris

## Test Framework

### Pre-Test
1. Define hypothesis: "New page will improve CVR by X% because [reason]"
2. Capture baseline: 4 weeks of current page performance (CVR, CPA, bounce rate)
3. Set success criteria: minimum CVR improvement to justify switch
4. Set rollback criteria: CPA increase threshold that triggers revert

### During Test
1. Traffic split: 50/50 via weblab (preferred) or Google Ads experiment
2. Duration: 4 weeks minimum (2 weeks for learning, 2 for steady-state)
3. Monitor weekly: CVR, CPA, bounce rate, time on page
4. Don't touch other variables during test (bids, keywords, budget)

### Post-Test
1. Statistical significance check (minimum 95% confidence)
2. Document: hypothesis, results, decision, learnings
3. If positive: scale to 100%, plan WW rollout
4. If negative: revert, document why, iterate

## Polaris Migration Checklist

- [ ] AEM translation submitted (if non-English market)
- [ ] Reftags configured correctly
- [ ] Mobile responsive verified
- [ ] CTA buttons working (registration flow)
- [ ] No broken links or missing images
- [ ] Minimal header/footer applied (PS-specific)
- [ ] Weblab or experiment set up for measurement

## Category Page Playbook

Category pages consistently outperform general pages:

| Category | CVR Lift vs General | Markets Live |
|----------|-------------------|-------------|
| Office | +52% | US |
| Apparel | +28% | US |
| Janitorial | +21% | US |
| Auto | TBD | MX (live 3/23) |
| Beauty | TBD | MX (live 3/23) |

Category pages are the highest-CVR play we have. Office at +52% is not a marginal improvement — it's a step change. Every market with search volume in a vertical should have a category page.

When to build a category page:
- Search volume exists for the vertical (100+ monthly searches)
- AB has relevant product catalog
- MCS can support the page build
- A clear keyword theme maps to the vertical

## Known Issues

- "Explore category" button on MX pages overwrites PS reftags — can't be removed, but reftags can be customized
- Minimal footer template doesn't exist in Polaris — use regular footer for now
- AEM translations take 5-7 business days

These are implementation friction, not blockers. The reftag workaround exists. The footer issue is cosmetic. AEM timelines are the real constraint.


## Sources
- Category page CVR lifts (Office +52%, Apparel +28%, Janitorial +21%) — source: ~/shared/context/body/memory.md → Compressed Context (category LP performance)
- Polaris migration approach — source: ~/shared/context/body/brain.md → D4: AU Landing Page (phased vs full)
- MX explore category button issue — source: Asana notification (Vijeth 3/24, Auto-Comms folder)
- Minimal footer template limitation — source: Asana notification (Vijeth 3/17, Auto-Comms folder)
- AEM translation timeline — source: ~/shared/context/active/current.md → Polaris Brand LP Rollout
- Weblab measurement approach — source: ~/shared/context/body/eyes.md → Predicted QA → Q4 (45% CP threshold)

<!-- AGENT_CONTEXT
machine_summary: "Landing page testing playbook for AB Paid Search. Covers pre/during/post test framework, Polaris migration checklist, and category page performance data. Category pages deliver +21-52% CVR lift over general pages."
key_entities: ["Polaris", "category pages", "weblab", "AEM translations", "CVR", "CPA", "MCS"]
action_verbs: ["test", "migrate", "measure", "scale", "revert"]
update_triggers: ["new LP test results", "Polaris migration milestones", "category page launches in new markets", "AEM process changes"]
-->
