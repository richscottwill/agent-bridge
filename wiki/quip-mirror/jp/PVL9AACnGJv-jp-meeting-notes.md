---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: '2023-12-27'
mirror_date: '2026-04-10'
owner: Richard Williams
quip_folder: JP/Meeting
quip_id: PVL9AACnGJv
source_url: https://quip-amazon.com/PVL9AACnGJv
status: DRAFT
title: JP Meeting notes
topics:
- JP
- meetings
- nonbrand
- AVT
- callback
- strategy
backfill_status: backfilled
---

# JP Meeting notes
# 2022.10.06
* Sey: Alex, Todd, and Fernando
 * JP team is creating a plan to finalize
 * Any big bets, then let Minami know and she'll add to doc
 * Project Jupiter, SBM, and ABX
 * SSR (OP1 discussion for 2023)
* Nonbrand:
 * Peter: Jamie wrote something about Jasper doc (virtual visit in March)
 * Maybe use doc with Alex, Todd, and Fernando to talk about piloting/improvements for paid search in 2023
# 2022.09.19
Mao - Telemarketing/paid search
* Work with Mao on more of a daily basis
Minami - Owns whole of acquisition, except paid search/email/telemarketing
* If more impact on registrations, then Minami
* Minami wants to create plan sales and events, and implement across channels
* * Have a quick update on small business month/anniversary for JP weekly update

Sei
* Want to increase Registration volume.
* Does nonbrand really not work in JP?
 * JP market could help with local
 * Also, why does US/EU work on NB?
 * It could be that JP uses First-touch attribution rather than Multi-touch.
  * *Is there a way to look at session data? (like GA) (ABGI - Rimpei can advise)
  * EU, US, JP look at in aggregate.
 * Want to understand the difference between EU/US vs. JP
  * Are we all structured the same?
