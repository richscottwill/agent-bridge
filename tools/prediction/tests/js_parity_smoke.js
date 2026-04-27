// Phase 6.1.7 JS parity smoke: MX Y2026 @ 75% via V1_1_Slim, compare to Python.

const fs = require('fs');
const path = require('path');

// Load v1_1_slim.js (sets V1_1_Slim on globalThis)
const slimSrc = fs.readFileSync(path.join(__dirname, '..', '..', '..', 'dashboards', 'v1_1_slim.js'), 'utf8');
eval(slimSrc);

// Load projection-data.json
const data = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', '..', 'dashboards', 'data', 'projection-data.json'), 'utf8'));

const markets = ['MX', 'US', 'DE', 'UK', 'FR', 'IT', 'ES', 'JP', 'CA', 'AU'];
console.log('JS V1_1_Slim parity smoke — Y2026 @ ieccp:0.75 (AU spend:500K)');
console.log(''.padEnd(80, '-'));

for (const m of markets) {
  const mdata = data.markets[m];
  if (!mdata || mdata.error) { console.log(`${m}: NO DATA`); continue; }
  const targetMode = m === 'AU' ? 'spend' : 'ieccp';
  const targetValue = m === 'AU' ? 500000 : 0.75;
  const v11 = V1_1_Slim.projectWithLockedYtd(mdata, 2026, targetMode, targetValue, {});
  const ie = v11.totals.computed_ieccp == null ? 'null' : v11.totals.computed_ieccp.toFixed(2) + '%';
  console.log(`${m.padEnd(3)} | total_spend $${Math.round(v11.totals.total_spend).toLocaleString().padStart(13)} | total_regs ${Math.round(v11.totals.total_regs).toLocaleString().padStart(9)} | ie%CCP ${ie.padStart(7)}`);
}
