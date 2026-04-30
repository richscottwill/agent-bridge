# Baloo Early Access — PS Feedback Consolidation

**Date:** 2026-04-30 | **Source:** Deep Dive & Debate 4/30 | **Author:** Richard Williams (prichwil@) | **For:** Aarushi Jain (aarushij@, Baloo TPM), Vamsi Kumar (vkumarmp@, PM), Brandon Munday, MCS team

**Purpose:** Consolidate feedback captured while testing Baloo Early Access, mapped against existing SIMs where known, with recommended follow-ups.

**Early Access wiki:** [w.amazon.com/bin/view/B2B/Baloo/EarlyAccess/](https://w.amazon.com/bin/view/B2B/Baloo/EarlyAccess/)
**SIM folder:** [open issues in QA folder](https://i.amazon.com/issues/search?q=is%3A(Open)+in%3A(6098fbca-c532-45a6-b716-0bc99f830d3c)) (id `6098fbca-c532-45a6-b716-0bc99f830d3c`)
**Slack:** [#baloo-interest](https://amazon.enterprise.slack.com/archives/C0A9HBB9H2B)

---

## 1) Search flows and ref-tag persistence (HIGH)

### 1a. Reftag after clicking a product from search
- **Observation:** When a Baloo customer clicks an organic product tile from the search results page, ref-tag state needs to persist so we can attribute the downstream reg / OPS to the PS keyword that brought them in.
- **Existing SIM:** [BALOO-8 — ref persistence](https://issues.amazon.com/issues/BALOO-8) (I previously flagged this in #baloo-interest on 4/14). Tracks the core reftag persistence ask.
- **Related URL-flip launch blockers (reftags lost via redirect to a.com):**
  - [D392301704](https://sim.amazon.com/issues/D392301704) — ABSearch Books "Advanced Search" link redirects to amazon.com
  - [D392294626](https://sim.amazon.com/issues/D392294626) — More Buying Options "Details" link redirects to pre-prod.amazon.com
  - [D394257968](https://sim.amazon.com/issues/D394257968) — Sponsored Product widget ads on search flip to amazon.com (Firebird SP; proposed `SubMarketplace.BUSINESS` enum fix)
- **Next action:** Ask Aarushi whether BALOO-8 covers the *full* "click from search → product → reg" reftag chain or only the subdomain persistence. If only subdomain, file a PS-specific companion SIM that references the `ps_kw`/`ref` parameters (see [Appendix 3 of EarlyAccess wiki](https://w.amazon.com/bin/view/B2B/Baloo/EarlyAccess/#HAppendix3:) for the canonical PS keyword → MCS LP mapping currently in use).

### 1b. New searches and reftag mutation
- **Observation:** When a Baloo user performs a *new* search from inside the subdomain (modifies the query), it's unclear whether the original PS reftag still rides with subsequent pageviews or gets replaced.
- **Ask Aarushi:** Document the reftag behavior across these state transitions. This is a measurement prerequisite for the AU/MX non-weblab Brand LP test (Asana 1214330104198712), which depends on stable reftag-to-reg attribution.

### 1c. Category vs. keyword landing path (strategic)
- **Current:** PS ads → MCS keyword LP → redirects to Baloo keyword search results.
- **Future proposal:** For category-level keywords (e.g., "wholesale"), send users directly to the Baloo category node rather than a keyword search. Keep keyword-level terms on the current keyword-search path for now.
- **Ask:** Who owns the decision on direct-to-category routing? Feels like a PS + ABSearch conversation (ABCA-242 workstream SIM referenced below).
- **Related SIMs:**
  - [ABCA-242](https://issues.amazon.com/issues/ABCA-242) — AB Search workstream for unauthenticated Baloo customers
  - [CIBELES-444 / SIP-27389](https://issues.amazon.com/issues/CIBELES-444) — Autocomplete features for unrecognized customers

---

## 2) Ad unit / MCS page discovery (opportunity)

### 2a. "Look for more of these types of pages"
- **Observation:** The current 26 keyword → MCS LP mappings in [Appendix 3](https://w.amazon.com/bin/view/B2B/Baloo/EarlyAccess/#HAppendix3:) cover specific verticals (apparel, beauty, restaurant, wholesale, etc.). There are likely more MCS category/vertical pages that could (a) be tested for Baloo readiness and (b) be candidates to expand PS keyword coverage against.
- **Next action:** Pull the full MCS LP inventory from Dwayne/Alex VanDerStuyf (MCS team) and cross-reference against PS keyword performance to prioritize expansion.

### 2b. Amazon gift card (retail-focused banners)
- **Observation:** Saw retail-focused banners (Amazon gift card, etc.) rendering on Baloo subdomain pages that don't make sense for a B2B acquisition flow.
- **Existing SIM:** [BALOO-31 — b2c targeted upsells on Cart/Smart Wagon are irrelevant for AB](https://sim.amazon.com/issues/BALOO-31) (LaunchBlocker). Same class of issue.
- **Separate issue to file if no SIM exists:** Amazon gift card banners specifically on Baloo browse/search pages. Different surface than Cart; likely different owner. Propose new SIM under the QA folder.

---

## 3) Checkout → shop.business.amazon.com acquisition CTA (HIGH — PS acq story)

### 3a. Make "Create your free business account" more prominent
- **Observation:** When a Baloo user clicks to check out and lands on the shop.business signup/acq page, the "Create your free business account" CTA is not prominent enough. Most Baloo traffic *from us* is pure acquisition (unrecognized customers new to AB), so this should be the primary path.
- **Related SIM:** [BALOO-35 — "Sign up now" on Cart page is confusing, goes to retail sign up](https://sim.amazon.com/issues/BALOO-35) (LaunchBlocker). Related but not identical — BALOO-35 is about destination correctness; this feedback is about CTA *prominence* relative to the "sign in" alternative on the AB AuthX page.
- **Ask Aarushi:** Talk to Aarushi about making the reg-start page the standard post-checkout landing for unrecognized Baloo customers. There's a link for existing customers who might not be logged in, but the default path for a brand-new prospect should be heavier on "Create."
- **Next action:** Confirm the CTA hierarchy owner is AuthX (ABCA-267 workstream) vs. Registration, then file a specific SIM with screenshots if no existing ticket covers this.

---

## 4) Sign-in / sign-up URL flips on adjacent flows (HIGH — known LaunchBlockers)

- **Observation:** Adding a coupon from a Baloo page takes you to the *business* login page (correct destination) but the overall CX bounces you out of the browse flow; worth confirming this is intentional vs. a redirect bug.
- **Known LaunchBlockers in this class (sign-in/sign-up URL flips):**
  - [V2099100304](https://sim.amazon.com/issues/V2099100304) — "Returns & Orders" nav CTA loads consumer sign-in
  - [V2099140513](https://sim.amazon.com/issues/V2099140513) — "Business Essentials" nav CTA → consumer marketplace
  - [BALOO-22](https://sim.amazon.com/issues/BALOO-22) — "Amazon Business Card" CTA in YADD flyout → retail page
  - [BALOO-20](https://sim.amazon.com/issues/BALOO-20) — Rufus sign-in → retail page
  - [BALOO-26](https://sim.amazon.com/issues/BALOO-26) — "Pay by Invoice Purchasing Line" footer → retail
  - [BALOO-27](https://sim.amazon.com/issues/BALOO-27) — mWeb "Change your Charity" footer → retail
  - [BALOO-28](https://sim.amazon.com/issues/BALOO-28) — mWeb "Your Orders" / "Business Essentials" hamburger → retail
  - [BALOO-44](https://sim.amazon.com/issues/BALOO-44) — Pay by invoice page links cause URL flip
- **Next action:** Tag the coupon flow specifically. If not already in the QA folder, file. Reference this cluster so the Baloo team can pattern-match.

---

## 5) Detail page — Prime placement on top right (observation)

- **Observation:** On product detail pages, the top-right Prime-style placement will be branded **Amazon Business** for Baloo customers. Makes sense, noting it for the PS callout/measurement story.
- **Related:** [ABDPX-6922](https://sim.amazon.com/issues/ABDPX-6922) — BuyBox `isBusinessCustomer` not propagating for Baloo customers (proposed migration from legacy `CustomerMembershipHelper` to R2D2 `isBusiness` URL param path). This is the fix that makes the B2B context correctly flow through to the DPX page placements.
- **PS-side question:** When the PAM / Brand Polaris reporting rolls up, does the "AB Prime" upsell placement count in the acquisition funnel or does it get double-counted with Business Prime opt-in? Flag for measurement.

---

## 6) Sponsored link on Baloo page → lands on a.com (URL flip, HIGH)

- **Observation:** When a Baloo user clicks a **sponsored product** link, the click navigates to amazon.com instead of staying on shop.business.amazon.com.
- **Existing SIMs (this is the root-cause cluster):**
  - [D394257968](https://sim.amazon.com/issues/D394257968) — Baloo team's Firebird intake: absolute URLs on SP widget ads (multi-ASIN carousels, skyscrapers). Proposed fix: add `SubMarketplace.BUSINESS` enum, mirror the SMILE/STORE pattern.
  - [V2194976274](https://sim.amazon.com/issues/V2194976274) — AB Ads Supply team intake requesting SP URL preservation on Baloo. Dev target 5/1, prod target 8/30.
- **PS concern:** This is our single most important measurement-integrity bug. A sponsored-click that flips to a.com will fragment attribution and nullify the Baloo PS test read-out. Dev 5/1, prod 8/30 — we need to pressure-test whether we can accept PS measurement during the 4-month gap or if we need an interim measurement approach.
- **Next action:** Sync with AB Ads Supply (kurinchi@ / chensar@) on a measurement bridge; file follow-up comment in V2194976274 explicitly flagging PS-attribution risk.

---

## 7) Measurement, attribution, and related data plumbing (cross-cutting)

**BALOO-specific measurement SIMs to pull into PS line-of-sight:**
- [DEX-18092](https://sim.amazon.com/issues/DEX-18092) — Recognize Baloo customers in Delivery Benefit Program B2B detection. Affects Prime upsell suppression, NPA gating — cascades into our acq funnel cleanliness.
- [ABMA-9583](https://sim.amazon.com/issues/ABMA-9583) — ABMA Epic for Q4-2025 unagted access tracking (engagement metrics infrastructure). Need to confirm PS keyword/campaign attribution is wired into the ABMA data cut.
- [SIP-27450](https://sim.amazon.com/issues/SIP-27450) — Enable B2B prices in AOD for unauthenticated AB customers (Business Prime visibility on Baloo).

**Open PS-side unknowns:**
- Are `ps_kw` and `tag=abpsgglacqus-20` URL params preserved across all the URL-flip fixes above, or do we lose them when URL-flip mitigation rewrites the destination?
- Is there a Baloo-specific QuickSight / Datanet view that joins `BusinessCustomerIdentifier` + Baloo session + PS reftag? If not, this is a gap that blocks the Brandon ROY Brand LP measurement story.

---

## 8) Proposed follow-ups from this session

| # | Action | Owner | By |
|---|--------|-------|-----|
| 1 | Confirm BALOO-8 reftag scope with Aarushi; file PS companion SIM if needed | RW + Aarushi | 5/2 |
| 2 | Talk to Aarushi re: making reg-start page standard post-checkout (#3a) | RW | 5/5 Brandon 1:1 context |
| 3 | File gift-card / retail banner SIM if not already covered by BALOO-31 scope | RW | 5/2 |
| 4 | File coupon-flow sign-in flip SIM with screenshots if not in QA folder | RW | 5/2 |
| 5 | Pull full MCS LP inventory from Dwayne/Alex; identify expansion candidates | RW | 5/7 |
| 6 | Comment on V2194976274 re: PS attribution risk during Baloo SP URL-flip gap | RW | 5/2 |
| 7 | Ask AB Ads / ABMA about Baloo-specific attribution data cut availability | RW | 5/5 |
| 8 | Share this doc with Brandon + Aarushi + Dwayne for comment | RW | 4/30 EOD |

---

## 9) Key reference SIMs (one-stop)

**Workstream parents (ABCA-*):**
- [ABCA-221](https://sim.amazon.com/issues/ABCA-221) — AB Nav
- [ABCA-228](https://sim.amazon.com/issues/ABCA-228) — AB Business Prime
- [ABCA-242](https://sim.amazon.com/issues/ABCA-242) — AB Search & Autocomplete
- [ABCA-267](https://sim.amazon.com/issues/ABCA-267) — Identity / AuthX
- [ABCA-270](https://sim.amazon.com/issues/ABCA-270) — New Sub-Domain
- [ABCA-341](https://sim.amazon.com/issues/ABCA-341) — BIOAB upsell on DPX

**Identity / AuthX (relevant to #3a, #4):**
- [SwansIntake-466](https://sim.amazon.com/issues/SwansIntake-466) — AuthPortal domain config to maintain Baloo subdomain
- [LYNX-19534](https://sim.amazon.com/issues/LYNX-19534) — QA Intake, Auth Portal Registration

**Attribution / Measurement (relevant to #6, #7):**
- [ABMA-9583](https://sim.amazon.com/issues/ABMA-9583) — ABMA Epic Q4-2025 Ungated Access
- [DEX-18092](https://sim.amazon.com/issues/DEX-18092) — Delivery Benefit Program B2B detection
- [V2194976274](https://sim.amazon.com/issues/V2194976274) — AB Ads SP URL preservation
- [D394257968](https://sim.amazon.com/issues/D394257968) — Firebird SP URL flip (proposed enum fix)

**Checkout / Cart (relevant to #3, #4):**
- [AB-MARBELLA-3009](https://sim.amazon.com/issues/AB-MARBELLA-3009) — Cart feature enable/disable for unauth AB
- [BALOO-4](https://sim.amazon.com/issues/BALOO-4), [BALOO-31](https://sim.amazon.com/issues/BALOO-31), [BALOO-35](https://sim.amazon.com/issues/BALOO-35) — Cart LaunchBlockers
- [PrimePURE-TT-9695](https://sim.amazon.com/issues/PrimePURE-TT-9695) — Centralized retail Prime upsell suppression

**Reftag / URL-flip cluster (relevant to #1, #6):**
- [BALOO-8](https://sim.amazon.com/issues/BALOO-8) — ref persistence
- [D392301704](https://sim.amazon.com/issues/D392301704), [D392294626](https://sim.amazon.com/issues/D392294626) — Search URL flips
- [V2099100304](https://sim.amazon.com/issues/V2099100304), [V2099140513](https://sim.amazon.com/issues/V2099140513), [BALOO-22](https://sim.amazon.com/issues/BALOO-22), [BALOO-20](https://sim.amazon.com/issues/BALOO-20), [BALOO-26](https://sim.amazon.com/issues/BALOO-26), [BALOO-27](https://sim.amazon.com/issues/BALOO-27), [BALOO-28](https://sim.amazon.com/issues/BALOO-28), [BALOO-44](https://sim.amazon.com/issues/BALOO-44) — Nav/footer URL flips

**Docs:**
- [Project Baloo Wiki](https://w.amazon.com/bin/view/B2B/Baloo/)
- [Baloo Early Access](https://w.amazon.com/bin/view/B2B/Baloo/EarlyAccess/)
- [BRD](https://amazon.sharepoint.com/:w:/s/ABCAT/IQAcRCsQhdI_RqnkePJcUnruAatP1K6v3XaAmJYNja5hm40)
- [PR-FAQ v4.0](https://amazon.sharepoint.com/:w:/s/ABCAT/IQBwTvKa4WaTSqI1poMiMwS_AZjQo8XKH4GbGXLjQgUvbjs)
- [HLD](https://quip-amazon.com/G5wPAmOSUIla/HLD-Enabling-Ungated-AB-Access-Baloo)
- [Tech Strategy](https://quip-amazon.com/VowbAhx4XGSK/Baloo-High-Level-Tech-Strategy)

---

*Raw notes from the meeting are preserved in the first line of each section header. This doc is a working artifact — comment freely.*
