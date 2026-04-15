# What should we change on the WW Brand Polaris template before the weblab?

**Context:** We've been testing and optimizing PS landing pages across CA, EU, MX, AU, and JP over the past 3 months. Before we launch the WW weblab for the Polaris Brand pages, we should apply what we've learned. All changes here are to the global template (not market-specific), per Brandon's direction on 4/10.

**Sources:** Adi's CA optimization work (Jan-Mar), Yun/Andrew's EU page updates, MX A/B test (live this week), AU CVR data post-Polaris switch, MCS-3004 ticket thread, and live page inspections across US/DE/FR/JP/AU.

---

## 1. Remove outbound links that take prospects off the page

The Polaris template has CTAs linking to the business-discounts page, browse nodes, and solutions page. These are for existing customers browsing the site, not prospects from paid search who need to register.

Our legacy PS pages were deliberately stripped of these links. That's partly why they converted better. When AU switched to Polaris on 3/25, we saw -34% NB CVR and -18% Brand CVR (Brandon's email to Lena, 4/8). The structural difference between gated PS pages and open Polaris pages, including more exit paths, is a likely contributor.

**Recommendation:** Remove all non-registration CTAs. The only clickable actions should be the register button, FAQ accordion expands, and on-page scroll.

## 2. Remove the product carousel (ASIN component)

Some markets have it, some don't. We tested percolate in the past and it didn't improve conversion (MCS-3004 comment, 4/8). The component is controlled by the tech team and requires a SIM per page to modify. Yun independently flagged this as something to remove from EU pages (Slack, 4/10: "the thing I really want to take out is carousel").

**Recommendation:** Delete the carousel/ASIN component from the WW template. Fill the space with benefit cards (see #3).

## 3. Add 4-5 benefit cards between the hero and FAQ sections

If we remove the carousel and outbound links, the page gets bare. Yun called this out directly: without the carousel, the page becomes "so text heavy" (Slack, 4/10). The fix is benefit cards.

The US and JP Polaris pages already have 5 benefit cards (Streamline purchasing, Maintain compliance, Analyze spend, Buy in bulk, Purchase responsibly). These are the strongest structural element on those pages. The AU page has almost none, just FAQs. The DE screenshot in the Loop doc shows benefit boxes as a positive example from Yun/Andrew's EU work.

**Recommendation:** Make benefit cards a required section in the WW template. 4-5 cards with icon, headline, and 1-line description, localized per market. US/JP is the model.

## 4. Confirm the minimal header is permanent (not an Adobe Target workaround)

Our legacy PS pages had no nav bar, by design. The Polaris template uses Adobe Target to hide the full header behind a minimal one. This already regressed once during a deployment (Alex flagged it on 4/6: "the work Vijeth did last week, specifically adding the minimal 1-button CTA nav, has been regressed"). Alex committed to building a dedicated AEM experience fragment/template (Polaris Rollout meeting, 3/24), but we don't have a confirmed status.

**Recommendation:** Confirm the AEM template with minimal header is deployed and stable before weblab launch. We can't rely on Target as a permanent solution.

## 5. Reduce white space on mobile

Adi's CA testing found significant dead space between the hero and first content block. 81% of traffic on the affected pages was mobile (Adi meeting, 4/8). Reducing white space was part of the optimization bundle that recovered CVR in Canada. Brandon also flagged dead space during the same review.

**Recommendation:** Tighten vertical padding between hero and content sections at the CSS/template level. Prioritize mobile viewport.


## 6. Support a localized headline with the country name

Adi's CA work added the country name to headlines ("Amazon Business in Canada"). This was part of what recovered CVR (Adi meeting, 4/8). Brandon directed the same approach for MX (Brandon/Richard sync, 4/14). The current US and JP pages use generic headlines with no country context.

**Recommendation:** Add a configurable headline field to the WW template. Default: "Sign up for Amazon Business in [Country]."

## 7. Update the hero image

Some markets still use "purple color wash" hero images from 2020. Adi's team replaced these with current, business-context imagery in Canada as part of the optimization work (Adi meeting, 4/8). There's no regular refresh cadence.

**Recommendation:** Update the WW template hero image. Establish a 6-month review cadence.

## 8. Fix the EU cookie banner implementation

When loading the DE and FR Polaris pages, a full-page cookie consent overlay blocks all content (live page inspection, 4/15). The hero, registration CTA, and benefit cards are invisible until the user interacts with the banner. US pages don't have this issue.

**Recommendation:** Ensure the EU cookie consent uses a dismissible bar (not full-page overlay) so the hero and CTA are visible on first load.

## 9. Standardize the FAQ section across all markets

The US and JP pages have 3 solid FAQ items. The AU page is nearly empty (live page inspection, 4/15). FAQ content should be consistent and address top prospect objections: Is it free? What documents do I need? Can I convert my personal account?

**Recommendation:** Standardize 3-5 FAQ items across all markets with localized text.

## 10. Establish a CVR monitoring window for template changes

The AU incident (-34% CVR) took nearly 2 weeks to formally flag and revert. There was no structured monitoring window. We proposed routine CVR-by-URL checks as a best practice during the Apr 8 meeting, and the team agreed.

**Recommendation:** Before weblab launch, define a 2-week monitoring protocol with daily CVR checks by URL and a pre-defined revert threshold.

---

## How should we prioritize?

| Priority | Change | Effort |
|----------|--------|--------|
| Do first | Add benefit cards (#3) | Medium (authoring + localization) |
| Do first | Remove outbound links (#1) | Low (authoring removal) |
| Do first | Confirm minimal header is permanent (#4) | Medium (tech status check) |
| Do second | Remove carousel (#2) | Low (component deletion) |
| Do second | Reduce mobile white space (#5) | Medium (CSS change) |
| Do second | Localized headline (#6) | Low (configurable field) |
| Nice to have | Hero image update (#7) | Low (asset swap) |
| Nice to have | EU cookie banner (#8) | Medium (tech/compliance) |
| Nice to have | Standardize FAQs (#9) | Low (authoring) |
| Process | CVR monitoring SOP (#10) | Low (process, not code) |

---

## What do we need to decide Thursday?

1. Is the AEM minimal-header template deployed and stable, or are we still on the Target workaround?
2. Do we proceed with the current WW template for the DE/FR weblab and iterate after, or hold for these changes first?
3. Should the "wholesale supplies" subheadline on the US page be part of the WW template or removed?
4. Can the personalization/ASIN container be disabled at the template level, or does it still require per-page SIMs?
