---
audience: amazon-internal
creator: Richard Williams
doc_type: document
last_modified: 2025-01-08
mirror_date: 2026-04-10
owner: Richard Williams
quip_folder: Onboarding/Data
quip_id: JNa9AA24e9W
source_url: https://quip-amazon.com/JNa9AA24e9W
status: DRAFT
title: Adobe Activity Map
topics:
- onboarding
- data
- analytics
backfill_status: backfilled
---

# Adobe Activity Map
#### Install plug-in:
 * Go to Adobe Analytics > Tools > Activity Map.
 * Clicking on Activity Map will take you to Download page where you can download extension.
 * [Link to article][1] for browser-specific setup.
#### Launch the extension:
 * After installation, browser extension will be in the top-right corner.
 * Navigate to the [business.amazon.com][2] website you want to see data on, click on the extension button to log in.
  * During login, if asked to choose, log in to Amazon Services LLC.
 * The activity map overlay appear and begin to load. (blue squares)
  * ![image.png][3]
#### Using Activity Map:
 * Activity Map has presets that you can adjust. Below I’ll go over each of the selections line by line.
  * **Standard**: Standard vs. Live (Live allows you to view data more granular than daily)
  * **Link Clicks**: This one is the event that you’d like to view for the specific page you’re on. You can change to any event that’s currently on Adobe Analytics. I wouldn’t change this around too much because you’d only want to select events that users are able to take on the page you’re looking at (and only events that are compatible.)
  * “**None**”: The third thing you can adjust is the audience. If none are selected, then it’ll show all traffic to the page. Some good audiences to narrow down to are :
   * Visitors to ABMCS with Refmarker. You can filter out organic/direct traffic this way.
   * New visits.
   * Free Offsite search.
   * Authenticated AB Customer. If you’d like to see behavior of existing registrants.
  * **Gradient**: This is a visual thing. You can view bubbles with the percentage/volume of clicks on screen, or gradient, which will highlight each link on the page inside of a box
  * **Date**: The last thing is the time range you’d like to view.
  * **Toggle Page Details:** On the top-right of the page, you can see an eye icon, which is clickable, and will open up details at the bottom. From here, you can view each link on the page, and the percentage/volume of total clicks on each link. You can also click the arrow on the top left to see aggregate data and a visual flow to see how your audience got there, and which action they eventually took. (left site, went to HP, registered)
  * **Settings**: On the top-right, you’ll also see a gear icon to go to settings.
   * You want to make sure that the “Report Suite” selected is your market’s tag (A production tag)
   * You can change between % of, or Volume numbers in the “Label overlays with” section here.
   * You can also change settings for Standard and Live views to include or exclude number of links to visualize on the page. (they default to a lower amount to keep the page from being cluttered) We don’t have too many links so you can increase this if you’d like.
 * [Link to video][4] to see Adobe’s walkthrough.

Overall, the tool is great for seeing a holistic view of page performance or page behavior for specific pages. For aggregate data, or data over time (monthly data over the past year), you’d want to view a report either by creating an ABMA ticket or via Adobe Analytics.

[1]: https://experienceleague.adobe.com/docs/analytics/analyze/activity-map/getting-started/get-started-users/activitymap-install.html?lang=en
[2]: http://business.amazon.com
[3]: https://quip-amazon.com/blob/JNa9AA24e9W/GmXTCgCITD3wjq7dekw_bQ
[4]: https://experienceleague.adobe.com/docs/analytics-learn/tutorials/components/activity-map/activity-map-overview.html?lang=en