* Should we ask JP agency to help understand?
* *Can we do keyword mining using jp data?
* *Start with RLSA campaigns?
* *LP specifically for NB? (need to come up with hypotheses and design LPs around tests)
* *Brandon: AVT data and see performance. Maybe people just don't want to put stuff into forms. (It's the CVR that isn't good?)
* *Paid Social - Linkedin acquisition test?
* *Drive nonbrand to [A.com][1] Amazon Business LP? (but they're not going to see pricing for members)
* Test a small number of keywords, and we'll have negative keywords applied as a safeguard.
 * Ask Google/Yahoo, if a person in US/CA will be more explicit about their search behavior.
* Is there room to tweak? Peter says probably yes.
 * Want to have a test fund for NB. (Set a mixed CPA target)
 * Maybe we can use Yahoo JP (the Yahoo team said they have access to 30% of audience data) audience data.

# 2022.09.13
Here are the notes and action items from today's meeting. There was a lot of back and forth in some parts of the meeting, so it might read like a script in certain parts. (really engaging meeting) Let me know if the below is concise enough.

**JP Callback page:**
* Main concern was that the callback CTA would reduce the number of direct registrations, but Sey is glad that this is not the case.
* Another concern was the cost, but Sey says that he doesn't care about this. Registrations are more valuable.
* Peter: shorten the amount of info needed, because of hesitancy across markets to provide info, and also because we could utilize progressive profiling rather than getting all info up-front.
 * Worth exploring which fields are required and which are optional based on market.
 * Suggestion to remove fields from front-end, and have them send null data on back end.
* SSR CTA: Interest in  testing additional CTAs on the LP to enhance visibility/interest in SSR  (vs Lead Form). Peter to look into possible changes.
* Callback Timing:
 * Callback is believed to  occur chronologically (rather than by size of opp). Minami is verifying.
 * Callbacks tend to occur  within 24 hours. Minami believes this can be further minimized and is  following up with Mao
 *
Action items:
* **Minami** to talk with Agency to speed up callback time (so that people will be reached when they're still engaged in the process)
* **Peter** to talk with Design team to support/give direction on improving the page.
* **Unclear who**: Explore the idea of shortening necessary fields, and tailoring to markets.
 * BY: I believe this  would be taken on by the JP team. Confirm with Peter; I believe he  mentioned they should work with 'Andrew'?

**Nonbrand:**
* Sey: In other markets we see that NB is bigger than in JP.
 * We have to figure this out. Dive deep to get to the bottom of this.
* Brandon: CPA for EU is right around 10x higher than Brand. It's about 30x in JP.
 * Peter/Chunsoo have tested in the past, and it may be brand penetration that's preventing success in NB.
 * Project Jupiter approved in OP1, planning to execute end of Q1 or in Q2 2023.
 * Is there  capability to retarget viewers/engagers of Proj Jupiter ads (PMax?), if  unknown, lets add to the next Google agenda.
 * Sey suggested that JP brand sentiment isn't worse than US/EU.
* The intent in the past (2019) was that we would restart NB and catch up to US/EU.
 * Definition of Brand and NB may have been different in 2019; also attribution may have been different.
 * We're not allowed to use general terms such as PC monitor alone because [amazon.com][2] team are given precedent for terms like this.
 * Competitor campaign: In JP, we can't bid on keywords of competitors. (different from our other accounts where we could bid on competitor and not use their name in the ads)
 * Another friction point that Chunsoo highlighted in chat: Keyword discovery process has been a challenge, even when we had internal resource in the past.
 * This may  be an opportunity for you, Richard. If we decide to test NB in the  future, you can collab with Yahoo JP to identify top kw opps. I also  think it might be interesting to test BSAs on NB.
* From a broad perspective, we tend to use a couple tactics:
 * LP to ask for registration/form fill
 * Offering discount, which may not apply to the items the user are interested in.
 * Suggestion: Maybe doing something similar to other competitor; sending users to a content site where users can browse products and see if discount is applicable and product is available.
  * Sey: Verification is a friction point, and Auto-Verification (AVT) is one solution that will help.
 * This is a pain point  across all countries. We're hoping there will be an immediate shopping  experience available in the future, but this is a controversial topic.
Action items:
* Action items for NB [highlighted in Quip][3]. No objections to them.

**AVT**:
* We've been talking through AVT, and hoping to get verification team to approve within a week or so.
* Minami: Tested in the past with Google Audiences. (Verify customers based on query rather than audience.)
 * Minami/Sey concerned about whether customers would abuse this, so maybe launch at a small scale?
 * Chunsoo: We can run an experiment within Google to split traffic and assess. (relatively simple implementation)
 * Concern is that non-businesses will enter site if they were to find out.
  * Currently 89% are verified businesses in JP, which is higher than other markets.
  * We see increased registrations on Branded traffic, and we can monitor fraud on an automated basis. (Investigate ref tags for traffic that comes back as fraud)
 * This round, we'll assess fraud rate/verified positive rate via Google audience. Sey is apprehensive about using channel to identify verified users.
  * Minami: Using Amazon business is fine, but biggest risk is giving credit line to customers that are auto-verified.
  * Sey: People are auto-verified, have access to Amazon Business, and will not be required to give registration details (legitimate business info) that we can verify later. We don't know how many of these people will be B2B vs. B2C. Anyone that knows they just have to search on Google will be able to do this to bypass.
  * Is it possible to auto-verify for view-only access, and verify info to have purchase?
  * Peter: We're trying to test this initiative. Should we test in larger markets first, then bring back to JP?
   * Sey would be comfortable if the verification team approves this and is also comfortable with the idea.
Action items:
* **Peter**: Work with verification team to approve, then communicate back to Sey. (Already in progress.)
 * If moving forward with  AVT, Minami/JP will need to investigate whether they can be barred from  credit lines until further verification is performed.
 * If moving forward,  Chunsoo may need to setup A/B test to monitor VP rates for non-AVT  registrants
[1]: http://A.com
[2]: http://amazon.com
[3]: https://quip-amazon.com/NbCOANa6BYTh/JP-2022-Paid-Search
