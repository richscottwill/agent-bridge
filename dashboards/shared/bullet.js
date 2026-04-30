/**
 * Shared bullet-chart helper — Stephen Few 2005 (M3 + M4 + M10 + MPE #078).
 *
 * A bullet chart encodes:
 *   1. An actual measurement (solid bar)
 *   2. A target (perpendicular tick mark)
 *   3. Qualitative performance bands (soft background fills)
 *
 * Designed to replace round gauges / speedometer dials / single-number
 * tiles with a compact, linear actual-vs-target comparator. Ships here
 * because both WR (vs-OP2 KPI card — M3) and MPE (distance-to-target —
 * #078) will consume it.
 *
 * Principle (report #015):
 *   A bullet communicates "actual against target, within qualitative
 *   bands" in under a second. A number alone needs the reader to do
 *   arithmetic.
 */

(function (global) {
  'use strict';

  // Default bands as fractions of target. [start, end, cls].
  // cls maps to `.bullet-band-<cls>` in bullet.css.
  const DEFAULT_BANDS = [
    [0.00, 0.80, 'bad'],
    [0.80, 0.95, 'warn'],
    [0.95, 1.20, 'good']
  ];

  /**
   * Render a bullet chart as HTML + inline styles.
   *
   * @param {Object} opts
   *   - actual  (number)  required. The current value.
   *   - target  (number)  required. The target / plan / reference.
   *   - bands   (array)   optional. Array of [start, end, cls] tuples;
   *                       values are fractions of `target`. Defaults to
   *                       [[0,0.8,'bad'],[0.8,0.95,'warn'],[0.95,1.2,'good']].
   *   - range   ([min,max]) optional. Axis extent in absolute units. When
   *                       omitted, computed as [0, max(target*1.2, actual*1.1)].
   *   - width   (number)  optional CSS width in px. Default: 100% of parent.
   *   - inverted (boolean) if true, lower values are better (e.g. CPA).
   *                       Defaults to false (higher = better).
   *   - label   (string)  aria-label; defaults to a plain-English summary.
   * @returns {string} HTML string
   */
  function renderBullet(opts) {
    opts = opts || {};
    const actual = Number(opts.actual);
    const target = Number(opts.target);
    if (!Number.isFinite(actual) || !Number.isFinite(target) || target === 0) {
      return '<div class="bullet bullet-empty" role="meter" aria-label="No target data"></div>';
    }
    const bands = opts.bands || DEFAULT_BANDS;
    const inverted = !!opts.inverted;

    // Determine axis extent. Default leaves a bit of headroom above
    // target so the "good" band is visible even when actual is below.
    let axisMin = 0;
    let axisMax;
    if (Array.isArray(opts.range) && opts.range.length === 2) {
      axisMin = opts.range[0];
      axisMax = opts.range[1];
    } else {
      // Last band's end × target sets the upper bound, unless actual
      // exceeds it (in which case scale to actual+10%).
      const bandMax = bands.length ? bands[bands.length - 1][1] * target : target * 1.2;
      axisMax = Math.max(bandMax, actual * 1.1);
    }
    const axisRange = axisMax - axisMin;
    const pct = (v) => axisRange > 0
      ? Math.max(0, Math.min(100, ((v - axisMin) / axisRange) * 100))
      : 0;

    // Render band fills — each absolute-positioned, width-as-pct, inset by left/right.
    const bandDivs = bands.map(([start, end, cls]) => {
      const leftPct = pct(start * target);
      const widthPct = Math.max(0, pct(end * target) - leftPct);
      return (
        `<div class="bullet-band bullet-band-${cls}" ` +
        `style="left:${leftPct.toFixed(2)}%;width:${widthPct.toFixed(2)}%" ` +
        `aria-hidden="true"></div>`
      );
    }).join('');

    const actualPct = pct(actual);
    const targetPct = pct(target);

    // Direction-aware class on the actual bar — meets target or doesn't.
    const meetsTarget = inverted ? actual <= target : actual >= target;
    const actualCls = meetsTarget ? 'bullet-actual-good' : 'bullet-actual-bad';

    const label = opts.label ||
      `Actual ${actual.toLocaleString()} vs target ${target.toLocaleString()}, ` +
      `${meetsTarget ? 'meets or exceeds' : 'below'} target`;

    const inlineStyle = opts.width ? `width:${opts.width}px` : '';

    return (
      `<div class="bullet" role="meter" ` +
      `aria-valuemin="${axisMin}" aria-valuemax="${axisMax}" aria-valuenow="${actual}" ` +
      `aria-label="${label}" ${inlineStyle ? 'style="' + inlineStyle + '"' : ''}>` +
      bandDivs +
      `<div class="bullet-actual ${actualCls}" ` +
      `style="width:${actualPct.toFixed(2)}%" aria-hidden="true"></div>` +
      `<div class="bullet-target" ` +
      `style="left:${targetPct.toFixed(2)}%" aria-hidden="true"></div>` +
      `</div>`
    );
  }

  global.Bullet = { renderBullet, DEFAULT_BANDS };
})(typeof window !== 'undefined' ? window : this);
