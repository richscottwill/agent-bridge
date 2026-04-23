#!/usr/bin/env python3
"""seed_mx_demo_artifacts.py — seed MX preset bundles + narrative template.

Writes:
- 6 preset bundles as `preset_bundle_{name}` rows in ps.market_projection_params
- 1 narrative_template row with market-specific template honoring ieccp_bound strategy

All values grounded in MX 2026 run-rate context (per session log: Lorena conversation
2026-04-22, $325k Q2 baseline, Polaris INTL post-launch baseline, W15 NB drop provisional).
"""
import json
import os
import sys

sys.path.insert(0, os.path.expanduser('~/shared/tools'))
import duckdb
from prediction.config import MOTHERDUCK_TOKEN

con = duckdb.connect(f'md:ps_analytics?motherduck_token={MOTHERDUCK_TOKEN}', read_only=False)

MX_PRESETS = {
    'base': {
        'description': 'Current run-rate projection with no adjustments',
        'spend_multiplier': 1.00,
        'brand_uplift_pct': 0,
        'nb_uplift_pct': 0,
    },
    'conservative': {
        'description': '10% spend pullback — efficiency mode',
        'spend_multiplier': 0.90,
        'brand_uplift_pct': 0,
        'nb_uplift_pct': 0,
    },
    'moderate': {
        'description': 'Current run-rate sustained',
        'spend_multiplier': 1.00,
        'brand_uplift_pct': 0,
        'nb_uplift_pct': 0,
    },
    'aggressive': {
        'description': '15% Brand spend uplift, NB flat',
        'spend_multiplier': 1.05,
        'brand_uplift_pct': 15,
        'nb_uplift_pct': 0,
    },
    'placement_persists': {
        'description': '12% Brand uplift sustained (new placement opportunity)',
        'spend_multiplier': 1.04,
        'brand_uplift_pct': 12,
        'nb_uplift_pct': 0,
    },
    'placement_decays': {
        'description': '12% Brand uplift decaying over 12 weeks (novelty effect)',
        'spend_multiplier': 1.02,
        'brand_uplift_pct': 6,   # average over decay window
        'nb_uplift_pct': 0,
    },
}

# Market-specific narrative template (honors ieccp_bound strategy, references regime events)
MX_NARRATIVE_TEMPLATE = """MX {time_period} projection: {total_regs:,.0f} registrations on {total_spend_fmt} spend, blended CPA {blended_cpa_fmt}, ie%CCP {ieccp:.1f}% vs 100% target. 90% credible interval on total regs: {regs_ci90_lo:,.0f} to {regs_ci90_hi:,.0f}. Brand contributes {brand_regs:,.0f} regs ({brand_pct:.0f}% of spend); NB contributes {nb_regs:,.0f} regs.

MX is an ie%CCP-bound market — Lorena manages against the 100% ceiling, which means every spend lever is evaluated against whether it moves us closer to 100% or further away. Current baseline reflects Polaris INTL post-launch (2025-08-28 structural shift), with Semana Santa and 2026-W15 NB drop accounted for as transients with known decay profiles.

Fit quality: Brand CPA elasticity r²=0.56 (market-specific, 110 weeks) but 12-week holdout MAPE 64.7% — holdout spans three regime events (Polaris + Semana Santa + W15). NB CPA elasticity r²=0.59 with holdout MAPE 13.3% (clean). YoY is a growth-ramp artifact (+69% ±114%) — multi-year MX projections fire VERY_WIDE_CI per R11.8.

For Lorena conversations: Brand is the demand-clean lever (11% of spend but ~3.5× the CCP impact per reg). NB is the volume lever. The W15 NB drop investigation with Yun-Kang is live; expect provisional regime flag to resolve at first refit (2026-07-15)."""

def seed():
    for name, spec in MX_PRESETS.items():
        value_json = {
            'spend_multiplier': spec['spend_multiplier'],
            'brand_uplift_pct': spec['brand_uplift_pct'],
            'nb_uplift_pct': spec['nb_uplift_pct'],
            'description': spec['description'],
        }
        param_name = f'preset_bundle_{name}'
        # Deactivate priors
        con.execute("""
            UPDATE ps.market_projection_params
            SET is_active = FALSE
            WHERE market = 'MX' AND parameter_name = ? AND is_active = TRUE
        """, [param_name])
        # Insert new
        con.execute("""
            INSERT INTO ps.market_projection_params
            (market, parameter_name, parameter_version, value_json, refit_cadence,
             last_refit_at, source, fallback_level, lineage, notes, is_active)
            VALUES (?, ?, 1, ?, 'annual', CURRENT_TIMESTAMP, 'manual_seed',
                    'market_specific', 'seeded via seed_mx_demo_artifacts.py 2026-04-22',
                    ?, TRUE)
        """, ['MX', param_name, json.dumps(value_json), spec['description']])
        print(f"Seeded {param_name}")

    # Narrative template
    con.execute("""
        UPDATE ps.market_projection_params
        SET is_active = FALSE
        WHERE market = 'MX' AND parameter_name = 'narrative_template' AND is_active = TRUE
    """)
    template_json = {
        'template': MX_NARRATIVE_TEMPLATE,
        'placeholders': ['time_period', 'total_regs', 'total_spend_fmt', 'blended_cpa_fmt',
                          'ieccp', 'regs_ci90_lo', 'regs_ci90_hi', 'brand_regs', 'brand_pct', 'nb_regs'],
        'strategy_type': 'ieccp_bound',
        'max_words_expanded': 300,
    }
    con.execute("""
        INSERT INTO ps.market_projection_params
        (market, parameter_name, parameter_version, value_json, refit_cadence,
         last_refit_at, source, fallback_level, lineage, notes, is_active)
        VALUES ('MX', 'narrative_template', 1, ?, 'annual', CURRENT_TIMESTAMP,
                'manual_seed', 'market_specific',
                'authored via seed_mx_demo_artifacts.py 2026-04-22',
                'ieccp_bound narrative; honors Lorena pressure-test context; 3 paragraphs',
                TRUE)
    """, [json.dumps(template_json)])
    print("Seeded narrative_template")

    con.close()
    print("\nDone.")

if __name__ == '__main__':
    seed()
