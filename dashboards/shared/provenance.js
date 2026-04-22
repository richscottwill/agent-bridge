/**
 * Provenance labels — who produced each card/section on the Kiro dashboard.
 *
 * Used by the leadership demo to show the human↔agent collaboration pattern.
 * Every card tells you its producer (agent / human / agent-reviewed-by-human).
 *
 * Design principles (soul.md):
 *   - Invisible over visible: labels are muted by default, readable up close.
 *   - Structural: metadata belongs to the data, not the markup. Cards pass
 *     a producer object and this module renders it identically everywhere.
 *   - Reduce decisions: emoji + short label + tooltip. No config, no options.
 */

(function () {
  'use strict';

  // Producer type → (emoji, label, color token)
  const TYPES = {
    agent:   { emoji: '🤖', label: 'Agent',    tone: '#93b4f5' }, // blue
    human:   { emoji: '👤', label: 'Human',    tone: '#e0c080' }, // warm
    reviewed:{ emoji: '🤝', label: 'Reviewed', tone: '#4ade80' }, // green
    system:  { emoji: '⚙️', label: 'System',   tone: '#9ca3af' }, // grey
  };

  /**
   * Render a provenance badge.
   *
   * @param {Object} prov - { type: 'agent'|'human'|'reviewed'|'system', producer: 'short name', detail: 'tooltip text', href?: 'link' }
   * @returns {string} HTML string — inline span with emoji + label.
   */
  function render(prov) {
    if (!prov || !prov.type) return '';
    const t = TYPES[prov.type] || TYPES.system;
    const producer = prov.producer || t.label;
    const tip = prov.detail ? ` title="${escapeAttr(prov.detail)}"` : '';
    const cursor = prov.href ? ' style="cursor:pointer"' : '';
    const click = prov.href ? ` onclick="event.stopPropagation();window.open('${escapeAttr(prov.href)}','_blank')"` : '';
    return `<span class="prov-badge prov-${prov.type}"${tip}${cursor}${click}>`
      + `<span class="prov-emoji">${t.emoji}</span>`
      + `<span class="prov-label">${escapeHtml(producer)}</span>`
      + `</span>`;
  }

  /**
   * Render a provenance bar — full row attached to a section header.
   * Shows up to 3 contributors and a "trace" link if present.
   *
   * @param {Array<Object>} provs - array of provenance entries
   * @param {string} [trace] - optional URL to the full lineage
   */
  function renderBar(provs, trace) {
    if (!provs || !provs.length) return '';
    const items = provs.slice(0, 3).map(render).join('');
    const more = provs.length > 3 ? `<span class="prov-more">+${provs.length - 3} more</span>` : '';
    const traceLink = trace ? `<a class="prov-trace" href="${escapeAttr(trace)}" target="_blank" onclick="event.stopPropagation()">trace →</a>` : '';
    return `<div class="prov-bar">${items}${more}${traceLink}</div>`;
  }

  /**
   * Inject a provenance bar after a section label element.
   *
   * @param {string} sectionId - DOM id of the section label (e.g. 'sec-blocks')
   * @param {Array<Object>} provs
   * @param {string} [trace]
   */
  function injectBar(sectionId, provs, trace) {
    const el = document.getElementById(sectionId);
    if (!el || !provs || !provs.length) return;
    // Remove any existing bar
    const existing = el.parentElement.querySelector('.prov-bar');
    if (existing) existing.remove();
    el.insertAdjacentHTML('afterend', renderBar(provs, trace));
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  function escapeAttr(s) {
    return String(s).replace(/"/g, '&quot;');
  }

  // CSS — inject once per page
  function ensureStyles() {
    if (document.getElementById('prov-styles')) return;
    const style = document.createElement('style');
    style.id = 'prov-styles';
    style.textContent = `
      .prov-bar{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:4px 0 10px;font-size:11px;color:#666;line-height:1.4}
      .prov-badge{display:inline-flex;align-items:center;gap:3px;padding:2px 7px;border-radius:10px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);font-size:11px;font-weight:500;transition:all .15s}
      .prov-badge:hover{background:rgba(255,255,255,.08);border-color:rgba(147,180,245,.25)}
      .prov-emoji{font-size:11px;line-height:1}
      .prov-label{color:#9aa3b0;font-weight:500;letter-spacing:.1px}
      .prov-agent .prov-label{color:#93b4f5}
      .prov-human .prov-label{color:#e0c080}
      .prov-reviewed .prov-label{color:#4ade80}
      .prov-system .prov-label{color:#9ca3af}
      .prov-more{font-size:11px;color:#555;padding:0 4px}
      .prov-trace{font-size:11px;color:#6b8acd;text-decoration:none;margin-left:auto;padding:2px 6px;border-radius:3px;transition:background .1s}
      .prov-trace:hover{color:#93b4f5;background:rgba(30,58,138,.15)}
    `;
    document.head.appendChild(style);
  }

  // Public API
  window.Provenance = {
    render,
    renderBar,
    injectBar,
    ensureStyles,
  };

  // Auto-init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ensureStyles);
  } else {
    ensureStyles();
  }
})();
