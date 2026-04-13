---
title: "Bi-Weekly: Unlock Marketing Superpowers (PSME)"
status: DRAFT
audience: amazon-internal
owner: Richard Williams
created: 2026-04-12
updated: 2026-04-12
---
<!-- DOC-0210 | duck_id: meeting-psme-marketing-superpowers -->

# Bi-Weekly: Unlock Marketing Superpowers (PSME)

## Metadata
- Cadence: Bi-weekly (Thursday, 8am PT)
- Attendees: Richard Williams, Ravi, Chinmay, Anand, Kishore, Shrinivas, Pratiba, Sunil, Shannon, Lake, Popus, Alexis Eck, Lena Zak, Lorena Alvarez Larrea + broader PSME/AB Prime product team
- Hedy Topic: (not mapped — first capture)
- Outlook Series: Bi-Weekly: Unlock Marketing Superpowers: PSME, AB Prime Product Demo & Feedback Series

## Context
Product demo and feedback series for marketing tools (Marketly, Omniaya). Cross-functional: product teams demo new capabilities, marketing teams provide feedback and plan adoption. Richard's role: PS perspective on channel expansion (WhatsApp, push) for AU/MX markets. Alexis, Lena, and Lorena attend — opportunity for cross-market coordination on new channels.

## Latest Session
### 2026-04-02 — WhatsApp and Push Campaigns Demo (52 min)
- WhatsApp campaign capabilities in Marketly: 4 template types (no image, static image, personalized image, double-button). Scheduling: one-time, daily, weekly. Targeting via Bullseye segments.
- Performance: WhatsApp achieves ~24x higher CTR and 2.5–3x higher open rates vs email. India-focused currently — mobile-heavy market (70% B2B purchases on mobile, email open rates only 21% vs 50-60% WW).
- Channel separation issue: AB and retail share same WhatsApp handle (Amazon.in). Bullseye segmentation gates targeting, but Shuma customers (dual B2B/B2C accounts) create overlap risk. Dedicated AB handle in development.
- No in-console preview for WhatsApp — must use Sonar tool in production. Suboptimal but necessary due to beta limitations.
- Push notifications launching via Omniaya AI for US marketplace (EN-US, ES-US). Workflow mirrors email. iOS/Android layout previews. AI-powered campaign creation from marketing brief or scratch.
- Two new push testing features: (1) "Send Test Push" via full API (daily limit), (2) "Send Preview" generates JSON for manual Sonar testing.
- TNC text/link fixed across all WhatsApp campaigns (legal requirement). No auto-opt-in — customers auto-enrolled at account creation, can opt out after first message.
- Fallback image support for WhatsApp not available yet — prioritization TBD (now vs next quarter).
- Decisions: WhatsApp for engagement only (existing V2B customers, not acquisition). Push launches US-first, then global. Dual-button templates supported for high-velocity events.
- Action items:
  - Anand's team: create separate AB WhatsApp handle (ASAP)
  - Chinmay: enable in-console WhatsApp preview in Marketly (future)
  - Omniaya team: publish release notes with limitations and tested scenarios
  - Richard: follow up with Lorena (MX) and Alexis (AU) on WhatsApp rollout plans for their markets

## Running Themes
- Channel expansion beyond email: WhatsApp (India-first), push (US-first), with global expansion planned
- AB vs retail channel separation: shared handles create targeting risk
- Preview/testing friction: no in-console preview, reliance on Sonar
- Mobile-first markets (India, MX) are natural WhatsApp adoption candidates

## Open Items
- [ ] Richard: follow up with Lorena and Alexis on WhatsApp rollout plans for MX and AU
- [ ] Anand's team: dedicated AB WhatsApp handle creation
- [ ] Omniaya: release notes for push campaign launch
- [ ] Chinmay: in-console WhatsApp preview timeline
