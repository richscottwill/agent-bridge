/**
 * section-freshness.js — subtle per-section "last updated" labels.
 *
 * Behavior:
 *   On DOMContentLoaded, finds every <h2> on the page and inserts a muted
 *   timestamp label below it. Ages the color from green (<3d) -> yellow
 *   (3-7d) -> red (>7d). Pulls updated timestamps from the manifest at
 *   ../data/section-freshness.json (page-relative path configurable).
 *
 * Section identification:
 *   Prefers explicit id="" on the h2. Falls back to a slug of the heading
 *   text. An h2 with data-freshness-skip is skipped.
 *
 * Soul check:
 *   - Invisible over visible: tiny text below each heading, same color palette
 *     as existing sub-text. Only noticeable when something is stale.
 *   - Subtraction before addition: no new section added to any page — just a
 *     label appended to existing headings.
 *
 * Portability:
 *   No framework deps. Pure DOM + fetch. Safe to ship anywhere.
 */
(function () {
  'use strict';

  // Manifest location relative to current page. Pages at dashboard root use
  // ./data/...; pages in subfolders use ../data/... The script auto-detects.
  function resolveManifestPath() {
    // WR-B1-3 (2026-04-29): original impl derived depth from a
    // `/dashboards/` URL substring, but the localhost:8080 server roots
    // at `~/shared/dashboards/` so URLs never contain that literal
    // prefix. Regex missed → depth=0 → page-relative `data/` → 404 on
    // `/performance/data/section-freshness.json`. Use pathname segment
    // count instead: `/performance/weekly-review.html` → 2 segments →
    // depth=1 → prefix `../data/` → correctly resolves to `/data/...`.
    var pathname = window.location.pathname;
    var parts = pathname.split('/').filter(Boolean);
    // Last segment is the filename (or empty for directory URLs); prior
    // segments are directories. Depth = number of parent dirs above root.
    var depth = Math.max(0, parts.length - 1);
    var prefix = depth === 0 ? 'data/' : '../'.repeat(depth) + 'data/';
    return prefix + 'section-freshness.json';
  }

  function pageKey() {
    var pathname = window.location.pathname;
    var m = pathname.match(/\/dashboards\/(.*)$/);
    if (!m) return 'unknown';
    var key = m[1] || 'index.html';
    if (key.endsWith('/')) key += 'index.html';
    return key;
  }

  function slugify(text) {
    return (text || '')
      .toLowerCase()
      .replace(/&[a-z]+;/g, ' ')
      .replace(/<[^>]+>/g, ' ')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 80);
  }

  function daysBetween(isoStr) {
    if (!isoStr) return null;
    var then = new Date(isoStr);
    if (isNaN(then.getTime())) return null;
    var now = new Date();
    return Math.floor((now - then) / (1000 * 60 * 60 * 24));
  }

  function formatAge(days) {
    if (days === null) return 'unknown';
    if (days <= 0) return 'today';
    if (days === 1) return '1d ago';
    if (days < 30) return days + 'd ago';
    var months = Math.floor(days / 30);
    if (months < 12) return months + 'mo ago';
    return Math.floor(days / 365) + 'y ago';
  }

  function colorForAge(days) {
    if (days === null) return 'var(--text3, #5a6a7a)';
    if (days < 3) return 'rgba(74, 222, 128, 0.55)';   // green, muted
    if (days < 7) return 'rgba(251, 191, 36, 0.70)';   // amber
    return 'rgba(248, 113, 113, 0.75)';                 // red
  }

  function injectStyles() {
    if (document.getElementById('section-freshness-style')) return;
    var style = document.createElement('style');
    style.id = 'section-freshness-style';
    style.textContent =
      '.section-freshness{' +
        'display:inline-block;' +
        'font-size:0.70em;' +
        'font-weight:500;' +
        'letter-spacing:0.3px;' +
        'text-transform:uppercase;' +
        'margin-left:10px;' +
        'vertical-align:middle;' +
        'opacity:0.8;' +
        'cursor:help;' +
      '}';
    document.head.appendChild(style);
  }

  function render(manifest) {
    var key = pageKey();
    var pageData = (manifest && manifest.pages && manifest.pages[key]) || {};
    var headings = document.querySelectorAll('h2');
    headings.forEach(function (h) {
      if (h.hasAttribute('data-freshness-skip')) return;
      // Skip h2 inside dynamically rendered cards (e.g., a detail modal)
      if (h.closest('.modal, .detail-modal')) return;
      // Skip h2 that appear inside <script> template strings will not be in DOM
      var sectionId = h.id || slugify(h.textContent || '');
      if (!sectionId) return;
      var entry = pageData[sectionId];
      var iso = entry && entry.updated_iso;
      var source = entry && entry.source;
      var days = daysBetween(iso);
      var label = document.createElement('span');
      label.className = 'section-freshness';
      label.style.color = colorForAge(days);
      label.textContent = iso ? 'updated ' + formatAge(days) : 'updated —';
      var tooltip = iso
        ? 'Last updated: ' + iso + (source ? ' (source: ' + source + ')' : '')
        : 'No freshness data for this section';
      label.title = tooltip;
      h.appendChild(label);
    });
  }

  function init() {
    injectStyles();
    fetch(resolveManifestPath() + '?t=' + Date.now())
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(render)
      .catch(function () { render({}); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
