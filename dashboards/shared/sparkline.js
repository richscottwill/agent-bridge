/**
 * Shared sparkline helper — Tufte word-sized graphics (M3 + M8 + M6 + M7).
 *
 * Renders a tiny line chart as SVG, suitable for embedding inside a KPI
 * card, table cell, inline prose, or thread cell. No axes, no legend,
 * no interaction — the whole point is "word-sized resolution" next to
 * the value it annotates.
 *
 * Consumers (current):
 *   - M3 · KPI cards (weekly-review.html — renderKPIs)
 *   - M8 · Prior-week thread (weekly-review.html — renderThreadStrip) (planned)
 *   - M6 · Small multiples (weekly-review.html — small multiples section) (planned)
 *
 * Principles the shape enforces (report #004 · Tufte):
 *   - No axes, no gridlines, no labels inside the sparkline.
 *   - Endpoint marker is a filled dot; no other markers.
 *   - Colour encodes direction; the only required semantic is "latest
 *     value vs prior avg".
 *   - Height is constant; width flexes. 72x18 is the default — roughly
 *     the size of a four-digit number in the surrounding serif.
 */

(function (global) {
  'use strict';

  /**
   * Build a sparkline SVG string.
   *
   * @param {number[]} values - the series to plot. Nulls are treated as gaps.
   * @param {Object} opts
   *   - color   (string)  CSS color for the stroke and endpoint dot. Default: '#0066cc'.
   *   - width   (number)  SVG width in px. Default: 72.
   *   - height  (number)  SVG height in px. Default: 18.
   *   - min, max (number) Optional Y-extent overrides for shared-axis rendering.
   *                       When omitted, computed from values.
   *   - showDot (boolean) Whether to paint the endpoint dot. Default: true.
   *   - strokeWidth (number) Default 1.5.
   *   - label   (string)  Optional aria-label; defaults to "Sparkline of N points".
   * @returns {string} SVG markup
   */
  function renderSparkline(values, opts) {
    opts = opts || {};
    const width       = opts.width  || 72;
    const height      = opts.height || 18;
    const color       = opts.color  || '#0066cc';
    const showDot     = opts.showDot !== false;
    const strokeWidth = opts.strokeWidth || 1.5;

    // Defensive: no points → empty SVG with the right aria-label so
    // screen readers don't announce "no accessible name".
    if (!values || !values.length) {
      return (
        `<svg class="sparkline" width="${width}" height="${height}" ` +
        `viewBox="0 0 ${width} ${height}" role="img" ` +
        `aria-label="${opts.label || 'Sparkline (no data)'}"></svg>`
      );
    }

    // Determine Y extent. `min` and `max` override for shared-axis cases
    // (e.g. M6 small multiples, where all 12 panels need to scale the
    // same way). Otherwise compute from the finite values in the series.
    const finite = values.filter(v => Number.isFinite(v));
    if (!finite.length) {
      return (
        `<svg class="sparkline" width="${width}" height="${height}" ` +
        `viewBox="0 0 ${width} ${height}" role="img" ` +
        `aria-label="${opts.label || 'Sparkline (no numeric data)'}"></svg>`
      );
    }
    let yMin = Number.isFinite(opts.min) ? opts.min : Math.min.apply(null, finite);
    let yMax = Number.isFinite(opts.max) ? opts.max : Math.max.apply(null, finite);
    // Degenerate case: all values equal. Give the line some vertical
    // padding so it doesn't collapse to the bottom edge.
    if (yMax === yMin) {
      const pad = Math.max(1, Math.abs(yMax) * 0.05);
      yMin -= pad;
      yMax += pad;
    }

    const xStep = values.length > 1 ? width / (values.length - 1) : 0;
    const scaleY = (v) => {
      if (!Number.isFinite(v)) return null;
      // Invert because SVG y=0 is at the top.
      const t = (v - yMin) / (yMax - yMin);
      // Inset by 1px so the stroke isn't clipped at the extremes.
      return 1 + (1 - t) * (height - 2);
    };

    // Build a polyline-compatible point list; null-safe by splitting on
    // gaps. We emit multiple <polyline> segments so the line doesn't
    // cross NaN regions.
    const segments = [];
    let cur = [];
    values.forEach((v, i) => {
      const y = scaleY(v);
      if (y == null) {
        if (cur.length) { segments.push(cur); cur = []; }
        return;
      }
      cur.push(`${(i * xStep).toFixed(2)},${y.toFixed(2)}`);
    });
    if (cur.length) segments.push(cur);

    const polylines = segments.map(pts => (
      `<polyline fill="none" stroke="${color}" stroke-width="${strokeWidth}" ` +
      `points="${pts.join(' ')}"/>`
    )).join('');

    // Endpoint dot — always sits on the last finite value.
    let endpoint = '';
    if (showDot) {
      for (let i = values.length - 1; i >= 0; i--) {
        const y = scaleY(values[i]);
        if (y != null) {
          const cx = (i * xStep).toFixed(2);
          endpoint = `<circle cx="${cx}" cy="${y.toFixed(2)}" r="2" fill="${color}"/>`;
          break;
        }
      }
    }

    const ariaLabel = opts.label ||
      `Sparkline of ${finite.length} point${finite.length === 1 ? '' : 's'}, ` +
      `last value ${finite[finite.length - 1]}`;

    return (
      `<svg class="sparkline" width="${width}" height="${height}" ` +
      `viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" ` +
      `role="img" aria-label="${ariaLabel}">` +
      polylines + endpoint +
      `</svg>`
    );
  }

  global.Sparkline = { renderSparkline };
})(typeof window !== 'undefined' ? window : this);
