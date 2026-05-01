/**
 * shortcuts-overlay.js — shared keyboard-shortcut help overlay.
 *
 * Consumer registers an array of {keys, description} and wires bindShortcuts()
 * to their page's keydown handlers. The overlay itself is self-contained: "?"
 * toggles it, Escape closes it. No emoji, no framework dependency.
 *
 * Usage:
 *   window.ShortcutsOverlay.install([
 *     { keys: 'J',  description: 'Next week' },
 *     { keys: 'K',  description: 'Previous week' },
 *     { keys: 'R',  description: 'Reset filters' },
 *     { keys: '/',  description: 'Focus market picker' },
 *     { keys: '?',  description: 'Toggle this overlay' },
 *   ]);
 *
 * The overlay DOM is created on first install and reused across subsequent
 * calls (useful for dynamic rebinding). Overlay is a centered modal with a
 * translucent backdrop.
 */
(function(global){
  'use strict';

  let overlayEl = null;
  let visible = false;

  function ensureOverlay() {
    if (overlayEl) return overlayEl;
    overlayEl = document.createElement('div');
    overlayEl.className = 'wk-shortcuts-overlay';
    overlayEl.setAttribute('role', 'dialog');
    overlayEl.setAttribute('aria-modal', 'true');
    overlayEl.setAttribute('aria-label', 'Keyboard shortcuts');
    overlayEl.style.cssText = [
      'position:fixed', 'inset:0',
      'background:rgba(0,0,0,0.35)', 'display:none',
      'align-items:center', 'justify-content:center',
      'z-index:10000',
    ].join(';');
    overlayEl.addEventListener('click', (e) => {
      if (e.target === overlayEl) hide();
    });
    document.body.appendChild(overlayEl);
    return overlayEl;
  }

  function renderBody(shortcuts) {
    const rows = shortcuts.map(s => {
      const keyHtml = String(s.keys)
        .split('+')
        .map(k => `<kbd style="background:#f3f4f6;border:1px solid #d1d5db;border-radius:4px;padding:2px 6px;font-family:ui-monospace,monospace;font-size:12px">${escapeHtml(k.trim())}</kbd>`)
        .join(' + ');
      return `<tr><td style="padding:6px 12px;vertical-align:top">${keyHtml}</td><td style="padding:6px 12px;color:#1f2937">${escapeHtml(s.description || '')}</td></tr>`;
    }).join('');
    return `
      <div style="background:#FFFFFF;border-radius:8px;box-shadow:0 12px 40px rgba(0,0,0,0.25);max-width:480px;min-width:360px;max-height:80vh;overflow:auto;padding:20px 24px 16px">
        <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px">
          <h3 style="margin:0;font-size:16px;font-weight:600;color:#111827">Keyboard shortcuts</h3>
          <button type="button" aria-label="Close shortcuts overlay" class="wk-shortcuts-close" style="background:none;border:0;font-size:20px;line-height:1;color:#6b7280;cursor:pointer;padding:0 4px">x</button>
        </div>
        <table style="border-collapse:collapse;width:100%;font-size:13px">${rows}</table>
        <div style="margin-top:12px;font-size:11px;color:#6b7280">Press <kbd style="background:#f3f4f6;border:1px solid #d1d5db;border-radius:3px;padding:1px 4px;font-family:ui-monospace,monospace">Esc</kbd> or <kbd style="background:#f3f4f6;border:1px solid #d1d5db;border-radius:3px;padding:1px 4px;font-family:ui-monospace,monospace">?</kbd> again to dismiss.</div>
      </div>`;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c => (
      { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]
    ));
  }

  function show(shortcuts) {
    const el = ensureOverlay();
    el.innerHTML = renderBody(shortcuts);
    el.style.display = 'flex';
    visible = true;
    const close = el.querySelector('.wk-shortcuts-close');
    if (close) close.addEventListener('click', hide);
  }

  function hide() {
    if (overlayEl) overlayEl.style.display = 'none';
    visible = false;
  }

  function toggle(shortcuts) { visible ? hide() : show(shortcuts); }

  /**
   * install(shortcuts)
   *   shortcuts: Array<{keys:string, description:string}>
   * Binds the global "?" key to toggle the overlay + Escape to dismiss.
   * Idempotent: calling install() twice rebinds to the new list without
   * duplicating keydown listeners.
   */
  function install(shortcuts) {
    const list = Array.isArray(shortcuts) ? shortcuts : [];
    if (!install._bound) {
      document.addEventListener('keydown', (e) => {
        // Ignore when user is typing in an input/textarea/contenteditable
        const t = e.target;
        const tag = (t && t.tagName || '').toLowerCase();
        const editable = t && (t.isContentEditable || tag === 'input' || tag === 'textarea' || tag === 'select');
        if (e.key === 'Escape' && visible) { hide(); return; }
        if (editable) return;
        if (e.key === '?' || (e.shiftKey && e.key === '/')) {
          e.preventDefault();
          toggle(install._currentShortcuts || []);
        }
      });
      install._bound = true;
    }
    install._currentShortcuts = list;
  }

  global.ShortcutsOverlay = { install, show, hide, toggle };
})(window);
